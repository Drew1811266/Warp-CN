#!/usr/bin/env python3
"""Apply local Chinese UI string overrides to the Warp source tree.

This is intentionally small and strict: each entry must match text in the
target file, so upstream string drift is reported during maintenance instead
of being silently missed.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


STRING_FIELDS = {"path", "source", "target", "key", "context", "status", "notes"}
INTEGER_FIELDS = {"expected_count"}
STRING_ARRAY_FIELDS = {"preserve_terms"}
ALLOWED_FIELDS = STRING_FIELDS | INTEGER_FIELDS | STRING_ARRAY_FIELDS
ALLOWED_STATUSES = {"active", "needs-review", "deprecated", "blocked"}
DEFAULT_GLOSSARY_CONFIG = "resources/localization/zh-Hans-glossary.toml"


@dataclass(frozen=True)
class GlossaryConfig:
    preserve_terms: tuple[str, ...] = ()
    required_translations: tuple[tuple[str, str], ...] = ()
    forbidden_targets: tuple[str, ...] = ()


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
            escape_map = {'"': '"', "\\": "\\", "n": "\n", "r": "\r", "t": "\t"}
            if char in escape_map:
                result.append(escape_map[char])
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


def _parse_string_array_manifest_value(path: Path, line_number: int, value: str) -> list[str]:
    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError(f"{path}:{line_number}: expected inline string array")

    content = value[1:-1].strip()
    if not content:
        return []

    result: list[str] = []
    index = 0
    while index < len(content):
        while index < len(content) and content[index].isspace():
            index += 1

        if index >= len(content):
            break
        if content[index] != '"':
            raise ValueError(f"{path}:{line_number}: array values must be quoted strings")

        start = index
        index += 1
        escaped = False
        while index < len(content):
            char = content[index]
            index += 1
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                result.append(_parse_quoted_manifest_value(content[start:index]))
                break
        else:
            raise ValueError(f"{path}:{line_number}: unterminated quoted array value")

        while index < len(content) and content[index].isspace():
            index += 1
        if index >= len(content):
            break
        if content[index] != ",":
            raise ValueError(f"{path}:{line_number}: expected comma between array values")
        index += 1

    return result


def _strip_toml_comment(line: str) -> str:
    result: list[str] = []
    escaped = False
    in_string = False

    for char in line:
        if escaped:
            result.append(char)
            escaped = False
            continue
        if char == "\\" and in_string:
            result.append(char)
            escaped = True
            continue
        if char == '"':
            result.append(char)
            in_string = not in_string
            continue
        if char == "#" and not in_string:
            break
        result.append(char)

    return "".join(result).strip()


def _bracket_delta_outside_strings(line: str) -> int:
    delta = 0
    escaped = False
    in_string = False

    for char in line:
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_string:
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "[":
            delta += 1
        elif char == "]":
            delta -= 1

    return delta


def _normalize_multiline_arrays(lines: list[str]) -> list[tuple[int, str]]:
    normalized: list[tuple[int, str]] = []
    pending_line_number = 0
    pending_parts: list[str] = []
    bracket_depth = 0

    for index, raw_line in enumerate(lines, start=1):
        line = _strip_toml_comment(raw_line)
        if not line:
            continue

        if bracket_depth == 0:
            pending_line_number = index
            pending_parts = [line]
        else:
            pending_parts.append(line)

        bracket_depth += _bracket_delta_outside_strings(line)
        if bracket_depth < 0:
            raise ValueError(f"line {index}: unexpected closing bracket")
        if bracket_depth == 0:
            normalized.append((pending_line_number, " ".join(pending_parts)))
            pending_parts = []

    if bracket_depth != 0:
        raise ValueError(f"line {pending_line_number}: unterminated array")

    return normalized


def _parse_multiline_manifest_value(
    path: Path,
    lines: list[str],
    line_index: int,
    value: str,
) -> tuple[str, int]:
    content = value[3:]
    parts: list[str] = []

    while True:
        closing_index = content.find('"""')
        if closing_index != -1:
            trailing = content[closing_index + 3 :].strip()
            if trailing:
                line_number = line_index + 1
                raise ValueError(f"{path}:{line_number}: unexpected content after multiline value")
            parts.append(content[:closing_index])
            return "".join(parts), line_index

        parts.append(content)
        line_index += 1
        if line_index >= len(lines):
            raise ValueError(f"{path}:{line_index}: unterminated multiline value")
        content = "\n" + lines[line_index]


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
            terminator = '"' + ("#" * raw_hash_count)
            if text[raw_end - len(terminator) : raw_end] != terminator:
                result.append(text[index:raw_end])
                index = raw_end
                continue

            literal = text[index + 1 : raw_end - len(terminator)]
            if literal == source:
                result.append('"')
                result.append(target)
                result.append(terminator)
                replaced += 1
            else:
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
                    result.append(_escape_rust_string_literal_content(target))
                    result.append('"')
                    replaced += 1
                else:
                    result.append(text[start:index])
                break
            literal_chars.append(current)
        else:
            result.append(text[start:index])

    return "".join(result), replaced


