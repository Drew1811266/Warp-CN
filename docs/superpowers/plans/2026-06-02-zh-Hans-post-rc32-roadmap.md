# zh-Hans Post-RC32 Evidence Packet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC32 evidence-intake linting toward RC33 by adding public-RC evidence reports, safe packet templates, optional redacted-artifact checks, lane-readiness packaging, and another heat-gated heavy validation decision.

**Architecture:** Keep source translations and PNG assets unchanged. Build on `script/zh_public_rc_evidence_lint.py` by adding a read-only report/template helper plus optional strict artifact checks, then document the next evidence handoff in phase records without using accounts, backend fixtures, or GUI unless the low-load gate allows it.

**Tech Stack:** Python `unittest`, existing small TOML parser in `script/zh_public_rc_evidence_lint.py`, Git, Markdown evidence records, existing zh-Hans validation scripts, macOS low-load gate.

---

## Current Baseline

RC32 status:

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
evidence linter: expected fail, exit_code 1, errors 11
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
1. Make the empty evidence ledger actionable by generating per-row report output and safe packet templates.
2. Add an optional strict-artifact scan so future redacted text artifacts can be checked before a row is considered ready.
3. Keep all current rows blocked until real matching external evidence is provided and reviewed.
4. Keep heavy Rust/bundle/GUI commands behind script/zh_low_load_gate.py.
5. Keep Git publication separate from evidence completion; do not stage, commit, push, merge, rebase, or tag without explicit user approval.
```

## File Structure

- Create `script/zh_public_rc_evidence_report.py` for row/category summaries and safe packet template rendering.
- Create `script/test_zh_public_rc_evidence_report.py` for report and template tests.
- Modify `script/zh_public_rc_evidence_lint.py` to support optional `--strict-artifacts` checks for future redacted text artifact references.
- Modify `script/test_zh_public_rc_evidence_lint.py` with strict-artifact tests.
- Create `docs/zh-Hans-public-rc-evidence-packet-template-rc33.md` to document the generated packet format.
- Create `docs/zh-Hans-public-rc-lane-readiness-rc33.md` to summarize backend, isolated-account, disposable-object, asset, heavy-build, and GUI lanes.
- Create `docs/zh-Hans-localization-phase236.md` through `docs/zh-Hans-localization-phase243.md`.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc33.md` only during Phase 243.
- Modify `README.md` only during Phase 243 for RC33 status and the new report helper.
- Modify `docs/zh-Hans-localization.md` during Phase 236 and Phase 243.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` when asset/heavy/GUI status changes.
- Do not modify `resources/localization/zh-Hans-overrides.toml` unless a phase finds real manifest/source drift.
- Do not modify `app/assets/async/png/onboarding/**/*.png` unless the user explicitly approves an asset-only branch.
- Do not create real evidence artifacts under `artifacts/redacted/` without user-provided evidence and explicit approval.
- Do not stage, commit, push, merge, rebase, or mutate tags unless the user explicitly asks for publication or integration.

## Phase Map

| Phase | Purpose | Qualification Gate |
| --- | --- | --- |
| 236 | Post-RC32 baseline and report scope lock | diff/privacy checks pass; current 11 blockers confirmed |
| 237 | Evidence report/template helper | unit tests pass; report shows 11 missing rows and 0 ready rows |
| 238 | Optional strict-artifact linting | linter tests pass; missing or sensitive future artifacts are rejected |
| 239 | Evidence packet template docs | docs match helper output and redaction rules |
| 240 | Lane-readiness package | backend/account/object/asset/heavy/GUI lanes remain honest |
| 241 | Asset and GUI dependency recheck | no PNG mutation; GUI remains gated by fresh bundle |
| 242 | Low-load heavy validation retry | run heavy commands only after `decision: run-heavy-gate`; otherwise record defer |
| 243 | RC33 freeze and publication boundary | validation passes; RC33 decision is explicit and honest |

### Task 1: Phase 236 Post-RC32 Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase236.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect the current branch and evidence state**

Run:

```bash
git status --short --branch
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py; code=$?; printf 'evidence_lint_exit_code=%s\n' "$code"; test "$code" -eq 1
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
branch remains codex/zh-Hans-post-rc26-execution
dry-run reports would_change: 0 and missing: 0
public-RC blocker total remains 11
evidence linter reports ready_rows: 0, errors: 11, decision: fail
privacy_guard.py exits 0
git diff --check exits 0
```

- [ ] **Step 2: Write Phase 236 record**

Create `docs/zh-Hans-localization-phase236.md`:

```markdown
# zh-Hans Localization Phase 236

