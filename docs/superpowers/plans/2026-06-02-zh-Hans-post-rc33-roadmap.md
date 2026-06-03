# zh-Hans Post-RC33 Public-RC Evidence Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC33 to RC34 by making public-RC evidence closure easier to execute and audit, while keeping all real account/backend/cloud/billing/GUI evidence behind explicit external approval and low-load gates.

**Architecture:** Keep `resources/localization/zh-Hans-public-rc-blockers.toml` as the blocker source of truth and `resources/localization/zh-Hans-public-rc-evidence.toml` as the committable evidence ledger. Extend the existing read-only report/lint helper path so future evidence packets can be mapped to exact rows without mutating real services, then freeze RC34 with the same honest local-use/public-RC distinction. Heavy Rust, bundle, and GUI validation remains gated by `script/zh_low_load_gate.py`.

**Tech Stack:** Python `unittest`, existing small TOML parser in `script/zh_public_rc_evidence_lint.py`, Markdown runbooks, existing zh-Hans validation scripts, Git diff/privacy checks, macOS low-load gate.

---

## Current Baseline

RC33 status:

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
heavy gate: defer-heavy-gate
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
onboarding PNG changes: none
```

Next-cycle priority:

```text
1. Preserve the current "public RC not ready" decision until real matching evidence exists.
2. Add row-level missing-action output so evidence owners can see exact required artifacts and safety rules.
3. Add strict-artifact positive-path tests using temporary safe redacted text, not real artifacts.
4. Create RC34 action/readiness docs that separate backend fixtures, isolated accounts, disposable objects, assets, heavy validation, GUI, and publication.
5. Retry heavy validation only if script/zh_low_load_gate.py returns decision: run-heavy-gate.
6. Keep stage, commit, push, merge, rebase, and tags outside this plan unless the user explicitly approves publication.
```

## File Structure

- Modify `script/zh_public_rc_evidence_report.py` to add `--missing-actions` output for exact row handoff instructions.
- Modify `script/test_zh_public_rc_evidence_report.py` to test missing-action output and partial-ready row omission.
- Modify `script/test_zh_public_rc_evidence_lint.py` to add a strict-artifact positive-path test using a temporary safe redacted text file.
- Create `docs/zh-Hans-public-rc-evidence-action-package-rc34.md` for the generated row action package.
- Create `docs/zh-Hans-public-rc-lane-readiness-rc34.md` for lane-specific readiness and external input boundaries.
- Create `docs/zh-Hans-localization-phase244.md` through `docs/zh-Hans-localization-phase251.md`.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc34.md` only during Phase 251.
- Modify `README.md` only during Phase 251 to point to RC34 and the new missing-action helper.
- Modify `docs/zh-Hans-localization.md` during Phase 244 and Phase 251.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` only when asset, heavy, or GUI status changes.
- Do not modify `resources/localization/zh-Hans-overrides.toml` unless validation finds real manifest/source drift.
- Do not change `resources/localization/zh-Hans-public-rc-evidence.toml` unless a phase receives reviewed redacted evidence and explicit approval.
- Do not create files under `artifacts/redacted/` except temporary files inside tests.
- Do not modify `app/assets/async/png/onboarding/**/*.png` without explicit asset approval.
- Do not stage, commit, push, merge, rebase, or mutate tags without explicit user approval.

## Phase Map

| Phase | Purpose | Qualification Gate |
| --- | --- | --- |
| 244 | Post-RC33 baseline and scope lock | current 11 blockers confirmed; privacy/diff checks pass |
| 245 | Missing-action report helper | tests pass; helper prints exact action rows without secrets |
| 246 | Strict artifact positive-path coverage | linter accepts temporary safe redacted artifact and rejects current missing evidence |
| 247 | RC34 evidence action package | docs match helper output and preserve no-real-evidence boundary |
| 248 | RC34 lane readiness package | every lane has clear external input, safety rule, and promotion rule |
| 249 | Asset/GUI dependency decision refresh | no PNG mutation; GUI remains gated by fresh bundle |
| 250 | Low-load heavy validation retry | run heavy commands only after `decision: run-heavy-gate`; otherwise record defer |
| 251 | RC34 freeze and publication boundary | validation passes; RC34 decision is explicit and honest |

### Task 1: Phase 244 Post-RC33 Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase244.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect current branch and public-RC status**

Run:

```bash
git status --short --branch
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py
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
strict evidence linter exits 1 because 11 rows still lack evidence
privacy_guard.py exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create Phase 244 record**

