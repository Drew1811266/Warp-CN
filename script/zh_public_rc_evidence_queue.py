#!/usr/bin/env python3
"""Render prioritized zh-Hans public-RC evidence collection queues."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

from zh_public_rc_evidence_lint import DEFAULT_BLOCKERS, DEFAULT_EVIDENCE, blocker_index, load_toml
from zh_public_rc_evidence_report import evidence_by_id, redacted_path


CATEGORY_PRIORITY = {
    "backend_fixture": 10,
    "isolated_account": 20,
    "disposable_object": 30,
}

CATEGORY_APPROVAL_GATE = {
    "backend_fixture": "fixture-owner-approval",
    "isolated_account": "isolated-account-approval",
    "disposable_object": "disposable-object-approval",
}

CATEGORY_RISK = {
    "backend_fixture": "medium",
    "isolated_account": "high",
    "disposable_object": "high",
}

CATEGORY_BLOCKERS = {
    "backend_fixture": ("fixture_owner", "fixture_reset_proof", "redacted_fixture_evidence"),
    "isolated_account": ("isolated_account", "logout_or_profile_cleanup", "redacted_gui_evidence"),
    "disposable_object": ("disposable_object", "explicit_delete_approval", "cleanup_absence_proof"),
}


@dataclasses.dataclass(frozen=True)
class QueueRow:
    row_id: str
    category: str
    status: str
    priority: int
    risk: str
    approval_gate: str
    artifact_path: str
    handoff_doc: str
    blocked_by: tuple[str, ...]
    required_evidence: tuple[str, ...]
    safety_rule: str


def _priority_for(category: str, row_id: str) -> int:
    base_priority = CATEGORY_PRIORITY.get(category, 90)
    if category == "disposable_object":
        return base_priority + 5
    return base_priority


def build_queue(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> tuple[QueueRow, ...]:
    evidence = evidence_by_id(evidence_doc)
    rows: list[QueueRow] = []
    for row_id, blocker in sorted(blocker_index(blockers).items()):
        evidence_row = evidence.get(row_id, {})
        evidence_status = str(evidence_row.get("status", "missing"))
        if evidence_status == "provided":
            continue
        category = str(blocker["category"])
        rows.append(
            QueueRow(
                row_id=row_id,
                category=category,
                status=evidence_status,
                priority=_priority_for(category, row_id),
                risk=CATEGORY_RISK.get(category, "unknown"),
                approval_gate=CATEGORY_APPROVAL_GATE.get(category, "manual-approval"),
                artifact_path=redacted_path(row_id),
                handoff_doc=str(blocker["handoff_doc"]),
                blocked_by=tuple(CATEGORY_BLOCKERS.get(category, ("manual_review",))),
                required_evidence=tuple(str(item) for item in blocker.get("required_evidence", [])),
                safety_rule=str(blocker["safety_rule"]),
            )
        )
    return tuple(sorted(rows, key=lambda row: (row.priority, row.row_id)))


def filter_queue(
    rows: tuple[QueueRow, ...],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> tuple[QueueRow, ...]:
    row_filter = {row_id.strip() for row_id in row_ids if row_id.strip()}
    category_filter = {category.strip() for category in categories if category.strip()}
    selected: list[QueueRow] = []
    for row in rows:
        if row_filter and row.row_id not in row_filter:
            continue
        if category_filter and row.category not in category_filter:
            continue
        selected.append(row)
    return tuple(selected)


def queue_to_json_data(rows: tuple[QueueRow, ...]) -> dict[str, Any]:
    category_counts = collections.Counter(row.category for row in rows)
    risk_counts = collections.Counter(row.risk for row in rows)
    return {
        "total_rows": len(rows),
        "category_counts": dict(sorted(category_counts.items())),
        "risk_counts": dict(sorted(risk_counts.items())),
        "rows": [
            {
                **dataclasses.asdict(row),
                "blocked_by": list(row.blocked_by),
                "required_evidence": list(row.required_evidence),
            }
            for row in rows
        ],
        "decision": "ready" if not rows else "blocked-until-queue-cleared",
    }


def render_json(rows: tuple[QueueRow, ...]) -> str:
    return json.dumps(queue_to_json_data(rows), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_text(rows: tuple[QueueRow, ...]) -> str:
    lines = [
        "zh-Hans public-RC evidence collection queue",
        f"total_rows: {len(rows)}",
    ]
    for row in rows:
        lines.append(
            f"{row.row_id}: priority={row.priority} category={row.category} risk={row.risk} approval={row.approval_gate}"
        )
    lines.append(f"decision: {'ready' if not rows else 'blocked-until-queue-cleared'}")
    return "\n".join(lines) + "\n"


def render_markdown(rows: tuple[QueueRow, ...]) -> str:
    lines = [
        "# zh-Hans Public-RC Evidence Collection Queue",
        "",
        "This queue is planning metadata only. It does not provide evidence and does not clear public-RC blockers.",
        "",
        "## Safety Boundary",
        "",
        "- Keep raw screenshots, recordings, callback URLs, cookies, tokens, account identifiers, endpoint URLs, team IDs, and private object names outside Git.",
        "- Do not mutate accounts, billing, cloud state, teams, secrets, endpoints, or environments without explicit approval.",
        "- Promote a row only after reviewed raw evidence, approved redacted artifact text, cleanup proof, and strict artifact lint pass.",
        "",
    ]
    if not rows:
        lines.extend(["## Empty Queue", "", "No missing public-RC evidence rows matched the supplied filters.", ""])
        return "\n".join(lines)

    for row in rows:
        lines.extend(
            [
                f"## {row.row_id}",
                "",
                f"- Priority: `{row.priority}`",
                f"- Category: `{row.category}`",
                f"- Risk: `{row.risk}`",
                f"- Approval gate: `{row.approval_gate}`",
                f"- Current status: `{row.status}`",
                f"- Expected redacted artifact: `{row.artifact_path}`",
                f"- Handoff doc: `{row.handoff_doc}`",
                f"- Blocked by: `{', '.join(row.blocked_by)}`",
                f"- Safety rule: {row.safety_rule}",
                "",
                "Required evidence:",
            ]
        )
        for item in row.required_evidence:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render zh-Hans public-RC evidence collection queue.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--json", action="store_true", help="Print queue as JSON")
    parser.add_argument("--markdown", action="store_true", help="Print queue as Markdown")
    parser.add_argument("--row-id", action="append", default=[], help="Limit queue output to a public-RC row ID")
    parser.add_argument("--category", action="append", default=[], help="Limit queue output to a blocker category")
    args = parser.parse_args(argv)

    rows = filter_queue(
        build_queue(load_toml(args.blockers), load_toml(args.evidence)),
        row_ids=tuple(args.row_id),
        categories=tuple(args.category),
    )
    if args.json:
        print(render_json(rows), end="")
        return 0
    if args.markdown:
        print(render_markdown(rows), end="")
        return 0
    print(render_text(rows), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
