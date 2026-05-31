#!/usr/bin/env python3
"""Inventory likely user-visible strings for the local zh-Hans fork."""

from __future__ import annotations

import argparse
import re
import signal
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from zh_apply_localization import (
    _consume_char_literal,
    _consume_raw_string,
    _raw_string_hash_count_before_quote,
    load_manifest,
)


ONBOARDING_ROOTS = ("crates/onboarding/src", "app/src/auth")
WORKSPACE_ROOTS = ("app/src/workspace", "app/src/app_menus.rs", "app/src/menu.rs")
SEARCH_ROOTS = ("app/src/search", "crates/warp_search_core/src")
SETTINGS_ROOTS = ("app/src/settings_view",)
MODALS_ROOTS = (
    "app/src/auth",
    "app/src/billing",
    "app/src/themes",
    "app/src/tab_configs",
    "app/src/drive",
    "app/src/terminal",
    "app/src/ai",
)
RELEASE_ROOTS = tuple(
    dict.fromkeys(
        ONBOARDING_ROOTS
        + WORKSPACE_ROOTS
        + SEARCH_ROOTS
        + SETTINGS_ROOTS
        + MODALS_ROOTS
    )
)

PRESETS: dict[str, tuple[str, ...]] = {
    "onboarding": ONBOARDING_ROOTS,
    "workspace": WORKSPACE_ROOTS,
    "search": SEARCH_ROOTS,
    "settings": SETTINGS_ROOTS,
    "modals": MODALS_ROOTS,
    "release": RELEASE_ROOTS,
}

URL_RE = re.compile(r"^[a-z][a-z0-9+.-]*:(//)?", re.IGNORECASE)
KEY_RE = re.compile(r"^[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.:-]+$")
ALL_CAPS_RE = re.compile(r"^[A-Z0-9_./:-]+$")
LOWER_IDENTIFIER_RE = re.compile(r"^[a-z_][a-z0-9_]*$")
FILTER_TOKEN_RE = re.compile(r"^[a-z_]+:$")
KEYBINDING_RE = re.compile(
    r"^(?:cmd|ctrl|alt|shift|super|orctrl|cmdorctrl|numpad|enter|return|escape|tab|up|down|left|right|y|o|v)(?:-(?:cmd|ctrl|alt|shift|super|orctrl|cmdorctrl|numpad|enter|return|escape|tab|up|down|left|right|y|o|v))*$",
    re.IGNORECASE,
)
PLACEHOLDER_ONLY_RE = re.compile(r"^(?:\{[A-Za-z0-9_:.?]+\}|%[A-Za-z](?: %[A-Za-z])*)$")
INTERNAL_ID_WITH_PLACEHOLDER_RE = re.compile(r"^[a-z][a-z0-9_:-]*:\{[A-Za-z0-9_]+\}$")
INTERNAL_NAME_RE = re.compile(
    r"^[A-Za-z0-9_]+(?:View|Slide|Modal|Dialog|Page|Panel|Action|Event|State|Id)$"
)
DEFAULT_IGNORE_CONFIG = "resources/localization/zh-Hans-inventory-ignore.toml"


@dataclass(frozen=True)
class InventoryIgnoreConfig:
    path_parts: tuple[str, ...] = ()
    exact_paths: tuple[str, ...] = ()
    line_patterns: tuple[str, ...] = ()
    literal_patterns: tuple[str, ...] = ()
    internal_words: tuple[str, ...] = ()


@dataclass(frozen=True)
class Literal:
    path: Path
    line: int
    value: str
    line_text: str


@dataclass(frozen=True)
class InventoryRow:
    status: str
    path: Path
    line: int
    literal: str


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


def _parse_toml_string_array(path: Path, key: str, value: str, line_number: int) -> tuple[str, ...]:
    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError(f"{path}:{line_number}: {key} must be an inline string array")

    content = value[1:-1].strip()
    if not content:
        return ()

    result: list[str] = []
    index = 0
    while index < len(content):
        while index < len(content) and content[index].isspace():
            index += 1
        if index >= len(content):
            break
        if content[index] != '"':
            raise ValueError(f"{path}:{line_number}: {key} values must be quoted strings")

        index += 1
        escaped = False
        value_chars: list[str] = []
        while index < len(content):
            char = content[index]
            index += 1
            if escaped:
                escape_map = {'"': '"', "\\": "\\", "n": "\n", "r": "\r", "t": "\t"}
                value_chars.append(escape_map.get(char, "\\" + char))
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                result.append("".join(value_chars))
                break
            value_chars.append(char)
        else:
            raise ValueError(f"{path}:{line_number}: unterminated string in {key}")

        while index < len(content) and content[index].isspace():
            index += 1
        if index >= len(content):
            break
        if content[index] != ",":
            raise ValueError(f"{path}:{line_number}: expected comma in {key}")
        index += 1

    return tuple(result)


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