Create `docs/zh-Hans-localization-phase244.md`:

```markdown
# zh-Hans Localization Phase 244

Date: 2026-06-02

## Scope

Phase 244 audits the post-RC33 baseline before adding missing-action evidence
report output.

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
strict evidence lint: expected fail, exit_code 1
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-missing-action-helper
public RC: still blocked by evidence
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 244
status: qualified-post-rc33-baseline
safe to continue to Phase 245: yes
```
```

- [ ] **Step 3: Update localization index**

Add this line to `docs/zh-Hans-localization.md` near the RC33 entry:

```markdown
- Phase 244 records the post-RC33 baseline before adding row-level missing-action evidence output.
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

### Task 2: Phase 245 Missing-Action Report Helper

**Files:**
- Modify: `script/zh_public_rc_evidence_report.py`
- Modify: `script/test_zh_public_rc_evidence_report.py`
- Create: `docs/zh-Hans-localization-phase245.md`

- [ ] **Step 1: Add failing tests for missing-action output**

Append to `script/test_zh_public_rc_evidence_report.py`:

```python
from zh_public_rc_evidence_report import render_missing_actions
```

Add these test methods inside `PublicRcEvidenceReportTests`:

```python
    def test_missing_actions_include_handoff_and_redacted_path(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = render_missing_actions(blockers, evidence)

        self.assertIn("row_id: GUI-AUTH-01", actions)
        self.assertIn("category: isolated_account", actions)
        self.assertIn("handoff_doc: docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md", actions)
        self.assertIn("artifact_path: artifacts/redacted/gui-auth-01.txt", actions)
        self.assertIn("- isolated browser-login test account", actions)
        self.assertIn("safety_rule:", actions)
        self.assertNotIn("person@example.com", actions)
        self.assertNotIn("https://", actions)

    def test_missing_actions_omit_ready_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-AUTH-01",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-auth-01.txt"],
                    "cleanup_proof": "redacted cleanup proof reviewed",
                    "redaction": "identifiers removed",
                    "notes": "safe isolated account packet",
                }
            ]
        }

        actions = render_missing_actions(blockers, evidence)

        self.assertNotIn("row_id: GUI-AUTH-01", actions)
        self.assertIn("row_id: GUI-SET-03", actions)
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
```

Expected:

```text
FAIL or ERROR because render_missing_actions is not implemented
```

- [ ] **Step 3: Implement missing-action output**

In `script/zh_public_rc_evidence_report.py`, add this function after `render_templates`:

```python
def render_missing_actions(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> str:
    evidence = evidence_by_id(evidence_doc)
    lines = [
        "zh-Hans public-RC missing evidence actions",
        "Only use these rows after external evidence has been captured, redacted, and approved.",
    ]
    for row_id, blocker in sorted(blocker_index(blockers).items()):
        evidence_row = evidence.get(row_id, {})
        if str(evidence_row.get("status", "missing")) == "provided":
            continue

        lines.extend(
            [
                "",
                f"row_id: {row_id}",
                f"category: {blocker['category']}",
                f"status: {evidence_row.get('status', 'missing')}",
                f"handoff_doc: {blocker['handoff_doc']}",
                f"artifact_path: {redacted_path(row_id)}",
                "required_evidence:",
            ]
        )
        for item in blocker.get("required_evidence", []):
            lines.append(f"- {item}")
        lines.append(f"safety_rule: {blocker['safety_rule']}")
    lines.append("")
    lines.append("decision: blocked-until-matching-evidence-is-reviewed")
    return "\n".join(lines) + "\n"
```

Update the CLI parser:

```python
    parser.add_argument("--missing-actions", action="store_true", help="Print row-level missing evidence actions")
```

Add this branch before the normal evidence report print:

```python
    evidence = load_toml(args.evidence)
    if args.missing_actions:
        print(render_missing_actions(blockers, evidence), end="")
        return 0
```

