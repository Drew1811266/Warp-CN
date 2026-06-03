# zh-Hans Post-RC31 Evidence Intake Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC31 local engineering readiness toward RC32 by making public-RC evidence intake machine-checkable, retrying heavy validation only when the low-load gate allows it, and freezing an honest public-RC decision.

**Architecture:** Keep the existing translation overlay unchanged unless validation finds real source-string drift. Add a small evidence-intake linter around the existing public-RC blocker registry, then use phase records to classify backend fixture, isolated account, disposable object, asset, heavy-build, and GUI readiness without touching external accounts or production state.

**Tech Stack:** Python `unittest`, TOML through Python 3.11 `tomllib`, Git, Cargo/Rust validation, Markdown evidence records, existing zh-Hans localization scripts.

---

## Current Baseline

RC31 status:

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
backend fixture blockers: 5
disposable object blockers: 3
isolated account blockers: 3
heavy gate: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
onboarding PNG status: 54 total, 50 deferred, 4 accepted decorative/brand assets
```

Next-cycle priority:

```text
1. Do not repeat release-candidate freezing without improving evidence intake.
2. Make every public-RC row require structured, redacted, row-matching evidence before status promotion.
3. Keep heavy Rust/bundle/GUI commands behind script/zh_low_load_gate.py.
4. Keep asset regeneration blocked unless the user explicitly approves an asset-only branch.
5. Keep Git publication separate from evidence completion; do not stage, commit, push, merge, rebase, or tag without explicit user approval.
```

## File Structure

- Create `script/zh_public_rc_evidence_lint.py` to validate structured evidence packets against `resources/localization/zh-Hans-public-rc-blockers.toml`.
- Create `script/test_zh_public_rc_evidence_lint.py` for evidence lint parser and rule tests.
- Create `resources/localization/zh-Hans-public-rc-evidence.toml` as the current empty evidence-intake ledger.
- Create `docs/zh-Hans-public-rc-evidence-intake-rc32.md` to document the intake format and redaction rules.
- Create `docs/zh-Hans-localization-phase228.md` through `docs/zh-Hans-localization-phase235.md`.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc32.md` only during Phase 235.
- Modify `README.md` only during Phase 235 for RC32 status.
- Modify `docs/zh-Hans-localization.md` during Phase 228 and Phase 235.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` when heavy/GUI/evidence status changes.
- Modify `docs/zh-Hans-public-rc-action-package-rc31.md` only if the new evidence-intake format clarifies required inputs.
- Do not modify `resources/localization/zh-Hans-overrides.toml` unless a phase finds real manifest/source drift.
- Do not modify `app/assets/async/png/onboarding/**/*.png` unless the user explicitly approves an asset-only branch.
- Do not stage, commit, push, merge, rebase, or mutate tags unless the user explicitly asks for publication or integration.

## Phase Map

| Phase | Purpose | Qualification Gate |
| --- | --- | --- |
| 228 | Post-RC31 baseline and evidence-intake scope lock | diff/privacy checks pass; no source/PNG mutation |
| 229 | Evidence-intake linter test-first implementation | linter unit tests pass; empty ledger reports 11 missing-evidence errors |
| 230 | Evidence-intake docs and current empty ledger | docs match linter schema; blocker count unchanged |
| 231 | Backend fixture lane classification | five backend rows classified from ledger only |
| 232 | Isolated account and disposable object lane classification | six account/object rows classified from ledger only |
| 233 | Asset approval preflight | no PNG mutation; asset branch remains blocked unless explicitly approved |
| 234 | Low-load heavy validation retry | run heavy commands only after `decision: run-heavy-gate`; otherwise record defer |
| 235 | RC32 freeze and publication boundary | validation passes; RC32 decision is explicit and honest |

### Task 1: Phase 228 Post-RC31 Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase228.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect the current branch and protected scopes**

Run:

```bash
git status --short --branch
git status --short -- '*.rs' '*.toml' '*.py' '*.png' 'resources/localization/**' 'app/assets/async/png/onboarding/**/*.png'
python3 script/zh_public_rc_status.py
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
branch remains codex/zh-Hans-post-rc26-execution
public-RC blocker total remains 11 before evidence-intake work
privacy_guard.py exits 0
git diff --check exits 0
```

- [ ] **Step 2: Write Phase 228 record**

Create `docs/zh-Hans-localization-phase228.md`:

```markdown
# zh-Hans Localization Phase 228

