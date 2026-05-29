#!/usr/bin/env python3
"""Inventory likely user-visible strings for the local zh-Hans fork."""

from __future__ import annotations

import argparse
import re
import signal
import sys
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
SEARCH_ROOTS = ("app/src/search",)
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

EXCLUDED_PATH_PARTS = (
    "/tests/",
    "/test_data/",
    "/models/onnx/",
    "/resources/bundled/",
)

SKIP_LINE_PATTERNS = (
    "#[cfg",
    "cfg!(",
    "feature =",
    "target_family",
    "#[serde",
    "serde(",
    "log::",
    "TelemetryEvent::",
    "send_telemetry",
    "id!(",
    "ui_name()",
    ".expect(",
    "debug_assert",
    "panic!",
    "anyhow!",
    "format_err!",
    "Error::",
)

URL_RE = re.compile(r"^[a-z][a-z0-9+.-]*:(//)?", re.IGNORECASE)
KEY_RE = re.compile(r"^[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.:-]+$")
ALL_CAPS_RE = re.compile(r"^[A-Z0-9_./:-]+$")
LOWER_IDENTIFIER_RE = re.compile(r"^[a-z_][a-z0-9_]*$")
INTERNAL_NAME_RE = re.compile(
    r"^[A-Za-z0-9_]+(?:View|Slide|Modal|Dialog|Page|Panel|Action|Event|State|Id)$"
)
INTERNAL_WORDS = {
    "darwin",
    "default_as_true",
    "integration_tests",
    "linux",
    "local_fs",
    "macos",
    "test",
    "unknown",
    "wasm",
    "windows",
}


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


def is_excluded_path(path: Path) -> bool:
    normalized = "/" + path.as_posix()
    return path.name.endswith("_tests.rs") or any(part in normalized for part in EXCLUDED_PATH_PARTS)


def iter_rust_files(repo_root: Path, roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        path = repo_root / root
        if not path.exists():
            print(f"{root}: path does not exist", file=sys.stderr)
            continue
        if path.is_file():
            if path.suffix == ".rs" and not is_excluded_path(path.relative_to(repo_root)):
                files.append(path)
            continue
        for candidate in path.rglob("*.rs"):
            rel_path = candidate.relative_to(repo_root)
            if not is_excluded_path(rel_path):
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
            index = _consume_raw_string(text, index, raw_hash_count)
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


def is_candidate_literal(value: str, line_text: str) -> bool:
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
    if INTERNAL_NAME_RE.match(stripped):
        return False
    if stripped in INTERNAL_WORDS:
        return False
    if stripped.endswith(".rs"):
        return False
    if ("/" in stripped or "\\" in stripped) and " " not in stripped:
        return False
    if any(pattern in line_text for pattern in SKIP_LINE_PATTERNS):
        return False
    return True


def build_inventory(repo_root: Path, roots: list[str], manifest: str) -> list[InventoryRow]:
    source_set, target_set = load_manifest_sets(repo_root, manifest)
    rows: list[InventoryRow] = []
    for file_path in iter_rust_files(repo_root, roots):
        rel_path = file_path.relative_to(repo_root)
        rel_string = rel_path.as_posix()
        for literal in extract_string_literals(file_path):
            key = (rel_string, literal.value)
            if key in source_set:
                status = "covered-source"
            elif key in target_set:
                status = "covered-target"
            elif is_candidate_literal(literal.value, literal.line_text):
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory zh-Hans localization candidates")
    parser.add_argument("roots", nargs="*", help="Rust file or directory roots to scan")
    parser.add_argument("--preset", choices=sorted(PRESETS), help="Named source root preset")
    parser.add_argument(
        "--manifest",
        default="resources/localization/zh-Hans-overrides.toml",
        help="Path to the TOML replacement manifest, relative to the repo root",
    )
    parser.add_argument("--coverage", action="store_true", help="Print coverage counts instead of rows")
    return parser.parse_args()


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
        rows = build_inventory(repo_root, roots, args.manifest)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if args.coverage:
        print_coverage(args.preset, rows)
    else:
        print_markdown(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