Keep the existing `--templates` behavior unchanged.

- [ ] **Step 4: Verify helper tests and output**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --missing-actions
```

Expected:

```text
report tests pass
missing-actions output lists 11 rows
output contains artifacts/redacted/gui-auth-01.txt
output ends with decision: blocked-until-matching-evidence-is-reviewed
```

- [ ] **Step 5: Create Phase 245 record**

Create `docs/zh-Hans-localization-phase245.md`:

```markdown
# zh-Hans Localization Phase 245

Date: 2026-06-02

## Scope

Phase 245 adds row-level missing-action output for the public-RC evidence report
helper.

This phase does not change blocker status, add real evidence, stage, commit,
push, merge, rebase, mutate tags, use accounts, create backend fixtures, touch
billing/cloud state, run Rust compile, build a bundle, launch GUI, or modify
PNG assets.

## Validation

```text
python3 -m unittest script/test_zh_public_rc_evidence_report.py: passed
python3 script/zh_public_rc_evidence_report.py --missing-actions: passed
listed rows: 11
rows promoted: 0
```

## Qualification Review

```text
phase: 245
status: qualified-missing-action-helper
safe to continue to Phase 246: yes
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

### Task 3: Phase 246 Strict Artifact Positive-Path Coverage

**Files:**
- Modify: `script/test_zh_public_rc_evidence_lint.py`
- Create: `docs/zh-Hans-localization-phase246.md`

- [ ] **Step 1: Add a safe strict-artifact acceptance test**

Append this test method inside `PublicRcEvidenceLintTests` in `script/test_zh_public_rc_evidence_lint.py`:

```python
    def test_strict_artifacts_accepts_safe_redacted_text(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            artifact = Path(root) / "artifacts/redacted/gui-set-05.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text(
                "row: GUI-SET-05\nredacted evidence summary only\nfixture reset proof reviewed\n",
                encoding="utf-8",
            )
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
                        "evidence_paths": ["artifacts/redacted/gui-set-05.txt"],
                        "cleanup_proof": "fixture reset proof captured",
                        "redaction": "identifiers removed",
                        "notes": "safe marker only",
                    }
                ]
            }

            result = lint_evidence(blockers, evidence, strict_artifacts=True, repo_root=Path(root))

        self.assertTrue(result.ok)
        self.assertEqual(result.ready_rows, ("GUI-SET-05",))
```

- [ ] **Step 2: Run strict-artifact tests**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
```

Expected:

```text
all evidence lint tests pass
```

If the test fails, fix only the strict artifact path/read logic needed for this safe temporary artifact to pass.

- [ ] **Step 3: Confirm current ledger remains blocked**

Run:

```bash
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts; code=$?; printf 'strict_evidence_lint_exit_code=%s\n' "$code"; test "$code" -eq 1
```

Expected:

```text
exit code 1 is accepted
decision: fail
reason: current 11 rows still have missing evidence
```

- [ ] **Step 4: Create Phase 246 record**

Create `docs/zh-Hans-localization-phase246.md`:

```markdown
# zh-Hans Localization Phase 246

Date: 2026-06-02

## Scope

Phase 246 adds a positive-path strict-artifact regression test with a temporary
safe redacted text artifact.

This phase does not create repository evidence artifacts, change evidence
ledger status, stage, commit, push, merge, rebase, mutate tags, use accounts,
create backend fixtures, touch billing/cloud state, run Rust compile, build a
bundle, launch GUI, or modify PNG assets.

## Validation

```text
strict artifact temporary safe-text test: passed
current ledger strict lint: expected fail, exit_code 1
rows promoted: 0
```

## Qualification Review

```text
phase: 246
status: qualified-strict-artifact-positive-path
safe to continue to Phase 247: yes
```
```

- [ ] **Step 5: Verify Task 3**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Phase 247 RC34 Evidence Action Package

**Files:**
- Create: `docs/zh-Hans-public-rc-evidence-action-package-rc34.md`
- Create: `docs/zh-Hans-localization-phase247.md`

- [ ] **Step 1: Generate current missing-action output**