def load_ignore_config(path: Path) -> InventoryIgnoreConfig:
    if not path.exists():
        return InventoryIgnoreConfig()

    fields: dict[str, tuple[str, ...]] = {
        "path_parts": (),
        "exact_paths": (),
        "line_patterns": (),
        "literal_patterns": (),
        "internal_words": (),
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
            raise ValueError(f"{path}:{line_number}: unknown ignore config field {key!r}")
        fields[key] = _parse_toml_string_array(path, key, value, line_number)

    return InventoryIgnoreConfig(**fields)


def is_excluded_path(path: Path, ignore_config: InventoryIgnoreConfig | None = None) -> bool:
    if ignore_config is None:
        ignore_config = InventoryIgnoreConfig()
    normalized = "/" + path.as_posix()
    return (
        path.name.endswith("_tests.rs")
        or path.name == "telemetry.rs"
        or path.as_posix() in ignore_config.exact_paths
        or any(part in normalized for part in ignore_config.path_parts)
    )


def iter_rust_files(repo_root: Path, roots: list[str], ignore_config: InventoryIgnoreConfig) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        path = repo_root / root
        if not path.exists():
            print(f"{root}: path does not exist", file=sys.stderr)
            continue
        if path.is_file():
            if path.suffix == ".rs" and not is_excluded_path(path.relative_to(repo_root), ignore_config):
                files.append(path)
            continue
        for candidate in path.rglob("*.rs"):
            rel_path = candidate.relative_to(repo_root)
            if not is_excluded_path(rel_path, ignore_config):
                files.append(candidate)
    return sorted(set(files))


def line_for_index(line_starts: list[int], index: int) -> int:
    low = 0
    high = len(line_starts)
    while low + 1 < high:
        mid = (low + high) // 2
        if line_starts[mid] <= index:
            low = mid
        else:
            high = mid
    return low + 1


def extract_string_literals(path: Path) -> list[Literal]:
    text = path.read_text(encoding="utf-8")
    line_starts = [0]
    line_starts.extend(index + 1 for index, char in enumerate(text) if char == "\n")
    lines = text.splitlines()

    literals: list[Literal] = []
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
            if text[raw_end - len(terminator) : raw_end] == terminator:
                line = line_for_index(line_starts, index)
                line_text = lines[line - 1] if line - 1 < len(lines) else ""
                literals.append(
                    Literal(
                        path=path,
                        line=line,
                        value=text[index + 1 : raw_end - len(terminator)],
                        line_text=line_text,
                    )
                )
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
                line = line_for_index(line_starts, start)
                line_text = lines[line - 1] if line - 1 < len(lines) else ""
                literals.append(Literal(path=path, line=line, value="".join(literal_chars), line_text=line_text))
                break
            literal_chars.append(current)

    return literals


def load_manifest_sets(repo_root: Path, manifest: str) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    replacements = load_manifest(repo_root / manifest)
    sources: set[tuple[str, str]] = set()
    targets: set[tuple[str, str]] = set()
    for replacement in replacements:
        rel_path = replacement.get("path")
        source = replacement.get("source")
        target = replacement.get("target")
        if isinstance(rel_path, str) and isinstance(source, str):
            sources.add((rel_path, source))
        if isinstance(rel_path, str) and isinstance(target, str):
            targets.add((rel_path, target))
    return sources, targets


def is_candidate_literal(
    value: str,
    line_text: str,
    ignore_config: InventoryIgnoreConfig | None = None,
) -> bool:
    if ignore_config is None:
        ignore_config = InventoryIgnoreConfig()
    stripped = value.strip()
    if len(stripped) < 2:
        return False
    if not re.search(r"[A-Za-z]", stripped):
        return False
    if URL_RE.match(stripped):
        return False
    if KEY_RE.match(stripped):
        return False
    if ALL_CAPS_RE.match(stripped):
        return False
    if LOWER_IDENTIFIER_RE.match(stripped):
        return False
    if FILTER_TOKEN_RE.match(stripped):
        return False
    if KEYBINDING_RE.match(stripped):
        return False
    if PLACEHOLDER_ONLY_RE.match(stripped):
        return False
    if INTERNAL_ID_WITH_PLACEHOLDER_RE.match(stripped):
        return False
    if INTERNAL_NAME_RE.match(stripped):
        return False
    if stripped in ignore_config.internal_words:
        return False
    if any(re.search(pattern, stripped) for pattern in ignore_config.literal_patterns):
        return False
    if stripped.endswith(".rs"):
        return False
    if ("/" in stripped or "\\" in stripped) and " " not in stripped:
        return False
    if any(pattern in line_text for pattern in ignore_config.line_patterns):
        return False
    return True


def build_inventory(
    repo_root: Path,
    roots: list[str],
    manifest: str,
    ignore_config: InventoryIgnoreConfig,
) -> list[InventoryRow]:
    source_set, target_set = load_manifest_sets(repo_root, manifest)
    rows: list[InventoryRow] = []
    for file_path in iter_rust_files(repo_root, roots, ignore_config):
        rel_path = file_path.relative_to(repo_root)
        rel_string = rel_path.as_posix()
        for literal in extract_string_literals(file_path):
            key = (rel_string, literal.value)
            if key in source_set:
                status = "covered-source"
            elif key in target_set:
                status = "covered-target"
            elif is_candidate_literal(literal.value, literal.line_text, ignore_config):
                status = "candidate"
            else:
                continue
            rows.append(InventoryRow(status=status, path=rel_path, line=literal.line, literal=literal.value))
    return rows


def markdown_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "\\n")


