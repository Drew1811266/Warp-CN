# zh-Hans Post-RC35 Evidence Packetization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC35 to RC36 by making the 11 public-RC evidence blockers filterable, packetized, and safer to hand off without creating or approving real evidence.

**Architecture:** Keep `resources/localization/zh-Hans-public-rc-blockers.toml` and `resources/localization/zh-Hans-public-rc-evidence.toml` as the source of truth. Extend `script/zh_public_rc_evidence_report.py` with row/category filtering and Markdown action-packet output, while preserving the existing text and JSON report contracts. Keep real evidence, GUI launch, backend fixtures, and heavy validation behind explicit approval and `script/zh_low_load_gate.py`.

**Tech Stack:** Python `unittest`, JSON serialization, Markdown reports, existing small TOML parser, existing zh-Hans validation scripts, `nice` for lightweight checks, low-concurrency Rust gates only after the low-load helper allows them.

---

## Current Baseline

RC35 status:

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
report JSON: available
missing-action JSON: available
row-specific artifact path guard: enabled
fresh bundle: passed
GUI launch: not run
PNG changes: none
```

Next-cycle priority:

```text
1. Keep public-RC blocked until real reviewed evidence exists.
2. Add row/category filters to missing-action text and JSON output.
3. Add Markdown action-packet output for safe row-owner handoff.
4. Refresh runbooks so humans know how to request exactly one safe row at a time.
5. Reclassify RC36 lane readiness without promoting missing evidence.
6. Retry heavy validation only if script/zh_low_load_gate.py returns decision: run-heavy-gate.
7. Do not stage, commit, push, merge, rebase, tag, launch GUI, create accounts, create backend fixtures, or mutate external state unless explicitly approved.
```

## File Structure

- Modify `script/zh_public_rc_evidence_report.py` to add missing-action row/category filters and Markdown action-packet output.
- Modify `script/test_zh_public_rc_evidence_report.py` to cover row filtering, category filtering, empty filter results, and Markdown action-packet output.
- Create `docs/zh-Hans-public-rc-evidence-action-package-rc36.md` to document filtered command usage and safe handoff boundaries.
- Create `docs/zh-Hans-public-rc-lane-readiness-rc36.md` to record lane status after filtered packetization.
- Create `docs/zh-Hans-localization-phase260.md` through `docs/zh-Hans-localization-phase267.md`.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc36.md` only during Phase 267.
- Modify `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md` to point isolated-account operators to filtered RC36 packet commands.
- Modify `docs/zh-Hans-backend-fixture-contract-rc19.md` to point backend-fixture and disposable-object operators to filtered RC36 packet commands.
- Modify `docs/zh-Hans-localization.md` during Phase 260 and Phase 267.
- Modify `README.md` only during Phase 267 to point to RC36 and the filtered evidence-packet helper.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` only when heavy, GUI, or asset status changes.
- Do not modify `resources/localization/zh-Hans-public-rc-evidence.toml` unless reviewed redacted evidence is provided and explicit approval is given.
- Do not modify `resources/localization/zh-Hans-public-rc-blockers.toml` unless a blocker is genuinely cleared with reviewed evidence and explicit approval is given.
- Do not create files under `artifacts/redacted/` except temporary files inside tests.
- Do not modify `app/assets/async/png/onboarding/**/*.png` without explicit asset approval.
- Do not stage, commit, push, merge, rebase, or mutate tags without explicit user approval.

## Phase Map

| Phase | Purpose | Qualification Gate |
| --- | --- | --- |
| 260 | Post-RC35 baseline and scope lock | RC35 status confirmed; privacy/diff checks pass |
| 261 | Missing-action row/category filters | tests prove filtered text and JSON output are stable |
| 262 | Markdown evidence action-packet output | tests prove Markdown packets are safe and row-scoped |
| 263 | RC36 action-package documentation | docs explain filtered outputs without creating evidence |
| 264 | Runbook filter-command refresh | isolated/backend/disposable operators have exact row commands |
| 265 | RC36 lane readiness refresh | lane boundaries remain explicit; no blockers are cleared |
| 266 | Low-load heavy validation retry | heavy commands run only after `decision: run-heavy-gate`; otherwise record defer |
| 267 | RC36 freeze and final review | validation passes; public-RC decision remains honest |

### Task 1: Phase 260 Post-RC35 Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase260.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect current branch and RC35 evidence state**

Run:

```bash
git status --short --branch
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
git diff --check
```

Expected:

```text
branch remains codex/zh-Hans-post-rc26-execution
dry-run reports would_change: 0 and missing: 0
public-RC blocker total remains 11
evidence report decision remains blocked
missing-action JSON reports total_actions: 11
strict evidence lint exits 1 because real evidence is still missing
privacy_guard.py exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create Phase 260 record**

