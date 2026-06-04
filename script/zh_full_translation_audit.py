#!/usr/bin/env python3
"""Generate a full per-entry simulated zh-Hans localization audit ledger.

The ledger is intentionally deterministic and traceable: every manifest entry
gets one row with source/target text, manifest line, source-file state,
machine-token checks, risk tags, public-RC evidence rows, and an audit decision.
It is a Codex simulated review aid, not a substitute for final human sign-off.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "script"))

from zh_apply_localization import (  # noqa: E402
    DEFAULT_GLOSSARY_CONFIG,
    check_glossary,
    load_glossary_config,
    load_manifest,
    validate_manifest,
)


DEFAULT_MANIFEST = REPO_ROOT / "resources/localization/zh-Hans-overrides.toml"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs/zh-Hans-full-translation-audit-0.18"

CJK_RE = re.compile(r"[\u3400-\u9fff]")
PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
UNICODE_ESCAPE_RE = re.compile(r"[0-9A-Fa-f]{2,6}")
LONG_FLAG_RE = re.compile(r"(?<![\w-])--[A-Za-z][A-Za-z0-9_-]*")
ENV_VAR_RE = re.compile(r"(?<![\w$])\$[A-Z_][A-Z0-9_]*|\$\{[A-Z_][A-Z0-9_]*\}")
URL_RE = re.compile(r"https?://[^\s)>\]\"'“”]+")
BACKTICK_RE = re.compile(r"`([^`]+)`")
SLASH_COMMAND_RE = re.compile(r"(?<![\w$])/[a-z][a-z0-9][a-z0-9_.-]*")
ANGLE_TOKEN_RE = re.compile(r"<[A-Za-z][A-Za-z0-9_.:-]*>")

DISPLAY_UNIT_SLASH_TOKENS = {
    "/day",
    "/hr",
    "/hour",
    "/min",
    "/mo",
    "/month",
    "/token",
    "/tokens",
    "/year",
    "/yr",
}

EXACT_ENGLISH_PRESERVE = {
    "AI",
    "Agent",
    "AWS Bedrock",
    "CLI",
    "Codex",
    "Command Search",
    "GitHub",
    "MCP",
    "OpenAI",
    "Warp",
    "Warp Agent",
    "Warp Drive",
}

HIGH_RISK_KEYWORDS = {
    "api-key-secret": (
        "api key",
        "api-key",
        "apikey",
        "secret",
        "token",
        "credential",
        "password",
        "managed auth",
    ),
    "auth-login": ("login", "log in", "logout", "sign in", "sign out", "oauth", "callback"),
    "billing-quota": (
        "billing",
        "credit",
        "credits",
        "quota",
        "capacity",
        "plan",
        "invoice",
        "subscription",
        "trial",
    ),
    "destructive-action": (
        "delete",
        "deleting",
        "remove",
        "removing",
        "destroy",
        "transfer ownership",
        "deactivate",
        "unlink",
        "disable",
        "reset",
    ),
    "environment-endpoint": (
        "environment",
        "endpoint",
        "custom inference",
        "bedrock",
        "model provider",
        "provider",
        "aws",
    ),
    "team-workspace": ("team", "workspace", "member", "owner", "admin", "role"),
    "terminal-command": (
        "command",
        "slash command",
        "terminal",
        "shell",
        "prompt",
        "workflow",
        "export",
    ),
}


@dataclass(frozen=True)
class AuditRow:
    entry_index: int
    manifest_line: int | str
    key: str
    path: str
    status: str
    context: str
    source: str
    target: str
    source_state: str
    expected_count: int | str
    source_count: int
    target_count: int
    decision: str
    confidence: str
    risk_tags: str
    public_rc_rows: str
    token_status: str
    glossary_status: str
    copy_status: str
    functional_status: str
    notes: str


def _sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted(set(values))


def _has_cjk(text: str) -> bool:
    return CJK_RE.search(text) is not None


def _extract_tokens(text: str) -> dict[str, list[str]]:
    placeholders: list[str] = []
    for match in PLACEHOLDER_RE.finditer(text):
        previous = text[match.start() - 1] if match.start() > 0 else ""
        content = match.group(0)[1:-1]
        if previous == "u" and UNICODE_ESCAPE_RE.fullmatch(content):
            continue
        placeholders.append(match.group(0))

    slash_commands = [
        token
        for token in SLASH_COMMAND_RE.findall(text)
        if token not in DISPLAY_UNIT_SLASH_TOKENS
    ]
    return {
        "placeholder": _sorted_unique(placeholders),
        "long_flag": _sorted_unique(LONG_FLAG_RE.findall(text)),
        "env_var": _sorted_unique(ENV_VAR_RE.findall(text)),
        "url": _sorted_unique(URL_RE.findall(text)),
        "backtick": _sorted_unique(match.group(1) for match in BACKTICK_RE.finditer(text)),
        "slash_command": _sorted_unique(slash_commands),
        "angle_token": _sorted_unique(ANGLE_TOKEN_RE.findall(text)),
    }


def _compare_tokens(source: str, target: str) -> tuple[str, list[str], list[str]]:
    source_tokens = _extract_tokens(source)
    target_tokens = _extract_tokens(target)
    critical_mismatches: list[str] = []
    notes: list[str] = []

    critical_categories = ("placeholder", "long_flag", "env_var", "url", "slash_command")
    note_categories = ("backtick", "angle_token")

    for category in critical_categories:
        if source_tokens[category] != target_tokens[category]:
            critical_mismatches.append(
                f"{category}:source={source_tokens[category]} target={target_tokens[category]}"
            )

    for category in note_categories:
        if source_tokens[category] != target_tokens[category]:
            notes.append(f"{category}:source={source_tokens[category]} target={target_tokens[category]}")

    if critical_mismatches:
        return "critical-mismatch", critical_mismatches, notes
    if notes:
        return "note", [], notes
    return "clean", [], []


def _glossary_errors_for_entry(replacement: dict[str, object], glossary) -> list[str]:
    return check_glossary([replacement], glossary)


def _classify_risks(path: str, source: str, target: str, context: str) -> list[str]:
    haystack = f"{path}\n{source}\n{target}\n{context}".lower()
    tags = [
        tag
        for tag, keywords in HIGH_RISK_KEYWORDS.items()
        if any(keyword in haystack for keyword in keywords)
    ]

    if PLACEHOLDER_RE.search(source) or PLACEHOLDER_RE.search(target):
        tags.append("dynamic-placeholder")
    if len(target) > max(len(source) * 2.4, len(source) + 36) and len(source) < 80:
        tags.append("ui-length-risk")
    if source == target and not _has_cjk(target) and source not in EXACT_ENGLISH_PRESERVE:
        tags.append("english-preserved")
    if "panic" in haystack or "error" in haystack or "stderr" in haystack:
        tags.append("error-state")

    return _sorted_unique(tags)


def _public_rc_rows_for(path: str, source: str, target: str, risk_tags: list[str]) -> list[str]:
    haystack = f"{path}\n{source}\n{target}".lower()
    rows: list[str] = []

    if "login" in haystack or "oauth" in haystack or "callback" in haystack:
        rows.append("GUI-AUTH-01")
    if "ai settings" in haystack or "custom inference" in haystack:
        rows.extend(["GUI-SET-03", "GUI-WS-06"])
    if "bedrock" in haystack or "aws" in haystack:
        rows.extend(["GUI-SET-04", "GUI-SET-05"])
    if "environment" in haystack and "delete" in haystack:
        rows.append("GUI-SET-06")
    if "managed auth" in haystack or "secret" in haystack:
        rows.append("GUI-WS-04")
    if "transfer ownership" in haystack or ("owner" in haystack and "team" in haystack):
        rows.append("GUI-WS-07")
    if "billing" in haystack or "credit" in haystack or "credits" in haystack:
        rows.extend(["GUI-BILL-01", "GUI-BILL-02"])
    if "capacity" in haystack or "quota" in haystack:
        rows.append("GUI-CLOUD-01")

    if "billing-quota" in risk_tags and not any(row.startswith("GUI-BILL") for row in rows):
        rows.append("GUI-BILL-01")
    if "api-key-secret" in risk_tags and "GUI-WS-04" not in rows:
        rows.append("GUI-WS-04")

    return _sorted_unique(rows)


def _copy_notes(source: str, target: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    if not target.strip():
        return "issue", ["empty target"]
    if ("TODO" in target or "FIXME" in target) and "TODO" not in source and "FIXME" not in source:
        return "issue", ["TODO/FIXME marker in target"]
    if "智能体" in target:
        return "issue", ["forbidden project term 智能体"]
    if source != target and _has_cjk(source) and not _has_cjk(target):
        notes.append("target lost CJK text that existed in source")
    if source == target and not _has_cjk(target):
        notes.append("English preserved; verify this is product/internal text")
    if "删除" in target and ("disable" in source.lower() or "deactivate" in source.lower()):
        notes.append("destructive wording should be checked in GUI context")
    if len(target) > max(len(source) * 2.6, len(source) + 44) and len(source) < 100:
        notes.append("target is much longer than source; check compact UI fit")

    return ("note" if notes else "clean"), notes


def _source_state(file_text: str | None, source: str, target: str) -> tuple[str, int, int]:
    if file_text is None:
        return "file-missing", 0, 0

    source_count = file_text.count(source)
    target_count = file_text.count(target)
    if target_count > 0 and source_count > 0:
        return "target-and-source-present", source_count, target_count
    if target_count > 0:
        return "target-present", source_count, target_count
    if source_count > 0:
        return "source-present-not-applied", source_count, target_count
    return "missing-in-current-source", source_count, target_count


def _decide(
    token_status: str,
    glossary_errors: list[str],
    copy_status: str,
    copy_notes: list[str],
    risk_tags: list[str],
    public_rc_rows: list[str],
    source_state: str,
) -> tuple[str, str, list[str], str]:
    notes: list[str] = []
    functional_status = "clean"

    if source_state in {"file-missing", "missing-in-current-source", "source-present-not-applied"}:
        functional_status = "source-state-review"
        notes.append(f"source state is {source_state}")

    if glossary_errors:
        return "needs-copy-review", "high", glossary_errors + notes, functional_status
    if token_status == "critical-mismatch":
        return "needs-functional-review", "high", notes, "token-critical-review"
    if copy_status == "issue":
        return "needs-copy-review", "high", copy_notes + notes, functional_status

    notes.extend(copy_notes)
    if public_rc_rows:
        return "blocked-public-rc", "medium", notes, functional_status
    if risk_tags or token_status == "note" or copy_status == "note":
        return "simulated-accepted-with-note", "medium", notes, functional_status
    return "simulated-accepted", "high", notes, functional_status


def _read_files(replacements: list[dict[str, object]]) -> dict[str, str | None]:
    paths = _sorted_unique(
        str(replacement["path"])
        for replacement in replacements
        if isinstance(replacement.get("path"), str)
    )
    texts: dict[str, str | None] = {}
    for rel_path in paths:
        abs_path = REPO_ROOT / rel_path
        if not abs_path.exists():
            texts[rel_path] = None
            continue
        texts[rel_path] = abs_path.read_text(encoding="utf-8")
    return texts


def _build_rows(replacements: list[dict[str, object]], glossary) -> list[AuditRow]:
    file_texts = _read_files(replacements)
    rows: list[AuditRow] = []

    for index, replacement in enumerate(replacements, start=1):
        path = str(replacement.get("path", ""))
        source = str(replacement.get("source", ""))
        target = str(replacement.get("target", ""))
        context = str(replacement.get("context", ""))
        key = str(replacement.get("key", ""))
        status = str(replacement.get("status", ""))
        manifest_line = replacement.get("__line", "")
        expected_count = replacement.get("expected_count", "")

        source_state, source_count, target_count = _source_state(file_texts.get(path), source, target)
        token_status, token_mismatches, token_notes = _compare_tokens(source, target)
        glossary_errors = _glossary_errors_for_entry(replacement, glossary)
        risk_tags = _classify_risks(path, source, target, context)
        public_rc_rows = _public_rc_rows_for(path, source, target, risk_tags)
        copy_status, copy_notes = _copy_notes(source, target)
        decision, confidence, decision_notes, functional_status = _decide(
            token_status=token_status,
            glossary_errors=glossary_errors,
            copy_status=copy_status,
            copy_notes=copy_notes,
            risk_tags=risk_tags,
            public_rc_rows=public_rc_rows,
            source_state=source_state,
        )

        notes = token_mismatches + token_notes + decision_notes
        if expected_count != "" and isinstance(expected_count, int) and target_count != expected_count:
            notes.append(f"target_count {target_count} differs from expected_count {expected_count}")
            if decision == "simulated-accepted":
                decision = "simulated-accepted-with-note"
                confidence = "medium"

        rows.append(
            AuditRow(
                entry_index=index,
                manifest_line=manifest_line if isinstance(manifest_line, int) else "",
                key=key,
                path=path,
                status=status,
                context=context,
                source=source,
                target=target,
                source_state=source_state,
                expected_count=expected_count if isinstance(expected_count, int) else "",
                source_count=source_count,
                target_count=target_count,
                decision=decision,
                confidence=confidence,
                risk_tags=";".join(risk_tags),
                public_rc_rows=";".join(public_rc_rows),
                token_status=token_status,
                glossary_status="error" if glossary_errors else "clean",
                copy_status=copy_status,
                functional_status=functional_status,
                notes=" | ".join(_sorted_unique(notes)),
            )
        )

    return rows


def _write_tsv(rows: list[AuditRow], path: Path) -> None:
    def tsv_value(value: object) -> object:
        if not isinstance(value, str):
            return value
        return value.replace("\t", "\\t").replace("\r\n", "\n").replace("\n", "\\n")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(AuditRow.__dataclass_fields__.keys()),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            values = row.__dict__.copy()
            values = {key: tsv_value(value) for key, value in values.items()}
            values["notes"] = values["notes"] or "none"
            writer.writerow(values)


def _write_json(rows: list[AuditRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [row.__dict__ for row in rows]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _counter_from_semicolon(rows: list[AuditRow], attr: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        value = getattr(row, attr)
        if not value:
            continue
        for item in value.split(";"):
            if item:
                counter[item] += 1
    return counter


def _format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "- none\n"
    return "".join(f"- {key}: {counter[key]}\n" for key in sorted(counter))


def _write_summary(rows: list[AuditRow], path: Path, manifest: Path) -> None:
    decisions = Counter(row.decision for row in rows)
    token_status = Counter(row.token_status for row in rows)
    source_states = Counter(row.source_state for row in rows)
    risk_tags = _counter_from_semicolon(rows, "risk_tags")
    public_rc_rows = _counter_from_semicolon(rows, "public_rc_rows")
    actionable = [
        row
        for row in rows
        if row.decision in {"needs-copy-review", "needs-functional-review"}
    ]

    lines = [
        "# zh-Hans Full Translation Audit 0.18",
        "",
        "Scope: Codex simulated per-entry review for every `[[replace]]` row in the zh-Hans override manifest.",
        "",
        f"- Manifest: `{manifest.relative_to(REPO_ROOT)}`",
        f"- Entries reviewed: {len(rows)}",
        "- Review mode: deterministic Codex simulation; this is not external human sign-off.",
        "",
        "## Decision Counts",
        "",
        _format_counter(decisions),
        "## Token Status Counts",
        "",
        _format_counter(token_status),
        "## Source State Counts",
        "",
        _format_counter(source_states),
        "## Risk Tag Counts",
        "",
        _format_counter(risk_tags),
        "## Public-RC Evidence Row Tags",
        "",
        _format_counter(public_rc_rows),
        "## Actionable Review Rows",
        "",
    ]

    if actionable:
        lines.append("| entry | manifest_line | decision | path | notes |")
        lines.append("| --- | ---: | --- | --- | --- |")
        for row in actionable[:200]:
            notes = row.notes.replace("|", "/")
            lines.append(
                f"| {row.entry_index} | {row.manifest_line} | {row.decision} | "
                f"`{row.path}` | {notes} |"
            )
        if len(actionable) > 200:
            lines.append(f"| ... | ... | ... | ... | {len(actionable) - 200} more rows omitted |")
    else:
        lines.append("No `needs-copy-review` or `needs-functional-review` rows were produced.")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `entries.tsv`: one row per manifest entry, intended for spreadsheet-style review.",
            "- `entries.json`: same rows in machine-readable form.",
            "- `summary.md`: this aggregate summary.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--glossary", type=Path, default=REPO_ROOT / DEFAULT_GLOSSARY_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--fail-on-actionable", action="store_true")
    args = parser.parse_args(argv)

    manifest = args.manifest.resolve()
    glossary_path = args.glossary.resolve()
    replacements = load_manifest(manifest)
    manifest_errors = validate_manifest(replacements)
    if manifest_errors:
        for error in manifest_errors:
            print(error, file=sys.stderr)
        return 2

    glossary = load_glossary_config(glossary_path)
    rows = _build_rows(replacements, glossary)

    output_dir = args.output_dir.resolve()
    _write_tsv(rows, output_dir / "entries.tsv")
    _write_json(rows, output_dir / "entries.json")
    _write_summary(rows, output_dir / "summary.md", manifest)

    decisions = Counter(row.decision for row in rows)
    print(f"entries: {len(rows)}")
    for decision in sorted(decisions):
        print(f"{decision}: {decisions[decision]}")
    print(f"output_dir: {output_dir}")

    if args.fail_on_actionable and any(
        row.decision in {"needs-copy-review", "needs-functional-review"} for row in rows
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
