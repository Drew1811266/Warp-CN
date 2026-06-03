# zh-Hans Post-RC34 Evidence Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC34 to RC35 by hardening public-RC evidence path checks and adding machine-readable evidence report output without creating real external evidence.

**Architecture:** Keep the blocker registry and evidence ledger as the source of truth. Tighten `script/zh_public_rc_evidence_lint.py` so strict artifact mode requires the expected row-specific redacted path, then extend `script/zh_public_rc_evidence_report.py` with JSON output for report summaries and missing-action rows. Keep heavy Rust, bundle, and GUI validation behind `script/zh_low_load_gate.py`.

**Tech Stack:** Python `unittest`, JSON serialization, existing small TOML parser in `script/zh_public_rc_evidence_lint.py`, Markdown release records, existing zh-Hans validation scripts, Git diff/privacy checks, macOS low-load gate.

---

## Current Baseline

RC34 status:

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
evidence ledger rows: 11
ready evidence rows: 0
strict evidence linter: expected fail, exit_code 1, errors 11
backend fixture blockers: 5
disposable object blockers: 3
isolated account blockers: 3
missing-action report: available
heavy gate: defer-heavy-gate
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
PNG changes: none
```

Next-cycle priority:

```text
1. Keep the public-RC decision blocked until real matching evidence exists.
2. Make strict artifact lint reject redacted artifacts attached to the wrong row.
3. Add JSON output for evidence reports so future handoffs can be consumed by tools.
4. Add JSON output for missing evidence actions so row owners can receive exact structured requirements.
5. Create RC35 docs that explain the new automation outputs and keep real evidence out of Git.
6. Retry heavy validation only if script/zh_low_load_gate.py returns decision: run-heavy-gate.
7. Keep stage, commit, push, merge, rebase, and tags outside this plan unless explicitly approved.
```

## File Structure

- Modify `script/zh_public_rc_evidence_lint.py` to add an expected row-path helper and strict artifact row-path check.
- Modify `script/test_zh_public_rc_evidence_lint.py` to add a wrong-row artifact regression test.
- Modify `script/zh_public_rc_evidence_report.py` to add JSON summary output and JSON missing-action output.
- Modify `script/test_zh_public_rc_evidence_report.py` to add JSON output tests.
- Create `docs/zh-Hans-public-rc-evidence-automation-rc35.md` for evidence automation output usage.
- Create `docs/zh-Hans-public-rc-lane-readiness-rc35.md` for updated lane readiness.
- Create `docs/zh-Hans-localization-phase252.md` through `docs/zh-Hans-localization-phase259.md`.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc35.md` only during Phase 259.
- Modify `README.md` only during Phase 259 to point to RC35 and the JSON evidence helper.
- Modify `docs/zh-Hans-localization.md` during Phase 252 and Phase 259.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` only when asset, heavy, or GUI status changes.
- Do not modify `resources/localization/zh-Hans-overrides.toml` unless validation finds real manifest/source drift.
- Do not change `resources/localization/zh-Hans-public-rc-evidence.toml` unless reviewed redacted evidence is provided and explicit approval is given.
- Do not create files under `artifacts/redacted/` except temporary files inside tests.
- Do not modify `app/assets/async/png/onboarding/**/*.png` without explicit asset approval.
- Do not stage, commit, push, merge, rebase, or mutate tags without explicit user approval.

## Phase Map

| Phase | Purpose | Qualification Gate |
| --- | --- | --- |
| 252 | Post-RC34 baseline and scope lock | current 11 blockers confirmed; privacy/diff checks pass |
| 253 | Strict artifact row-path guard | linter rejects wrong-row artifacts and accepts exact row path |
| 254 | Evidence report JSON output | tests pass; JSON report has stable counts and rows |
| 255 | Missing-action JSON output | tests pass; JSON actions expose safe structured row requirements |
| 256 | RC35 evidence automation docs | docs describe text and JSON outputs without creating evidence |
| 257 | RC35 lane readiness refresh | lane boundaries and external inputs remain explicit |
| 258 | Low-load heavy validation retry | run heavy commands only after `decision: run-heavy-gate`; otherwise record defer |
| 259 | RC35 freeze and publication boundary | validation passes; RC35 decision is explicit and honest |

### Task 1: Phase 252 Post-RC34 Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase252.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect current branch and public-RC status**

Run:

```bash
git status --short --branch
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --missing-actions
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts; code=$?; printf 'strict_evidence_lint_exit_code=%s\n' "$code"; test "$code" -eq 1
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
branch remains codex/zh-Hans-post-rc26-execution
dry-run reports would_change: 0 and missing: 0
public-RC blocker total remains 11
evidence report says ready_rows: 0 and decision: blocked
missing-action report exits 0
strict evidence linter exits 1 because 11 rows still lack evidence
privacy_guard.py exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create Phase 252 record**