Date: 2026-06-02

## Scope

Phase 236 audits the post-RC32 branch before adding evidence report and packet
helpers.

This phase does not stage, commit, push, merge, rebase, create a worktree,
mutate tags, run Rust compile, build a bundle, launch GUI, use accounts,
create backend fixtures, touch billing/cloud state, create evidence artifacts,
or modify PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
dry-run: would_change 0, missing 0
public-RC blockers: 11
evidence ready rows: 0
evidence errors: 11 missing evidence rows
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-evidence-report-helper
status promotion without matching evidence: forbidden
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 236
status: qualified-post-rc32-baseline
safe to continue to Phase 237: yes
```
```

- [ ] **Step 3: Update localization index**

In `docs/zh-Hans-localization.md`, add after the RC32 status bullet:

```markdown
- Phase 236 records the post-RC32 baseline before adding evidence report and packet helpers.
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

### Task 2: Phase 237 Evidence Report And Packet Template Helper

**Files:**
- Create: `script/zh_public_rc_evidence_report.py`
- Create: `script/test_zh_public_rc_evidence_report.py`
- Create: `docs/zh-Hans-localization-phase237.md`

- [ ] **Step 1: Create failing tests**

Create `script/test_zh_public_rc_evidence_report.py`:

```python
#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_lint import load_toml
from zh_public_rc_evidence_report import build_report, render_templates, render_text