Run:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-actions
```

Expected:

```text
output lists GUI-AUTH-01, GUI-SET-03, GUI-SET-04, GUI-SET-05, GUI-SET-06, GUI-WS-04, GUI-WS-06, GUI-WS-07, GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01
decision: blocked-until-matching-evidence-is-reviewed
```

- [ ] **Step 2: Create RC34 action package**

Create `docs/zh-Hans-public-rc-evidence-action-package-rc34.md`:

```markdown
# zh-Hans Public-RC Evidence Action Package RC34

Date: 2026-06-02

## Purpose

This action package converts the RC33 evidence packet template into row-level
owner actions. It does not provide evidence and does not clear blockers.

## Generate Current Actions

```bash
python3 script/zh_public_rc_evidence_report.py --missing-actions
```

## Current Required Rows

```text
GUI-AUTH-01: isolated_account, artifacts/redacted/gui-auth-01.txt
GUI-SET-03: isolated_account, artifacts/redacted/gui-set-03.txt
GUI-SET-04: backend_fixture, artifacts/redacted/gui-set-04.txt
GUI-SET-05: backend_fixture, artifacts/redacted/gui-set-05.txt
GUI-SET-06: disposable_object, artifacts/redacted/gui-set-06.txt
GUI-WS-04: disposable_object, artifacts/redacted/gui-ws-04.txt
GUI-WS-06: isolated_account, artifacts/redacted/gui-ws-06.txt
GUI-WS-07: disposable_object, artifacts/redacted/gui-ws-07.txt
GUI-BILL-01: backend_fixture, artifacts/redacted/gui-bill-01.txt
GUI-BILL-02: backend_fixture, artifacts/redacted/gui-bill-02.txt
GUI-CLOUD-01: backend_fixture, artifacts/redacted/gui-cloud-01.txt
```

## Promotion Rule

```text
1. Raw evidence is captured outside Git.
2. Raw evidence is manually reviewed for row match and safety.
3. Redacted text is created under artifacts/redacted/*.txt only after explicit approval.
4. The matching [[evidence]] row is changed to status = "provided".
5. python3 script/zh_public_rc_evidence_lint.py --strict-artifacts passes.
6. The blocker registry is updated only after the evidence row and raw evidence review are accepted.
```

## Current Boundary

```text
ready rows: 0
rows promoted by this package: 0
real evidence artifacts created by this package: none
public RC: not ready
```
```

- [ ] **Step 3: Create Phase 247 record**

Create `docs/zh-Hans-localization-phase247.md`:

```markdown
# zh-Hans Localization Phase 247

Date: 2026-06-02

## Scope

Phase 247 creates the RC34 public-RC evidence action package.

This phase does not create real evidence, clear blockers, stage, commit, push,
merge, rebase, mutate tags, use accounts, create backend fixtures, touch
billing/cloud state, run Rust compile, build a bundle, launch GUI, or modify
PNG assets.

## Validation

```text
missing-action helper: passed
required action rows: 11
rows promoted: 0
public RC: not ready
```

## Qualification Review

```text
phase: 247
status: qualified-evidence-action-package
safe to continue to Phase 248: yes
```
```

- [ ] **Step 4: Verify Task 4**

Run:

```bash
python3 script/privacy_guard.py --paths docs/zh-Hans-public-rc-evidence-action-package-rc34.md docs/zh-Hans-localization-phase247.md
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 5: Phase 248 RC34 Lane Readiness Package

**Files:**
- Create: `docs/zh-Hans-public-rc-lane-readiness-rc34.md`
- Create: `docs/zh-Hans-localization-phase248.md`

- [ ] **Step 1: Re-render report and status**

Run:

```bash
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --missing-actions
```

Expected:

```text
public-RC blockers remain 11
backend_fixture: total=5 ready=0 missing=5
disposable_object: total=3 ready=0 missing=3
isolated_account: total=3 ready=0 missing=3
```

- [ ] **Step 2: Create RC34 lane readiness**

Create `docs/zh-Hans-public-rc-lane-readiness-rc34.md`:

```markdown
# zh-Hans Public-RC Lane Readiness RC34

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

## Lane Inputs Required

```text
backend_fixture: safe fixture owner, reset path, redacted artifact, raw evidence review
isolated_account: non-main isolated account, callback/settings proof, logout cleanup proof, raw evidence review
disposable_object: exact allowlisted object, cancel-first proof, cleanup proof, raw evidence review
asset lane: design/product approval for asset-only branch or accepted deferral
heavy validation lane: script/zh_low_load_gate.py decision: run-heavy-gate
GUI lane: fresh bundle plus low-load allowance
publication lane: explicit user request for stage/commit/push/tag
```

## Rows By Lane

```text
backend_fixture: GUI-SET-04, GUI-SET-05, GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01
isolated_account: GUI-AUTH-01, GUI-SET-03, GUI-WS-06
disposable_object: GUI-SET-06, GUI-WS-04, GUI-WS-07
```

## Promotion Rule

No lane can promote a row unless the matching evidence row is `status = "provided"`,
`python3 script/zh_public_rc_evidence_lint.py --strict-artifacts` passes, and
raw evidence has been manually reviewed for safety and row match.
```

- [ ] **Step 3: Create Phase 248 record**

Create `docs/zh-Hans-localization-phase248.md`:

```markdown
# zh-Hans Localization Phase 248

Date: 2026-06-02

## Scope

Phase 248 creates the RC34 lane readiness package.

This phase does not clear blockers, create evidence, stage, commit, push, merge,
rebase, mutate tags, use accounts, create backend fixtures, touch billing/cloud
state, run Rust compile, build a bundle, launch GUI, or modify PNG assets.

## Validation

```text
public-RC blocker summary: 11 blockers
evidence report: ready_rows 0
lane package: created
public RC: not ready
```

## Qualification Review

```text
phase: 248
status: qualified-lane-readiness-package
safe to continue to Phase 249: yes
```
```

- [ ] **Step 4: Verify Task 5**

Run:

```bash
python3 script/privacy_guard.py --paths docs/zh-Hans-public-rc-lane-readiness-rc34.md docs/zh-Hans-localization-phase248.md
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 6: Phase 249 Asset And GUI Dependency Decision Refresh

**Files:**
- Create: `docs/zh-Hans-localization-phase249.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Confirm PNG asset status**

Run:

```bash
git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
rg -n "asset lane|PNG|fresh bundle|GUI launch|skipped" docs/zh-Hans-release-candidate-2026-06-02-rc33.md docs/zh-Hans-public-rc-lane-readiness-rc34.md docs/zh-Hans-gui-smoke-matrix.md
```

Expected:

```text
no PNG changes
asset lane remains blocked-no-asset-approval
GUI remains blocked-no-fresh-bundle unless Phase 250 later creates a fresh bundle
```

- [ ] **Step 2: Create Phase 249 record**

Create `docs/zh-Hans-localization-phase249.md`:

```markdown
# zh-Hans Localization Phase 249

Date: 2026-06-02

## Scope

Phase 249 refreshes the asset and GUI dependency decision before another
low-load heavy validation attempt.

This phase does not modify PNG assets, launch GUI, build a bundle, stage,
commit, push, merge, rebase, mutate tags, use accounts, create backend fixtures,
touch billing/cloud state, or create real evidence artifacts.

## Findings

```text
PNG changes: none
asset lane: blocked-no-asset-approval
GUI lane before Phase 250: blocked-no-fresh-bundle
```

## Qualification Review

```text
phase: 249
status: qualified-asset-gui-dependency-refresh
safe to continue to Phase 250: yes
```
```

- [ ] **Step 3: Update GUI smoke matrix**

Append a short RC34 pre-heavy-gate entry to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## RC34 Pre-Heavy-Gate Refresh

```text
asset lane: blocked-no-asset-approval
PNG changes: none
fresh bundle: pending-low-load-gate
GUI launch: blocked-no-fresh-bundle
```
```

- [ ] **Step 4: Verify Task 6**

Run:

```bash
python3 script/privacy_guard.py --paths docs/zh-Hans-localization-phase249.md docs/zh-Hans-gui-smoke-matrix.md
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 7: Phase 250 Low-Load Heavy Validation Retry

**Files:**
- Create: `docs/zh-Hans-localization-phase250.md`
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