def _escape_rust_string_literal_content(value: str) -> str:
    """Escape replacement text before writing it into a normal Rust string."""

    result: list[str] = []
    for char in value:
        if char == "\\":
            result.append("\\\\")
        elif char == '"':
            result.append('\\"')
        elif char == "\n":
            result.append("\\n")
        elif char == "\r":
            result.append("\\r")
        elif char == "\t":
            result.append("\\t")
        else:
            result.append(char)
    return "".join(result)


def replace_rust_string_literals_many(
    text: str,
    replacements_by_source: dict[str, str],
) -> tuple[dict[str, int], dict[str, int]]:
    """Count many replacement sources/targets in one Rust string-literal pass."""

    found_counts = {source: 0 for source in replacements_by_source}
    target_counts = {source: 0 for source in replacements_by_source}
    sources_by_target: dict[str, list[str]] = {}
    for source, target in replacements_by_source.items():
        sources_by_target.setdefault(target, []).append(source)

    def count_literal(literal: str) -> None:
        if literal in replacements_by_source:
            found_counts[literal] += 1
        for source in sources_by_target.get(literal, ()):
            target_counts[source] += 1

    index = 0

    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if char == "/" and next_char == "/":
            newline = text.find("\n", index + 2)
            if newline == -1:
                break
            index = newline + 1
            continue

        if char == "/" and next_char == "*":
            end = text.find("*/", index + 2)
            if end == -1:
                break
            index = end + 2
            continue

        if char == "'":
            char_end = _consume_char_literal(text, index)
            if char_end is not None:
                index = char_end
                continue

        if char != '"':
            index += 1
            continue

        raw_hash_count = _raw_string_hash_count_before_quote(text, index)
        if raw_hash_count is not None:
            raw_end = _consume_raw_string(text, index, raw_hash_count)
            terminator = '"' + ("#" * raw_hash_count)
            if text[raw_end - len(terminator) : raw_end] != terminator:
                index = raw_end
                continue

            literal = text[index + 1 : raw_end - len(terminator)]
            count_literal(literal)
            index = raw_end
            continue

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
                count_literal("".join(literal_chars))
                break
            literal_chars.append(current)

    return found_counts, target_counts


def replace_rust_string_literals_many_apply(
    text: str,
    replacements_by_source: dict[str, str],
) -> tuple[str, dict[str, int], dict[str, int]]:
    """Replace many Rust string literals in one pass and report source/target counts."""

    result: list[str] = []
    found_counts = {source: 0 for source in replacements_by_source}
    target_counts = {source: 0 for source in replacements_by_source}
    sources_by_target: dict[str, list[str]] = {}
    for source, target in replacements_by_source.items():
        sources_by_target.setdefault(target, []).append(source)

    def replacement_for_literal(literal: str) -> str | None:
        if literal in replacements_by_source:
            found_counts[literal] += 1
            return replacements_by_source[literal]
        for source in sources_by_target.get(literal, ()):
            target_counts[source] += 1
        return None

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
            terminator = '"' + ("#" * raw_hash_count)
            if text[raw_end - len(terminator) : raw_end] != terminator:
                result.append(text[index:raw_end])
                index = raw_end
                continue

            literal = text[index + 1 : raw_end - len(terminator)]
            replacement = replacement_for_literal(literal)
            if replacement is None:
                result.append(text[index:raw_end])
            else:
                result.append('"')
                result.append(replacement)
                result.append(terminator)
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
                replacement = replacement_for_literal(literal)
                if replacement is None:
                    result.append(text[start:index])
                else:
                    result.append('"')
                    result.append(_escape_rust_string_literal_content(replacement))
                    result.append('"')
                break
            literal_chars.append(current)
        else:
            result.append(text[start:index])

    return "".join(result), found_counts, target_counts


