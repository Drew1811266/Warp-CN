# zh-Hans Post-RC30 Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC30 local-use readiness toward repeatable public-RC evidence by adding a low-load gate helper, then using it to control heavy validation, GUI smoke, public-RC prerequisite packaging, and RC31 freeze.

**Architecture:** Keep the translation overlay unchanged unless a real source-string drift appears. Add a small Python heat/load gate that produces deterministic pass/defer decisions, then use phase records to document heavy validation, GUI evidence, external prerequisite blockers, and release freeze.

**Tech Stack:** Python `unittest`, Git, Cargo/Rust validation, macOS process/load probes, Markdown evidence records.

---

## Current Baseline

RC30 status:

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 8574 covered, 2 candidates, 100.0%
public-RC blockers: 11
heavy gate: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
onboarding PNGs: 54 total, 50 deferred visual-residue assets
```

Post-RC30 priority:

```text
1. Make heat/load gating repeatable with a small script and tests.
2. Use the script before any Rust, bundle, or GUI command.
3. Keep public-RC blockers explicit instead of repeatedly rechecking without an action package.
4. Preserve the current evidence branch unless the user explicitly asks to stage, commit, push, merge, rebase, or tag.
```

## File Structure

- Create `script/zh_low_load_gate.py` for two-probe low-load decisions.
- Create `script/test_zh_low_load_gate.py` for parser and decision tests.
- Create `docs/zh-Hans-heat-safe-validation.md` to document the gate and thresholds.
- Create `docs/zh-Hans-localization-phase220.md` through `docs/zh-Hans-localization-phase227.md`.
- Create `docs/zh-Hans-public-rc-action-package-rc31.md` to turn the 11 blockers into user/actionable prerequisite requests.
- Create `docs/zh-Hans-publication-readiness-rc31.md` to separate evidence completion from GitHub publication.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc31.md` only during Phase 227.
- Modify `README.md` only during Phase 222 for the new low-load gate and during Phase 227 for RC31 status.
- Modify `docs/zh-Hans-localization.md` during Phase 220 and Phase 227.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` when heavy/GUI/public-RC/PNG status changes.
- Do not modify `resources/localization/zh-Hans-overrides.toml` unless a phase finds real manifest/source drift.
- Do not modify `app/assets/async/png/onboarding/**/*.png` unless the user explicitly approves an asset-only branch.
- Do not stage, commit, push, merge, rebase, or mutate tags unless the user explicitly asks for publication or integration.

### Task 1: Phase 220 Evidence Branch Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase220.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect current evidence branch scope**

Run:

```bash
git status --short --branch
git status --short -- '*.rs' '*.toml' '*.py' '*.png' 'resources/localization/**' 'app/assets/async/png/onboarding/**/*.png'
git diff --check
python3 script/privacy_guard.py --all-tracked
```

Expected:

```text
branch is codex/zh-Hans-post-rc26-execution
source/TOML/Python/PNG status is empty before Task 2
git diff --check exits 0
privacy_guard.py exits 0
```

- [ ] **Step 2: Write Phase 220 record**

Create `docs/zh-Hans-localization-phase220.md`:

```markdown
# zh-Hans Localization Phase 220

Date: 2026-06-02

## Scope

Phase 220 audits the post-RC30 evidence branch before adding a repeatable low-load gate.

This phase does not stage, commit, push, merge, rebase, create a worktree,
mutate tags, build a bundle, launch GUI, use accounts, create backend fixtures,
touch billing/cloud state, or modify PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
source/TOML/Python/PNG dirtiness before gate work: none
git diff --check: passed
privacy guard: passed
```

## Decision

```text
decision: proceed-to-low-load-gate-helper
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 220
status: qualified-post-rc30-baseline
safe to continue to Phase 221: yes
```
```

- [ ] **Step 3: Update localization index**

In `docs/zh-Hans-localization.md`, add one status bullet after the RC30 bullet:

```markdown
- Phase 220 records the post-RC30 branch baseline before adding a repeatable low-load gate helper.
```

- [ ] **Step 4: Verify Task 1**

Run:

```bash
git diff --check
python3 script/privacy_guard.py --all-tracked
```

Expected:

```text
both commands exit 0
```

### Task 2: Phase 221 Low-Load Gate Helper

**Files:**
- Create: `script/zh_low_load_gate.py`
- Create: `script/test_zh_low_load_gate.py`
- Create: `docs/zh-Hans-localization-phase221.md`

- [ ] **Step 1: Create failing tests**

