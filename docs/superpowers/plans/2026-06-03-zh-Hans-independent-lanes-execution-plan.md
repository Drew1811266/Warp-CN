# zh-Hans Independent Public-RC Lanes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare the non-backend-approval public-RC work lanes while Warp backend fixture approval is pending.

**Architecture:** Keep backend fixture evidence blocked on the upstream approval issue, and split independent work into isolated-account, disposable-object, release-note, packaging-preflight, and translation-rescan lanes. Each lane produces only planning records, off-Git intake material, or low-load validation output until explicit evidence or release approval exists.

**Tech Stack:** Markdown release docs, Python localization/evidence scripts, TOML public-RC registries, GitHub issue handoff, privacy guard, low-load build gate, no GUI or external account mutation in planning mode.

---

## Current Baseline

```text
backend fixture request: https://github.com/warpdotdev/warp/issues/12129
public-RC blockers: 11
backend_fixture blockers: 5
isolated_account blockers: 3
disposable_object blockers: 3
ready evidence rows: 0
dry-run would_change: 0
dry-run missing: 0
release inventory coverage: 100.0%
strict artifact lint: expected fail until evidence exists
```

## File Structure

- Create `docs/zh-Hans-public-rc-independent-lanes-execution.md` for cross-lane execution boundaries and commands.
- Create `docs/superpowers/plans/2026-06-03-zh-Hans-independent-lanes-execution-plan.md` as this agentic implementation plan.
- Modify `docs/zh-Hans-official-release-next-development-tasks.md` to link the independent lane execution path.
- Modify `README.md` to add the independent lane execution document to the maintenance index.
- Do not modify `resources/localization/zh-Hans-public-rc-evidence.toml` in this plan.
- Do not modify `resources/localization/zh-Hans-public-rc-blockers.toml` in this plan.
- Do not create `artifacts/redacted/*` in this plan.
- Do not create `/tmp/gui-*-candidate.txt` files in this plan.

## Task 1: Verify Independent Lane Baseline

**Files:**
- Read: `resources/localization/zh-Hans-public-rc-blockers.toml`
- Read: `resources/localization/zh-Hans-public-rc-evidence.toml`
- Read: `script/zh_public_rc_status.py`
- Read: `script/zh_public_rc_evidence_queue.py`

- [ ] **Step 1: Inspect the working tree**

Run:

```bash
git status --short --branch
```

Expected:

```text
branch is codex/zh-Hans-post-rc26-execution
existing docs work may be untracked or modified
no protected evidence/blocker TOML changes are required
```

- [ ] **Step 2: Inspect isolated account queue**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
```

Expected:

```text
output contains GUI-AUTH-01
output contains GUI-SET-03
output contains GUI-WS-06
approval gate is isolated-account-approval
```

- [ ] **Step 3: Inspect disposable object queue**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
```

Expected:

```text
output contains GUI-SET-06
output contains GUI-WS-04
output contains GUI-WS-07
approval gate is disposable-object-approval
```

- [ ] **Step 4: Inspect localization baseline**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
```

Expected:

```text
manifest validation passed
glossary check passed
would_change: 0
missing: 0
release coverage: 100.0%
public-RC blocker total: 11
```

## Task 2: Create Independent Lane Execution Document

**Files:**
- Create: `docs/zh-Hans-public-rc-independent-lanes-execution.md`

- [ ] **Step 1: Write the document header and baseline**

Create the document with:

````markdown
# zh-Hans Public-RC Independent Lanes Execution

Date: 2026-06-03

## Purpose

This document defines the work that can continue while backend fixture approval
is pending in warpdotdev/warp#12129. It is an execution guide for preparation,
low-load verification, and release documentation only. It does not provide
evidence and does not clear public-RC blockers.

## Current Baseline

```text
backend fixture approval: waiting on warpdotdev/warp#12129
public-RC blockers: 11
backend_fixture blockers: 5
isolated_account blockers: 3
disposable_object blockers: 3
ready evidence rows: 0
strict artifact lint: expected fail until reviewed evidence exists
```
````

- [ ] **Step 2: Add the parallel work matrix**

Add:

```markdown
## Parallel Work Matrix