Date: 2026-06-02

## Scope

Phase 228 audits the post-RC31 branch before evidence-intake tooling work.

This phase does not stage, commit, push, merge, rebase, create a worktree,
mutate tags, run Rust compile, build a bundle, launch GUI, use accounts,
create backend fixtures, touch billing/cloud state, or modify PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
public-RC blockers before intake tooling: 11
protected source/PNG mutation in this phase: none
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-evidence-intake-linter
status promotion without matching evidence: forbidden
```

## Qualification Review

```text
phase: 228
status: qualified-post-rc31-baseline
safe to continue to Phase 229: yes
```
```

- [ ] **Step 3: Update localization index**

In `docs/zh-Hans-localization.md`, add:

```markdown
- Phase 228 records the post-RC31 baseline before adding structured public-RC evidence intake checks.
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

### Task 2: Phase 229 Evidence-Intake Linter

**Files:**
- Create: `script/zh_public_rc_evidence_lint.py`
- Create: `script/test_zh_public_rc_evidence_lint.py`
- Create: `resources/localization/zh-Hans-public-rc-evidence.toml`
- Create: `docs/zh-Hans-localization-phase229.md`

- [ ] **Step 1: Create failing tests**

Create `script/test_zh_public_rc_evidence_lint.py`:

```python
#!/usr/bin/env python3

from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_lint import lint_evidence, load_toml


class PublicRcEvidenceLintTests(unittest.TestCase):
    def write_temp(self, content: str) -> Path:
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".toml", delete=False)
        temp.write(textwrap.dedent(content).strip() + "\n")
        temp.close()
        return Path(temp.name)

    def test_empty_evidence_reports_missing_required_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence_path = self.write_temp(
            """
            generated_on = "2026-06-02"
            [[evidence]]
            row_id = "GUI-AUTH-01"
            status = "missing"
            evidence_paths = []
            cleanup_proof = ""
            redaction = "none"
            notes = "not provided"
            """
        )

        result = lint_evidence(blockers, load_toml(evidence_path))

        self.assertFalse(result.ok)
        self.assertEqual(result.total_required, 11)
        self.assertIn("GUI-AUTH-01: missing evidence", result.errors)

    def test_complete_safe_fixture_row_passes(self) -> None:
        blockers = {
            "blocker": [
                {
                    "id": "GUI-SET-05",
                    "category": "backend_fixture",
                    "required_evidence": ["invalid credential fixture", "redacted error GUI evidence"],
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
                    "redaction": "email, token, key, endpoint url removed",
                    "notes": "uses zh-smoke-invalid-token only",
                }
            ]
        }

        result = lint_evidence(blockers, evidence)

        self.assertTrue(result.ok)
        self.assertEqual(result.ready_rows, ("GUI-SET-05",))

    def test_rejects_unknown_row(self) -> None:
        blockers = {"blocker": []}
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-NOT-REAL",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-not-real.txt"],
                    "cleanup_proof": "cleanup proof captured",
                    "redaction": "identifiers removed",
                    "notes": "unknown",
                }
            ]
        }

        result = lint_evidence(blockers, evidence)

        self.assertFalse(result.ok)
        self.assertIn("GUI-NOT-REAL: unknown row_id", result.errors)

    def test_rejects_sensitive_terms_in_committable_metadata(self) -> None:
        blockers = {
            "blocker": [
                {
                    "id": "GUI-AUTH-01",
                    "category": "isolated_account",
                    "required_evidence": ["isolated account", "redacted login"],
                    "public_rc_required": True,
                }
            ]
        }
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-AUTH-01",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-auth-01.txt"],
                    "cleanup_proof": "logout captured",
                    "redaction": "token removed",
                    "notes": "test email is person@example.com",
                }
            ]
        }

        result = lint_evidence(blockers, evidence)

        self.assertFalse(result.ok)
        self.assertIn("GUI-AUTH-01: sensitive-looking metadata in notes", result.errors)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and confirm they fail**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
