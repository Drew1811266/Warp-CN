#!/usr/bin/env python3
"""Scan zh-Hans localization assets for mojibake, encoding, and layout risks."""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Iterable

from zh_apply_localization import load_manifest


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATHS = (
    REPO_ROOT / "resources/localization",
    REPO_ROOT / "app",
    REPO_ROOT / "crates",
    REPO_ROOT / "docs",
)
TEXT_EXTENSIONS = {
    ".json",
    ".md",
    ".py",
    ".rs",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SKIP_DIRS = {
    ".git",
    ".worktrees",
    "node_modules",
    "target",
}
MOJIBAKE_SIGNATURES = (
    "\ufffd",
    "Ã",
    "Â",
    "â€™",
    "â€œ",
    "â€",
    "ä¸",
)
COMPACT_UI_TERMS = (
    "button",
    "menu",
    "modal",
    "toast",
    "tab",
    "label",
    "placeholder",
    "title",
    "toggle",
    "settings",
    "toolbar",
)


@dataclasses.dataclass(frozen=True)
class Finding:
    path: str
    line: int
    category: str
    decision: str
    snippet: str


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _iter_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        resolved = path if path.is_absolute() else REPO_ROOT / path
        if not resolved.exists():
            continue
        if resolved.is_file():
            if resolved.suffix in TEXT_EXTENSIONS:
                yield resolved
            continue
        for child in resolved.rglob("*"):
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            if child.is_file() and child.suffix in TEXT_EXTENSIONS:
                yield child


def _line_is_documentation_example(path: Path, line: str) -> bool:
    if "docs" not in path.parts:
        return False
    if "calibration" in path.name:
        return True
    lowered = line.lower()
    return "mojibake" in lowered or "example" in lowered or "例如" in line or "rg -n" in line


def _line_is_test_fixture(path: Path) -> bool:
    return any(part in {"test_data", "test_fixtures", "tests"} for part in path.parts)


def _snippet(line: str) -> str:
    return line.strip().encode("unicode_escape").decode("ascii")[:180]


def _scan_text_file(path: Path) -> list[Finding]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return [
            Finding(
                path=_relative(path),
                line=error.start + 1,
                category="invalid-utf8",
                decision="needs-encoding-review",
                snippet=f"decode error at byte {error.start}",
            )
        ]

    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        for signature in MOJIBAKE_SIGNATURES:
            if signature not in line:
                continue
            if signature == "\ufffd":
                category = "replacement-character"
            else:
                category = "mojibake-signature"
            if _line_is_documentation_example(path, line):
                decision = "example-only"
            elif _line_is_test_fixture(path):
                decision = "fixture-only"
            else:
                decision = "needs-review"
            findings.append(
                Finding(
                    path=_relative(path),
                    line=line_number,
                    category=category,
                    decision=decision,
                    snippet=_snippet(line),
                )
            )
            break
        if any(ord(char) < 32 and char not in "\t" for char in line):
            if "\x1b[" in line:
                findings.append(
                    Finding(
                        path=_relative(path),
                        line=line_number,
                        category="terminal-ansi-sequence",
                        decision="accepted-token",
                        snippet=_snippet(line),
                    )
                )
                continue
            findings.append(
                Finding(
                    path=_relative(path),
                    line=line_number,
                    category="control-character",
                    decision="needs-review",
                    snippet=_snippet(line),
                )
            )
    return findings


def _is_compact_context(path: str, source: str, context: str) -> bool:
    haystack = f"{path}\n{source}\n{context}".lower()
    return any(term in haystack for term in COMPACT_UI_TERMS)


def _scan_manifest_layout(manifest_path: Path) -> list[Finding]:
    if not manifest_path.exists():
        return []
    findings: list[Finding] = []
    for replacement in load_manifest(manifest_path):
        path = str(replacement.get("path", ""))
        source = str(replacement.get("source", ""))
        target = str(replacement.get("target", ""))
        context = str(replacement.get("context", ""))
        line = replacement.get("__line", 0)
        if not _is_compact_context(path, source, context):
            continue
        source_len = len(source)
        target_len = len(target)
        if source_len < 100 and target_len > max(source_len * 2.4, source_len + 36):
            findings.append(
                Finding(
                    path=_relative(manifest_path),
                    line=line if isinstance(line, int) else 0,
                    category="overlong-compact-ui-target",
                    decision="needs-layout-review",
                    snippet=target[:180],
                )
            )
    return findings


def scan(paths: Iterable[Path], *, manifest_path: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_files(paths):
        findings.extend(_scan_text_file(path))
    if manifest_path is not None:
        findings.extend(_scan_manifest_layout(manifest_path))
    return sorted(findings, key=lambda finding: (finding.path, finding.line, finding.category))


def render_json(findings: list[Finding]) -> str:
    actionable_decisions = {"needs-review", "needs-encoding-review", "needs-layout-review"}
    payload = {
        "total_findings": len(findings),
        "actionable_findings": sum(1 for finding in findings if finding.decision in actionable_decisions),
        "findings": [dataclasses.asdict(finding) for finding in findings],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_markdown(findings: list[Finding]) -> str:
    actionable_decisions = {"needs-review", "needs-encoding-review", "needs-layout-review"}
    lines = [
        "# zh-Hans Mojibake And Layout Findings",
        "",
        "This report is static and low-load. It does not prove GUI rendering readiness.",
        "",
        f"- Total findings: {len(findings)}",
        f"- Actionable findings: {sum(1 for finding in findings if finding.decision in actionable_decisions)}",
        "",
    ]
    if not findings:
        lines.extend(["## Findings", "", "No mojibake or static layout findings were produced.", ""])
        return "\n".join(lines)

    lines.extend(["## Findings", "", "| file | line | category | decision | snippet |", "| --- | ---: | --- | --- | --- |"])
    for finding in findings:
        snippet = finding.snippet.replace("|", "/")
        lines.append(
            f"| `{finding.path}` | {finding.line} | `{finding.category}` | `{finding.decision}` | {snippet} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", nargs="*", type=Path, default=list(DEFAULT_PATHS))
    parser.add_argument("--manifest", type=Path, default=REPO_ROOT / "resources/localization/zh-Hans-overrides.toml")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument("--markdown", action="store_true", help="Print Markdown output")
    args = parser.parse_args(argv)

    findings = scan(args.paths, manifest_path=args.manifest)
    if args.json:
        print(render_json(findings), end="")
        return 0
    if args.markdown:
        print(render_markdown(findings), end="")
        return 0
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.category}: {finding.decision}: {finding.snippet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
