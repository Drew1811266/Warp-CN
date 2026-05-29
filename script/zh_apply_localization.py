#!/usr/bin/env python3
"""Apply local Chinese UI string overrides to the Warp source tree.

This is intentionally small and strict: each entry must match text in the
target file, so upstream string drift is reported during maintenance instead
of being silently missed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _is_identifier_char(char: str) -> bool:
    return char == "_" or char.isalnum()


def _raw_string_hash_count_before_quote(text: str, quote_index: int) -> int | None:
    hash_count = 0
    index = quote_index - 1
    while index >= 0 and text[index] == "#":
        hash_count += 1
        index -= 1

    if index < 0 or text[index] != "r":
        return None

    prefix_index = index - 1
    if prefix_index >= 0 and text[prefix_index] == "b":
        prefix_index -= 1
    if prefix_index >= 0 and _is_identifier_char(text[prefix_index]):
        return None

    return hash_count


def _consume_raw_string(text: str, quote_index: int, hash_count: int) -> int:
    terminator = '"' + ("#" * hash_count)
    end = text.find(terminator, quote_index + 1)
    if end == -1:
        return len(text)
    return end + len(terminator)


def _consume_char_literal(text: str, quote_index: int) -> int | None:
    index = quote_index + 1
    escaped = False
    chars_seen = 0

    while index < len(text):
        current = text[index]
        if current == "\n":
            return None
        if escaped:
            escaped = False
            chars_seen += 1
            index += 1
            continue
        if current == "\\":
            escaped = True
            index += 1
            continue
        if current == "'":
            if chars_seen == 0:
                return None
            return index + 1
        chars_seen += 1
        if chars_seen > 8:
            return None
        index += 1

    return None


def _parse_quoted_manifest_value(value: str) -> str:
    content = value[1:-1]
    result: list[str] = []
    escaped = False

    for char in content:
        if escaped:
            if char in {'"', "\\"}:
                result.append(char)
            else:
                result.append("\\")
                result.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        result.append(char)

    if escaped:
        result.append("\\")

    return "".join(result)


def replace_rust_string_literals(text: str, source: str, target: str) -> tuple[str, int]:
    result: list[str] = []
    replaced = 0
    index = 0

    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if char == "/" and next_char == "/":
            newline = text.find("\n", index + 2)
            if newline == -1:
                result.append(text[index:])
                break
            result.append(text[index : newline + 1])
            index = newline + 1
            continue

        if char == "/" and next_char == "*":
            end = text.find("*/", index + 2)
            if end == -1:
                result.append(text[index:])
                break
            result.append(text[index : end + 2])
            index = end + 2
            continue

        if char == "'":
            char_end = _consume_char_literal(text, index)
            if char_end is not None:
                result.append(text[index:char_end])
                index = char_end
                continue

        if char != '"':
            result.append(char)
            index += 1
            continue

        raw_hash_count = _raw_string_hash_count_before_quote(text, index)
        if raw_hash_count is not None:
            raw_end = _consume_raw_string(text, index, raw_hash_count)
            result.append(text[index:raw_end])
            index = raw_end
            continue

        start = index
        index += 1
        literal_chars: list[str] = []
        escaped = False

        while index < len(text):
            current = text[index]
            index += 1

            if escaped:
                if current == "\n":
                    while index < len(text) and text[index] in " \t":
                        index += 1
                    escaped = False
                    continue
                if current == "\r":
                    if index < len(text) and text[index] == "\n":
                        index += 1
                    while index < len(text) and text[index] in " \t":
                        index += 1
                    escaped = False
                    continue
                literal_chars.append(current)
                escaped = False
                continue
            if current == "\\":
                escaped = True
                continue
            if current == '"':
                literal = "".join(literal_chars)
                if literal == source:
                    result.append('"')
                    result.append(target)
                    result.append('"')
                    replaced += 1
                else:
                    result.append(text[start:index])
                break
            literal_chars.append(current)
        else:
            result.append(text[start:index])

    return "".join(result), replaced


def load_manifest(path: Path) -> list[dict[str, object]]:
    replacements: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[[replace]]":
            current = {"__line": line_number}
            replacements.append(current)
            continue
        if current is None:
            raise ValueError(f"{path}:{line_number}: expected [[replace]] before key/value entries")
        if "=" not in line:
            raise ValueError(f"{path}:{line_number}: expected key = value")

        key, value = [part.strip() for part in line.split("=", 1)]
        if value.startswith('"') and value.endswith('"'):
            current[key] = _parse_quoted_manifest_value(value)
        elif value.isdigit():
            current[key] = int(value)
        else:
            raise ValueError(f"{path}:{line_number}: only quoted strings and integers are supported")

    seen: dict[tuple[str, str], int] = {}
    for replacement in replacements:
        rel_path = replacement.get("path")
        source = replacement.get("source")
        line_number = replacement.get("__line")
        if not isinstance(rel_path, str) or not isinstance(source, str):
            continue
        key = (rel_path, source)
        if key in seen:
            raise ValueError(
                f"{path}:{line_number}: duplicate replacement for {rel_path} {source!r}; "
                f"first declared at line {seen[key]}"
            )
        if isinstance(line_number, int):
            seen[key] = line_number

    return replacements


def apply_replacements(
    repo_root: Path,
    replacements: list[dict[str, object]],
    dry_run: bool,
    summary: bool,
) -> int:
    changed_files: set[Path] = set()
    manifest_files: set[Path] = set()
    already_applied = 0
    would_change = 0
    failures = 0
    replacements = sorted(
        replacements,
        key=lambda replacement: (
            str(replacement.get("path", "")),
            -len(str(replacement.get("source", ""))),
        ),
    )

    for index, replacement in enumerate(replacements, start=1):
        rel_path = replacement.get("path")
        source = replacement.get("source")
        target = replacement.get("target")
        expected_count = replacement.get("expected_count")

        if not isinstance(rel_path, str) or not isinstance(source, str) or not isinstance(target, str):
            print(f"replacement #{index} is missing string path/source/target fields", file=sys.stderr)
            failures += 1
            continue

        file_path = repo_root / rel_path
        manifest_files.add(file_path)
        if not file_path.exists():
            print(f"{rel_path}: file does not exist", file=sys.stderr)
            failures += 1
            continue

        text = file_path.read_text(encoding="utf-8")
        updated_text, found = replace_rust_string_literals(text, source, target)
        if found == 0:
            _, target_count = replace_rust_string_literals(text, target, target)
            if target_count > 0:
                already_applied += 1
                continue
            print(f"{rel_path}: source string literal not found: {source!r}", file=sys.stderr)
            failures += 1
            continue

        if expected_count is not None and found != expected_count:
            print(
                f"{rel_path}: expected {expected_count} occurrence(s) for {source!r}, found {found}",
                file=sys.stderr,
            )
            failures += 1
            continue

        if source == target:
            continue

        would_change += 1
        if not dry_run:
            file_path.write_text(updated_text, encoding="utf-8")
        changed_files.add(file_path)

    if summary:
        print(f"entries: {len(replacements)}")
        print(f"files: {len(manifest_files)}")
        print(f"already_applied: {already_applied}")
        print(f"would_change: {would_change}")
        print(f"missing: {failures}")
    else:
        for file_path in sorted(changed_files):
            print(file_path.relative_to(repo_root))

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply zh-Hans localization overrides")
    parser.add_argument(
        "--manifest",
        default="resources/localization/zh-Hans-overrides.toml",
        help="Path to the TOML replacement manifest, relative to the repo root",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate replacements without writing files")
    parser.add_argument("--summary", action="store_true", help="Print replacement status counts")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / args.manifest
    try:
        replacements = load_manifest(manifest_path)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    failures = apply_replacements(repo_root, replacements, args.dry_run, args.summary)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