class PublicRcEvidenceReportTests(unittest.TestCase):
    def test_current_empty_ledger_summary(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        report = build_report(blockers, evidence)

        self.assertEqual(report.total_required, 11)
        self.assertEqual(report.ready_rows, ())
        self.assertEqual(report.status_counts["missing"], 11)
        self.assertEqual(report.category_counts["backend_fixture"], 5)
        self.assertEqual(report.category_counts["disposable_object"], 3)
        self.assertEqual(report.category_counts["isolated_account"], 3)

    def test_text_report_contains_lane_counts(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        text = render_text(build_report(blockers, evidence))

        self.assertIn("backend_fixture: total=5 ready=0 missing=5", text)
        self.assertIn("disposable_object: total=3 ready=0 missing=3", text)
        self.assertIn("isolated_account: total=3 ready=0 missing=3", text)
        self.assertIn("decision: blocked", text)

    def test_template_output_uses_redacted_paths(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))

        templates = render_templates(blockers)

        self.assertIn('row_id = "GUI-SET-05"', templates)
        self.assertIn('evidence_paths = ["artifacts/redacted/gui-set-05.txt"]', templates)
        self.assertNotIn("@", templates)
        self.assertNotIn("https://", templates)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and confirm they fail**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
```

Expected:

```text
fails with ModuleNotFoundError or missing zh_public_rc_evidence_report symbols
```

- [ ] **Step 3: Create report helper**

Create `script/zh_public_rc_evidence_report.py`:

```python
#!/usr/bin/env python3
"""Render zh-Hans public-RC evidence readiness reports and safe packet templates."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import sys
from pathlib import Path
from typing import Any

from zh_public_rc_evidence_lint import DEFAULT_BLOCKERS, DEFAULT_EVIDENCE, blocker_index, load_toml


@dataclasses.dataclass(frozen=True)
class ReportRow:
    row_id: str
    category: str
    status: str
    ready: bool


@dataclasses.dataclass(frozen=True)
class EvidenceReport:
    total_required: int
    ready_rows: tuple[str, ...]
    status_counts: dict[str, int]
    category_counts: dict[str, int]
    category_ready_counts: dict[str, int]
    rows: tuple[ReportRow, ...]


def evidence_by_id(evidence_doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in evidence_doc.get("evidence", []):
        if isinstance(row, dict) and row.get("row_id"):
            rows[str(row["row_id"])] = row
    return rows


def build_report(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> EvidenceReport:
    blockers_by_id = blocker_index(blockers)
    evidence = evidence_by_id(evidence_doc)
    rows: list[ReportRow] = []

    for row_id, blocker in sorted(blockers_by_id.items()):
        category = str(blocker["category"])
        evidence_row = evidence.get(row_id, {})
        status = str(evidence_row.get("status", "missing"))
        ready = status == "provided"
        rows.append(ReportRow(row_id=row_id, category=category, status=status, ready=ready))

    status_counts = collections.Counter(row.status for row in rows)
    category_counts = collections.Counter(row.category for row in rows)
    category_ready_counts = collections.Counter(row.category for row in rows if row.ready)

    return EvidenceReport(
        total_required=len(rows),
        ready_rows=tuple(row.row_id for row in rows if row.ready),
        status_counts=dict(sorted(status_counts.items())),
        category_counts=dict(sorted(category_counts.items())),
        category_ready_counts=dict(sorted(category_ready_counts.items())),
        rows=tuple(rows),
    )


def render_text(report: EvidenceReport) -> str:
    lines = [
        "zh-Hans public-RC evidence report",
        f"total_required: {report.total_required}",
        f"ready_rows: {len(report.ready_rows)}",
        "categories:",
    ]
    for category, total in report.category_counts.items():
        ready = report.category_ready_counts.get(category, 0)
        missing = total - ready
        lines.append(f"  {category}: total={total} ready={ready} missing={missing}")
    lines.append("rows:")
    for row in report.rows:
        state = "ready" if row.ready else "missing"
        lines.append(f"  {row.row_id}: {row.category} {state}")
    lines.append(f"decision: {'ready' if len(report.ready_rows) == report.total_required else 'blocked'}")
    return "\n".join(lines)


def redacted_path(row_id: str) -> str:
    return f"artifacts/redacted/{row_id.lower()}.txt"


def render_templates(blockers: dict[str, Any]) -> str:
    lines = [
        "# Copy one block into resources/localization/zh-Hans-public-rc-evidence.toml only after redacted evidence exists.",
        "# Keep raw screenshots, recordings, tokens, callback URLs, account identifiers, and private team names outside Git.",
    ]
    for row_id, blocker in sorted(blocker_index(blockers).items()):
        lines.extend(
            [
                "",
                "[[evidence]]",
                f'row_id = "{row_id}"',
                'status = "provided"',
                f'evidence_paths = ["{redacted_path(row_id)}"]',
                'cleanup_proof = "redacted cleanup proof reviewed"',
                'redaction = "email, token, key, callback url, endpoint url, team id, account id, and private identifiers removed"',
                f'notes = "{blocker["category"]} evidence packet reviewed against {row_id}"',
            ]
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render zh-Hans public-RC evidence readiness output.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--templates", action="store_true", help="Print safe evidence TOML packet templates")
    args = parser.parse_args(argv)

    blockers = load_toml(args.blockers)
    if args.templates:
        print(render_templates(blockers), end="")
        return 0

    evidence = load_toml(args.evidence)
    print(render_text(build_report(blockers, evidence)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Verify report helper**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --templates | sed -n '1,80p'
```

Expected:

```text
unit tests pass
report shows total_required: 11 and ready_rows: 0
report shows backend_fixture total=5 ready=0 missing=5
template output contains only artifacts/redacted/*.txt paths and no raw identifiers
```

- [ ] **Step 5: Write Phase 237 record**

Create `docs/zh-Hans-localization-phase237.md`:

```markdown
# zh-Hans Localization Phase 237

Date: 2026-06-02

## Scope

Phase 237 adds a read-only public-RC evidence report and safe packet template helper.

This phase does not create real evidence artifacts, clear blockers, run GUI,
use accounts, create backend fixtures, touch billing/cloud state, modify PNG
assets, or mutate Git refs.

## Added

```text
script/zh_public_rc_evidence_report.py
script/test_zh_public_rc_evidence_report.py
```

## Findings

```text
total required evidence rows: 11
ready evidence rows: 0
backend_fixture: total=5 ready=0 missing=5
disposable_object: total=3 ready=0 missing=3
isolated_account: total=3 ready=0 missing=3
blockers cleared: 0
```

## Qualification Review

```text
phase: 237
status: qualified-evidence-report-helper
safe to continue to Phase 238: yes
```
```

- [ ] **Step 6: Verify Task 2**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_report.py
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
all commands exit 0
```

### Task 3: Phase 238 Optional Strict Artifact Lint

**Files:**
- Modify: `script/zh_public_rc_evidence_lint.py`
- Modify: `script/test_zh_public_rc_evidence_lint.py`
- Create: `docs/zh-Hans-localization-phase238.md`

- [ ] **Step 1: Add strict-artifact tests**

Append these tests to `script/test_zh_public_rc_evidence_lint.py` inside `PublicRcEvidenceLintTests`:

```python
    def test_strict_artifacts_rejects_missing_referenced_path(self) -> None:
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

        result = lint_evidence(blockers, evidence, strict_artifacts=True, repo_root=Path("/tmp/nonexistent-warp-cn"))

        self.assertFalse(result.ok)
        self.assertIn("GUI-SET-05: referenced artifact does not exist: artifacts/redacted/gui-set-05.txt", result.errors)

    def test_strict_artifacts_rejects_sensitive_artifact_text(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            artifact = Path(root) / "artifacts/redacted/gui-set-05.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("email person@example.com leaked\n", encoding="utf-8")
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

        self.assertFalse(result.ok)
        self.assertIn("GUI-SET-05: sensitive-looking text in artifact artifacts/redacted/gui-set-05.txt", result.errors)
```

- [ ] **Step 2: Run tests and confirm they fail**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
```

Expected:

```text
fails because lint_evidence does not yet accept strict_artifacts or repo_root
```

- [ ] **Step 3: Add strict-artifact support**

Modify `script/zh_public_rc_evidence_lint.py`:

```python
TEXT_ARTIFACT_SUFFIXES = (".txt", ".md")


def strict_artifact_errors(row_id: str, evidence_paths: object, repo_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(evidence_paths, list):
        return errors
    for artifact_path in evidence_paths:
        if not isinstance(artifact_path, str):
            continue
        normalized = artifact_path.strip()
        full_path = repo_root / normalized
        if Path(normalized).suffix.lower() not in TEXT_ARTIFACT_SUFFIXES:
            errors.append(f"{row_id}: referenced artifact must be redacted text: {normalized}")
            continue
        if not full_path.exists():
            errors.append(f"{row_id}: referenced artifact does not exist: {normalized}")
            continue
        content = full_path.read_text(encoding="utf-8", errors="replace")
        if has_sensitive_metadata(content):
            errors.append(f"{row_id}: sensitive-looking text in artifact {normalized}")
    return errors
```

Change the `lint_evidence` signature:

```python
def lint_evidence(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    strict_artifacts: bool = False,
    repo_root: Path | None = None,
) -> LintResult:
```

Before adding a row to `ready_rows`, add:

```python
        if strict_artifacts:
            strict_errors = strict_artifact_errors(row_id, evidence_paths, repo_root or Path.cwd())
            if strict_errors:
                errors.extend(strict_errors)
                continue
```

In `main`, add:

```python
    parser.add_argument("--strict-artifacts", action="store_true", help="Check referenced artifacts exist and are redacted text")
```

And pass the option:

```python
        result = lint_evidence(
            load_toml(args.blockers),
            load_toml(args.evidence),
            strict_artifacts=args.strict_artifacts,
            repo_root=Path.cwd(),
        )
```

- [ ] **Step 4: Verify strict-artifact support**

Run:

```bash
python3 -m unittest script/test_zh_public_rc_evidence_lint.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts; code=$?; printf 'exit_code=%s\n' "$code"; test "$code" -eq 1
```

Expected:

```text
unit tests pass
default current ledger still exits 1 because all rows are missing evidence
strict-artifacts does not create or require artifacts for missing rows
```

- [ ] **Step 5: Write Phase 238 record**

Create `docs/zh-Hans-localization-phase238.md`:

```markdown
# zh-Hans Localization Phase 238

Date: 2026-06-02

## Scope

Phase 238 adds optional strict-artifact checks for future redacted public-RC
evidence references.

This phase does not create real artifacts, clear blockers, run GUI, use
accounts, create backend fixtures, touch billing/cloud state, modify PNG assets,
or mutate Git refs.

## Findings

```text
strict-artifacts support: added
missing artifact references rejected in tests: yes
sensitive artifact text rejected in tests: yes
current ledger ready rows: 0
current blockers cleared: 0
```

## Qualification Review

```text
phase: 238
status: qualified-strict-artifact-lint
safe to continue to Phase 239: yes
```
```

- [ ] **Step 6: Verify Task 3**

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

### Task 4: Phase 239 Evidence Packet Template Documentation

**Files:**
- Create: `docs/zh-Hans-public-rc-evidence-packet-template-rc33.md`
- Create: `docs/zh-Hans-localization-phase239.md`
- Modify: `README.md`

- [ ] **Step 1: Generate template preview**

Run:

```bash
python3 script/zh_public_rc_evidence_report.py --templates | sed -n '1,120p'
```

Expected:

```text
output contains [[evidence]] blocks
output uses artifacts/redacted/*.txt paths
output contains no email addresses, callback URLs, tokens, or endpoint URLs
```

- [ ] **Step 2: Create evidence packet template docs**

Create `docs/zh-Hans-public-rc-evidence-packet-template-rc33.md`:

```markdown
# zh-Hans Public-RC Evidence Packet Template RC33

Date: 2026-06-02

## Purpose

This document defines how future public-RC evidence packets should be prepared
before any blocker status is promoted.

## Generate Packet TOML

```bash
python3 script/zh_public_rc_evidence_report.py --templates
```

## Required Review Order

```text
1. Capture raw evidence outside the repository.
2. Redact account identifiers, callback URLs, cookies, tokens, API keys,
   endpoint URLs, team IDs, billing IDs, and private object names.
3. Convert the reviewed artifact to redacted text under artifacts/redacted/*.txt
   only after explicit approval.
4. Add the matching [[evidence]] block to resources/localization/zh-Hans-public-rc-evidence.toml.
5. Run python3 script/zh_public_rc_evidence_lint.py --strict-artifacts.
6. Manually review the raw evidence and the redacted artifact before changing
   any blocker status.
```

## Current Boundary

```text
ready rows: 0
blockers cleared by this document: 0
real evidence artifacts created by this document: none
```
```

- [ ] **Step 3: Add README helper row**

In `README.md`, add this row to the core file table:

```markdown
| `script/zh_public_rc_evidence_report.py` | 生成 public-RC 证据分类报表和安全 packet 模板 |
```

- [ ] **Step 4: Write Phase 239 record**

Create `docs/zh-Hans-localization-phase239.md`:

```markdown
# zh-Hans Localization Phase 239

Date: 2026-06-02

## Scope

Phase 239 documents the public-RC evidence packet template workflow.

This phase does not create real artifacts, clear blockers, run GUI, use
accounts, create backend fixtures, touch billing/cloud state, modify PNG assets,
or mutate Git refs.

## Findings

```text
template helper: script/zh_public_rc_evidence_report.py --templates
required path prefix: artifacts/redacted/
required artifact type: redacted text
blockers cleared: 0
```

## Qualification Review

```text
phase: 239
status: qualified-evidence-packet-template-docs
safe to continue to Phase 240: yes
```
```

- [ ] **Step 5: Verify Task 4**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 5: Phase 240 Lane-Readiness Package

**Files:**
- Create: `docs/zh-Hans-public-rc-lane-readiness-rc33.md`
- Create: `docs/zh-Hans-localization-phase240.md`

- [ ] **Step 1: Render evidence report**

Run:

```bash
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_status.py
```

Expected:

```text
evidence report shows ready_rows: 0
public-RC status still shows 11 blockers
```

- [ ] **Step 2: Create lane-readiness package**

Create `docs/zh-Hans-public-rc-lane-readiness-rc33.md`:

```markdown
# zh-Hans Public-RC Lane Readiness RC33

Date: 2026-06-02

## Current Lane Status

```text
backend_fixture: total=5 ready=0 missing=5
disposable_object: total=3 ready=0 missing=3
isolated_account: total=3 ready=0 missing=3
asset lane: blocked-no-asset-approval
heavy validation lane: blocked-by-low-load-gate
GUI lane: blocked-no-fresh-bundle
publication lane: blocked-no-explicit-approval
```

## Required External Inputs

```text
backend fixture lane: safe fixture owner, reset path, cleanup proof, redacted artifact
isolated account lane: non-main test account, callback proof, cleanup proof, redacted artifact
disposable object lane: exact allowlisted object existence, cancel path, cleanup proof, redacted artifact
asset lane: design/product approval for asset-only branch
heavy validation lane: script/zh_low_load_gate.py decision: run-heavy-gate
publication lane: explicit user request for stage/commit/push/tag
```

## Promotion Rule

No lane can promote a row unless the matching evidence row is `status = "provided"`,
`python3 script/zh_public_rc_evidence_lint.py --strict-artifacts` passes, and
raw evidence has been manually reviewed for safety and row match.
```

- [ ] **Step 3: Write Phase 240 record**

Create `docs/zh-Hans-localization-phase240.md`:

```markdown
# zh-Hans Localization Phase 240

Date: 2026-06-02

## Scope

Phase 240 creates the RC33 public-RC lane-readiness package.

This phase does not create real artifacts, clear blockers, run GUI, use
accounts, create backend fixtures, touch billing/cloud state, modify PNG assets,
or mutate Git refs.

## Findings

```text
backend_fixture: total=5 ready=0 missing=5
disposable_object: total=3 ready=0 missing=3
isolated_account: total=3 ready=0 missing=3
asset lane: blocked-no-asset-approval
heavy validation lane: blocked-by-low-load-gate
GUI lane: blocked-no-fresh-bundle
publication lane: blocked-no-explicit-approval
```

## Qualification Review

```text
phase: 240
status: qualified-lane-readiness-package
safe to continue to Phase 241: yes
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

### Task 6: Phase 241 Asset And GUI Dependency Recheck

**Files:**
- Create: `docs/zh-Hans-localization-phase241.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Check PNG and fresh-bundle dependency**

Run:

```bash
git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
rg -n "fresh bundle: passed|fresh bundle: skipped-with-heat-safety|fresh bundle: not run" docs/zh-Hans-localization-phase234.md docs/zh-Hans-release-candidate-2026-06-02-rc32.md
```

Expected:

```text
PNG commands produce no output
fresh bundle remains skipped-with-heat-safety or not run
```

- [ ] **Step 2: Write Phase 241 record**

Create `docs/zh-Hans-localization-phase241.md`:

```markdown
# zh-Hans Localization Phase 241

Date: 2026-06-02

## Scope

Phase 241 rechecks asset and GUI dependencies before another heavy-gate attempt.

This phase does not generate, edit, upload, replace, or commit PNG assets. It
does not launch GUI because no fresh bundle exists.

## Findings

```text
PNG changes in this phase: none
asset regeneration: blocked-no-asset-approval
fresh bundle dependency: not available
GUI smoke: skipped-no-fresh-bundle
```

## Qualification Review

```text
phase: 241
status: qualified-asset-gui-dependency-recheck
safe to continue to Phase 242: yes
```
```

- [ ] **Step 3: Update GUI smoke matrix**

Add this section to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## 2026-06-02 P241 asset and GUI dependency recheck

Phase 241 status: `qualified-asset-gui-dependency-recheck`.

- PNG status remained clean.
- Asset regeneration remains blocked without an explicitly approved asset-only branch.
- GUI smoke remains blocked because no current-cycle fresh bundle exists.
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

### Task 7: Phase 242 Heat-Gated Heavy Validation Retry

**Files:**
- Create: `docs/zh-Hans-localization-phase242.md`
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
GUI. Record the exact helper output in `docs/zh-Hans-localization-phase242.md`.

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

- [ ] **Step 4: Write Phase 242 record**

Create `docs/zh-Hans-localization-phase242.md` with the branch that matches the actual gate decision:

```markdown
# zh-Hans Localization Phase 242

Date: 2026-06-02

## Scope

Phase 242 retries heavy validation through `script/zh_low_load_gate.py`.

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
GUI launch: skipped-no-fresh-bundle
```

## Qualification Review

```text
phase: 242
status: qualified-heavy-gate-decision
safe to continue to Phase 243: yes
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

Add a Phase 242 note to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## 2026-06-02 P242 heavy gate

Phase 242 status: `qualified-heavy-gate-decision`.

- Phase 242 retried heavy validation through `script/zh_low_load_gate.py`.
- GUI launch is allowed only if this phase produced a fresh bundle.
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

### Task 8: Phase 243 RC33 Freeze

**Files:**
- Create: `docs/zh-Hans-localization-phase243.md`
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc33.md`
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
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts; lint_code=$?; printf 'evidence_lint_exit_code=%s\n' "$lint_code"; test "$lint_code" -eq 1
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py
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
evidence report shows ready_rows: 0
evidence linter exits 1 unless external evidence has been provided
privacy guard passes
Python tests pass
cargo fmt --check passes
git diff --check passes
```

- [ ] **Step 2: Write RC33 release-candidate record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc33.md`:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC33

Date: 2026-06-02

## Scope

RC33 covers Phases 236 through 243. It adds public-RC evidence report and packet
template helpers, optional strict-artifact linting, a lane-readiness package,
asset/GUI dependency recheck, heat-gated heavy validation retry, and the next
local-use/public-RC decision freeze.

RC33 does not add manifest translations, change PNG assets, produce GUI
evidence unless Phase 242 produced a fresh bundle, log in, create backend
fixtures, touch billing/cloud state, create or delete managed secrets/endpoints,
mutate team state, mutate Git refs, stage, commit, push, merge, or rebase.

## Evidence Packet Readiness

```text
evidence report: script/zh_public_rc_evidence_report.py
evidence linter strict mode: script/zh_public_rc_evidence_lint.py --strict-artifacts
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC33: 0
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC33 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, fresh bundle/current-cycle
GUI evidence exists, onboarding PNG visual status is approved or regenerated,
and publication is explicitly approved by the user.
```

- [ ] **Step 3: Write Phase 243 record**

Create `docs/zh-Hans-localization-phase243.md`:

```markdown
# zh-Hans Localization Phase 243

Date: 2026-06-02

## Scope

Phase 243 runs the final RC33 low-load validation suite and writes the RC33
release-candidate record.

This phase does not stage, commit, push, merge, rebase, mutate tags, use
accounts, create backend fixtures, touch billing/cloud state, create real
evidence artifacts, or modify PNG assets.

## Validation

```text
manifest validation: passed
dry-run summary: would_change 0, missing 0
release coverage: 100.0%
public-RC blocker summary: 11 blockers
evidence report: ready_rows 0
evidence linter strict mode: expected fail unless real evidence was provided
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
phase: 243
status: qualified-rc33-freeze
safe to continue beyond RC33: yes, but public RC remains evidence-gated
```
```

- [ ] **Step 4: Update README and localization index**

In `README.md`, update:

```text
最后核验记录：2026-06-02 RC33
当前版本 remains 0.15 unless the user explicitly requests a version bump
public RC remains blocked unless strict evidence gates pass with real inputs
```

In `docs/zh-Hans-localization.md`, add:

```markdown
- RC33 decision: `ready-for-local-use-with-fixture-evidence`; public RC remains evidence-gated. RC33 adds evidence report/template helpers, strict-artifact linting, lane-readiness packaging, asset/GUI dependency recheck, and heat-gated heavy validation retry.
```

- [ ] **Step 5: Verify Task 8**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py
git diff --check
git status --short --branch
```

Expected:

```text
manifest validation passes
dry-run reports would_change: 0 and missing: 0
public-RC blocker status remains explicit
evidence report shows ready_rows: 0 unless real evidence was provided
privacy guard passes
evidence linter and report unit tests pass
git diff --check exits 0
git status shows only planned files and pre-existing evidence branch changes
```

## Acceptance Criteria

- `script/zh_public_rc_evidence_report.py` exists and reports category counts, row readiness, and safe evidence packet templates.
- `script/zh_public_rc_evidence_lint.py --strict-artifacts` rejects missing future artifacts, non-text artifact types, and sensitive-looking redacted artifact text.
- No public-RC row is promoted unless matching evidence metadata and redacted artifact checks pass.
- No PNG asset is modified unless the user explicitly approves an asset-only branch.
- Heavy Rust/bundle/GUI commands are attempted only after `script/zh_low_load_gate.py` prints `decision: run-heavy-gate`.
- Final RC33 docs clearly distinguish local engineering readiness from public-RC readiness.
- `python3 script/privacy_guard.py --all-tracked` and `git diff --check` pass.
- No stage, commit, push, merge, rebase, or tag mutation happens without explicit user approval.

## Risks And Mitigations

- Risk: Generated packet templates are mistaken for real evidence.
  Mitigation: Templates print only safe `artifacts/redacted/*.txt` paths and docs state that blocker promotion still requires real reviewed evidence.
- Risk: Strict artifact scanning blocks rows because artifacts are intentionally absent.
  Mitigation: Strict mode only evaluates rows marked `status = "provided"`; current missing rows remain an honest blocker signal.
- Risk: Sensitive data appears inside a redacted text artifact.
  Mitigation: Strict mode rejects email addresses, URLs, token/key-looking strings, and secret/key labels.
- Risk: Heavy validation overheats the Mac.
  Mitigation: Keep the low-load gate mandatory, run heavy commands serially, and record defer decisions as qualified skips.
- Risk: Publication pressure causes premature Git mutation.
  Mitigation: RC33 keeps publication as a separate, explicitly approved workflow.

## Verification Summary

Run at the end of the plan:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py
cargo fmt --check
git diff --check
```

Expected:

```text
all commands exit 0 except strict evidence lint when no external evidence is present
dry-run remains would_change: 0 and missing: 0
public-RC readiness remains blocked unless every row has real matching evidence
```

## Self-Review

```text
Spec coverage: current RC32 blockers, evidence reports, packet templates, strict artifact checks, asset gate, heat safety, GUI gate, and publication boundary are covered.
Marker scan: no banned planning markers are used.
Type consistency: script, TOML, docs, phase numbers, and row IDs use consistent names across tasks.
Execution boundary: plan is executable without external evidence by recording blocked rows honestly; it cannot fake public-RC promotion.
```