Create `docs/zh-Hans-localization-phase260.md`:

```markdown
# zh-Hans Localization Phase 260

Date: 2026-06-02

## Scope

Phase 260 audits the post-RC35 baseline before adding filtered evidence action
packet output.

This phase does not stage, commit, push, merge, rebase, mutate tags, launch GUI,
use accounts, create backend fixtures, touch billing/cloud state, create real
evidence artifacts, run Rust compile, build a bundle, or modify PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
dry-run: would_change 0, missing 0
public-RC blockers: 11
evidence ready rows: 0
missing-action JSON rows: 11
strict evidence lint: expected fail, exit_code 1
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-filtered-evidence-action-output
public RC: still blocked by evidence
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 260
status: qualified-post-rc35-baseline
safe to continue to Phase 261: yes
```
```

- [ ] **Step 3: Update localization index**

Add this line near the RC35 status in `docs/zh-Hans-localization.md`:

```markdown
- Phase 260 records the post-RC35 baseline before adding filtered evidence action packets.
```

- [ ] **Step 4: Verify Task 1**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 2: Phase 261 Missing-Action Row And Category Filters

**Files:**
- Modify: `script/zh_public_rc_evidence_report.py`
- Modify: `script/test_zh_public_rc_evidence_report.py`
- Create: `docs/zh-Hans-localization-phase261.md`

- [ ] **Step 1: Add failing tests for row and category filters**

Extend the import list in `script/test_zh_public_rc_evidence_report.py` with:

```python
    filter_actions,