Create `script/test_zh_low_load_gate.py`:

```python
#!/usr/bin/env python3

from __future__ import annotations

import unittest

from zh_low_load_gate import LoadProbe, classify_probe, parse_load_averages, should_run_heavy_gate


class LowLoadGateTests(unittest.TestCase):
    def test_parse_load_averages_from_uptime(self) -> None:
        line = "18:15  up 6 days, 20:44, 1 user, load averages: 2.31 3.23 3.09"

        self.assertEqual(parse_load_averages(line), (2.31, 3.23, 3.09))

    def test_parse_linux_style_load_average(self) -> None:
        line = "18:15:49 up 6 days, 20:44, 1 user, load average: 0.41, 0.53, 0.61"

        self.assertEqual(parse_load_averages(line), (0.41, 0.53, 0.61))

    def test_safe_probe_when_load_and_cpu_are_low(self) -> None:
        probe = LoadProbe(
            load_averages=(0.70, 0.80, 0.90),
            thermal_warning=False,
            performance_warning=False,
            hot_processes=(),
        )

        verdict = classify_probe(probe, max_load=2.50, max_hot_process_percent=25.0)

        self.assertTrue(verdict.safe)
        self.assertEqual(verdict.reasons, ())

    def test_rejects_high_load(self) -> None:
        probe = LoadProbe(
            load_averages=(2.31, 3.23, 3.09),
            thermal_warning=False,
            performance_warning=False,
            hot_processes=(),
        )

        verdict = classify_probe(probe, max_load=2.50, max_hot_process_percent=25.0)

        self.assertFalse(verdict.safe)
        self.assertIn("load average exceeds 2.50", verdict.reasons)

    def test_rejects_hot_process(self) -> None:
        probe = LoadProbe(
            load_averages=(0.70, 0.80, 0.90),
            thermal_warning=False,
            performance_warning=False,
            hot_processes=(("WindowServer", 42.3),),
        )

        verdict = classify_probe(probe, max_load=2.50, max_hot_process_percent=25.0)

        self.assertFalse(verdict.safe)
        self.assertIn("hot process WindowServer at 42.3%", verdict.reasons)

    def test_two_probe_decision_requires_both_safe(self) -> None:
        safe = LoadProbe((0.70, 0.80, 0.90), False, False, ())
        unsafe = LoadProbe((3.44, 3.63, 3.21), False, False, ())

        self.assertTrue(should_run_heavy_gate((safe, safe), max_load=2.50, max_hot_process_percent=25.0).safe)
        self.assertFalse(should_run_heavy_gate((safe, unsafe), max_load=2.50, max_hot_process_percent=25.0).safe)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and confirm they fail**

Run:

```bash
python3 -m unittest script/test_zh_low_load_gate.py
```

Expected:

```text
fails with ModuleNotFoundError or missing zh_low_load_gate symbols
```

- [ ] **Step 3: Create low-load gate helper**

Create `script/zh_low_load_gate.py`:

```python
#!/usr/bin/env python3

from __future__ import annotations

import argparse
import dataclasses
import re
import subprocess
import sys
import time
from collections.abc import Sequence


LOAD_RE = re.compile(r"load averages?:\s*([0-9.]+),?\s+([0-9.]+),?\s+([0-9.]+)")


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
    thermal_warning = "ThermalWarning" in therm_output and "0" not in therm_output
    performance_warning = "PerformanceWarning" in therm_output and "0" not in therm_output

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
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
python3 -m unittest script/test_zh_low_load_gate.py
```

Expected:

```text
Ran 6 tests
OK
```

- [ ] **Step 5: Run a no-wait smoke probe**

Run:

```bash
python3 script/zh_low_load_gate.py --probes 1 --wait-seconds 0
```

Expected:

```text
prints one probe and either decision: run-heavy-gate or decision: defer-heavy-gate
exit code is 0 when safe or 2 when deferred
```

- [ ] **Step 6: Write Phase 221 record**

Create `docs/zh-Hans-localization-phase221.md`:

```markdown
# zh-Hans Localization Phase 221

Date: 2026-06-02

## Scope

Phase 221 adds a repeatable low-load gate helper for future Rust, bundle, and GUI phases.

## Decision

```text
decision: low-load-gate-helper-added
script: script/zh_low_load_gate.py
tests: script/test_zh_low_load_gate.py
```

## Qualification Review