def print_markdown(rows: list[InventoryRow]) -> None:
    print("| status | path | line | literal |")
    print("| --- | --- | ---: | --- |")
    for row in rows:
        print(
            f"| {row.status} | `{row.path.as_posix()}` | {row.line} | "
            f"{markdown_escape(row.literal)} |"
        )


def print_coverage(preset: str | None, rows: list[InventoryRow]) -> None:
    covered = sum(1 for row in rows if row.status != "candidate")
    candidates = sum(1 for row in rows if row.status == "candidate")
    total = covered + candidates
    coverage = (covered / total * 100) if total else 100.0
    print(f"preset: {preset or 'custom'}")
    print(f"covered: {covered}")
    print(f"candidates: {candidates}")
    print(f"coverage: {coverage:.1f}%")


def print_top_paths(rows: list[InventoryRow], limit: int) -> None:
    counts = Counter(row.path.as_posix() for row in rows if row.status == "candidate")
    print("| candidates | path |")
    print("| ---: | --- |")
    for path, count in counts.most_common(limit):
        print(f"| {count} | `{path}` |")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory zh-Hans localization candidates")
    parser.add_argument("roots", nargs="*", help="Rust file or directory roots to scan")
    parser.add_argument("--preset", choices=sorted(PRESETS), help="Named source root preset")
    parser.add_argument(
        "--manifest",
        default="resources/localization/zh-Hans-overrides.toml",
        help="Path to the TOML replacement manifest, relative to the repo root",
    )
    parser.add_argument(
        "--ignore-config",
        default=DEFAULT_IGNORE_CONFIG,
        help="Path to inventory ignore config, relative to the repo root",
    )
    parser.add_argument("--coverage", action="store_true", help="Print coverage counts instead of rows")
    parser.add_argument(
        "--status",
        choices=("candidate", "covered-source", "covered-target"),
        help="Only print rows with this status",
    )
    parser.add_argument(
        "--top-paths",
        type=int,
        metavar="N",
        help="Print the top N paths by candidate count instead of row details",
    )
    args = parser.parse_args()
    if args.coverage and args.top_paths is not None:
        parser.error("--coverage cannot be combined with --top-paths")
    if args.top_paths is not None and args.top_paths < 1:
        parser.error("--top-paths must be greater than 0")
    return args


def main() -> int:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    args = parse_args()
    if args.preset:
        roots = list(PRESETS[args.preset])
    else:
        roots = args.roots

    if not roots:
        print("provide roots or --preset", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    try:
        ignore_config = load_ignore_config(repo_root / args.ignore_config)
        rows = build_inventory(repo_root, roots, args.manifest, ignore_config)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if args.coverage:
        print_coverage(args.preset, rows)
    elif args.top_paths is not None:
        print_top_paths(rows, args.top_paths)
    else:
        if args.status is not None:
            rows = [row for row in rows if row.status == args.status]
        print_markdown(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