If the output says `decision: defer-heavy-gate`, do not run Cargo, bundle, or GUI commands. Create `docs/zh-Hans-localization-phase250.md`:

```markdown
# zh-Hans Localization Phase 250

Date: 2026-06-02

## Scope

Phase 250 retries the low-load gate for heavy validation.

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
phase: 250
status: qualified-heat-safety-defer
safe to continue to Phase 251: yes
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

Then create `docs/zh-Hans-localization-phase250.md` with:

```markdown
# zh-Hans Localization Phase 250

Date: 2026-06-02

## Scope

Phase 250 runs minimal heavy validation only because the low-load gate allowed
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
phase: 250
status: qualified-heavy-validation
safe to continue to Phase 251: yes
```
```

- [ ] **Step 4: Update GUI smoke matrix**

If heavy validation was skipped, append:

```markdown
## RC34 Heavy Validation Retry

```text
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```
```

If heavy validation ran and passed, append:

```markdown
## RC34 Heavy Validation Retry

```text
fresh bundle: passed
GUI launch: pending-explicit-gui-smoke-approval
```
```

- [ ] **Step 5: Verify Task 7**

Run:

```bash
python3 script/privacy_guard.py --paths docs/zh-Hans-localization-phase250.md docs/zh-Hans-gui-smoke-matrix.md
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 8: Phase 251 RC34 Freeze

**Files:**
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc34.md`
- Create: `docs/zh-Hans-localization-phase251.md`
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
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions
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
missing-action helper exits 0
strict evidence lint exits 1 when no real evidence is provided
privacy guard exits 0
Python tests pass
cargo fmt --check exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create RC34 release-candidate record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc34.md`:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC34

Date: 2026-06-02

## Scope

RC34 covers Phases 244 through 251. It adds row-level missing-action evidence
output, positive-path strict artifact regression coverage, RC34 evidence action
and lane readiness packages, asset/GUI dependency refresh, low-load heavy
validation retry, and the next local-use/public-RC decision freeze.

RC34 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Readiness

```text
evidence report: script/zh_public_rc_evidence_report.py
missing-action report: script/zh_public_rc_evidence_report.py --missing-actions
strict evidence linter: script/zh_public_rc_evidence_lint.py --strict-artifacts
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC34: 0
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC34 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, fresh bundle/current-cycle
GUI evidence exists, onboarding PNG visual status is approved or regenerated,
and publication is explicitly approved by the user.
```

- [ ] **Step 3: Create Phase 251 record**

Create `docs/zh-Hans-localization-phase251.md`:

```markdown
# zh-Hans Localization Phase 251

Date: 2026-06-02

## Scope

Phase 251 runs the final RC34 low-load validation suite and writes the RC34
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
evidence report: ready_rows 0
missing-action report: passed
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
phase: 251
status: qualified-rc34-freeze
safe to continue beyond RC34: yes, but public RC remains evidence-gated
```
```

- [ ] **Step 4: Update README and localization index**

Update `README.md` to mention:

```markdown
Last verified zh-Hans release-candidate snapshot: 2026-06-02 RC34.
```

Update `docs/zh-Hans-localization.md` to mention:

```markdown
- RC34 adds row-level missing-action evidence output and strict artifact positive-path coverage while keeping public-RC blocked by missing real evidence.
```

- [ ] **Step 5: Verify final docs and tests**

Run:

```bash
set -e
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions
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
missing-action helper exits 0
strict evidence lint expected fail exits 1 with missing evidence rows
privacy guard exits 0
targeted tests pass
cargo fmt --check exits 0
git diff --check exits 0
git status shows local changes only; no stage/commit/push has been performed
```

## Self-Review

```text
spec coverage: phases cover post-RC33 baseline, helper hardening, evidence action packaging, lane readiness, asset/GUI dependency refresh, low-load heavy retry, and RC34 freeze
red-flag scan: no unresolved plan steps
external-state safety: all account/backend/cloud/billing/GUI evidence creation remains forbidden without explicit approval
machine-load safety: heavy commands are gated by script/zh_low_load_gate.py
publication safety: no stage/commit/push/merge/rebase/tag steps are included
```