```text
phase: 221
status: qualified-low-load-gate-helper
tests passed: yes
safe to continue to Phase 222: yes
```
```

- [ ] **Step 7: Verify Task 2**

Run:

```bash
python3 -m unittest script/test_zh_low_load_gate.py
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
unit tests pass
privacy guard exits 0
git diff --check exits 0
```

### Task 3: Phase 222 Heat-Safe Validation Documentation

**Files:**
- Create: `docs/zh-Hans-heat-safe-validation.md`
- Create: `docs/zh-Hans-localization-phase222.md`
- Modify: `README.md`

- [ ] **Step 1: Create heat-safe validation document**

Create `docs/zh-Hans-heat-safe-validation.md`:

```markdown
# zh-Hans Heat-Safe Validation

Date: 2026-06-02

## Purpose

Use `script/zh_low_load_gate.py` before heavy Warp CN validation commands.

## Default Gate

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Run heavy commands only when the script prints:

```text
decision: run-heavy-gate
```

When it prints `decision: defer-heavy-gate`, record the reasons in the current
phase document and skip Rust compile, bundle build, and GUI launch for that
phase.

## Heavy Commands

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

## Safety Rules

- Run heavy commands serially.
- Do not retry repeatedly in the same phase after a defer decision.
- Do not use GUI launch as public-RC evidence unless the current phase produced a fresh bundle.
- Never touch accounts, billing, cloud objects, secrets, endpoints, or team ownership during heat-gate checks.
```

- [ ] **Step 2: Update README validation section**

In `README.md`, add this after the low-load daily validation block:

```markdown
重型 gate 前先运行散热保护检查：

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

只有输出 `decision: run-heavy-gate` 时才继续跑 Rust compile、bundle 和 GUI。
```

- [ ] **Step 3: Write Phase 222 record**

Create `docs/zh-Hans-localization-phase222.md`:

```markdown
# zh-Hans Localization Phase 222

Date: 2026-06-02

## Decision

```text
decision: heat-safe-validation-doc-added
doc: docs/zh-Hans-heat-safe-validation.md
README updated: yes
```

## Qualification Review

```text
phase: 222
status: qualified-heat-safe-docs
safe to continue to Phase 223: yes
```
```

- [ ] **Step 4: Verify Task 3**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Phase 223 Heavy Gate Retry With Helper

**Files:**
- Create: `docs/zh-Hans-localization-phase223.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Run the low-load gate helper**

Run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Expected:

```text
decision is either run-heavy-gate or defer-heavy-gate
the output lists probe loads and defer reasons when unsafe
```

- [ ] **Step 2: If helper defers, write Phase 223 defer**

Create `docs/zh-Hans-localization-phase223.md`:

```markdown
# zh-Hans Localization Phase 223

Date: 2026-06-02

## Decision

```text
decision: skip-heavy-validation-for-heat-safety
gate helper: defer-heavy-gate
Rust compile: not run
fresh bundle: not run
GUI launch: not run
```

## Qualification Review

```text
phase: 223
status: qualified-heavy-gate-deferred
safe to continue to Phase 224: yes
```
```

- [ ] **Step 3: If helper passes, run Rust compile and bundle serially**

Run:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
cargo check exits 0
script/run exits 0
target/debug/bundle/osx/WarpOss.app exists
```

- [ ] **Step 4: If heavy commands pass, write Phase 223 pass record**

Create `docs/zh-Hans-localization-phase223.md`:

```markdown
# zh-Hans Localization Phase 223

Date: 2026-06-02

## Decision

```text
decision: heavy-validation-passed
gate helper: run-heavy-gate
Rust compile: passed
fresh bundle: passed
```

## Qualification Review

```text
phase: 223
status: qualified-heavy-gate-passed
safe to continue to Phase 224: yes
```
```

- [ ] **Step 5: Update GUI matrix**

Append to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## 2026-06-02 P223 heavy validation with helper

Phase 223 status: `qualified-heavy-gate-passed` or `qualified-heavy-gate-deferred`.

- The low-load helper decided whether Rust compile and bundle were safe.
- Rust compile and bundle status are recorded in `docs/zh-Hans-localization-phase223.md`.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was touched.
```

- [ ] **Step 6: Verify Task 4**

Run:

```bash
git diff --check
python3 script/privacy_guard.py --all-tracked
```

Expected:

```text
both commands exit 0
```

### Task 5: Phase 224 Current-Cycle GUI Smoke

