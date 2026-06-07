#!/usr/bin/env python3
"""Record low-load zh-Hans calibration timing and high-load deferrals."""

from __future__ import annotations

import argparse
import dataclasses
import json
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "docs/zh-Hans-calibration-cycles/2026-06-05/performance-probe.md"
DEFAULT_AUDIT_OUTPUT_DIR = REPO_ROOT / "docs/zh-Hans-calibration-cycles/2026-06-05"

LOW_LOAD_COMMANDS = (
    ("python3", "script/zh_apply_localization.py", "--dry-run", "--summary"),
    (
        "python3",
        "script/zh_full_translation_audit.py",
        "--fail-on-actionable",
        "--output-dir",
        "docs/zh-Hans-calibration-cycles/2026-06-05",
    ),
    ("python3", "script/zh_localization_inventory.py", "--preset", "release", "--coverage"),
)

DEFERRED_HIGH_LOAD_COMMANDS = (
    "python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25",
    "cargo fmt --check",
    "CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp",
    "TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open",
    "open -n target/debug/bundle/osx/WarpOss.app",
    "GUI automation and runtime log probes",
)


@dataclasses.dataclass(frozen=True)
class ProbeResult:
    command: str
    exit_code: int
    elapsed_seconds: float
    stdout: str
    stderr: str


def run_low_load_commands(commands: tuple[tuple[str, ...], ...] = LOW_LOAD_COMMANDS) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    for command in commands:
        start = time.perf_counter()
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        elapsed = time.perf_counter() - start
        results.append(
            ProbeResult(
                command=" ".join(command),
                exit_code=completed.returncode,
                elapsed_seconds=round(elapsed, 3),
                stdout=completed.stdout.strip(),
                stderr=completed.stderr.strip(),
            )
        )
    return results


def high_load_skip_payload() -> dict[str, object]:
    return {
        "status": "skipped-by-heat-safety-policy",
        "not_run": list(DEFERRED_HIGH_LOAD_COMMANDS),
        "runtime_performance_readiness": "not-evaluated",
    }


def render_markdown(results: list[ProbeResult], *, include_high_load_skip: bool = True) -> str:
    lines = [
        "# zh-Hans Low-Load Performance Probe",
        "",
        "This report records low-load script timing only. It does not evaluate app runtime performance.",
        "",
        "## Low-Load Commands",
        "",
        "| command | exit | seconds | stdout summary | stderr summary |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for result in results:
        stdout = result.stdout.replace("|", "/").replace("\n", " ")[:240] or "none"
        stderr = result.stderr.replace("|", "/").replace("\n", " ")[:240] or "none"
        lines.append(f"| `{result.command}` | {result.exit_code} | {result.elapsed_seconds:.3f} | {stdout} | {stderr} |")

    if include_high_load_skip:
        lines.extend(
            [
                "",
                "## High-Load Runtime Work",
                "",
                "- Status: `skipped-by-heat-safety-policy`",
                "- Runtime performance readiness: `not-evaluated`",
                "",
                "The following commands were not run:",
                "",
            ]
        )
        for command in DEFERRED_HIGH_LOAD_COMMANDS:
            lines.append(f"- `{command}`")
    lines.append("")
    return "\n".join(lines)


def render_json(results: list[ProbeResult], *, include_high_load_skip: bool = True) -> str:
    payload: dict[str, object] = {
        "low_load_results": [dataclasses.asdict(result) for result in results],
    }
    if include_high_load_skip:
        payload["high_load_runtime"] = high_load_skip_payload()
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument(
        "--record-high-load-skipped",
        action="store_true",
        help="Write only the high-load deferral report without running timing commands",
    )
    args = parser.parse_args(argv)

    results: list[ProbeResult] = []
    if not args.record_high_load_skipped:
        results = run_low_load_commands()

    if args.json:
        print(render_json(results), end="")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(results), encoding="utf-8")
    print(f"output: {args.output.resolve()}")
    if any(result.exit_code != 0 for result in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