```

Add these tests inside `PublicRcEvidenceReportTests`:

```python
    def test_filter_actions_by_row_id(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = filter_actions(missing_actions(blockers, evidence), row_ids=("GUI-SET-05",))

        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["row_id"], "GUI-SET-05")
        self.assertEqual(actions[0]["artifact_path"], "artifacts/redacted/gui-set-05.txt")

    def test_filter_actions_by_category(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = filter_actions(missing_actions(blockers, evidence), categories=("backend_fixture",))

        self.assertEqual(len(actions), 5)
        self.assertTrue(all(action["category"] == "backend_fixture" for action in actions))

    def test_filter_actions_allows_empty_result(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = filter_actions(missing_actions(blockers, evidence), row_ids=("GUI-NOT-REAL",))

        self.assertEqual(actions, ())
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_report.py
```

Expected:

```text
FAIL because filter_actions does not exist yet
```

- [ ] **Step 3: Implement action filtering**

In `script/zh_public_rc_evidence_report.py`, add this helper after `missing_actions`:

```python
def filter_actions(
    actions: tuple[dict[str, Any], ...],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> tuple[dict[str, Any], ...]:
    row_filter = {row_id.strip() for row_id in row_ids if row_id.strip()}
    category_filter = {category.strip() for category in categories if category.strip()}
    selected: list[dict[str, Any]] = []
    for action in actions:
        if row_filter and action["row_id"] not in row_filter:
            continue
        if category_filter and action["category"] not in category_filter:
            continue
        selected.append(action)
    return tuple(selected)
```

Update `render_missing_actions_json`:

```python
def render_missing_actions_json(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> str:
    actions = filter_actions(missing_actions(blockers, evidence_doc), row_ids=row_ids, categories=categories)
    data = {
        "total_actions": len(actions),
        "actions": list(actions),
        "decision": "blocked-until-matching-evidence-is-reviewed",
    }
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
```

Update `render_missing_actions`:

```python
def render_missing_actions(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> str:
    lines = [
        "zh-Hans public-RC missing evidence actions",
        "Only use these rows after external evidence has been captured, redacted, and approved.",
    ]
    actions = filter_actions(missing_actions(blockers, evidence_doc), row_ids=row_ids, categories=categories)
    for action in actions:
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

Add CLI args in `main`:

```python
    parser.add_argument("--row-id", action="append", default=[], help="Limit missing-action output to a public-RC row ID")
    parser.add_argument("--category", action="append", default=[], help="Limit missing-action output to a blocker category")
```

Pass filters into missing-action branches:

```python
    row_ids = tuple(args.row_id)
    categories = tuple(args.category)

    if args.missing_actions_json:
        print(render_missing_actions_json(blockers, evidence, row_ids=row_ids, categories=categories), end="")
        return 0

    if args.missing_actions:
        print(render_missing_actions(blockers, evidence, row_ids=row_ids, categories=categories), end="")
        return 0
```

- [ ] **Step 4: Verify filtered output**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_report.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions --category backend_fixture
```

Expected:

```text
unit tests pass
row filter returns total_actions: 1 and GUI-SET-05
category filter prints backend_fixture rows only
```

- [ ] **Step 5: Create Phase 261 record**

Create `docs/zh-Hans-localization-phase261.md`:

```markdown
# zh-Hans Localization Phase 261

Date: 2026-06-02

## Scope

Phase 261 adds row and category filters to missing-action text and JSON output.

No evidence rows are promoted, and no raw or redacted evidence artifacts are
created.

## Verification

```text
script/test_zh_public_rc_evidence_report.py: passed
--missing-actions-json --row-id GUI-SET-05: total_actions 1
--missing-actions --category backend_fixture: backend fixture rows only
```

## Decision

```text
decision: proceed-to-markdown-action-packet-output
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 261
status: qualified-filtered-missing-action-output
safe to continue to Phase 262: yes
```
```

- [ ] **Step 6: Verify Task 2**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 3: Phase 262 Markdown Evidence Action-Packet Output

**Files:**
- Modify: `script/zh_public_rc_evidence_report.py`
- Modify: `script/test_zh_public_rc_evidence_report.py`
- Create: `docs/zh-Hans-localization-phase262.md`

- [ ] **Step 1: Add failing Markdown packet test**

Extend the import list in `script/test_zh_public_rc_evidence_report.py` with:

```python
    render_missing_action_markdown,
```

Add this test inside `PublicRcEvidenceReportTests`:

```python
    def test_missing_action_markdown_is_row_scoped_and_safe(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        markdown = render_missing_action_markdown(blockers, evidence, row_ids=("GUI-SET-05",))

        self.assertIn("# zh-Hans Public-RC Missing Evidence Action Packet", markdown)
        self.assertIn("## GUI-SET-05", markdown)
        self.assertIn("artifacts/redacted/gui-set-05.txt", markdown)
        self.assertIn("Use only safe invalid marker values", markdown)
        self.assertNotIn("GUI-AUTH-01", markdown)
        self.assertNotIn("@", markdown)
        self.assertNotIn("https://", markdown)
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_report.py
```

Expected:

```text
FAIL because render_missing_action_markdown does not exist yet
```

- [ ] **Step 3: Implement Markdown packet renderer**

Add this function after `render_missing_actions`:

```python
def render_missing_action_markdown(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> str:
    actions = filter_actions(missing_actions(blockers, evidence_doc), row_ids=row_ids, categories=categories)
    lines = [
        "# zh-Hans Public-RC Missing Evidence Action Packet",
        "",
        "This packet is safe handoff metadata only. It does not provide evidence and does not clear public-RC blockers.",
        "",
        "## Safety Boundary",
        "",
        "- Keep raw screenshots, recordings, callback URLs, cookies, tokens, account identifiers, endpoint URLs, team IDs, and private object names outside Git.",
        "- Commit only reviewed redacted text under the exact `artifacts/redacted/<row-id>.txt` path after explicit approval.",
        "- Do not mutate accounts, billing, cloud state, teams, secrets, endpoints, or environments without explicit approval.",
        "",
    ]
    if not actions:
        lines.extend(["## No Matching Actions", "", "No missing evidence action matched the supplied filters.", ""])
        return "\n".join(lines)

    for action in actions:
        lines.extend(
            [
                f"## {action['row_id']}",
                "",
                f"- Category: `{action['category']}`",
                f"- Current status: `{action['status']}`",
                f"- Handoff doc: `{action['handoff_doc']}`",
                f"- Expected redacted artifact: `{action['artifact_path']}`",
                f"- Safety rule: {action['safety_rule']}",
                "",
                "Required evidence:",
            ]
        )
        for item in action["required_evidence"]:
            lines.append(f"- {item}")
        lines.extend(["", "Qualification rule:", "", "```text", "status may become provided only after raw evidence is reviewed, redacted artifact text is approved, strict artifact lint passes, and cleanup proof is present.", "```", ""])
    return "\n".join(lines)
```

Add the CLI argument:

```python
    parser.add_argument("--missing-action-markdown", action="store_true", help="Print filtered missing evidence actions as Markdown")
```

Add this branch after loading `evidence` and filter tuples:

```python
    if args.missing_action_markdown:
        print(render_missing_action_markdown(blockers, evidence, row_ids=row_ids, categories=categories), end="")
        return 0
```

- [ ] **Step 4: Verify Markdown output**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_report.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account
```

Expected:

```text
unit tests pass
row-scoped Markdown includes only GUI-SET-05
category-scoped Markdown includes isolated_account rows only
```

- [ ] **Step 5: Create Phase 262 record**

Create `docs/zh-Hans-localization-phase262.md`:

```markdown
# zh-Hans Localization Phase 262

Date: 2026-06-02

## Scope

Phase 262 adds Markdown missing-action packet output for safe row-owner handoff.

No evidence rows are promoted, and no evidence artifacts are created.

## Verification

```text
script/test_zh_public_rc_evidence_report.py: passed
--missing-action-markdown --row-id GUI-SET-05: row-scoped packet passed
--missing-action-markdown --category isolated_account: category packet passed
```

## Decision

```text
decision: proceed-to-rc36-action-package-docs
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 262
status: qualified-markdown-action-packet-output
safe to continue to Phase 263: yes
```
```

- [ ] **Step 6: Verify Task 3**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Phase 263 RC36 Evidence Action-Package Docs

**Files:**
- Create: `docs/zh-Hans-public-rc-evidence-action-package-rc36.md`
- Create: `docs/zh-Hans-localization-phase263.md`

- [ ] **Step 1: Generate filtered outputs for documentation**

Run:

```bash
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category backend_fixture
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
```

Expected:

```text
GUI-SET-05 row filter returns one action
backend_fixture category filter returns five actions
Markdown row packet excludes unrelated rows
disposable_object category packet returns three actions
```

- [ ] **Step 2: Create RC36 action-package doc**

Create `docs/zh-Hans-public-rc-evidence-action-package-rc36.md`:

```markdown
# zh-Hans Public-RC Evidence Action Package RC36

Date: 2026-06-02

## Purpose

RC36 adds filtered missing-evidence action packets. These packets let an operator
request one row or one category at a time without exposing raw evidence and
without changing the evidence ledger.

## Commands

```bash
python3 script/zh_public_rc_evidence_report.py --missing-actions --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_report.py --missing-actions --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
```

## Row Filters

```text
--row-id GUI-AUTH-01
--row-id GUI-SET-03
--row-id GUI-SET-04
--row-id GUI-SET-05
--row-id GUI-SET-06
--row-id GUI-WS-04
--row-id GUI-WS-06
--row-id GUI-WS-07
--row-id GUI-BILL-01
--row-id GUI-BILL-02
--row-id GUI-CLOUD-01
```

## Category Filters

```text
--category isolated_account
--category backend_fixture
--category disposable_object
```

## Safety Boundary

```text
filtered packets are handoff metadata only
raw evidence stays outside Git
redacted artifact text requires explicit approval before adding to artifacts/redacted/
ledger promotion requires reviewed raw evidence and strict artifact lint pass
blocker promotion requires accepted evidence row and explicit approval
```

## RC36 Status

```text
public-RC rows tracked: 11
ready rows: 0
filtered packet output: available
decision: blocked
```
```

- [ ] **Step 3: Create Phase 263 record**

Create `docs/zh-Hans-localization-phase263.md`:

```markdown
# zh-Hans Localization Phase 263

Date: 2026-06-02

## Scope

Phase 263 documents RC36 filtered evidence action packages.

No evidence rows are promoted, and no evidence artifacts are created.

## Verification

```text
row JSON filter: passed
category JSON filter: passed
row Markdown packet: passed
category Markdown packet: passed
```

## Decision

```text
decision: proceed-to-runbook-filter-refresh
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 263
status: qualified-action-package-docs
safe to continue to Phase 264: yes
```
```

- [ ] **Step 4: Verify Task 4**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 5: Phase 264 Runbook Filter-Command Refresh

**Files:**
- Modify: `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`
- Modify: `docs/zh-Hans-backend-fixture-contract-rc19.md`
- Create: `docs/zh-Hans-localization-phase264.md`

- [ ] **Step 1: Update isolated-account runbook**

Append this section to `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`:

```markdown
## RC36 Filtered Action Packet Commands

Use these commands to request isolated-account evidence one row at a time:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-AUTH-01
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-03
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-WS-06
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category isolated_account
```

These commands do not create evidence. They print safe handoff metadata only.
Do not use the user's main account, and do not store account identifiers,
callback URLs, cookies, tokens, or magic links in repository files.
```

- [ ] **Step 2: Update backend/disposable fixture contract**

Append this section to `docs/zh-Hans-backend-fixture-contract-rc19.md`:

```markdown
## RC36 Filtered Action Packet Commands

Use these commands to request backend-fixture and disposable-object evidence by
category:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category disposable_object
```

Use these commands to request high-risk rows one at a time:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-06
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-WS-04
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-WS-07
```

These commands do not create evidence. They print safe handoff metadata only.
Do not attach payment methods, use real credentials, mutate production teams,
delete real objects, or consume cloud capacity while collecting evidence.
```

- [ ] **Step 3: Create Phase 264 record**

Create `docs/zh-Hans-localization-phase264.md`:

```markdown
# zh-Hans Localization Phase 264

Date: 2026-06-02

## Scope

Phase 264 refreshes the isolated-account and backend/disposable-object runbooks
with RC36 filtered action packet commands.

No evidence rows are promoted, and no evidence artifacts are created.

## Verification

```text
isolated-account runbook: RC36 filtered commands added
backend/disposable runbook: RC36 filtered commands added
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-rc36-lane-readiness-refresh
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 264
status: qualified-runbook-filter-refresh
safe to continue to Phase 265: yes
```
```

- [ ] **Step 4: Verify Task 5**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 6: Phase 265 RC36 Lane Readiness Refresh

**Files:**
- Create: `docs/zh-Hans-public-rc-lane-readiness-rc36.md`
- Create: `docs/zh-Hans-localization-phase265.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md` only if lane status text needs a current RC36 entry.

- [ ] **Step 1: Recheck lane counts and asset status**

Run:

```bash
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
```

Expected:

```text
public-RC blocker total remains 11
ready evidence rows remain 0
PNG commands produce no onboarding asset changes unless explicitly approved
```

- [ ] **Step 2: Create RC36 lane readiness doc**

Create `docs/zh-Hans-public-rc-lane-readiness-rc36.md`:

```markdown
# zh-Hans Public-RC Lane Readiness RC36

Date: 2026-06-02

## Current Lane Status

```text
backend_fixture: total=5 ready=0 missing=5
disposable_object: total=3 ready=0 missing=3
isolated_account: total=3 ready=0 missing=3
asset lane: blocked-no-asset-approval
heavy validation lane: pending-low-load-gate
GUI lane: blocked-no-explicit-gui-smoke-approval
publication lane: blocked-no-explicit-approval
```

## RC36 Packetization Outputs

```text
row text packet: python3 script/zh_public_rc_evidence_report.py --missing-actions --row-id GUI-SET-05
row JSON packet: python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
row Markdown packet: python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-05
category Markdown packet: python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
```

## Promotion Rule

No lane can promote a row unless the matching evidence row is `status = "provided"`,
the expected row-specific artifact path exists, strict artifact lint passes, raw
evidence has been manually reviewed for safety and row match, and the user has
explicitly approved the promotion.
```

- [ ] **Step 3: Update GUI smoke matrix only if needed**

If `docs/zh-Hans-gui-smoke-matrix.md` lacks a current RC36 lane entry, add:

```markdown
## RC36 Filtered Evidence Packetization

```text
filtered action packets: available
backend_fixture rows: 5 missing
disposable_object rows: 3 missing
isolated_account rows: 3 missing
GUI launch: pending explicit GUI smoke approval
PNG assets: unchanged
```
```

- [ ] **Step 4: Create Phase 265 record**

Create `docs/zh-Hans-localization-phase265.md`:

```markdown
# zh-Hans Localization Phase 265

Date: 2026-06-02

## Scope

Phase 265 refreshes RC36 lane readiness after filtered evidence packetization.

No evidence rows are promoted, no GUI is launched, and no PNG assets are changed.

## Verification

```text
public-RC blocker status: 11 blockers
evidence report JSON: blocked, ready rows 0
PNG asset status: unchanged
```

## Decision

```text
decision: proceed-to-low-load-heavy-validation-retry
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 265
status: qualified-lane-readiness-refresh
safe to continue to Phase 266: yes
```
```

- [ ] **Step 5: Verify Task 6**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 7: Phase 266 Low-Load Heavy Validation Retry

**Files:**
- Create: `docs/zh-Hans-localization-phase266.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md` only to record heavy validation result.

- [ ] **Step 1: Run low-load gate**

Run:

```bash
nice -n 10 python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Expected:

```text
If output contains decision: run-heavy-gate, continue to Step 2.
If output contains decision: defer-heavy-gate, skip Step 2 and record skipped-with-heat-safety.
```

- [ ] **Step 2: Run heavy validation only if allowed**

Run only if Step 1 prints `decision: run-heavy-gate`:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
cargo check passes
bundle generation passes
GUI is not launched
```

- [ ] **Step 3: Record heavy validation result**

Create `docs/zh-Hans-localization-phase266.md` with one of these result blocks.

If heavy validation ran:

```markdown
# zh-Hans Localization Phase 266

Date: 2026-06-02

## Scope

Phase 266 retries heavy validation only after the low-load gate allows it.

GUI launch remains out of scope.

## Verification

```text
low-load gate: run-heavy-gate
cargo check -j 1 -p warp: passed
script/run --dont-open: passed
fresh bundle: passed
GUI launch: not run
```

## Decision

```text
decision: proceed-to-rc36-freeze
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 266
status: qualified-heavy-validation-passed
safe to continue to Phase 267: yes
```
```

If heavy validation was deferred:

```markdown
# zh-Hans Localization Phase 266

Date: 2026-06-02

## Scope

Phase 266 checks whether heavy validation can run safely.

GUI launch remains out of scope.

## Verification

```text
low-load gate: defer-heavy-gate
cargo check -j 1 -p warp: skipped-with-heat-safety
script/run --dont-open: skipped-with-heat-safety
fresh bundle: not refreshed in Phase 266
GUI launch: not run
```

## Decision

```text
decision: proceed-to-rc36-freeze-with-qualified-heavy-defer
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 266
status: qualified-heavy-validation-deferred
safe to continue to Phase 267: yes
```
```

- [ ] **Step 4: Update GUI smoke matrix**

Add a short RC36 heavy validation entry to `docs/zh-Hans-gui-smoke-matrix.md` matching the Phase 266 result:

```markdown
## RC36 Heavy Validation Retry

```text
low-load gate: run-heavy-gate or defer-heavy-gate
fresh bundle: passed or skipped-with-heat-safety
GUI launch: pending explicit GUI smoke approval
```
```

- [ ] **Step 5: Verify Task 7**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 8: Phase 267 RC36 Freeze And Final Review

**Files:**
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc36.md`
- Create: `docs/zh-Hans-localization-phase267.md`
- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Run final lightweight validation**

Run:

```bash
set -e
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
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
manifest and glossary pass
dry-run reports would_change 0 and missing 0
release coverage remains 100.0%
public-RC blocker total remains 11
JSON evidence report remains blocked
filtered row JSON returns one action for GUI-SET-05
filtered category Markdown returns backend_fixture actions
strict evidence lint exits 1 because evidence is still missing
Python tests pass
cargo fmt --check exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create RC36 release candidate record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc36.md`:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC36

Date: 2026-06-02

## Scope

RC36 covers Phases 260 through 267. It adds row/category filters for missing
evidence actions, Markdown missing-action packet output, RC36 evidence action
package docs, filtered command updates in public-RC runbooks, lane readiness
refresh, low-load heavy validation retry, and the next local-use/public-RC
decision freeze.

RC36 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Packetization

```text
text report: script/zh_public_rc_evidence_report.py
JSON report: script/zh_public_rc_evidence_report.py --json
filtered text missing actions: script/zh_public_rc_evidence_report.py --missing-actions --row-id GUI-SET-05
filtered JSON missing actions: script/zh_public_rc_evidence_report.py --missing-actions-json --category backend_fixture
filtered Markdown packet: script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-05
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC36: 0
```

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 100.0%
```

## Public-RC Blocker Registry

```text
total: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

No blocker was cleared in RC36.

## Command-Line Gates

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
release inventory coverage
public-RC blocker summary
public-RC evidence JSON report
public-RC filtered missing-action JSON
public-RC filtered missing-action Markdown
privacy guard
Python localization, public-RC, report, and gate tests
cargo fmt --check
git diff --check
```

Expected blocker signal:

```text
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
exit_code: 1
decision: fail
reason: 11 rows still missing evidence
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC36 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
```

- [ ] **Step 3: Create Phase 267 record**

Create `docs/zh-Hans-localization-phase267.md`:

```markdown
# zh-Hans Localization Phase 267

Date: 2026-06-02

## Scope

Phase 267 freezes RC36 after filtered evidence packetization and final
lightweight validation.

No evidence rows are promoted, and no integration or publication action is
performed.

## Verification

```text
manifest validation: passed
glossary check: passed
dry-run: would_change 0, missing 0
release coverage: 100.0%
public-RC blockers: 11
ready evidence rows: 0
filtered row JSON: passed
filtered category Markdown: passed
strict evidence lint: expected fail, exit_code 1
privacy guard: passed
Python test suite: passed
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
phase: 267
status: qualified-rc36-freeze
safe to stop: yes
```
```

- [ ] **Step 4: Update README and localization index**

Update `README.md` and `docs/zh-Hans-localization.md` so they point to RC36:

```text
Last verified release audit: 2026-06-02 RC36
RC36 adds filtered missing-action row/category output and Markdown action packets.
Current public-RC blocker total remains 11, and ready evidence rows remain 0.
```

Also add a helper description:

```text
For RC36 and later, use --row-id and --category with --missing-actions,
--missing-actions-json, and --missing-action-markdown to produce scoped handoff
packets.
```

- [ ] **Step 5: Run final post-doc verification**

Run:

```bash
set -e
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
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
dry-run remains clean
public-RC remains blocked with 11 blockers
filtered outputs pass
strict lint expected-fails with exit code 1
targeted tests pass
cargo fmt --check exits 0
git diff --check exits 0
git status shows changes only from planned files and earlier uncommitted project work
```

## Final Review Checklist

Before marking the RC36 goal complete:

```text
all Phase 260-267 records exist
script/test_zh_public_rc_evidence_report.py includes row/category/Markdown tests
script/zh_public_rc_evidence_report.py existing text and JSON behavior still works
strict evidence lint still blocks missing evidence
no resources/localization/zh-Hans-public-rc-evidence.toml promotion happened without approved evidence
no artifacts/redacted/ files were created outside tests
no GUI launch happened without explicit approval
no heavy command ran unless low-load gate allowed it
no stage/commit/push/merge/rebase/tag action happened
```
