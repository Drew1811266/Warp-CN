#!/usr/bin/env python3

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


MEDIA_EXTENSIONS = {
    ".avi",
    ".bmp",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".png",
    ".tif",
    ".tiff",
    ".webm",
    ".webp",
}

RAW_EVIDENCE_EXTENSIONS = {
    ".har",
    ".log",
    ".pcap",
    ".trace",
    ".webarchive",
}

RAW_EVIDENCE_SUFFIXES = (
    ".log.txt",
)

RAW_EVIDENCE_PREFIXES = (
    ".gui-smoke-artifacts/",
    ".local-artifacts/",
    ".privacy-artifacts/",
    "docs/gui-smoke-artifacts/",
    "gui-smoke-artifacts/",
    "playwright-report/",
    "test-results/",
)

SENSITIVE_PATH_PARTS = {
    ".gui-smoke-artifacts",
    ".local-artifacts",
    ".privacy-artifacts",
    "captures",
    "desktop-captures",
    "gui-smoke-artifacts",
    "playwright-report",
    "screen-captures",
    "screen-recordings",
    "screenshots",
    "test-results",
}

SENSITIVE_NAME_TOKENS = (
    "clean shot",
    "cleanshot",
    "desktop",
    "frame_capture",
    "gui-smoke",
    "screen capture",
    "screen recording",
    "screen-capture",
    "screen-recording",
    "screen_capture",
    "screen_recording",
    "screenshot",
    "screen-shot",
    "screen_shot",
    "截屏",
    "截图",
    "录屏",
)

APPROVED_MEDIA_PREFIXES = (
    "app/DockTilePlugin/Resources/",
    "app/assets/",
    "app/channels/",
    "app/src/editor/view/figma_utils/",
    "crates/editor/test_fixtures/",
    "crates/warpui/examples/assets/",
    "crates/warpui_core/test_data/",
    "images/",
    "script/windows/installer-images/",
    "specs/GH11107/",
)

ALLOWLIST_FILE = Path("script/privacy_guard_allowlist.txt")


@dataclasses.dataclass(frozen=True)
class Finding:
    path: str
    reason: str


def normalize_path(path: Path | str) -> str:
    return Path(path).as_posix().lstrip("./")


def lower_parts(path: str) -> set[str]:
    return {part.lower() for part in path.split("/") if part}


def has_sensitive_name(path: str) -> bool:
    lowered = path.lower()
    return any(token in lowered for token in SENSITIVE_NAME_TOKENS)


def has_raw_evidence_suffix(path: str) -> bool:
    lowered = path.lower()
    suffix = Path(lowered).suffix
    return suffix in RAW_EVIDENCE_EXTENSIONS or any(lowered.endswith(item) for item in RAW_EVIDENCE_SUFFIXES)


def is_under_prefix(path: str, prefixes: Sequence[str]) -> bool:
    return any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in prefixes)


def load_allowlist(repo_root: Path | None = None) -> tuple[str, ...]:
    root = repo_root or Path.cwd()
    allowlist_path = root / ALLOWLIST_FILE
    if not allowlist_path.exists():
        return ()

    patterns: list[str] = []
    for line in allowlist_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return tuple(patterns)


def is_allowlisted(path: str, allowlist: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in allowlist)


def classify_path(path: Path | str, allowlist: Sequence[str] = ()) -> str | None:
    normalized = normalize_path(path)
    if not normalized or normalized == "docs/gui-smoke-artifacts/.gitkeep":
        return None

    lowered = normalized.lower()
    suffix = Path(lowered).suffix
    parts = lower_parts(normalized)
    is_media = suffix in MEDIA_EXTENSIONS
    is_raw_evidence = has_raw_evidence_suffix(normalized)

    if normalized.startswith("docs/gui-smoke-artifacts/"):
        return "raw GUI smoke evidence must never be committed"

    if is_under_prefix(normalized, RAW_EVIDENCE_PREFIXES):
        return "local test evidence must stay outside Git history"

    if is_media and normalized.startswith("docs/"):
        return "documentation media is blocked by default; commit only reviewed redacted evidence via allowlist"

    if is_media and has_sensitive_name(normalized):
        return "screen capture or desktop recording media must not be committed"

    if is_media and parts.intersection(SENSITIVE_PATH_PARTS):
        return "screen capture or test artifact media must not be committed"

    if is_raw_evidence and (parts.intersection(SENSITIVE_PATH_PARTS) or has_sensitive_name(normalized)):
        return "raw logs or traces from local evidence runs must not be committed"

    if is_allowlisted(normalized, allowlist):
        return None

    if is_media and not is_under_prefix(normalized, APPROVED_MEDIA_PREFIXES):
        return "new media outside approved product asset paths must be reviewed before commit"

    return None


