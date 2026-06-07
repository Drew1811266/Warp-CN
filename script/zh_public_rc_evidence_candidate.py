#!/usr/bin/env python3
"""Preflight redacted zh-Hans public-RC evidence candidate artifacts."""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

from zh_public_rc_evidence_lint import DEFAULT_BLOCKERS, DEFAULT_EVIDENCE, blocker_index, has_sensitive_metadata, load_toml


REQUIRED_FIELDS = (
    "row_id",
    "profile",
    "visible_anchors",
    "redaction",
    "cleanup_proof",
    "safety_confirmation",
    "artifact_kind",
)

DISPOSABLE_OBJECT_NAMES = {
    "GUI-SET-06": "zh-smoke-delete-environment",
    "GUI-WS-04": "zh-smoke-delete-secret",
    "GUI-WS-06": "zh-smoke-delete-endpoint",
    "GUI-WS-07": "zh-smoke-public-rc-team",
}


@dataclasses.dataclass(frozen=True)
class CandidateResult:
    ok: bool
    row_id: str
    category: str
    artifact_path: str
    decision: str
    fields_present: tuple[str, ...]
    errors: tuple[str, ...]


def parse_candidate_text(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_lines
        if current_key is not None:
            fields[current_key] = "\n".join(line for line in current_lines).strip()
        current_key = None
        current_lines = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if ":" in line and not line.startswith(("-", " ")):
            flush()
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_lines = [value.strip()]
            continue
        if current_key is not None:
            current_lines.append(line.strip())
    flush()
    return fields


def _evidence_status(evidence_doc: dict[str, Any], row_id: str) -> str:
    rows = evidence_doc.get("evidence", [])
    if not isinstance(rows, list):
        return "missing"
    for row in rows:
        if isinstance(row, dict) and str(row.get("row_id", "")) == row_id:
            return str(row.get("status", "missing"))
    return "missing"


def _candidate_errors(blocker: dict[str, Any], evidence_doc: dict[str, Any], row_id: str, fields: dict[str, str], text: str) -> list[str]:
    errors: list[str] = []
    if has_sensitive_metadata(text):
        errors.append("sensitive-looking text in candidate artifact")
    if _evidence_status(evidence_doc, row_id) == "provided":
        errors.append("row already has provided evidence; use strict evidence lint instead")

    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            errors.append(f"{field} is required")

    if fields.get("row_id") and fields["row_id"] != row_id:
        errors.append("candidate row_id does not match requested row")

    if fields.get("artifact_kind") and fields["artifact_kind"] != "redacted-text":
        errors.append("artifact_kind must be redacted-text")

    anchors = fields.get("visible_anchors", "")
    if anchors and not any("\u4e00" <= char <= "\u9fff" for char in anchors):
        errors.append("visible_anchors must include at least one Chinese anchor")

    expected_object = DISPOSABLE_OBJECT_NAMES.get(row_id)
    if expected_object:
        object_name = fields.get("object_name", "")
        if object_name != expected_object:
            errors.append(f"object_name must be {expected_object}")

    safety = fields.get("safety_confirmation", "")
    if safety and "main account" not in safety and "主账号" not in safety:
        errors.append("safety_confirmation must state that the main account was not used")

    cleanup = fields.get("cleanup_proof", "")
    if cleanup and not any(marker in cleanup.lower() for marker in ("cleanup", "reset", "absent", "restored", "清理", "重置", "不存在", "恢复")):
        errors.append("cleanup_proof must describe cleanup, reset, absence, or restore proof")

    if not blocker.get("public_rc_required"):
        errors.append("row is not public-RC required")

    return errors


def preflight_candidate(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_id: str,
    artifact_path: Path,
) -> CandidateResult:
    blockers_by_id = blocker_index(blockers)
    blocker = blockers_by_id.get(row_id)
    if blocker is None:
        return CandidateResult(
            ok=False,
            row_id=row_id,
            category="unknown",
            artifact_path=str(artifact_path),
            decision="candidate-rejected",
            fields_present=(),
            errors=(f"unknown row_id: {row_id}",),
        )

    errors: list[str] = []
    if artifact_path.suffix.lower() not in (".txt", ".md"):
        errors.append("candidate artifact must be .txt or .md")
    if not artifact_path.exists():
        errors.append("candidate artifact does not exist")
        return CandidateResult(
            ok=False,
            row_id=row_id,
            category=str(blocker["category"]),
            artifact_path=str(artifact_path),
            decision="candidate-rejected",
            fields_present=(),
            errors=tuple(errors),
        )

    text = artifact_path.read_text(encoding="utf-8", errors="replace")
    fields = parse_candidate_text(text)
    errors.extend(_candidate_errors(blocker, evidence_doc, row_id, fields, text))
    ok = not errors
    return CandidateResult(
        ok=ok,
        row_id=row_id,
        category=str(blocker["category"]),
        artifact_path=str(artifact_path),
        decision="candidate-ready-for-human-review" if ok else "candidate-rejected",
        fields_present=tuple(sorted(fields)),
        errors=tuple(errors),
    )


def result_to_json_data(result: CandidateResult) -> dict[str, Any]:
    return dataclasses.asdict(result)


def render_json(result: CandidateResult) -> str:
    return json.dumps(result_to_json_data(result), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_text(result: CandidateResult) -> str:
    lines = [
        "zh-Hans public-RC evidence candidate preflight",
        f"row_id: {result.row_id}",
        f"category: {result.category}",
        f"artifact_path: {result.artifact_path}",
        f"decision: {result.decision}",
        f"errors: {len(result.errors)}",
    ]
    for error in result.errors:
        lines.append(f"error: {error}")
    return "\n".join(lines) + "\n"


def render_markdown(result: CandidateResult) -> str:
    lines = [
        "# zh-Hans Public-RC Evidence Candidate Preflight",
        "",
        "This preflight checks a redacted text candidate only. It does not collect evidence, edit the ledger, or clear blockers.",
        "",
        f"- Row ID: `{result.row_id}`",
        f"- Category: `{result.category}`",
        f"- Artifact path: `{result.artifact_path}`",
        f"- Decision: `{result.decision}`",
        f"- Fields present: `{', '.join(result.fields_present)}`",
        "",
    ]
    if result.errors:
        lines.append("## Errors")
        lines.append("")
        for error in result.errors:
            lines.append(f"- {error}")
        lines.append("")
    else:
        lines.append("## Next Review Gate")
        lines.append("")
        lines.append("- Human reviewer must inspect the raw evidence outside Git.")
        lines.append("- The ledger must not be updated until redaction, cleanup proof, row match, and safety boundaries are approved.")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preflight a redacted zh-Hans public-RC evidence candidate.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--row-id", required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args(argv)

    result = preflight_candidate(
        load_toml(args.blockers),
        load_toml(args.evidence),
        row_id=args.row_id,
        artifact_path=args.artifact,
    )
    if args.json:
        print(render_json(result), end="")
    elif args.markdown:
        print(render_markdown(result), end="")
    else:
        print(render_text(result), end="")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