```

Expected:

```text
fails with ModuleNotFoundError or missing zh_public_rc_evidence_lint symbols
```

- [ ] **Step 3: Create evidence linter**

Create `script/zh_public_rc_evidence_lint.py`:

```python
#!/usr/bin/env python3

from __future__ import annotations

import argparse
import dataclasses
import re
import sys
import tomllib
from pathlib import Path


DEFAULT_BLOCKERS = Path("resources/localization/zh-Hans-public-rc-blockers.toml")
DEFAULT_EVIDENCE = Path("resources/localization/zh-Hans-public-rc-evidence.toml")

SENSITIVE_PATTERNS = (
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"\b(sk|pk|ghp|gho|xoxb|AKIA)[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"https?://[^\s]+"),
    re.compile(r"\b(token|cookie|secret|api[_ -]?key)\s*[:=]", re.IGNORECASE),
)


@dataclasses.dataclass(frozen=True)
class LintResult:
    ok: bool
    total_required: int
    ready_rows: tuple[str, ...]
    missing_rows: tuple[str, ...]
    errors: tuple[str, ...]


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def has_sensitive_metadata(value: object) -> bool:
    if not isinstance(value, str):
        return False
    return any(pattern.search(value) for pattern in SENSITIVE_PATTERNS)


def blocker_index(blockers: dict) -> dict[str, dict]:
    return {
        str(row["id"]): row
        for row in blockers.get("blocker", [])
        if row.get("public_rc_required") is True
    }


def lint_evidence(blockers: dict, evidence_doc: dict) -> LintResult:
    blockers_by_id = blocker_index(blockers)
    evidence_rows = evidence_doc.get("evidence", [])
    errors: list[str] = []
    ready_rows: list[str] = []
    seen: set[str] = set()

    for row in evidence_rows:
        row_id = str(row.get("row_id", "")).strip()
        if not row_id:
            errors.append("evidence row is missing row_id")
            continue
        if row_id not in blockers_by_id:
            errors.append(f"{row_id}: unknown row_id")
            continue
        if row_id in seen:
            errors.append(f"{row_id}: duplicate evidence row")
            continue
        seen.add(row_id)

        status = str(row.get("status", "")).strip()
        evidence_paths = row.get("evidence_paths", [])
        cleanup_proof = str(row.get("cleanup_proof", "")).strip()
        redaction = str(row.get("redaction", "")).strip()
        notes = str(row.get("notes", "")).strip()

        for key in ("cleanup_proof", "redaction", "notes"):
            if has_sensitive_metadata(row.get(key)):
                errors.append(f"{row_id}: sensitive-looking metadata in {key}")

        if status != "provided":
            errors.append(f"{row_id}: missing evidence")
            continue
        if not isinstance(evidence_paths, list) or not evidence_paths:
            errors.append(f"{row_id}: evidence_paths must be a non-empty list")
            continue
        if any(not isinstance(path, str) or not path.startswith("artifacts/redacted/") for path in evidence_paths):
            errors.append(f"{row_id}: evidence_paths must use artifacts/redacted/")
            continue
        if not cleanup_proof:
            errors.append(f"{row_id}: cleanup_proof is required")
            continue
        if not redaction:
            errors.append(f"{row_id}: redaction is required")
            continue
        if not notes:
            errors.append(f"{row_id}: notes are required")
            continue

        ready_rows.append(row_id)

    missing_rows = tuple(sorted(set(blockers_by_id) - seen))
    return LintResult(
        ok=not errors and not missing_rows,
        total_required=len(blockers_by_id),
        ready_rows=tuple(sorted(ready_rows)),
        missing_rows=missing_rows,
        errors=tuple(errors),
    )