def scan_paths(paths: Iterable[Path | str], *, repo_root: Path | None = None) -> list[Finding]:
    allowlist = load_allowlist(repo_root)
    findings: list[Finding] = []
    seen: set[str] = set()

    for path in paths:
        normalized = normalize_path(path)
        if normalized in seen:
            continue
        seen.add(normalized)

        reason = classify_path(normalized, allowlist)
        if reason:
            findings.append(Finding(path=normalized, reason=reason))

    return findings


def parse_name_status_z(payload: bytes) -> list[tuple[str, Path]]:
    tokens = [token.decode("utf-8", errors="replace") for token in payload.split(b"\0") if token]
    entries: list[tuple[str, Path]] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        if status.startswith(("R", "C")):
            index += 1
        if index >= len(tokens):
            break
        entries.append((status, Path(tokens[index])))
        index += 1
    return entries


def run_git(args: Sequence[str], *, stdin: bytes | None = None) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        input=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr.decode("utf-8", errors="replace"))
        raise SystemExit(completed.returncode)
    return completed.stdout


def staged_paths() -> list[Path]:
    output = run_git(["diff", "--cached", "--name-status", "-z", "--diff-filter=ACMR"])
    return [path for _, path in parse_name_status_z(output)]


def pre_push_paths(stdin: bytes) -> list[Path]:
    paths: list[Path] = []
    zero_sha = "0" * 40
    for raw_line in stdin.decode("utf-8", errors="replace").splitlines():
        fields = raw_line.split()
        if len(fields) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = fields
        if local_sha == zero_sha:
            continue
        if remote_sha == zero_sha:
            output = run_git(["diff-tree", "--root", "-r", "--name-status", "-z", "--diff-filter=ACMR", local_sha])
        else:
            output = run_git(["diff", "--name-status", "-z", "--diff-filter=ACMR", f"{remote_sha}..{local_sha}"])
        paths.extend(path for _, path in parse_name_status_z(output))
    return paths


def all_tracked_paths() -> list[Path]:
    output = run_git(["ls-files", "-z"])
    return [Path(token.decode("utf-8", errors="replace")) for token in output.split(b"\0") if token]


def format_findings(findings: Sequence[Finding]) -> str:
    lines = [
        "privacy_guard blocked files that may contain private desktop data or raw local evidence:",
        "",
    ]
    for finding in findings:
        lines.append(f"- {finding.path}: {finding.reason}")
    lines.extend(
        [
            "",
            "Move raw screenshots/recordings/logs outside the repository, or replace them with reviewed, cropped/redacted documentation.",
            f"If a media asset is intentionally safe, add a narrow pattern to {ALLOWLIST_FILE.as_posix()} in the same reviewed change.",
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Block private screenshots, recordings, and raw local test artifacts from Git.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--staged", action="store_true", help="scan staged paths for pre-commit")
    group.add_argument("--pre-push", action="store_true", help="scan paths introduced by refs received on stdin")
    group.add_argument("--all-tracked", action="store_true", help="scan all tracked paths")
    group.add_argument("--paths", nargs="*", help="scan explicit paths")
    args = parser.parse_args(argv)

    repo_root = Path(run_git(["rev-parse", "--show-toplevel"]).decode("utf-8").strip())
    os.chdir(repo_root)

    if args.staged:
        paths = staged_paths()
    elif args.pre_push:
        paths = pre_push_paths(sys.stdin.buffer.read())
    elif args.all_tracked:
        paths = all_tracked_paths()
    else:
        paths = [Path(path) for path in args.paths]

    findings = scan_paths(paths, repo_root=repo_root)
    if findings:
        sys.stderr.write(format_findings(findings) + "\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