def load_manifest(path: Path) -> list[dict[str, object]]:
    replacements: list[dict[str, object]] = []
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
        if line == "[[replace]]":
            current = {"__line": line_number}
            replacements.append(current)
            line_index += 1
            continue
        if current is None:
            raise ValueError(f"{path}:{line_number}: expected [[replace]] before key/value entries")
        if "=" not in line:
            raise ValueError(f"{path}:{line_number}: expected key = value")

        key, value = [part.strip() for part in line.split("=", 1)]
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"{path}:{line_number}: unknown manifest field {key!r}")
        if key in STRING_ARRAY_FIELDS:
            current[key] = _parse_string_array_manifest_value(path, line_number, value)
        elif key in INTEGER_FIELDS:
            if not value.isdigit():
                raise ValueError(f"{path}:{line_number}: {key} must be an integer")
            current[key] = int(value)
        elif value.startswith('"""'):
            current[key], line_index = _parse_multiline_manifest_value(path, lines, line_index, value)
        elif value.startswith('"') and value.endswith('"'):
            current[key] = _parse_quoted_manifest_value(value)
        else:
            raise ValueError(f"{path}:{line_number}: {key} must be a quoted string")
        line_index += 1

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


def _parse_required_translation(raw_value: str, path: Path, line_number: int) -> tuple[str, str]:
    if "=>" not in raw_value:
        raise ValueError(f"{path}:{line_number}: required_translations values must use 'source => target'")
    source, target = [part.strip() for part in raw_value.split("=>", 1)]
    if not source or not target:
        raise ValueError(f"{path}:{line_number}: required_translations values must not be empty")
    return source, target


def load_glossary_config(path: Path) -> GlossaryConfig:
    if not path.exists():
        raise ValueError(f"{path}: glossary config does not exist")

    fields: dict[str, tuple[str, ...]] = {
        "preserve_terms": (),
        "required_translations": (),
        "forbidden_targets": (),
    }
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        entries = _normalize_multiline_arrays(lines)
    except ValueError as error:
        raise ValueError(f"{path}:{error}") from error

    for line_number, line in entries:
        if "=" not in line:
            raise ValueError(f"{path}:{line_number}: expected key = value")
        key, value = [part.strip() for part in line.split("=", 1)]
        if key not in fields:
            raise ValueError(f"{path}:{line_number}: unknown glossary field {key!r}")
        fields[key] = tuple(_parse_string_array_manifest_value(path, line_number, value))

    required_translations = tuple(
        _parse_required_translation(value, path, 1)
        for value in fields["required_translations"]
    )

    return GlossaryConfig(
        preserve_terms=fields["preserve_terms"],
        required_translations=required_translations,
        forbidden_targets=fields["forbidden_targets"],
    )


def check_glossary(
    replacements: list[dict[str, object]],
    glossary: GlossaryConfig,
) -> list[str]:
    errors: list[str] = []

    for index, replacement in enumerate(replacements, start=1):
        source = replacement.get("source")
        target = replacement.get("target")
        if not isinstance(source, str) or not isinstance(target, str):
            continue

        line_number = replacement.get("__line")
        location = f"replacement #{index}"
        if isinstance(line_number, int):
            location = f"replacement #{index} at line {line_number}"

        for term in glossary.preserve_terms:
            if term in source and term not in target:
                errors.append(f"{location}: missing preserved term {term!r} in target")

        for source_term, target_term in glossary.required_translations:
            if source_term in source and target_term not in target:
                errors.append(
                    f"{location}: expected translation {target_term!r} for source term {source_term!r}"
                )

        for forbidden_target in glossary.forbidden_targets:
            if forbidden_target in target:
                errors.append(f"{location}: forbidden target term {forbidden_target!r}")

    return errors