def run_text(result: LintResult) -> str:
    lines = [
        "zh-Hans public-RC evidence lint",
        f"total_required: {result.total_required}",
        f"ready_rows: {len(result.ready_rows)}",
        f"missing_rows: {len(result.missing_rows)}",
        f"errors: {len(result.errors)}",
    ]
    for row_id in result.ready_rows:
        lines.append(f"ready: {row_id}")
    for row_id in result.missing_rows:
        lines.append(f"missing: {row_id}")
    for error in result.errors:
        lines.append(f"error: {error}")
    lines.append(f"decision: {'pass' if result.ok else 'fail'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint zh-Hans public-RC evidence intake metadata.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    args = parser.parse_args(argv)

    result = lint_evidence(load_toml(args.blockers), load_toml(args.evidence))
    print(run_text(result))
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Create current empty evidence ledger**

Create `resources/localization/zh-Hans-public-rc-evidence.toml`:

```toml
# zh-Hans public-RC evidence intake ledger.
# This file stores only redacted, committable metadata. Raw screenshots,
# recordings, account identifiers, callback URLs, cookies, tokens, endpoint
# URLs, team IDs, and private object names must stay outside the repository.

generated_on = "2026-06-02"

[[evidence]]
row_id = "GUI-AUTH-01"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "isolated account evidence not provided"

[[evidence]]
row_id = "GUI-SET-03"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "isolated AI settings evidence not provided"

[[evidence]]
row_id = "GUI-SET-04"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "backend AWS/Bedrock fixture evidence not provided"

[[evidence]]
row_id = "GUI-SET-05"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "invalid Bedrock credential fixture evidence not provided"

[[evidence]]
row_id = "GUI-SET-06"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "disposable environment evidence not provided"

[[evidence]]
row_id = "GUI-WS-04"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "disposable managed secret evidence not provided"

[[evidence]]
row_id = "GUI-WS-06"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "isolated custom inference endpoint evidence not provided"

[[evidence]]
row_id = "GUI-WS-07"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "disposable team ownership evidence not provided"

[[evidence]]
row_id = "GUI-BILL-01"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "safe quota or billing fixture evidence not provided"

[[evidence]]
row_id = "GUI-BILL-02"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "Build plan migration fixture evidence not provided"

[[evidence]]
row_id = "GUI-CLOUD-01"
status = "missing"
evidence_paths = []
cleanup_proof = ""
redaction = ""
notes = "cloud capacity fixture evidence not provided"
```

- [ ] **Step 5: Verify linter behavior**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
python3 script/zh_public_rc_evidence_lint.py
```

Expected:

```text
unit tests pass
default linter exits 1
default linter reports total_required: 11
default linter reports missing_rows: 0
default linter reports errors: 11
default linter reports decision: fail
```

- [ ] **Step 6: Write Phase 229 record**

Create `docs/zh-Hans-localization-phase229.md`:

```markdown
# zh-Hans Localization Phase 229

Date: 2026-06-02

## Scope

Phase 229 adds structured public-RC evidence intake linting.

This phase does not clear any public-RC blocker because no matching external
evidence is present. It does not stage, commit, push, merge, rebase, mutate
tags, run Rust compile, build a bundle, launch GUI, use accounts, create
backend fixtures, touch billing/cloud state, or modify PNG assets.

## Added

```text
script/zh_public_rc_evidence_lint.py
script/test_zh_public_rc_evidence_lint.py
resources/localization/zh-Hans-public-rc-evidence.toml
```

## Findings

```text
evidence rows tracked: 11
ready rows: 0
errors: 11 missing evidence rows
blockers cleared: 0
```

## Qualification Review

```text
phase: 229
status: qualified-evidence-intake-linter
safe to continue to Phase 230: yes
```
```

- [ ] **Step 7: Verify Task 2**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
all commands exit 0
```

### Task 3: Phase 230 Evidence-Intake Documentation

**Files:**
- Create: `docs/zh-Hans-public-rc-evidence-intake-rc32.md`
- Create: `docs/zh-Hans-localization-phase230.md`
- Modify: `docs/zh-Hans-public-rc-action-package-rc31.md`

- [ ] **Step 1: Create evidence-intake documentation**

Create `docs/zh-Hans-public-rc-evidence-intake-rc32.md`:

```markdown
# zh-Hans Public-RC Evidence Intake RC32

Date: 2026-06-02

## Purpose

This document defines committable metadata for public-RC evidence. It does not
authorize using the user's main account, entering real credentials, buying
credits, consuming quota, creating production cloud objects, deleting production
objects, or committing raw screenshots.

## Ledger

```text
resources/localization/zh-Hans-public-rc-evidence.toml
```

## Linter

```bash
python3 script/zh_public_rc_evidence_lint.py
```

## Evidence Row Schema

```toml
[[evidence]]
row_id = "GUI-SET-05"
status = "provided"
evidence_paths = ["artifacts/redacted/gui-set-05.txt"]
cleanup_proof = "fixture reset proof captured"
redaction = "email, token, key, endpoint url, team id, and account identifiers removed"
notes = "uses zh-smoke-invalid-token only"
```

## Committable Metadata Rules

```text
row_id must match resources/localization/zh-Hans-public-rc-blockers.toml
status must be provided before a row can be promoted
evidence_paths must point under artifacts/redacted/
cleanup_proof must describe reset or cleanup proof
redaction must list removed sensitive fields
notes must not contain email addresses, URLs, tokens, cookies, API keys, secrets, endpoint URLs, team IDs, or account identifiers
```

## Public-RC Promotion Boundary

Rows remain blocked until the linter passes and the matching human evidence is
reviewed. Linter success proves metadata completeness only; it does not prove
that raw evidence is safe, true, or visually adequate.
```

- [ ] **Step 2: Link intake docs from the RC31 action package**

Add this section to `docs/zh-Hans-public-rc-action-package-rc31.md`:

```markdown
## RC32 Evidence Intake

Before changing any blocker status, record committable metadata in
`resources/localization/zh-Hans-public-rc-evidence.toml` and run:

```bash
python3 script/zh_public_rc_evidence_lint.py
```

The linter must pass, and the raw evidence must still be manually reviewed for
redaction and row match before a public-RC blocker can be cleared.
```

- [ ] **Step 3: Write Phase 230 record**

Create `docs/zh-Hans-localization-phase230.md`:

```markdown
# zh-Hans Localization Phase 230

Date: 2026-06-02

## Scope

Phase 230 documents the structured evidence-intake workflow for RC32.

This phase does not clear blockers, run GUI, create fixtures, use accounts,
modify PNG assets, or mutate Git refs.

## Added

```text
docs/zh-Hans-public-rc-evidence-intake-rc32.md
```

## Decision

```text
evidence promotion requires linter pass: yes
manual raw-evidence review still required: yes
blockers cleared in this phase: 0
```

## Qualification Review

```text
phase: 230
status: qualified-evidence-intake-docs
safe to continue to Phase 231: yes
```
```

- [ ] **Step 4: Verify Task 3**

Run:

```bash
python3 script/zh_public_rc_evidence_lint.py; code=$?; printf 'exit_code=%s\n' "$code"; test "$code" -eq 1
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
linter exits 1 because no evidence is provided
privacy guard exits 0
git diff --check exits 0
```

### Task 4: Phase 231 Backend Fixture Lane

**Files:**
- Create: `docs/zh-Hans-localization-phase231.md`
- Modify: `docs/zh-Hans-backend-fixture-contract-rc19.md`

- [ ] **Step 1: Run backend fixture classification**

Run:

```bash
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py; code=$?; printf 'exit_code=%s\n' "$code"; test "$code" -eq 1
```

Expected:

```text
blocked-no-backend-fixture: 5
ready backend fixture rows: 0 unless external evidence has been added and linted
```

- [ ] **Step 2: Add RC32 backend fixture intake note**

Append to `docs/zh-Hans-backend-fixture-contract-rc19.md`:

```markdown
## RC32 Evidence Intake Gate

Before any backend fixture row can be promoted, `resources/localization/zh-Hans-public-rc-evidence.toml`
must contain a `status = "provided"` row for the matching blocker, the row must
pass `python3 script/zh_public_rc_evidence_lint.py`, and the raw fixture evidence
must still be reviewed for redaction, row match, and cleanup proof.

Rows still requiring backend fixture evidence:

```text
GUI-SET-04
GUI-SET-05
GUI-BILL-01
GUI-BILL-02
GUI-CLOUD-01
```
```

- [ ] **Step 3: Write Phase 231 record**

Create `docs/zh-Hans-localization-phase231.md`:

```markdown
# zh-Hans Localization Phase 231

Date: 2026-06-02

## Scope

Phase 231 classifies backend fixture readiness through the RC32 evidence-intake
ledger and linter.

This phase does not contact backend services, enter credentials, purchase
credits, consume quota, mutate cloud state, or clear rows without matching
evidence.

## Findings

```text
backend fixture blocker rows: 5
rows promoted from evidence ledger: 0 unless linter passed with provided rows
production backend mutation: none
```

## Qualification Review

```text
phase: 231
status: qualified-backend-fixture-lane-classification
safe to continue to Phase 232: yes
```
```

- [ ] **Step 4: Verify Task 4**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 5: Phase 232 Account And Disposable Object Lanes

**Files:**
- Create: `docs/zh-Hans-localization-phase232.md`
- Modify: `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`

- [ ] **Step 1: Run account/object classification**

Run:

```bash
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py; code=$?; printf 'exit_code=%s\n' "$code"; test "$code" -eq 1
```

Expected:

```text
blocked-no-isolated-account: 3
blocked-no-disposable-object: 3
ready account/object rows: 0 unless external evidence has been added and linted
```

- [ ] **Step 2: Add RC32 isolated-account intake note**

Append to `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`:

```markdown
## RC32 Evidence Intake Gate

Before any isolated-account row can be promoted, `resources/localization/zh-Hans-public-rc-evidence.toml`
must contain a `status = "provided"` row for the matching blocker, the row must
pass `python3 script/zh_public_rc_evidence_lint.py`, and the raw evidence must
still be reviewed for redaction, row match, and cleanup proof.

Rows still requiring isolated-account evidence:

```text
GUI-AUTH-01
GUI-SET-03
GUI-WS-06
```

Disposable-object rows must additionally prove that only the exact allowlisted
object names were used:

```text
GUI-SET-06: zh-smoke-delete-environment
GUI-WS-04: zh-smoke-delete-secret
GUI-WS-07: zh-smoke-public-rc-team
```
```

- [ ] **Step 3: Write Phase 232 record**

Create `docs/zh-Hans-localization-phase232.md`:

```markdown
# zh-Hans Localization Phase 232

Date: 2026-06-02

## Scope

Phase 232 classifies isolated-account and disposable-object readiness through
the RC32 evidence-intake ledger and linter.

This phase does not log in, use the user's main account, create or delete
endpoints, create or delete managed secrets, transfer team ownership, or clear
rows without matching evidence.

## Findings

```text
isolated-account blocker rows: 3
disposable-object blocker rows: 3
rows promoted from evidence ledger: 0 unless linter passed with provided rows
account/object mutation: none
```

## Qualification Review

```text
phase: 232
status: qualified-account-object-lane-classification
safe to continue to Phase 233: yes
```
```

- [ ] **Step 4: Verify Task 5**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 6: Phase 233 Onboarding Asset Approval Preflight

**Files:**
- Create: `docs/zh-Hans-localization-phase233.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Check PNG scope**

Run:

```bash
git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
```

Expected:

```text
no output unless the user explicitly approved an asset-only branch
```

- [ ] **Step 2: Write Phase 233 record**

Create `docs/zh-Hans-localization-phase233.md`:

```markdown
# zh-Hans Localization Phase 233

Date: 2026-06-02

## Scope

Phase 233 checks whether onboarding PNG regeneration is authorized.

This phase does not generate, edit, upload, replace, or commit PNG assets.

## Findings

```text
onboarding PNG total: 54
deferred asset count: 50
accepted decorative/brand asset count: 4
asset-only branch approval available in this phase: no unless explicitly provided by user
PNG changes in this phase: none
```

## Decision

```text
asset regeneration: blocked-no-asset-approval
future asset-only branch required: yes
```

## Qualification Review

```text
phase: 233
status: qualified-asset-approval-preflight
safe to continue to Phase 234: yes
```
```

- [ ] **Step 3: Update GUI smoke matrix**

Add a Phase 233 note to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## Phase 233 Asset Preflight

Phase 233 confirmed that onboarding PNG regeneration remains blocked unless the
user explicitly approves an asset-only branch. No PNG files were modified.
```

- [ ] **Step 4: Verify Task 6**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 7: Phase 234 Heat-Gated Heavy Validation Retry

**Files:**
- Create: `docs/zh-Hans-localization-phase234.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Run the low-load gate**

Run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Expected:

```text
decision is either run-heavy-gate or defer-heavy-gate
```

- [ ] **Step 2: If the decision is defer-heavy-gate, skip heavy commands**

When the gate prints `decision: defer-heavy-gate`, do not run Cargo, bundle, or
GUI. Record the exact reasons in `docs/zh-Hans-localization-phase234.md`.

- [ ] **Step 3: If the decision is run-heavy-gate, run heavy commands serially**

Run only when Step 1 printed `decision: run-heavy-gate`:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
cargo check exits 0
script/run exits 0 or produces a diagnosable bundle failure
commands are run serially
no repeated retries in the same phase
```

- [ ] **Step 4: Write Phase 234 record**

Create `docs/zh-Hans-localization-phase234.md` with the branch that matches the actual gate decision:

```markdown
# zh-Hans Localization Phase 234

Date: 2026-06-02

## Scope

Phase 234 retries heavy validation through `script/zh_low_load_gate.py`.

This phase does not use accounts, create backend fixtures, touch billing/cloud
state, modify PNG assets, stage, commit, push, merge, rebase, or mutate tags.

## Low-Load Gate

```text
decision: defer-heavy-gate
reason: record exact helper reasons here
```

## Heavy Validation

```text
Rust compile: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
bundle build: skipped-with-heat-safety
```

## Qualification Review

```text
phase: 234
status: qualified-heavy-gate-decision
safe to continue to Phase 235: yes
```
```

If the helper allows heavy validation and the heavy commands pass, replace the
`Heavy Validation` block with:

```text
Rust compile: passed
fresh bundle: passed
bundle build: passed
```

- [ ] **Step 5: Update GUI smoke matrix**

Add a Phase 234 note to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## Phase 234 Heavy Gate

Phase 234 retried heavy validation through `script/zh_low_load_gate.py`.
GUI launch is allowed only if this phase produced a fresh bundle.
```

- [ ] **Step 6: Verify Task 7**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 8: Phase 235 RC32 Freeze

**Files:**
- Create: `docs/zh-Hans-localization-phase235.md`
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc32.md`
- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Run final low-load validation suite**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py; lint_code=$?; printf 'evidence_lint_exit_code=%s\n' "$lint_code"; test "$lint_code" -eq 1
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py
cargo fmt --check
git diff --check
```

Expected:

```text
manifest validation passes
glossary check passes
dry-run reports would_change: 0 and missing: 0
release inventory remains 100.0% covered
public-RC blocker status remains explicit
evidence linter exits 1 unless external evidence has been provided
privacy guard passes
Python tests pass
cargo fmt --check passes
git diff --check passes
```

- [ ] **Step 2: Write RC32 release-candidate record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc32.md`:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC32

Date: 2026-06-02

## Scope

RC32 covers Phases 228 through 235. It adds structured public-RC evidence
intake linting, documents evidence metadata rules, reclassifies backend,
isolated-account, disposable-object, asset, heavy validation, and GUI readiness,
and freezes the next local-use/public-RC decision.

RC32 does not add manifest translations, change PNG assets, produce GUI
evidence unless Phase 234 produced a fresh bundle, log in, create backend
fixtures, touch billing/cloud state, create or delete managed secrets/endpoints,
mutate team state, mutate Git refs, stage, commit, push, merge, or rebase.

## Evidence Intake

```text
evidence ledger: resources/localization/zh-Hans-public-rc-evidence.toml
evidence linter: script/zh_public_rc_evidence_lint.py
public-RC rows tracked: 11
rows promoted in RC32: 0 unless linter passed with provided evidence rows
```

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
would_change: 0
missing: 0
release coverage: 100.0%
```

## Public-RC Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC32 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until the evidence linter passes with real
matching evidence, the raw evidence is reviewed, fresh bundle/current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
```

- [ ] **Step 3: Write Phase 235 record**

Create `docs/zh-Hans-localization-phase235.md`:

```markdown
# zh-Hans Localization Phase 235

Date: 2026-06-02

## Scope

Phase 235 runs the final RC32 low-load validation suite and writes the RC32
release-candidate record.

This phase does not stage, commit, push, merge, rebase, mutate tags, use
accounts, create backend fixtures, touch billing/cloud state, or modify PNG
assets.

## Validation

```text
manifest validation: passed
dry-run summary: would_change 0, missing 0
release coverage: 100.0%
privacy guard: passed
Python tests: passed
cargo fmt --check: passed
git diff --check: passed
```

## Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready unless all evidence gates passed with real inputs
```

## Qualification Review

```text
phase: 235
status: qualified-rc32-freeze
safe to continue beyond RC32: yes, but public RC remains evidence-gated
```
```

- [ ] **Step 4: Update README and localization index**

In `README.md`, update:

```text
最后核验记录：2026-06-02 RC32
当前版本 remains 0.15 unless the user explicitly requests a version bump
public RC remains blocked unless evidence gates passed with real inputs
```

In `docs/zh-Hans-localization.md`, add:

```markdown
- RC32 decision: `ready-for-local-use-with-fixture-evidence`; public RC remains evidence-gated. RC32 adds structured public-RC evidence intake linting, evidence metadata docs, lane reclassification, and a heat-gated heavy validation retry.
```

- [ ] **Step 5: Verify Task 8**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
git diff --check
git status --short --branch
```

Expected:

```text
manifest validation passes
dry-run reports would_change: 0 and missing: 0
public-RC blocker status remains explicit
privacy guard passes
evidence linter unit tests pass
git diff --check exits 0
git status shows only planned files and pre-existing evidence branch changes
```

## Acceptance Criteria

- `script/zh_public_rc_evidence_lint.py` exists and rejects missing, unknown, duplicate, incomplete, or sensitive-looking evidence metadata.
- `resources/localization/zh-Hans-public-rc-evidence.toml` tracks all 11 public-RC rows without claiming evidence that is not present.
- Public-RC blocker status is not promoted unless structured evidence metadata passes lint and raw evidence has been reviewed.
- Heavy Rust/bundle/GUI commands are attempted only after `script/zh_low_load_gate.py` prints `decision: run-heavy-gate`.
- No PNG asset is modified unless the user explicitly approves an asset-only branch.
- Final RC32 docs clearly distinguish local engineering readiness from public-RC readiness.
- `python3 script/privacy_guard.py --all-tracked` and `git diff --check` pass.
- No stage, commit, push, merge, rebase, or tag mutation happens without explicit user approval.

## Risks And Mitigations

- Risk: Evidence metadata gives false confidence while raw screenshots still contain sensitive data.
  Mitigation: Linter success is metadata-only; RC32 docs require separate raw-evidence review before status promotion.
- Risk: The linter blocks valid evidence because the schema is too strict.
  Mitigation: Keep the schema small and explicit: row ID, status, redacted paths, cleanup proof, redaction statement, notes.
- Risk: Heavy validation overheats the Mac.
  Mitigation: Keep the low-load gate mandatory, run heavy commands serially, and record defer decisions as qualified skips.
- Risk: Asset generation contaminates the evidence branch.
  Mitigation: Keep PNG generation blocked unless an asset-only branch is explicitly approved.
- Risk: Publication pressure causes premature Git mutation.
  Mitigation: RC32 keeps publication as a separate, explicitly approved workflow.

## Verification Summary

Run at the end of the plan:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py
cargo fmt --check
git diff --check
```

Expected:

```text
all commands exit 0 except script/zh_public_rc_evidence_lint.py when no external evidence is present
dry-run remains would_change: 0 and missing: 0
public-RC readiness remains blocked unless every row has real matching evidence
```

## Self-Review

```text
Spec coverage: current RC31 blockers, evidence intake, heat safety, asset gate, GUI gate, and publication boundary are covered.
Placeholder scan: no banned planning markers are used.
Type consistency: script, TOML, docs, phase numbers, and row IDs use consistent names across tasks.
Execution boundary: plan is executable without external evidence by recording blocked rows honestly; it cannot fake public-RC promotion.
```
