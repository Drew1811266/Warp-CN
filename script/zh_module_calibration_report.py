#!/usr/bin/env python3
"""Render module-level zh-Hans calibration reports from full audit JSON."""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT_JSON = REPO_ROOT / "docs/zh-Hans-calibration-cycles/2026-06-05/entries.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs/zh-Hans-calibration-cycles/2026-06-05"


def _split_semicolon(value: object) -> list[str]:
    if not value:
        return []
    return [item for item in str(value).split(";") if item]


def _escape(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ")


def load_rows(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def module_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        groups[str(row.get("module_group") or "unknown")].append(row)

    summaries: list[dict[str, Any]] = []
    for group, group_rows in sorted(groups.items()):
        decisions = collections.Counter(str(row.get("decision", "")) for row in group_rows)
        copy_scores = collections.Counter(str(row.get("machine_copy_score", "")) for row in group_rows)
        functional = collections.Counter(str(row.get("functional_status", "")) for row in group_rows)
        mojibake = collections.Counter(str(row.get("mojibake_status", "")) for row in group_rows)
        public_rc_rows = collections.Counter(
            tag for row in group_rows for tag in _split_semicolon(row.get("public_rc_rows"))
        )
        top_files = collections.Counter(str(row.get("path", "")) for row in group_rows).most_common(5)
        if public_rc_rows:
            next_action = "collect-safe-evidence-or-keep-public-rc-blocked"
        elif any(row.get("decision") in {"needs-copy-review", "needs-functional-review"} for row in group_rows):
            next_action = "resolve-actionable-findings"
        elif any(str(row.get("ui_density_risk")) != "clean" for row in group_rows):
            next_action = "review-layout-risk"
        else:
            next_action = "source-level-reviewed"
        summaries.append(
            {
                "module_group": group,
                "entries": len(group_rows),
                "decisions": dict(sorted(decisions.items())),
                "copy_scores": dict(sorted(copy_scores.items())),
                "functional_status": dict(sorted(functional.items())),
                "mojibake_status": dict(sorted(mojibake.items())),
                "public_rc_rows": dict(sorted(public_rc_rows.items())),
                "top_files": top_files,
                "next_action": next_action,
            }
        )
    return summaries


def render_module_matrix(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# zh-Hans Module Calibration Matrix",
        "",
        "This report aggregates the full audit ledger by module. Source-level review, GUI readiness, and public-RC readiness remain separate.",
        "",
        "| module | entries | decisions | copy scores | functional | public-RC rows | top files | next action |",
        "| --- | ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for summary in module_summary(rows):
        top_files = ", ".join(f"{path} ({count})" for path, count in summary["top_files"])
        lines.append(
            "| "
            f"`{summary['module_group']}` | "
            f"{summary['entries']} | "
            f"`{_escape(summary['decisions'])}` | "
            f"`{_escape(summary['copy_scores'])}` | "
            f"`{_escape(summary['functional_status'])}` | "
            f"`{_escape(summary['public_rc_rows'])}` | "
            f"{_escape(top_files)} | "
            f"`{summary['next_action']}` |"
        )
    lines.append("")
    return "\n".join(lines)


def _row_line(row: dict[str, Any]) -> str:
    notes = _escape(row.get("notes", ""))
    return (
        f"| {row.get('entry_index')} | {row.get('manifest_line')} | `{_escape(row.get('path', ''))}` | "
        f"{_escape(row.get('source', ''))[:140]} | {_escape(row.get('target', ''))[:140]} | {notes[:180]} |"
    )


def _section(lines: list[str], title: str, rows: list[dict[str, Any]], limit: int = 120) -> None:
    lines.extend(["", f"## {title}", ""])
    if not rows:
        lines.append("No rows.")
        return
    lines.extend(["| entry | line | path | source | target | notes |", "| ---: | ---: | --- | --- | --- | --- |"])
    for row in rows[:limit]:
        lines.append(_row_line(row))
    if len(rows) > limit:
        lines.append(f"| ... | ... | ... | ... | ... | {len(rows) - limit} more rows omitted |")


def render_copy_findings(rows: list[dict[str, Any]]) -> str:
    needs_fix = [row for row in rows if row.get("decision") == "needs-copy-review" or row.get("machine_copy_score") == 0]
    note_rows = [
        row
        for row in rows
        if row.get("machine_copy_score") == 1 and row not in needs_fix and row.get("copy_status") != "clean"
    ]
    english = [row for row in rows if "english-preserved" in _split_semicolon(row.get("risk_tags"))]
    long_ui = [row for row in rows if row.get("ui_density_risk") != "clean"]

    lines = [
        "# zh-Hans Copy Review Findings",
        "",
        "This report is a review queue. Rows listed here still require source-context judgment before any manifest edit.",
        "",
        f"- Needs copy fix candidates: {len(needs_fix)}",
        f"- Machine translation risk notes: {len(note_rows)}",
        f"- English preserved review rows: {len(english)}",
        f"- Long compact UI text rows: {len(long_ui)}",
    ]
    _section(lines, "Needs Copy Fix", needs_fix)
    _section(lines, "Machine Translation Risk Notes", note_rows)
    _section(lines, "English Preserved Review Queue", english)
    _section(lines, "Long Compact UI Text", long_ui)
    _section(lines, "Accepted False Positives", [])
    lines.append("")
    return "\n".join(lines)


def render_functional_findings(rows: list[dict[str, Any]]) -> str:
    critical_tokens = [row for row in rows if row.get("token_status") == "critical-mismatch"]
    source_state = [row for row in rows if row.get("functional_status") == "source-state-review"]
    placeholder_url = [
        row
        for row in rows
        if "dynamic-placeholder" in _split_semicolon(row.get("risk_tags")) or row.get("token_status") == "note"
    ]
    command = [row for row in rows if "terminal-command" in _split_semicolon(row.get("risk_tags"))]
    search_protocol = [
        row
        for row in rows
        if row.get("module_group") == "search-command-palette"
        or any(tag in _split_semicolon(row.get("risk_tags")) for tag in ("environment-endpoint", "api-key-secret"))
    ]
    public_rc = [row for row in rows if _split_semicolon(row.get("public_rc_rows"))]

    lines = [
        "# zh-Hans Functional Risk Findings",
        "",
        "This report separates behavior-sensitive strings from copy-only review. Public-RC rows remain evidence-gated.",
        "",
        f"- Critical token mismatches: {len(critical_tokens)}",
        f"- Source-state review rows: {len(source_state)}",
        f"- Placeholder and URL risk rows: {len(placeholder_url)}",
        f"- Command and slash command risk rows: {len(command)}",
        f"- Search, action, storage, protocol risk rows: {len(search_protocol)}",
        f"- Public-RC evidence gated rows: {len(public_rc)}",
    ]
    _section(lines, "Critical Token Mismatches", critical_tokens)
    _section(lines, "Source State Review", source_state)
    _section(lines, "Placeholder And URL Risks", placeholder_url)
    _section(lines, "Command And Slash Command Risks", command)
    _section(lines, "Search, Action, Storage, Protocol Risks", search_protocol)
    _section(lines, "Public-RC Evidence Gated", public_rc)
    lines.append("")
    return "\n".join(lines)


def render_json_summary(rows: list[dict[str, Any]]) -> str:
    return json.dumps({"modules": module_summary(rows), "total_rows": len(rows)}, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_reports(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "module-matrix.md").write_text(render_module_matrix(rows), encoding="utf-8")
    (output_dir / "copy-review-findings.md").write_text(render_copy_findings(rows), encoding="utf-8")
    (output_dir / "functional-risk-findings.md").write_text(render_functional_findings(rows), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--json", action="store_true", help="Print JSON summary instead of writing Markdown reports")
    args = parser.parse_args(argv)

    rows = load_rows(args.audit_json)
    if args.json:
        print(render_json_summary(rows), end="")
        return 0
    write_reports(rows, args.output_dir)
    print(f"module_groups: {len(module_summary(rows))}")
    print(f"output_dir: {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
