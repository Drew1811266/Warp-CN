#!/usr/bin/env python3
"""Render zh-Hans public-RC evidence readiness reports and safe packet templates."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

from zh_public_rc_evidence_lint import DEFAULT_BLOCKERS, DEFAULT_EVIDENCE, blocker_index, load_toml


@dataclasses.dataclass(frozen=True)
class ReportRow:
    row_id: str
    category: str
    status: str
    ready: bool


@dataclasses.dataclass(frozen=True)
class EvidenceReport:
    total_required: int
    ready_rows: tuple[str, ...]
    status_counts: dict[str, int]
    category_counts: dict[str, int]
    category_ready_counts: dict[str, int]
    rows: tuple[ReportRow, ...]


def evidence_by_id(evidence_doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in evidence_doc.get("evidence", []):
        if isinstance(row, dict) and row.get("row_id"):
            rows[str(row["row_id"])] = row
    return rows


def build_report(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> EvidenceReport:
    blockers_by_id = blocker_index(blockers)
    evidence = evidence_by_id(evidence_doc)
    rows: list[ReportRow] = []

    for row_id, blocker in sorted(blockers_by_id.items()):
        category = str(blocker["category"])
        evidence_row = evidence.get(row_id, {})
        status = str(evidence_row.get("status", "missing"))
        ready = status == "provided"
        rows.append(ReportRow(row_id=row_id, category=category, status=status, ready=ready))

    status_counts = collections.Counter(row.status for row in rows)
    category_counts = collections.Counter(row.category for row in rows)
    category_ready_counts = collections.Counter(row.category for row in rows if row.ready)

    return EvidenceReport(
        total_required=len(rows),
        ready_rows=tuple(row.row_id for row in rows if row.ready),
        status_counts=dict(sorted(status_counts.items())),
        category_counts=dict(sorted(category_counts.items())),
        category_ready_counts=dict(sorted(category_ready_counts.items())),
        rows=tuple(rows),
    )


def render_text(report: EvidenceReport) -> str:
    lines = [
        "zh-Hans public-RC evidence report",
        f"total_required: {report.total_required}",
        f"ready_rows: {len(report.ready_rows)}",
        "categories:",
    ]
    for category, total in report.category_counts.items():
        ready = report.category_ready_counts.get(category, 0)
        missing = total - ready
        lines.append(f"  {category}: total={total} ready={ready} missing={missing}")
    lines.append("rows:")
    for row in report.rows:
        state = "ready" if row.ready else "missing"
        lines.append(f"  {row.row_id}: {row.category} {state}")
    lines.append(f"decision: {'ready' if len(report.ready_rows) == report.total_required else 'blocked'}")
    return "\n".join(lines)


def report_to_json_data(report: EvidenceReport) -> dict[str, Any]:
    return {
        "total_required": report.total_required,
        "ready_rows": list(report.ready_rows),
        "status_counts": report.status_counts,
        "category_counts": report.category_counts,
        "category_ready_counts": report.category_ready_counts,
        "rows": [dataclasses.asdict(row) for row in report.rows],
        "decision": "ready" if len(report.ready_rows) == report.total_required else "blocked",
    }


def render_json(report: EvidenceReport) -> str:
    return json.dumps(report_to_json_data(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def redacted_path(row_id: str) -> str:
    return f"artifacts/redacted/{row_id.lower()}.txt"


def render_templates(blockers: dict[str, Any]) -> str:
    lines = [
        "# Copy one block into resources/localization/zh-Hans-public-rc-evidence.toml only after redacted evidence exists.",
        "# Keep raw screenshots, recordings, tokens, callback URLs, account identifiers, and private team names outside Git.",
    ]
    for row_id, blocker in sorted(blocker_index(blockers).items()):
        lines.extend(
            [
                "",
                "[[evidence]]",
                f'row_id = "{row_id}"',
                'status = "provided"',
                f'evidence_paths = ["{redacted_path(row_id)}"]',
                'cleanup_proof = "redacted cleanup proof reviewed"',
                'redaction = "email, token, key, callback url, endpoint url, team id, account id, and private identifiers removed"',
                f'notes = "{blocker["category"]} evidence packet reviewed against {row_id}"',
            ]
        )
    return "\n".join(lines) + "\n"


def missing_actions(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    evidence = evidence_by_id(evidence_doc)
    actions: list[dict[str, Any]] = []
    for row_id, blocker in sorted(blocker_index(blockers).items()):
        evidence_row = evidence.get(row_id, {})
        if str(evidence_row.get("status", "missing")) == "provided":
            continue
        actions.append(
            {
                "row_id": row_id,
                "category": str(blocker["category"]),
                "status": str(evidence_row.get("status", "missing")),
                "handoff_doc": str(blocker["handoff_doc"]),
                "artifact_path": redacted_path(row_id),
                "required_evidence": list(blocker.get("required_evidence", [])),
                "safety_rule": str(blocker["safety_rule"]),
            }
        )
    return tuple(actions)


def filter_actions(
    actions: tuple[dict[str, Any], ...],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> tuple[dict[str, Any], ...]:
    row_filter = {row_id.strip() for row_id in row_ids if row_id.strip()}
    category_filter = {category.strip() for category in categories if category.strip()}
    selected: list[dict[str, Any]] = []
    for action in actions:
        if row_filter and action["row_id"] not in row_filter:
            continue
        if category_filter and action["category"] not in category_filter:
            continue
        selected.append(action)
    return tuple(selected)


def render_missing_actions_json(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> str:
    actions = filter_actions(missing_actions(blockers, evidence_doc), row_ids=row_ids, categories=categories)
    data = {
        "total_actions": len(actions),
        "actions": list(actions),
        "decision": "blocked-until-matching-evidence-is-reviewed",
    }
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_missing_actions(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> str:
    lines = [
        "zh-Hans public-RC missing evidence actions",
        "Only use these rows after external evidence has been captured, redacted, and approved.",
    ]
    actions = filter_actions(missing_actions(blockers, evidence_doc), row_ids=row_ids, categories=categories)
    for action in actions:
        lines.extend(
            [
                "",
                f"row_id: {action['row_id']}",
                f"category: {action['category']}",
                f"status: {action['status']}",
                f"handoff_doc: {action['handoff_doc']}",
                f"artifact_path: {action['artifact_path']}",
                "required_evidence:",
            ]
        )
        for item in action["required_evidence"]:
            lines.append(f"- {item}")
        lines.append(f"safety_rule: {action['safety_rule']}")
    lines.append("")
    lines.append("decision: blocked-until-matching-evidence-is-reviewed")
    return "\n".join(lines) + "\n"


def render_missing_action_markdown(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> str:
    actions = filter_actions(missing_actions(blockers, evidence_doc), row_ids=row_ids, categories=categories)
    lines = [
        "# zh-Hans Public-RC Missing Evidence Action Packet",
        "",
        "This packet is safe handoff metadata only. It does not provide evidence and does not clear public-RC blockers.",
        "",
        "## Safety Boundary",
        "",
        "- Keep raw screenshots, recordings, callback URLs, cookies, tokens, account identifiers, endpoint URLs, team IDs, and private object names outside Git.",
        "- Commit only reviewed redacted text under the exact `artifacts/redacted/<row-id>.txt` path after explicit approval.",
        "- Do not mutate accounts, billing, cloud state, teams, secrets, endpoints, or environments without explicit approval.",
        "",
    ]
    if not actions:
        lines.extend(["## No Matching Actions", "", "No missing evidence action matched the supplied filters.", ""])
        return "\n".join(lines)

    for action in actions:
        lines.extend(
            [
                f"## {action['row_id']}",
                "",
                f"- Category: `{action['category']}`",
                f"- Current status: `{action['status']}`",
                f"- Handoff doc: `{action['handoff_doc']}`",
                f"- Expected redacted artifact: `{action['artifact_path']}`",
                f"- Safety rule: {action['safety_rule']}",
                "",
                "Required evidence:",
            ]
        )
        for item in action["required_evidence"]:
            lines.append(f"- {item}")
        lines.extend(
            [
                "",
                "Qualification rule:",
                "",
                "```text",
                "status may become provided only after raw evidence is reviewed, redacted artifact text is approved, strict artifact lint passes, and cleanup proof is present.",
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render zh-Hans public-RC evidence readiness output.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--templates", action="store_true", help="Print safe evidence TOML packet templates")
    parser.add_argument("--missing-actions", action="store_true", help="Print row-level missing evidence actions")
    parser.add_argument("--missing-actions-json", action="store_true", help="Print row-level missing evidence actions as JSON")
    parser.add_argument("--missing-action-markdown", action="store_true", help="Print filtered missing evidence actions as Markdown")
    parser.add_argument("--json", action="store_true", help="Print evidence report JSON")
    parser.add_argument("--row-id", action="append", default=[], help="Limit missing-action output to a public-RC row ID")
    parser.add_argument("--category", action="append", default=[], help="Limit missing-action output to a blocker category")
    args = parser.parse_args(argv)

    blockers = load_toml(args.blockers)
    if args.templates:
        print(render_templates(blockers), end="")
        return 0

    evidence = load_toml(args.evidence)
    row_ids = tuple(args.row_id)
    categories = tuple(args.category)
    if args.missing_action_markdown:
        print(render_missing_action_markdown(blockers, evidence, row_ids=row_ids, categories=categories), end="")
        return 0

    if args.missing_actions_json:
        print(render_missing_actions_json(blockers, evidence, row_ids=row_ids, categories=categories), end="")
        return 0

    if args.missing_actions:
        print(render_missing_actions(blockers, evidence, row_ids=row_ids, categories=categories), end="")
        return 0

    report = build_report(blockers, evidence)
    if args.json:
        print(render_json(report), end="")
        return 0

    print(render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
