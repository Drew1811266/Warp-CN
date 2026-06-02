#!/usr/bin/env python3
"""Validate and summarize zh-Hans public-RC blocker status."""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path


DEFAULT_REGISTRY = "resources/localization/zh-Hans-public-rc-blockers.toml"

REQUIRED_FIELDS = (
    "id",
    "category",
    "status",
    "reason",
    "required_evidence",
    "handoff_doc",
    "safety_rule",
    "public_rc_required",
    "local_fixture_allowed",
)


class RegistryError(ValueError):
    """Raised when the public-RC blocker registry is invalid."""


def _parse_string(path: Path, line_number: int, value: str) -> str:
    if not (value.startswith('"') and value.endswith('"')):
        raise RegistryError(f"{path}:{line_number}: expected quoted string")
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise RegistryError(f"{path}:{line_number}: invalid quoted string") from error
    if not isinstance(parsed, str):
        raise RegistryError(f"{path}:{line_number}: expected string")
    return parsed


def _parse_array(path: Path, line_number: int, value: str) -> list[str]:
    if not (value.startswith("[") and value.endswith("]")):
        raise RegistryError(f"{path}:{line_number}: expected array")

    inner = value[1:-1].strip()
    if not inner:
        return []

    tokens = re.findall(r'"(?:\\.|[^"\\])*"', inner)
    residue = re.sub(r'"(?:\\.|[^"\\])*"', "", inner).replace(",", "").strip()
    if residue:
        raise RegistryError(f"{path}:{line_number}: array values must be quoted strings")
    return [_parse_string(path, line_number, token) for token in tokens]


def _collect_multiline_array(lines: list[str], start_index: int, initial_value: str) -> tuple[str, int]:
    parts = [initial_value]
    line_index = start_index
    while not parts[-1].endswith("]"):
        line_index += 1
        if line_index >= len(lines):
            raise RegistryError(f"line {start_index + 1}: unterminated array")
        parts.append(lines[line_index].strip())
    return " ".join(parts), line_index


def load_registry(path: Path) -> list[dict[str, object]]:
    blockers: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    lines = path.read_text(encoding="utf-8").splitlines()
    line_index = 0
    while line_index < len(lines):
        raw_line = lines[line_index]
        line_number = line_index + 1
        line = raw_line.strip()
        if not line or line.startswith("#"):
            line_index += 1
            continue
        if line == "[[blocker]]":
            current = {"__line": line_number}
            blockers.append(current)
            line_index += 1
            continue
        if current is None:
            raise RegistryError(f"{path}:{line_number}: expected [[blocker]] before key/value entries")
        if "=" not in line:
            raise RegistryError(f"{path}:{line_number}: expected key = value")

        key, value = [part.strip() for part in line.split("=", 1)]
        if key not in REQUIRED_FIELDS:
            raise RegistryError(f"{path}:{line_number}: unknown registry field {key!r}")
        if key in current:
            raise RegistryError(f"{path}:{line_number}: duplicate field {key!r}")

        if value.startswith("[") and not value.endswith("]"):
            value, line_index = _collect_multiline_array(lines, line_index, value)

        if value.startswith("["):
            current[key] = _parse_array(path, line_number, value)
        elif value in ("true", "false"):
            current[key] = value == "true"
        else:
            current[key] = _parse_string(path, line_number, value)
        line_index += 1

    return blockers


def validate_registry(blockers: list[dict[str, object]], repo_root: Path) -> None:
    seen_ids: dict[str, int] = {}
    for index, blocker in enumerate(blockers, start=1):
        line_number = blocker.get("__line", index)
        missing = [field for field in REQUIRED_FIELDS if field not in blocker]
        if missing:
            raise RegistryError(f"blocker #{index} at line {line_number}: missing fields {missing}")

        blocker_id = blocker["id"]
        if not isinstance(blocker_id, str) or not blocker_id:
            raise RegistryError(f"blocker #{index} at line {line_number}: id must be a non-empty string")
        if blocker_id in seen_ids:
            raise RegistryError(
                f"{blocker_id}: duplicate blocker id; first declared at line {seen_ids[blocker_id]}"
            )
        if isinstance(line_number, int):
            seen_ids[blocker_id] = line_number

        for field in ("category", "status", "reason", "handoff_doc", "safety_rule"):
            if not isinstance(blocker[field], str) or not blocker[field]:
                raise RegistryError(f"{blocker_id}: {field} must be a non-empty string")

        evidence = blocker["required_evidence"]
        if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item for item in evidence):
            raise RegistryError(f"{blocker_id}: required_evidence must be a non-empty string array")

        for field in ("public_rc_required", "local_fixture_allowed"):
            if not isinstance(blocker[field], bool):
                raise RegistryError(f"{blocker_id}: {field} must be a boolean")

        handoff_path = repo_root / str(blocker["handoff_doc"])
        if not handoff_path.exists():
            raise RegistryError(f"{blocker_id}: handoff_doc does not exist: {blocker['handoff_doc']}")


def build_summary(blockers: list[dict[str, object]]) -> dict[str, object]:
    public_required = [
        blocker for blocker in blockers
        if blocker.get("public_rc_required") is True
    ]
    return {
        "total": len(blockers),
        "public_rc_required": len(public_required),
        "statuses": dict(sorted(collections.Counter(str(b["status"]) for b in blockers).items())),
        "categories": dict(sorted(collections.Counter(str(b["category"]) for b in blockers).items())),
        "blockers": [
            {
                "id": blocker["id"],
                "category": blocker["category"],
                "status": blocker["status"],
                "handoff_doc": blocker["handoff_doc"],
                "local_fixture_allowed": blocker["local_fixture_allowed"],
            }
            for blocker in sorted(blockers, key=lambda item: str(item["id"]))
        ],
    }


def render_text(summary: dict[str, object]) -> str:
    lines = [
        "zh-Hans public-RC blocker status",
        f"total: {summary['total']}",
        f"public_rc_required: {summary['public_rc_required']}",
        "statuses:",
    ]
    statuses = summary["statuses"]
    if isinstance(statuses, dict):
        for status, count in statuses.items():
            lines.append(f"  {status}: {count}")
    lines.append("categories:")
    categories = summary["categories"]
    if isinstance(categories, dict):
        for category, count in categories.items():
            lines.append(f"  {category}: {count}")
    lines.append("blockers:")
    blockers = summary["blockers"]
    if isinstance(blockers, list):
        for blocker in blockers:
            if isinstance(blocker, dict):
                lines.append(f"  {blocker['id']}: {blocker['status']} ({blocker['category']})")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize zh-Hans public-RC blockers")
    parser.add_argument(
        "--registry",
        default=DEFAULT_REGISTRY,
        help="Path to the public-RC blocker registry, relative to the repo root",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    registry_path = repo_root / args.registry
    try:
        blockers = load_registry(registry_path)
        validate_registry(blockers, repo_root)
    except (OSError, RegistryError) as error:
        print(error, file=sys.stderr)
        return 1

    summary = build_summary(blockers)
    if args.json:
        sys.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    else:
        sys.stdout.write(render_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