def validate_manifest(replacements: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    seen_keys: dict[str, int] = {}

    for index, replacement in enumerate(replacements, start=1):
        line_number = replacement.get("__line")
        location = f"replacement #{index}"
        if isinstance(line_number, int):
            location = f"replacement #{index} at line {line_number}"

        for required_field in ("path", "source", "target"):
            if not isinstance(replacement.get(required_field), str):
                errors.append(f"{location}: missing required string field {required_field!r}")

        key = replacement.get("key")
        if key is not None:
            if not isinstance(key, str) or not key.strip():
                errors.append(f"{location}: key must be a non-empty string")
            elif key in seen_keys:
                errors.append(
                    f"{location}: duplicate key {key!r}; first declared at line {seen_keys[key]}"
                )
            elif isinstance(line_number, int):
                seen_keys[key] = line_number

        status = replacement.get("status")
        if status is not None and status not in ALLOWED_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_STATUSES))
            errors.append(f"{location}: invalid status {status!r}; expected one of: {allowed}")

        preserve_terms = replacement.get("preserve_terms")
        if preserve_terms is not None and (
            not isinstance(preserve_terms, list)
            or any(not isinstance(term, str) or not term for term in preserve_terms)
        ):
            errors.append(f"{location}: preserve_terms must be an array of non-empty strings")

        expected_count = replacement.get("expected_count")
        if expected_count is not None and (
            not isinstance(expected_count, int) or expected_count < 1
        ):
            errors.append(f"{location}: expected_count must be a positive integer")

    return errors


def metadata_summary(replacements: list[dict[str, object]]) -> dict[str, int]:
    summary = {
        "entries": len(replacements),
        "key": 0,
        "context": 0,
        "status": 0,
        "preserve_terms": 0,
        "notes": 0,
        "expected_count": 0,
    }

    for replacement in replacements:
        for field in ("key", "context", "status", "notes"):
            value = replacement.get(field)
            if isinstance(value, str) and value.strip():
                summary[field] += 1

        preserve_terms = replacement.get("preserve_terms")
        if isinstance(preserve_terms, list) and preserve_terms:
            summary["preserve_terms"] += 1

        expected_count = replacement.get("expected_count")
        if isinstance(expected_count, int):
            summary["expected_count"] += 1

    return summary


def metadata_summary_report(replacements: list[dict[str, object]]) -> dict[str, object]:
    summary = metadata_summary(replacements)
    entries = summary["entries"]
    report: dict[str, object] = {"entries": entries}
    for field in ("key", "context", "status", "preserve_terms", "notes", "expected_count"):
        count = summary[field]
        percentage = (count / entries * 100) if entries else 0.0
        report[field] = {"count": count, "percent": round(percentage, 1)}
    return report