Create `docs/zh-Hans-localization-phase252.md`:

```markdown
# zh-Hans Localization Phase 252

Date: 2026-06-02

## Scope

Phase 252 audits the post-RC34 baseline before adding stricter artifact row-path
checks and JSON evidence report output.

This phase does not stage, commit, push, merge, rebase, mutate tags, use
accounts, create backend fixtures, touch billing/cloud state, create real
evidence artifacts, run Rust compile, build a bundle, launch GUI, or modify
PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
dry-run: would_change 0, missing 0
public-RC blockers: 11
evidence ready rows: 0
missing-action report: passed
strict evidence lint: expected fail, exit_code 1
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-strict-row-path-guard
public RC: still blocked by evidence
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 252
status: qualified-post-rc34-baseline
safe to continue to Phase 253: yes
```
```

- [ ] **Step 3: Update localization index**

Add this line to `docs/zh-Hans-localization.md` near the RC34 entry:

```markdown
- Phase 252 records the post-RC34 baseline before adding stricter row-path evidence checks and JSON report output.
```

- [ ] **Step 4: Verify Task 1**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 2: Phase 253 Strict Artifact Row-Path Guard

**Files:**
- Modify: `script/zh_public_rc_evidence_lint.py`
- Modify: `script/test_zh_public_rc_evidence_lint.py`
- Create: `docs/zh-Hans-localization-phase253.md`

- [ ] **Step 1: Add a failing wrong-row artifact test**

Add this test method inside `PublicRcEvidenceLintTests` in `script/test_zh_public_rc_evidence_lint.py`:

```python
    def test_strict_artifacts_rejects_wrong_row_artifact_path(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            artifact = Path(root) / "artifacts/redacted/gui-auth-01.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("safe redacted text for another row\n", encoding="utf-8")
            blockers = {
                "blocker": [
                    {
                        "id": "GUI-SET-05",
                        "category": "backend_fixture",
                        "required_evidence": ["invalid credential fixture"],
                        "public_rc_required": True,
                    }
                ]
            }
            evidence = {
                "evidence": [
                    {
                        "row_id": "GUI-SET-05",
                        "status": "provided",
                        "evidence_paths": ["artifacts/redacted/gui-auth-01.txt"],
                        "cleanup_proof": "fixture reset proof captured",
                        "redaction": "identifiers removed",
                        "notes": "safe marker only",
                    }
                ]
            }

            result = lint_evidence(blockers, evidence, strict_artifacts=True, repo_root=Path(root))

        self.assertFalse(result.ok)
        self.assertIn(
            "GUI-SET-05: evidence_paths must include artifacts/redacted/gui-set-05.txt",
            result.errors,
        )
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
```

Expected:

```text
FAIL because strict artifact mode does not yet require the row-specific path
```

- [ ] **Step 3: Implement row-specific path check**

In `script/zh_public_rc_evidence_lint.py`, add this helper after `has_sensitive_metadata`:

```python
def expected_redacted_path(row_id: str) -> str:
    return f"artifacts/redacted/{row_id.lower()}.txt"
```

Update `strict_artifact_errors` so the first lines become:

```python
def strict_artifact_errors(row_id: str, evidence_paths: object, repo_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(evidence_paths, list):
        return errors
    expected_path = expected_redacted_path(row_id)
    if expected_path not in evidence_paths:
        errors.append(f"{row_id}: evidence_paths must include {expected_path}")
    for artifact_path in evidence_paths:
        if not isinstance(artifact_path, str):
            continue
```

Keep the existing suffix, existence, and sensitive-text checks unchanged.

- [ ] **Step 4: Verify linter tests and current ledger**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts; code=$?; printf 'strict_evidence_lint_exit_code=%s\n' "$code"; test "$code" -eq 1
```

Expected:

```text
all evidence lint tests pass
current ledger still exits 1 because all 11 rows are missing evidence
```

- [ ] **Step 5: Create Phase 253 record**

Create `docs/zh-Hans-localization-phase253.md`:

```markdown
# zh-Hans Localization Phase 253

Date: 2026-06-02

## Scope

Phase 253 hardens strict artifact linting so a provided row must include its
row-specific redacted artifact path.

This phase does not create repository evidence artifacts, change evidence
ledger status, stage, commit, push, merge, rebase, mutate tags, use accounts,
create backend fixtures, touch billing/cloud state, run Rust compile, build a
bundle, launch GUI, or modify PNG assets.

## Validation

```text
wrong-row artifact path regression: passed
strict artifact linter tests: passed
current ledger strict lint: expected fail, exit_code 1
rows promoted: 0
```

## Qualification Review

```text
phase: 253
status: qualified-strict-row-path-guard
safe to continue to Phase 254: yes
```
```

- [ ] **Step 6: Verify Task 2**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 3: Phase 254 Evidence Report JSON Output

**Files:**
- Modify: `script/zh_public_rc_evidence_report.py`
- Modify: `script/test_zh_public_rc_evidence_report.py`
- Create: `docs/zh-Hans-localization-phase254.md`

- [ ] **Step 1: Add failing JSON report tests**

Add `import json` near the top of `script/test_zh_public_rc_evidence_report.py`.

Extend the report import line:

```python
from zh_public_rc_evidence_report import (
    build_report,
    render_json,
    render_missing_actions,
    render_templates,
    render_text,
)
```

Add this test method inside `PublicRcEvidenceReportTests`:

```python
    def test_json_report_contains_stable_counts_and_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        data = json.loads(render_json(build_report(blockers, evidence)))

        self.assertEqual(data["total_required"], 11)
        self.assertEqual(data["ready_rows"], [])
        self.assertEqual(data["decision"], "blocked")
        self.assertEqual(data["category_counts"]["backend_fixture"], 5)
        self.assertEqual(data["category_ready_counts"].get("backend_fixture", 0), 0)
        self.assertEqual(data["rows"][0]["row_id"], "GUI-AUTH-01")
        self.assertEqual(data["rows"][0]["status"], "missing")
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
```

Expected:

```text
FAIL or ERROR because render_json is not implemented
```

- [ ] **Step 3: Implement JSON report rendering**

In `script/zh_public_rc_evidence_report.py`, add `import json` near the top.

Add these functions after `render_text`:

```python
def report_to_json_data(report: EvidenceReport) -> dict[str, Any]:
    return {
        "total_required": report.total_required,
        "ready_rows": list(report.ready_rows),
        "status_counts": report.status_counts,
        "category_counts": report.category_counts,
        "category_ready_counts": report.category_ready_counts,
        "rows": [dataclasses.asdict(row) for row in report.rows],
        "decision": "ready" if len(report.ready_rows) == report.total_required else "blocked",
    }


def render_json(report: EvidenceReport) -> str:
    return json.dumps(report_to_json_data(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
```

Update the CLI parser:

```python
    parser.add_argument("--json", action="store_true", help="Print evidence report JSON")
```

Update the normal report branch:

```python
    report = build_report(blockers, evidence)
    if args.json:
        print(render_json(report), end="")
        return 0

    print(render_text(report))
    return 0
```

- [ ] **Step 4: Verify JSON report**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --json
```

Expected:

```text
report tests pass
JSON output contains total_required 11, ready_rows [], decision blocked
```

- [ ] **Step 5: Create Phase 254 record**

Create `docs/zh-Hans-localization-phase254.md`:

```markdown
# zh-Hans Localization Phase 254

Date: 2026-06-02

## Scope

Phase 254 adds machine-readable JSON output for the public-RC evidence report.

This phase does not change blocker status, add real evidence, stage, commit,
push, merge, rebase, mutate tags, use accounts, create backend fixtures, touch
billing/cloud state, run Rust compile, build a bundle, launch GUI, or modify
PNG assets.

## Validation

```text
python3 -m unittest script/test_zh_public_rc_evidence_report.py: passed
python3 script/zh_public_rc_evidence_report.py --json: passed
ready rows: 0
decision: blocked
```

## Qualification Review

```text
phase: 254
status: qualified-json-evidence-report
safe to continue to Phase 255: yes
```
```

- [ ] **Step 6: Verify Task 3**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Phase 255 Missing-Action JSON Output

**Files:**
- Modify: `script/zh_public_rc_evidence_report.py`
- Modify: `script/test_zh_public_rc_evidence_report.py`
- Create: `docs/zh-Hans-localization-phase255.md`

- [ ] **Step 1: Add failing missing-action JSON tests**

Extend the report import line in `script/test_zh_public_rc_evidence_report.py`:

```python
from zh_public_rc_evidence_report import (
    build_report,
    missing_actions,
    render_json,
    render_missing_actions,
    render_missing_actions_json,
    render_templates,
    render_text,
)
```

Add these test methods inside `PublicRcEvidenceReportTests`:

```python
    def test_missing_actions_data_is_structured_and_safe(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = missing_actions(blockers, evidence)

        self.assertEqual(len(actions), 11)
        self.assertEqual(actions[0]["row_id"], "GUI-AUTH-01")
        self.assertEqual(actions[0]["artifact_path"], "artifacts/redacted/gui-auth-01.txt")
        self.assertIn("required_evidence", actions[0])
        self.assertIn("safety_rule", actions[0])

    def test_missing_actions_json_contains_actions_and_decision(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        data = json.loads(render_missing_actions_json(blockers, evidence))

        self.assertEqual(data["total_actions"], 11)
        self.assertEqual(data["decision"], "blocked-until-matching-evidence-is-reviewed")
        self.assertEqual(data["actions"][0]["row_id"], "GUI-AUTH-01")
        self.assertEqual(data["actions"][0]["category"], "isolated_account")
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
```

Expected:

```text
FAIL or ERROR because missing_actions and render_missing_actions_json are not implemented
```

- [ ] **Step 3: Implement structured missing actions**

In `script/zh_public_rc_evidence_report.py`, add these functions before `render_missing_actions`:

```python
def missing_actions(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    evidence = evidence_by_id(evidence_doc)
    actions: list[dict[str, Any]] = []
    for row_id, blocker in sorted(blocker_index(blockers).items()):
        evidence_row = evidence.get(row_id, {})
        if str(evidence_row.get("status", "missing")) == "provided":
            continue
        actions.append(
            {
                "row_id": row_id,
                "category": str(blocker["category"]),
                "status": str(evidence_row.get("status", "missing")),
                "handoff_doc": str(blocker["handoff_doc"]),
                "artifact_path": redacted_path(row_id),
                "required_evidence": list(blocker.get("required_evidence", [])),
                "safety_rule": str(blocker["safety_rule"]),
            }
        )
    return tuple(actions)


def render_missing_actions_json(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> str:
    actions = missing_actions(blockers, evidence_doc)
    data = {
        "total_actions": len(actions),
        "actions": list(actions),
        "decision": "blocked-until-matching-evidence-is-reviewed",
    }
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
```

Update `render_missing_actions` to consume `missing_actions`:

```python
def render_missing_actions(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> str:
    lines = [
        "zh-Hans public-RC missing evidence actions",
        "Only use these rows after external evidence has been captured, redacted, and approved.",
    ]
    for action in missing_actions(blockers, evidence_doc):
        lines.extend(
            [
                "",
                f"row_id: {action['row_id']}",
                f"category: {action['category']}",
                f"status: {action['status']}",
                f"handoff_doc: {action['handoff_doc']}",
                f"artifact_path: {action['artifact_path']}",
                "required_evidence:",
            ]
        )
        for item in action["required_evidence"]:
            lines.append(f"- {item}")
        lines.append(f"safety_rule: {action['safety_rule']}")
    lines.append("")
    lines.append("decision: blocked-until-matching-evidence-is-reviewed")
    return "\n".join(lines) + "\n"
```

Update the CLI parser:

```python
    parser.add_argument("--missing-actions-json", action="store_true", help="Print row-level missing evidence actions as JSON")
```

Add this branch after loading `evidence` and before `--missing-actions`:

```python
    if args.missing_actions_json:
        print(render_missing_actions_json(blockers, evidence), end="")
        return 0
```

- [ ] **Step 4: Verify missing-action JSON**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --missing-actions-json
```

Expected:

```text
report tests pass
JSON output contains total_actions 11 and decision blocked-until-matching-evidence-is-reviewed
```

- [ ] **Step 5: Create Phase 255 record**

Create `docs/zh-Hans-localization-phase255.md`:

```markdown
# zh-Hans Localization Phase 255

Date: 2026-06-02

## Scope

Phase 255 adds machine-readable JSON output for missing public-RC evidence
actions.

This phase does not change blocker status, add real evidence, stage, commit,
push, merge, rebase, mutate tags, use accounts, create backend fixtures, touch
billing/cloud state, run Rust compile, build a bundle, launch GUI, or modify
PNG assets.

## Validation

```text
python3 -m unittest script/test_zh_public_rc_evidence_report.py: passed
python3 script/zh_public_rc_evidence_report.py --missing-actions-json: passed
missing action rows: 11
rows promoted: 0
```

## Qualification Review

```text
phase: 255
status: qualified-json-missing-actions
safe to continue to Phase 256: yes
```
```

- [ ] **Step 6: Verify Task 4**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 5: Phase 256 RC35 Evidence Automation Package

**Files:**
- Create: `docs/zh-Hans-public-rc-evidence-automation-rc35.md`
- Create: `docs/zh-Hans-localization-phase256.md`

- [ ] **Step 1: Generate current text and JSON outputs**

Run:

```bash
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --json
python3 script/zh_public_rc_evidence_report.py --missing-actions
python3 script/zh_public_rc_evidence_report.py --missing-actions-json
```

Expected:

```text
all four commands exit 0
report decision remains blocked
ready rows remain 0
missing action rows remain 11
```

- [ ] **Step 2: Create RC35 evidence automation package**

Create `docs/zh-Hans-public-rc-evidence-automation-rc35.md`:

```markdown
# zh-Hans Public-RC Evidence Automation RC35

Date: 2026-06-02

## Purpose

This document records the RC35 evidence automation outputs. It does not provide
real evidence and does not clear blockers.

## Commands

```bash
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --json
python3 script/zh_public_rc_evidence_report.py --missing-actions
python3 script/zh_public_rc_evidence_report.py --missing-actions-json
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

## Current Summary

```text
public-RC rows tracked: 11
ready rows: 0
missing action rows: 11
decision: blocked
strict lint: expected fail until real evidence exists
```

## JSON Output Use

```text
--json: use for dashboards and release readiness summaries
--missing-actions-json: use for row-owner handoff and evidence packet generation
```

## Safety Boundary

```text
raw evidence stays outside Git
redacted artifacts under artifacts/redacted/*.txt require explicit approval
ledger promotion requires strict lint pass and manual raw evidence review
blocker registry promotion requires accepted evidence row and reviewed raw evidence
```
```

- [ ] **Step 3: Create Phase 256 record**

Create `docs/zh-Hans-localization-phase256.md`:

```markdown
# zh-Hans Localization Phase 256

Date: 2026-06-02

## Scope

Phase 256 creates the RC35 public-RC evidence automation package.

This phase does not create real evidence, clear blockers, stage, commit, push,
merge, rebase, mutate tags, use accounts, create backend fixtures, touch
billing/cloud state, run Rust compile, build a bundle, launch GUI, or modify
PNG assets.

## Validation

```text
text evidence report: passed
JSON evidence report: passed
text missing-action report: passed
JSON missing-action report: passed
ready rows: 0
missing action rows: 11
public RC: not ready
```

## Qualification Review

```text
phase: 256
status: qualified-evidence-automation-package
safe to continue to Phase 257: yes
```
```

- [ ] **Step 4: Verify Task 5**

Run:

```bash
python3 script/privacy_guard.py --paths docs/zh-Hans-public-rc-evidence-automation-rc35.md docs/zh-Hans-localization-phase256.md
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 6: Phase 257 RC35 Lane Readiness Refresh

**Files:**
- Create: `docs/zh-Hans-public-rc-lane-readiness-rc35.md`
- Create: `docs/zh-Hans-localization-phase257.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Re-render status and check PNG dirtiness**

Run:

```bash
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py --json
git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
```

Expected:

```text
public-RC blockers remain 11
JSON report decision remains blocked
no PNG status output
no PNG diff output
```

- [ ] **Step 2: Create RC35 lane readiness**

Create `docs/zh-Hans-public-rc-lane-readiness-rc35.md`:

```markdown
# zh-Hans Public-RC Lane Readiness RC35

Date: 2026-06-02

## Current Lane Status

```text
backend_fixture: total=5 ready=0 missing=5
disposable_object: total=3 ready=0 missing=3
isolated_account: total=3 ready=0 missing=3
asset lane: blocked-no-asset-approval
heavy validation lane: pending-low-load-gate
GUI lane: blocked-no-fresh-bundle
publication lane: blocked-no-explicit-approval
```

## Automation Outputs

```text
report JSON: python3 script/zh_public_rc_evidence_report.py --json
missing-action JSON: python3 script/zh_public_rc_evidence_report.py --missing-actions-json
strict lint: python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

## Promotion Rule

No lane can promote a row unless the matching evidence row is `status = "provided"`,
the expected row-specific artifact path exists, strict artifact lint passes, and
raw evidence has been manually reviewed for safety and row match.
```

- [ ] **Step 3: Create Phase 257 record**

Create `docs/zh-Hans-localization-phase257.md`:

```markdown
# zh-Hans Localization Phase 257

Date: 2026-06-02

## Scope

Phase 257 refreshes RC35 lane readiness and asset/GUI dependency status.

This phase does not clear blockers, create evidence, stage, commit, push, merge,
rebase, mutate tags, use accounts, create backend fixtures, touch billing/cloud
state, run Rust compile, build a bundle, launch GUI, or modify PNG assets.

## Validation

```text
public-RC blocker summary: 11 blockers
JSON evidence report: blocked
PNG changes: none
asset lane: blocked-no-asset-approval
GUI lane: blocked-no-fresh-bundle
```

## Qualification Review

```text
phase: 257
status: qualified-lane-readiness-refresh
safe to continue to Phase 258: yes
```
```

- [ ] **Step 4: Update GUI smoke matrix**

Append this entry to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## RC35 Lane And Asset Refresh

```text
asset lane: blocked-no-asset-approval
PNG changes: none
fresh bundle: pending-low-load-gate
GUI launch: blocked-no-fresh-bundle
```
```

- [ ] **Step 5: Verify Task 6**

Run:

```bash
python3 script/privacy_guard.py --paths docs/zh-Hans-public-rc-lane-readiness-rc35.md docs/zh-Hans-localization-phase257.md docs/zh-Hans-gui-smoke-matrix.md
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 7: Phase 258 Low-Load Heavy Validation Retry

**Files:**
- Create: `docs/zh-Hans-localization-phase258.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Run the low-load gate**

Run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25; code=$?; printf 'low_load_gate_exit_code=%s\n' "$code"
```

Expected:

```text
decision: run-heavy-gate
```

or:

```text
decision: defer-heavy-gate
```

- [ ] **Step 2: If the gate defers, record safe skip**

If the output says `decision: defer-heavy-gate`, do not run Cargo, bundle, or GUI commands. Create `docs/zh-Hans-localization-phase258.md`:

```markdown
# zh-Hans Localization Phase 258

Date: 2026-06-02

## Scope

Phase 258 retries the low-load gate for heavy validation.

This phase does not run Rust compile, build a bundle, launch GUI, stage, commit,
push, merge, rebase, mutate tags, use accounts, create backend fixtures, touch
billing/cloud state, create real evidence artifacts, or modify PNG assets when
the low-load gate defers.

## Low-Load Gate

```text
decision: defer-heavy-gate
heavy validation: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```

## Qualification Review

```text
phase: 258
status: qualified-heat-safety-defer
safe to continue to Phase 259: yes
```
```

- [ ] **Step 3: If the gate allows, run minimal heavy validation**

Only if the output says `decision: run-heavy-gate`, run:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
cargo check exits 0
./script/run --dont-open creates a current debug bundle without opening GUI
```

Then create `docs/zh-Hans-localization-phase258.md` with:

```markdown
# zh-Hans Localization Phase 258

Date: 2026-06-02

## Scope

Phase 258 runs minimal heavy validation only because the low-load gate allowed
it.

This phase does not launch GUI, stage, commit, push, merge, rebase, mutate tags,
use accounts, create backend fixtures, touch billing/cloud state, create real
evidence artifacts, or modify PNG assets.

## Validation

```text
low-load gate: run-heavy-gate
cargo check -p warp: passed
fresh bundle command: passed
GUI launch: not run
```

## Qualification Review

```text
phase: 258
status: qualified-heavy-validation
safe to continue to Phase 259: yes
```
```

- [ ] **Step 4: Update GUI smoke matrix**

If heavy validation was skipped, append:

```markdown
## RC35 Heavy Validation Retry

```text
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```
```

If heavy validation ran and passed, append:

```markdown
## RC35 Heavy Validation Retry

```text
fresh bundle: passed
GUI launch: pending-explicit-gui-smoke-approval
```
```

- [ ] **Step 5: Verify Task 7**

Run:

```bash
python3 script/privacy_guard.py --paths docs/zh-Hans-localization-phase258.md docs/zh-Hans-gui-smoke-matrix.md
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 8: Phase 259 RC35 Freeze

**Files:**
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc35.md`
- Create: `docs/zh-Hans-localization-phase259.md`
- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Run final low-load validation suite**

Run:

```bash
set -e
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json
set +e
nice -n 10 python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
lint_code=$?
set -e
printf 'strict_evidence_lint_exit_code=%s\n' "$lint_code"
test "$lint_code" -eq 1
nice -n 10 python3 script/privacy_guard.py --all-tracked
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py
nice -n 10 cargo fmt --check
git diff --check
```

Expected:

```text
manifest validation passes
glossary check passes
dry-run reports would_change 0 and missing 0
release coverage remains 100.0%
public-RC status still lists 11 blockers unless real evidence was explicitly added
JSON evidence outputs exit 0
strict evidence lint exits 1 when no real evidence is provided
privacy guard exits 0
Python tests pass
cargo fmt --check exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create RC35 release-candidate record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc35.md`:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC35

Date: 2026-06-02

## Scope

RC35 covers Phases 252 through 259. It adds strict row-specific artifact path
checks, JSON evidence report output, JSON missing-action output, RC35 evidence
automation docs, lane readiness refresh, low-load heavy validation retry, and
the next local-use/public-RC decision freeze.

RC35 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Automation

```text
text report: script/zh_public_rc_evidence_report.py
JSON report: script/zh_public_rc_evidence_report.py --json
text missing actions: script/zh_public_rc_evidence_report.py --missing-actions
JSON missing actions: script/zh_public_rc_evidence_report.py --missing-actions-json
strict evidence linter: script/zh_public_rc_evidence_lint.py --strict-artifacts
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC35: 0
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC35 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, fresh bundle/current-cycle
GUI evidence exists, onboarding PNG visual status is approved or regenerated,
and publication is explicitly approved by the user.
```

- [ ] **Step 3: Create Phase 259 record**

Create `docs/zh-Hans-localization-phase259.md`:

```markdown
# zh-Hans Localization Phase 259

Date: 2026-06-02

## Scope

Phase 259 runs the final RC35 low-load validation suite and writes the RC35
release-candidate record.

This phase does not stage, commit, push, merge, rebase, mutate tags, use
accounts, create backend fixtures, touch billing/cloud state, create real
evidence artifacts, or modify PNG assets.

## Validation

```text
manifest validation: passed
glossary check: passed
dry-run summary: would_change 0, missing 0
release coverage: 100.0%
public-RC blocker summary: 11 blockers
text evidence report: passed
JSON evidence report: passed
text missing-action report: passed
JSON missing-action report: passed
strict evidence linter: expected fail, exit_code 1
privacy guard: passed
Python tests: passed
cargo fmt --check: passed
git diff --check: passed
```

## Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

## Qualification Review

```text
phase: 259
status: qualified-rc35-freeze
safe to continue beyond RC35: yes, but public RC remains evidence-gated
```
```

- [ ] **Step 4: Update README and localization index**

Update `README.md` to mention:

```markdown
最后核验记录：`2026-06-02 RC35`
```

Update `docs/zh-Hans-localization.md` to mention:

```markdown
- RC35 adds strict row-specific artifact path checks plus JSON evidence and missing-action outputs while keeping public-RC blocked by missing real evidence.
```

- [ ] **Step 5: Verify final docs and tests**

Run:

```bash
set -e
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json
set +e
nice -n 10 python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
lint_code=$?
set -e
printf 'strict_evidence_lint_exit_code=%s\n' "$lint_code"
test "$lint_code" -eq 1
nice -n 10 python3 script/privacy_guard.py --all-tracked
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py
nice -n 10 cargo fmt --check
git diff --check
git status --short --branch
```

Expected:

```text
dry-run reports would_change 0 and missing 0
public-RC remains blocked unless external evidence was explicitly added
JSON evidence outputs exit 0
strict evidence lint expected fail exits 1 with missing evidence rows
privacy guard exits 0
targeted tests pass
cargo fmt --check exits 0
git diff --check exits 0
git status shows local changes only; no stage/commit/push has been performed
```

## Self-Review

```text
spec coverage: phases cover post-RC34 baseline, strict row-path hardening, JSON reports, JSON missing actions, evidence automation docs, lane readiness, heat-safe heavy retry, and RC35 freeze
red-flag scan: no unresolved plan steps
external-state safety: all account/backend/cloud/billing/GUI evidence creation remains forbidden without explicit approval
machine-load safety: heavy commands are gated by script/zh_low_load_gate.py
publication safety: no stage/commit/push/merge/rebase/tag steps are included
```
