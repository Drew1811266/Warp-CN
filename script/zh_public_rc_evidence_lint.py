#!/usr/bin/env python3
"""Lint redacted zh-Hans public-RC evidence metadata."""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_BLOCKERS = Path("resources/localization/zh-Hans-public-rc-blockers.toml")
DEFAULT_EVIDENCE = Path("resources/localization/zh-Hans-public-rc-evidence.toml")
TEXT_ARTIFACT_SUFFIXES = (".txt", ".md")

SENSITIVE_PATTERNS = (
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"\b(sk|pk|ghp|gho|xoxb|AKIA)[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"https?://[^\s]+"),
    re.compile(r"\b(token|cookie|secret|api[_ -]?key)\s*[:=]", re.IGNORECASE),
)


@dataclasses.dataclass(frozen=True)
class LintResult:
    ok: bool
    total_required: int
    ready_rows: tuple[str, ...]
    missing_rows: tuple[str, ...]
    errors: tuple[str, ...]


class TomlLoadError(ValueError):
    """Raised when the small TOML subset used by evidence files is invalid."""


def _parse_string(path: Path, line_number: int, value: str) -> str:
    if not (value.startswith('"') and value.endswith('"')):
        raise TomlLoadError(f"{path}:{line_number}: expected quoted string")
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise TomlLoadError(f"{path}:{line_number}: invalid quoted string") from error
    if not isinstance(parsed, str):
        raise TomlLoadError(f"{path}:{line_number}: expected string")
    return parsed


def _parse_array(path: Path, line_number: int, value: str) -> list[str]:
    if not (value.startswith("[") and value.endswith("]")):
        raise TomlLoadError(f"{path}:{line_number}: expected array")

    inner = value[1:-1].strip()
    if not inner:
        return []

    tokens = re.findall(r'"(?:\\.|[^"\\])*"', inner)
    residue = re.sub(r'"(?:\\.|[^"\\])*"', "", inner).replace(",", "").strip()
    if residue:
        raise TomlLoadError(f"{path}:{line_number}: array values must be quoted strings")
    return [_parse_string(path, line_number, token) for token in tokens]


def _collect_multiline_array(lines: list[str], start_index: int, initial_value: str) -> tuple[str, int]:
    parts = [initial_value]
    line_index = start_index
    while not parts[-1].endswith("]"):
        line_index += 1
        if line_index >= len(lines):
            raise TomlLoadError(f"line {start_index + 1}: unterminated array")
        parts.append(lines[line_index].strip())
    return " ".join(parts), line_index


def load_toml(path: Path) -> dict[str, Any]:
    """Load the small TOML subset used by zh-Hans blocker and evidence ledgers."""

    doc: dict[str, Any] = {}
    current_array: str | None = None
    current: dict[str, Any] | None = None
    lines = path.read_text(encoding="utf-8").splitlines()

    line_index = 0
    while line_index < len(lines):
        raw_line = lines[line_index]
        line_number = line_index + 1
        line = raw_line.strip()
        if not line or line.startswith("#"):
            line_index += 1
            continue

        if line.startswith("[[") and line.endswith("]]"):
            current_array = line[2:-2].strip()
            if not current_array:
                raise TomlLoadError(f"{path}:{line_number}: empty array table name")
            current = {}
            doc.setdefault(current_array, []).append(current)
            line_index += 1
            continue

        if "=" not in line:
            raise TomlLoadError(f"{path}:{line_number}: expected key = value")

        key, value = [part.strip() for part in line.split("=", 1)]
        if value.startswith("[") and not value.endswith("]"):
            value, line_index = _collect_multiline_array(lines, line_index, value)

        if value.startswith("["):
            parsed: Any = _parse_array(path, line_number, value)
        elif value in ("true", "false"):
            parsed = value == "true"
        else:
            parsed = _parse_string(path, line_number, value)

        target = current if current is not None else doc
        if key in target:
            context = current_array if current_array is not None else "document"
            raise TomlLoadError(f"{path}:{line_number}: duplicate field {key!r} in {context}")
        target[key] = parsed
        line_index += 1

    return doc


def has_sensitive_metadata(value: object) -> bool:
    if not isinstance(value, str):
        return False
    return any(pattern.search(value) for pattern in SENSITIVE_PATTERNS)


def expected_redacted_path(row_id: str) -> str:
    return f"artifacts/redacted/{row_id.lower()}.txt"