def print_metadata_summary(
    replacements: list[dict[str, object]],
    *,
    json_output: bool = False,
) -> None:
    if json_output:
        print(json.dumps(metadata_summary_report(replacements), ensure_ascii=False, indent=2))
        return

    summary = metadata_summary(replacements)
    entries = summary["entries"]
    print(f"entries: {entries}")
    for field in ("key", "context", "status", "preserve_terms", "notes", "expected_count"):
        count = summary[field]
        percentage = (count / entries * 100) if entries else 0.0
        print(f"{field}: {count} ({percentage:.1f}%)")


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

    if dry_run:
        grouped_replacements: dict[Path, list[tuple[int, dict[str, object]]]] = {}
        for index, replacement in enumerate(replacements, start=1):
            rel_path = replacement.get("path")
            source = replacement.get("source")
            target = replacement.get("target")

            if not isinstance(rel_path, str) or not isinstance(source, str) or not isinstance(target, str):
                print(f"replacement #{index} is missing string path/source/target fields", file=sys.stderr)
                failures += 1
                continue

            file_path = repo_root / rel_path
            manifest_files.add(file_path)
            grouped_replacements.setdefault(file_path, []).append((index, replacement))

        for file_path, file_replacements in grouped_replacements.items():
            rel_path = str(file_path.relative_to(repo_root))
            if not file_path.exists():
                print(f"{rel_path}: file does not exist", file=sys.stderr)
                failures += len(file_replacements)
                continue

            text = file_path.read_text(encoding="utf-8")
            replacements_by_source = {
                str(replacement["source"]): str(replacement["target"])
                for _, replacement in file_replacements
            }
            found_counts, target_counts = replace_rust_string_literals_many(
                text,
                replacements_by_source,
            )

            for _, replacement in file_replacements:
                source = str(replacement["source"])
                target = str(replacement["target"])
                expected_count = replacement.get("expected_count")
                found = found_counts[source]

                if found == 0:
                    if target_counts[source] > 0:
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

    grouped_replacements: dict[Path, list[tuple[int, dict[str, object]]]] = {}
    for index, replacement in enumerate(replacements, start=1):
        rel_path = replacement.get("path")
        source = replacement.get("source")
        target = replacement.get("target")

        if not isinstance(rel_path, str) or not isinstance(source, str) or not isinstance(target, str):
            print(f"replacement #{index} is missing string path/source/target fields", file=sys.stderr)
            failures += 1
            continue

        file_path = repo_root / rel_path
        manifest_files.add(file_path)
        grouped_replacements.setdefault(file_path, []).append((index, replacement))

    updated_file_cache: dict[Path, str] = {}

    for file_path, file_replacements in grouped_replacements.items():
        rel_path = str(file_path.relative_to(repo_root))
        if not file_path.exists():
            print(f"{rel_path}: file does not exist", file=sys.stderr)
            failures += len(file_replacements)
            continue

        text = file_path.read_text(encoding="utf-8")
        replacements_by_source = {
            str(replacement["source"]): str(replacement["target"])
            for _, replacement in file_replacements
        }
        found_counts, target_counts = replace_rust_string_literals_many(
            text,
            replacements_by_source,
        )

        valid_replacements: dict[str, str] = {}
        for _, replacement in file_replacements:
            source = str(replacement["source"])
            target = str(replacement["target"])
            expected_count = replacement.get("expected_count")
            found = found_counts[source]

            if found == 0:
                if target_counts[source] > 0:
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
            valid_replacements[source] = target
            changed_files.add(file_path)

        if valid_replacements:
            updated_text, _, _ = replace_rust_string_literals_many_apply(text, valid_replacements)
            updated_file_cache[file_path] = updated_text

    for file_path in sorted(updated_file_cache):
        file_path.write_text(updated_file_cache[file_path], encoding="utf-8")

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
    parser.add_argument(
        "--validate-manifest",
        action="store_true",
        help="Validate manifest schema and metadata without applying replacements",
    )
    parser.add_argument(
        "--glossary-config",
        default=DEFAULT_GLOSSARY_CONFIG,
        help="Path to zh-Hans glossary config, relative to the repo root",
    )
    parser.add_argument(
        "--check-glossary",
        action="store_true",
        help="Validate manifest translations against the zh-Hans glossary",
    )
    parser.add_argument(
        "--metadata-summary",
        action="store_true",
        help="Print manifest v2 metadata coverage counts without applying replacements",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output. Currently supported with --metadata-summary.",
    )
    args = parser.parse_args()
    if args.json and not args.metadata_summary:
        parser.error("--json is currently supported only with --metadata-summary")

    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / args.manifest
    try:
        replacements = load_manifest(manifest_path)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if args.validate_manifest:
        errors = validate_manifest(replacements)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("manifest validation passed")
        return 0

    if args.check_glossary:
        try:
            glossary = load_glossary_config(repo_root / args.glossary_config)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1
        errors = check_glossary(replacements, glossary)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("glossary check passed")
        return 0

    if args.metadata_summary:
        print_metadata_summary(replacements, json_output=args.json)
        return 0

    failures = apply_replacements(repo_root, replacements, args.dry_run, args.summary)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