**Files:**
- Create: `docs/zh-Hans-localization-phase224.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Check fresh bundle dependency**

Run:

```bash
rg -n "fresh bundle: passed|fresh bundle: not run|fresh bundle: skipped" docs/zh-Hans-localization-phase223.md
```

Expected:

```text
continue GUI only if Phase 223 says fresh bundle passed
otherwise write a no-fresh-bundle defer
```

- [ ] **Step 2: If no fresh bundle exists, write Phase 224 defer**

Create `docs/zh-Hans-localization-phase224.md`:

```markdown
# zh-Hans Localization Phase 224

Date: 2026-06-02

## Decision

```text
decision: skip-current-cycle-gui-smoke-no-fresh-bundle
GUI launch: not run
rows promoted: none
```

## Qualification Review

```text
phase: 224
status: qualified-gui-smoke-deferred
safe to continue to Phase 225: yes
```
```

- [ ] **Step 3: If fresh bundle exists, launch and inspect GUI**

Run:

```bash
open -n target/debug/bundle/osx/WarpOss.app
sleep 8
pgrep -afil 'warp-oss|terminal-server' || true
```

Expected:

```text
warp-oss and terminal-server processes are visible
```

- [ ] **Step 4: Capture safe anchors through Computer Use**

Record only redacted accessibility anchors in `docs/zh-Hans-localization-phase224.md`.

Expected anchors:

```text
Chinese menu labels such as 文件, 编辑, 视图, 标签页, 窗口, 帮助
one no-account shell or onboarding anchor if visible
no account identifiers, tokens, callback URLs, local usernames, or private team names
```

- [ ] **Step 5: Shut down GUI**

Run:

```bash
pkill -f 'target/debug/bundle/osx/WarpOss.app|warp-oss|terminal-server' || true
pgrep -afil 'warp-oss|terminal-server' || true
```

Expected:

```text
final pgrep shows no remaining warp-oss or terminal-server process
```

- [ ] **Step 6: Verify Task 5**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 6: Phase 225 Public-RC Action Package

**Files:**
- Create: `docs/zh-Hans-public-rc-action-package-rc31.md`
- Create: `docs/zh-Hans-localization-phase225.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Refresh blocker status**

Run:

```bash
python3 script/zh_public_rc_status.py
```

Expected:

```text
total remains 11 unless matching evidence and registry updates were added earlier
```

- [ ] **Step 2: Create public-RC action package**

Create `docs/zh-Hans-public-rc-action-package-rc31.md`:

```markdown
# zh-Hans Public-RC Action Package RC31

Date: 2026-06-02

## Required Inputs

| Category | Rows | Required input |
| --- | --- | --- |
| isolated account | GUI-AUTH-01, GUI-SET-03, GUI-WS-06 | An isolated test account that is not the user's main account, plus cleanup proof. |
| backend fixture | GUI-SET-04, GUI-SET-05, GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01 | Safe AWS/Bedrock, invalid credential, billing/quota, Build plan, and cloud capacity fixtures. |
| disposable object | GUI-SET-06, GUI-WS-04, GUI-WS-07 | Exact disposable objects named `zh-smoke-delete-environment`, `zh-smoke-delete-secret`, and `zh-smoke-public-rc-team`. |
| visual assets | onboarding PNG residue | Design/product approval for an asset-only branch and before/after contact sheets. |
| heavy validation | Rust/bundle/GUI | A quiet-window `decision: run-heavy-gate` from `script/zh_low_load_gate.py`. |

## Safety Rules

- Do not use the user's main account.
- Do not enter real provider credentials.
- Do not attach payment methods, buy credits, or consume real quota.
- Do not delete or transfer any object whose name is not explicitly allowlisted here.
- Do not submit raw screenshots, screen recordings, tokens, callback URLs, account identifiers, or private team names.
```

- [ ] **Step 3: Write Phase 225 record**

Create `docs/zh-Hans-localization-phase225.md`:

```markdown
# zh-Hans Localization Phase 225

Date: 2026-06-02

## Decision

```text
decision: public-rc-action-package-created
action package: docs/zh-Hans-public-rc-action-package-rc31.md
registry mutation: none
```

## Qualification Review

```text
phase: 225
status: qualified-public-rc-action-package
safe to continue to Phase 226: yes
```
```

- [ ] **Step 4: Update GUI matrix and verify**

Append a Phase 225 summary to `docs/zh-Hans-gui-smoke-matrix.md`, then run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 7: Phase 226 Publication Readiness Separation

**Files:**
- Create: `docs/zh-Hans-publication-readiness-rc31.md`
- Create: `docs/zh-Hans-localization-phase226.md`

