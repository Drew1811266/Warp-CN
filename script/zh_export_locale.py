#!/usr/bin/env python3
"""Export zh-Hans manifest entries into migration-friendly locale files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from zh_apply_localization import load_manifest


EXPORT_FIELDS = (
    "key",
    "path",
    "source",
    "target",
    "context",
    "status",
    "preserve_terms",
    "notes",
)


def build_locale_entries(replacements: list[dict[str, object]]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []

    for replacement in replacements:
        entry: dict[str, object] = {}
        for field in EXPORT_FIELDS:
            value = replacement.get(field)
            if field == "preserve_terms":
                if isinstance(value, list):
                    entry[field] = [term for term in value if isinstance(term, str)]
                else:
                    entry[field] = []
            elif isinstance(value, str):
                entry[field] = value
            else:
                entry[field] = ""
        entries.append(entry)

    return entries


def render_json(entries: list[dict[str, object]]) -> str:
    return json.dumps(entries, ensure_ascii=False, indent=2) + "\n"


def _yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_yaml(entries: list[dict[str, object]]) -> str:
    lines: list[str] = []
    for entry in entries:
        lines.append(f"- key: {_yaml_quote(str(entry['key']))}")
        for field in EXPORT_FIELDS:
            if field == "key":
                continue
            value = entry[field]
            if field == "preserve_terms":
                terms = value if isinstance(value, list) else []
                if not terms:
                    lines.append("  preserve_terms: []")
                else:
                    lines.append("  preserve_terms:")
                    for term in terms:
                        lines.append(f"    - {_yaml_quote(str(term))}")
                continue
            lines.append(f"  {field}: {_yaml_quote(str(value))}")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export zh-Hans localization manifest")
    parser.add_argument(
        "--manifest",
        default="resources/localization/zh-Hans-overrides.toml",
        help="Path to the TOML replacement manifest, relative to the repo root",
    )
    parser.add_argument("--format", choices=("json", "yaml"), required=True, help="Export format")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    try:
        replacements = load_manifest(repo_root / args.manifest)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    entries = build_locale_entries(replacements)
    if args.format == "json":
        sys.stdout.write(render_json(entries))
    else:
        sys.stdout.write(render_yaml(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
