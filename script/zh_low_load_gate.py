#!/usr/bin/env python3

from __future__ import annotations

import argparse
import dataclasses
import re
import subprocess
import time
from collections.abc import Sequence


LOAD_RE = re.compile(r"load averages?:\s*([0-9.]+),?\s+([0-9.]+),?\s+([0-9.]+)")
WARNING_RE = re.compile(r"(thermal|performance).*warning.*(?:level|=)?\s*([1-9]\d*)", re.IGNORECASE)


@dataclasses.dataclass(frozen=True)
class LoadProbe:
    load_averages: tuple[float, float, float]
    thermal_warning: bool
    performance_warning: bool
    hot_processes: tuple[tuple[str, float], ...]


@dataclasses.dataclass(frozen=True)
class GateVerdict:
    safe: bool
    reasons: tuple[str, ...]


def parse_load_averages(line: str) -> tuple[float, float, float]:
    match = LOAD_RE.search(line)
    if not match:
        raise ValueError(f"could not parse load averages from: {line}")
    return (float(match.group(1)), float(match.group(2)), float(match.group(3)))


def has_warning(output: str, warning_name: str) -> bool:
    lowered_name = warning_name.lower()
    for line in output.splitlines():
        lowered_line = line.lower()
        if lowered_name not in lowered_line or "warning" not in lowered_line:
            continue
        if "no " in lowered_line and "recorded" in lowered_line:
            continue
        match = WARNING_RE.search(line)
        if match and int(match.group(2)) > 0:
            return True
    return False


def classify_probe(probe: LoadProbe, *, max_load: float, max_hot_process_percent: float) -> GateVerdict:
    reasons: list[str] = []
    if any(load > max_load for load in probe.load_averages):
        reasons.append(f"load average exceeds {max_load:.2f}")
    if probe.thermal_warning:
        reasons.append("thermal warning recorded")
    if probe.performance_warning:
        reasons.append("performance warning recorded")
    for name, percent in probe.hot_processes:
        if percent > max_hot_process_percent:
            reasons.append(f"hot process {name} at {percent:.1f}%")
    return GateVerdict(safe=not reasons, reasons=tuple(reasons))


def should_run_heavy_gate(
    probes: Sequence[LoadProbe], *, max_load: float, max_hot_process_percent: float
) -> GateVerdict:
    reasons: list[str] = []
    for index, probe in enumerate(probes, start=1):
        verdict = classify_probe(
            probe,
            max_load=max_load,
            max_hot_process_percent=max_hot_process_percent,
        )
        reasons.extend(f"probe {index}: {reason}" for reason in verdict.reasons)
    return GateVerdict(safe=not reasons, reasons=tuple(reasons))


def run_text(command: Sequence[str]) -> str:
    return subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout


def collect_probe(max_hot_process_percent: float) -> LoadProbe:
    uptime_output = run_text(["uptime"]).strip()
    load_averages = parse_load_averages(uptime_output)

    therm_output = run_text(["pmset", "-g", "therm"])
    thermal_warning = has_warning(therm_output, "thermal")
    performance_warning = has_warning(therm_output, "performance")

    process_output = run_text(["ps", "-axo", "pcpu,comm"])
    hot_processes: list[tuple[str, float]] = []
    watched_names = ("WindowServer", "Finder", "trustd", "syspolicyd", "Codex", "node", "npm", "mds")
    for line in process_output.splitlines()[1:]:
        parts = line.strip().split(None, 1)
        if len(parts) != 2:
            continue
        try:
            percent = float(parts[0])
        except ValueError:
            continue
        name = parts[1].split("/")[-1]
        if percent > max_hot_process_percent and any(item in parts[1] for item in watched_names):
            hot_processes.append((name, percent))

    return LoadProbe(
        load_averages=load_averages,
        thermal_warning=thermal_warning,
        performance_warning=performance_warning,
        hot_processes=tuple(sorted(hot_processes, key=lambda item: item[1], reverse=True)),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check whether it is safe to run Warp CN heavy validation.")
    parser.add_argument("--max-load", type=float, default=2.50)
    parser.add_argument("--max-hot-process-percent", type=float, default=25.0)
    parser.add_argument("--wait-seconds", type=int, default=60)
    parser.add_argument("--probes", type=int, default=2)
    args = parser.parse_args(argv)

    probes: list[LoadProbe] = []
    for index in range(args.probes):
        probe = collect_probe(args.max_hot_process_percent)
        probes.append(probe)
        print(
            f"probe {index + 1}: load={probe.load_averages[0]:.2f} "
            f"{probe.load_averages[1]:.2f} {probe.load_averages[2]:.2f}"
        )
        for name, percent in probe.hot_processes:
            print(f"probe {index + 1}: hot_process={name} {percent:.1f}%")
        if index + 1 < args.probes:
            time.sleep(args.wait_seconds)

    verdict = should_run_heavy_gate(
        probes,
        max_load=args.max_load,
        max_hot_process_percent=args.max_hot_process_percent,
    )
    if verdict.safe:
        print("decision: run-heavy-gate")
        return 0

    print("decision: defer-heavy-gate")
    for reason in verdict.reasons:
        print(f"reason: {reason}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