- [ ] **Step 1: Inspect local and remote refs without mutating them**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git ls-remote --heads origin main master
git ls-remote --tags origin 'refs/tags/0.*'
```

Expected:

```text
commands read refs only
no stage, commit, push, merge, rebase, or tag mutation occurs
```

- [ ] **Step 2: Create publication readiness document**

Create `docs/zh-Hans-publication-readiness-rc31.md`:

```markdown
# zh-Hans Publication Readiness RC31

Date: 2026-06-02

## Boundary

This document separates evidence completion from publication.

## Current Decision

```text
stage: not run
commit: not run
push: not run
merge: not run
tag mutation: not run
```

## Publication Requirements

- Low-load validation passes.
- Heavy Rust/bundle/GUI gate is either passed or explicitly accepted as deferred by the user.
- Public-RC blockers remain clearly labeled if not cleared.
- Privacy guard passes.
- Remote branch and tag plan is explicitly approved by the user.
```

- [ ] **Step 3: Write Phase 226 record**

Create `docs/zh-Hans-localization-phase226.md`:

```markdown
# zh-Hans Localization Phase 226

Date: 2026-06-02

## Decision

```text
decision: publication-readiness-separated
publication doc: docs/zh-Hans-publication-readiness-rc31.md
stage/commit/push/merge/tag mutation: not run
```

## Qualification Review

```text
phase: 226
status: qualified-publication-readiness-record
safe to continue to Phase 227: yes
```
```

- [ ] **Step 4: Verify Task 7**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 8: Phase 227 RC31 Freeze

**Files:**
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc31.md`
- Create: `docs/zh-Hans-localization-phase227.md`
- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Run final low-load validation**

Run:

```bash
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/privacy_guard.py --all-tracked
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py
cargo fmt --check
git diff --check
```

Expected:

```text
manifest validation passed
glossary check passed
dry-run would_change is 0
dry-run missing is 0
public-RC blocker total is recorded
Python localization tests pass
low-load gate tests pass
cargo fmt --check exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create RC31 release record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc31.md`:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC31

Date: 2026-06-02

## Scope

RC31 covers Phases 220 through 227.

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
```

## Validation

```text
low-load gate helper: present
Python low-load gate tests: passed
heavy gate status: recorded in Phase 223
GUI status: recorded in Phase 224
public-RC blockers: recorded in Phase 225
publication readiness: recorded in Phase 226
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready unless all blockers, fresh bundle, GUI, and PNG/asset evidence are cleared
```
```

- [ ] **Step 3: Update README and localization index**

Update `README.md`:

```text
最后核验记录：`2026-06-02 RC31`
```

Update `docs/zh-Hans-localization.md`:

```markdown
Last verified release audit: 2026-06-02 RC31, generated on 2026-06-02 Asia/Shanghai.

- RC31 decision: `ready-for-local-use-with-fixture-evidence`; public RC remains blocked unless Phase 223 through Phase 226 cleared every required evidence gate.
```

- [ ] **Step 4: Create Phase 227 freeze record**

Create `docs/zh-Hans-localization-phase227.md`:

```markdown
# zh-Hans Localization Phase 227

Date: 2026-06-02

## Decision

```text
decision: rc31-freeze
public RC: not ready unless all evidence gates passed
```

## Qualification Review

```text
phase: 227
status: qualified-rc31-freeze
all roadmap phases complete: yes
```
```

- [ ] **Step 5: Final verification**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_low_load_gate.py
git diff --check
git status --short --branch
```

Expected:

```text
validation passes
dry-run would_change is 0
dry-run missing is 0
public-RC blocker total is explicit
low-load gate tests pass
privacy guard exits 0
diff check exits 0
status shows only planned code/docs/evidence changes unless explicitly approved source or asset work happened
```

## Self-Review

Spec coverage:

```text
post-RC30 branch baseline: Task 1
repeatable low-load gate helper: Task 2
heat-safe validation docs: Task 3
heavy validation retry: Task 4
GUI evidence recovery: Task 5
public-RC action package: Task 6
publication boundary: Task 7
RC31 freeze: Task 8
```

Placeholder scan:

```text
No task uses placeholder markers or undefined external code.
All commands, files, and expected outcomes are explicit.
```

Risk boundary:

```text
No stage/commit/push/merge/rebase/tag mutation is planned without explicit user approval.
No real account, billing, cloud, secret, endpoint, or team state is touched unless the matching prerequisite is explicitly provided and documented.
```