def strict_artifact_errors(row_id: str, evidence_paths: object, repo_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(evidence_paths, list):
        return errors
    expected_path = expected_redacted_path(row_id)
    if expected_path not in evidence_paths:
        errors.append(f"{row_id}: evidence_paths must include {expected_path}")
    for artifact_path in evidence_paths:
        if not isinstance(artifact_path, str):
            continue
        normalized = artifact_path.strip()
        full_path = repo_root / normalized
        if Path(normalized).suffix.lower() not in TEXT_ARTIFACT_SUFFIXES:
            errors.append(f"{row_id}: referenced artifact must be redacted text: {normalized}")
            continue
        if not full_path.exists():
            errors.append(f"{row_id}: referenced artifact does not exist: {normalized}")
            continue
        content = full_path.read_text(encoding="utf-8", errors="replace")
        if has_sensitive_metadata(content):
            errors.append(f"{row_id}: sensitive-looking text in artifact {normalized}")
    return errors


def blocker_index(blockers: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row["id"]): row
        for row in blockers.get("blocker", [])
        if isinstance(row, dict) and row.get("public_rc_required") is True and row.get("id")
    }


def lint_evidence(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    strict_artifacts: bool = False,
    repo_root: Path | None = None,
) -> LintResult:
    blockers_by_id = blocker_index(blockers)
    evidence_rows = evidence_doc.get("evidence", [])
    errors: list[str] = []
    ready_rows: list[str] = []
    seen: set[str] = set()

    if not isinstance(evidence_rows, list):
        errors.append("evidence must be an array table")
        evidence_rows = []

    for row in evidence_rows:
        if not isinstance(row, dict):
            errors.append("evidence row must be an object")
            continue

        row_id = str(row.get("row_id", "")).strip()
        if not row_id:
            errors.append("evidence row is missing row_id")
            continue
        if row_id not in blockers_by_id:
            errors.append(f"{row_id}: unknown row_id")
            continue
        if row_id in seen:
            errors.append(f"{row_id}: duplicate evidence row")
            continue
        seen.add(row_id)

        status = str(row.get("status", "")).strip()
        evidence_paths = row.get("evidence_paths", [])
        cleanup_proof = str(row.get("cleanup_proof", "")).strip()
        redaction = str(row.get("redaction", "")).strip()
        notes = str(row.get("notes", "")).strip()

        for key in ("cleanup_proof", "redaction", "notes"):
            if has_sensitive_metadata(row.get(key)):
                errors.append(f"{row_id}: sensitive-looking metadata in {key}")

        if status != "provided":
            errors.append(f"{row_id}: missing evidence")
            continue
        if not isinstance(evidence_paths, list) or not evidence_paths:
            errors.append(f"{row_id}: evidence_paths must be a non-empty list")
            continue
        if any(not isinstance(path, str) or not path.startswith("artifacts/redacted/") for path in evidence_paths):
            errors.append(f"{row_id}: evidence_paths must use artifacts/redacted/")
            continue
        if not cleanup_proof:
            errors.append(f"{row_id}: cleanup_proof is required")
            continue
        if not redaction:
            errors.append(f"{row_id}: redaction is required")
            continue
        if not notes:
            errors.append(f"{row_id}: notes are required")
            continue

        if strict_artifacts:
            strict_errors = strict_artifact_errors(row_id, evidence_paths, repo_root or Path.cwd())
            if strict_errors:
                errors.extend(strict_errors)
                continue

        ready_rows.append(row_id)

    missing_rows = tuple(sorted(set(blockers_by_id) - seen))
    return LintResult(
        ok=not errors and not missing_rows,
        total_required=len(blockers_by_id),
        ready_rows=tuple(sorted(ready_rows)),
        missing_rows=missing_rows,
        errors=tuple(errors),
    )


def run_text(result: LintResult) -> str:
    lines = [
        "zh-Hans public-RC evidence lint",
        f"total_required: {result.total_required}",
        f"ready_rows: {len(result.ready_rows)}",
        f"missing_rows: {len(result.missing_rows)}",
        f"errors: {len(result.errors)}",
    ]
    for row_id in result.ready_rows:
        lines.append(f"ready: {row_id}")
    for row_id in result.missing_rows:
        lines.append(f"missing: {row_id}")
    for error in result.errors:
        lines.append(f"error: {error}")
    lines.append(f"decision: {'pass' if result.ok else 'fail'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint zh-Hans public-RC evidence intake metadata.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--strict-artifacts", action="store_true", help="Check referenced artifacts exist and are redacted text")
    args = parser.parse_args(argv)

    try:
        result = lint_evidence(
            load_toml(args.blockers),
            load_toml(args.evidence),
            strict_artifacts=args.strict_artifacts,
            repo_root=Path.cwd(),
        )
    except (OSError, TomlLoadError) as error:
        print(error, file=sys.stderr)
        return 1
    print(run_text(result))
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