| Lane | Can proceed now | Must wait for |
| --- | --- | --- |
| Isolated account | Request isolated account approval, prepare candidate format, define cleanup proof, run queue/action packet commands | actual isolated account, login approval, reviewed raw evidence |
| Disposable object | Request allowlisted object approval, prepare cancel-first/delete/transfer proof format, run queue/action packet commands | exact disposable objects, explicit delete/transfer approval, reviewed raw evidence |
| Release notes | Draft current status, known blockers, evidence policy, no-go wording, version checklist | all evidence rows, heavy gate results, final version approval |
| Packaging check | Run low-load manifest/inventory/status checks, document heavy-gate commands and expected outputs | low-load gate, explicit approval for Rust compile, bundle, GUI launch |
| Translation rescan | Run manifest, glossary, dry-run, inventory, public-RC status, and unit evidence tests | only required if source drift or glossary errors appear |
```

- [ ] **Step 3: Add lane sections**

Add sections for:

```text
Isolated Account Lane
Disposable Object Lane
Release Notes Draft Lane
Packaging Check Lane
Translation Rescan Lane
No-Go
```

Each lane must list exact row IDs, exact candidate paths, exact commands, and explicit stop rules.

- [ ] **Step 4: Verify the document**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
needles = ["TB" + "D", "TO" + "DO", "fill " + "in", "place" + "holder"]
path = Path("docs/zh-Hans-public-rc-independent-lanes-execution.md")
hits = [
    (index, line)
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
    if any(needle in line for needle in needles)
]
for index, line in hits:
    print(f"{path}:{index}: {line}")
raise SystemExit(1 if hits else 0)
PY
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
red-flag search returns no matches
privacy guard exits 0
git diff --check exits 0
```

## Task 3: Update Release Task Index

**Files:**
- Modify: `docs/zh-Hans-official-release-next-development-tasks.md`

- [ ] **Step 1: Add independent-lanes status**

Add a section after the current completion state:

```markdown
## Backend Fixture Wait State

Backend fixture approval is now tracked externally:

- https://github.com/warpdotdev/warp/issues/12129

While that issue is open, continue only the independent lanes documented in
`docs/zh-Hans-public-rc-independent-lanes-execution.md`.
```

- [ ] **Step 2: Add R4-R6 execution links**

Add these links to the relevant R4-R6 sections:

```markdown
- `docs/zh-Hans-public-rc-independent-lanes-execution.md`
- `docs/superpowers/plans/2026-06-03-zh-Hans-independent-lanes-execution-plan.md`
```

- [ ] **Step 3: Verify protected files stayed untouched**

Run:

```bash
git diff --name-only -- resources/localization/zh-Hans-public-rc-evidence.toml resources/localization/zh-Hans-public-rc-blockers.toml artifacts/redacted
```

Expected:

```text
no output
```

## Task 4: Update README Maintenance Index

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add the independent lane document**

Add this bullet under the maintenance docs list:

```markdown
- `docs/zh-Hans-public-rc-independent-lanes-execution.md`：等待官方 backend fixture 审批期间可并行推进的 isolated account、disposable object、release notes、packaging preflight 和 translation rescan 执行边界。
```

- [ ] **Step 2: Verify README diff**

Run:

```bash
git diff -- README.md
git diff --check
```

Expected:

```text
README diff contains one new maintenance-doc bullet
git diff --check exits 0
```

## Task 5: Final Documentation Verification

**Files:**
- Read: `docs/zh-Hans-public-rc-independent-lanes-execution.md`
- Read: `docs/zh-Hans-official-release-next-development-tasks.md`
- Read: `README.md`

- [ ] **Step 1: Run privacy and formatting checks**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

- [ ] **Step 2: Confirm public-RC status remains blocked**

Run:

```bash
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

Expected:

```text
status still reports 11 public-RC blockers
strict artifact lint still fails with missing evidence until real reviewed evidence exists
```

- [ ] **Step 3: Confirm no candidate or artifact promotion happened**

Run:

```bash
for f in /tmp/gui-auth-01-candidate.txt /tmp/gui-set-03-candidate.txt /tmp/gui-ws-06-candidate.txt /tmp/gui-set-06-candidate.txt /tmp/gui-ws-04-candidate.txt /tmp/gui-ws-07-candidate.txt; do
  if [ -f "$f" ]; then
    printf 'PRESENT %s\n' "$f"
  else
    printf 'MISSING %s\n' "$f"
  fi
done
git diff --name-only -- resources/localization/zh-Hans-public-rc-evidence.toml resources/localization/zh-Hans-public-rc-blockers.toml artifacts/redacted
```

Expected:

```text
candidate files are missing unless separately approved
protected evidence/blocker/artifact paths have no diff
```
