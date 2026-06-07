# zh-Hans Backend Fixture Evidence Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the five backend-fixture public-RC evidence rows by collecting approved fixture evidence outside Git, preflighting reviewed redacted candidates, and promoting only approved redacted artifacts into the evidence ledger.

**Architecture:** Keep raw evidence outside the repository. Use `docs/zh-Hans-public-rc-backend-fixture-execution.md` for lane safety, `docs/zh-Hans-backend-fixture-contract-rc19.md` for fixture requirements, `/tmp/*-candidate.txt` for machine preflight, `artifacts/redacted/*.txt` only after explicit approval, and `resources/localization/zh-Hans-public-rc-evidence.toml` as the only evidence ledger. Do not change `resources/localization/zh-Hans-public-rc-blockers.toml` in this plan; blocker status vocabulary is deferred until all evidence lanes are ready.

**Tech Stack:** Python public-RC evidence scripts, TOML evidence ledger, Markdown handoff docs, Git working tree checks, privacy guard, no GUI or backend automation unless explicitly approved.

---

## Current Baseline

```text
backend_fixture rows: 5
rows: GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01, GUI-SET-04, GUI-SET-05
current evidence status: missing
current backend fixture queue decision: blocked-until-queue-cleared
allowed candidate preflight location: /tmp
approved artifact destination prefix: artifacts/redacted/
protected files not modified until approval: resources/localization/zh-Hans-public-rc-evidence.toml
protected files not modified in this plan: resources/localization/zh-Hans-public-rc-blockers.toml
```

## File Structure

- Create `docs/zh-Hans-backend-fixture-r3-readiness.md` to record fixture owner approvals, evidence availability, and per-row readiness without containing secrets.
- Create `docs/zh-Hans-backend-fixture-r3-preflight-results.md` to record candidate preflight command outcomes without embedding raw evidence.
- Modify `resources/localization/zh-Hans-public-rc-evidence.toml` only after reviewed redacted candidate text exists, preflight passes, and explicit approval is given.
- Create `artifacts/redacted/gui-bill-01.txt` only after explicit approval.
- Create `artifacts/redacted/gui-bill-02.txt` only after explicit approval.
- Create `artifacts/redacted/gui-cloud-01.txt` only after explicit approval.
- Create `artifacts/redacted/gui-set-04.txt` only after explicit approval.
- Create `artifacts/redacted/gui-set-05.txt` only after explicit approval.
- Do not modify `resources/localization/zh-Hans-public-rc-blockers.toml` in this plan.
- Do not store raw screenshots, recordings, callback URLs, endpoint URLs, cookies, tokens, API keys, account identifiers, team IDs, billing IDs, private object names, real credentials, or private fixture identifiers in Git.

## Task 1: Backend Fixture Baseline And Owner Packet

**Files:**
- Create: `docs/zh-Hans-backend-fixture-r3-readiness.md`

- [ ] **Step 1: Inspect the backend fixture queue**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --json --category backend_fixture > /tmp/warp-cn-r3-backend-queue.json
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture > /tmp/warp-cn-r3-backend-queue.md
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture > /tmp/warp-cn-r3-backend-actions.md
python3 -m json.tool /tmp/warp-cn-r3-backend-queue.json > /tmp/warp-cn-r3-backend-queue.pretty.json
```

Expected:

```text
/tmp/warp-cn-r3-backend-queue.json contains total_rows: 5
/tmp/warp-cn-r3-backend-queue.md contains GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01, GUI-SET-04, GUI-SET-05
/tmp/warp-cn-r3-backend-actions.md contains artifacts/redacted/gui-bill-01.txt, artifacts/redacted/gui-bill-02.txt, artifacts/redacted/gui-cloud-01.txt, artifacts/redacted/gui-set-04.txt, artifacts/redacted/gui-set-05.txt
```

- [ ] **Step 2: Create the R3 readiness record**

Create `docs/zh-Hans-backend-fixture-r3-readiness.md`:

````markdown
# zh-Hans Backend Fixture R3 Readiness

Date: 2026-06-03

## Scope

Rows:

- `GUI-BILL-01`
- `GUI-BILL-02`
- `GUI-CLOUD-01`
- `GUI-SET-04`
- `GUI-SET-05`

## Current State

```text
category: backend_fixture
queue total_rows: 5
approval gate: fixture-owner-approval
evidence ledger status: missing
blocker registry status: unchanged
```

## Required Fixture Package

Every backend fixture row requires a fixture owner packet with:

- fixture owner approval
- allowed mutations
- reset procedure
- cleanup proof format
- redaction requirements
- expiration or teardown date
- statement that no production object is affected

## Row Requirements

| Row | Required evidence | Safety boundary |
| --- | --- | --- |
| `GUI-BILL-01` | safe quota or billing fixture; redacted billing GUI evidence; fixture reset proof | no credit purchase, no payment method, no real quota consumption |
| `GUI-BILL-02` | backend test team with build-plan migration state; redacted modal GUI evidence; backend flag reset proof | backend test state only, no production team or billing mutation |
| `GUI-CLOUD-01` | controlled capacity or quota fixture; redacted cloud capacity GUI evidence; fixture reset proof | no production cloud capacity creation, deletion, or exhaustion |
| `GUI-SET-04` | disposable AWS or Bedrock fixture; redacted settings GUI evidence; fixture reset proof | no real AWS credentials, no real profile names |
| `GUI-SET-05` | invalid credential fixture; redacted error GUI evidence; fixture reset proof | safe invalid marker values only, no real API keys or provider credentials |

## Execution Decision

```text
decision: blocked-until-fixture-owner-approval-and-reviewed-raw-evidence
```

This document does not provide evidence and does not clear blockers.
````

- [ ] **Step 3: Verify Task 1**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

## Task 2: Candidate Text Preparation Gate

**Files:**
- No repository files are modified in this task.

- [ ] **Step 1: Stop unless reviewed raw evidence exists outside Git**

Before creating any candidate file, confirm all conditions below are true:

```text
fixture owner approval is present outside Git
raw evidence has been reviewed outside Git
redaction review has removed account identifiers, callback URLs, endpoint URLs, cookies, tokens, API keys, secrets, team IDs, billing IDs, and private object names
cleanup proof exists outside Git
no production object or real credential was used
```

Expected:

```text
If any condition is false, stop with BLOCKED and do not create candidate files.
```

- [ ] **Step 2: Verify reviewed redacted candidate files outside Git**

Only after Step 1 passes, verify that a reviewer or fixture owner has provided
these candidate files outside Git:

```text
/tmp/gui-bill-01-candidate.txt
/tmp/gui-bill-02-candidate.txt
/tmp/gui-cloud-01-candidate.txt
/tmp/gui-set-04-candidate.txt
/tmp/gui-set-05-candidate.txt
```

Run:

```bash
test -f /tmp/gui-bill-01-candidate.txt
test -f /tmp/gui-bill-02-candidate.txt
test -f /tmp/gui-cloud-01-candidate.txt
test -f /tmp/gui-set-04-candidate.txt
test -f /tmp/gui-set-05-candidate.txt
rg -n '^row_id: GUI-BILL-01$' /tmp/gui-bill-01-candidate.txt
rg -n '^row_id: GUI-BILL-02$' /tmp/gui-bill-02-candidate.txt
rg -n '^row_id: GUI-CLOUD-01$' /tmp/gui-cloud-01-candidate.txt
rg -n '^row_id: GUI-SET-04$' /tmp/gui-set-04-candidate.txt
rg -n '^row_id: GUI-SET-05$' /tmp/gui-set-05-candidate.txt
rg -n '^profile:' /tmp/gui-bill-01-candidate.txt /tmp/gui-bill-02-candidate.txt /tmp/gui-cloud-01-candidate.txt /tmp/gui-set-04-candidate.txt /tmp/gui-set-05-candidate.txt
rg -n '^visible_anchors:' /tmp/gui-bill-01-candidate.txt /tmp/gui-bill-02-candidate.txt /tmp/gui-cloud-01-candidate.txt /tmp/gui-set-04-candidate.txt /tmp/gui-set-05-candidate.txt
rg -n '^redaction:' /tmp/gui-bill-01-candidate.txt /tmp/gui-bill-02-candidate.txt /tmp/gui-cloud-01-candidate.txt /tmp/gui-set-04-candidate.txt /tmp/gui-set-05-candidate.txt
rg -n '^cleanup_proof:' /tmp/gui-bill-01-candidate.txt /tmp/gui-bill-02-candidate.txt /tmp/gui-cloud-01-candidate.txt /tmp/gui-set-04-candidate.txt /tmp/gui-set-05-candidate.txt
rg -n '^safety_confirmation:' /tmp/gui-bill-01-candidate.txt /tmp/gui-bill-02-candidate.txt /tmp/gui-cloud-01-candidate.txt /tmp/gui-set-04-candidate.txt /tmp/gui-set-05-candidate.txt
rg -n '^artifact_kind: redacted-text$' /tmp/gui-bill-01-candidate.txt /tmp/gui-bill-02-candidate.txt /tmp/gui-cloud-01-candidate.txt /tmp/gui-set-04-candidate.txt /tmp/gui-set-05-candidate.txt
```

Expected:

```text
candidate files are outside Git under /tmp
each candidate file has the required candidate-preflight fields
candidate files do not contain raw evidence, private URLs, identifiers, tokens, keys, cookies, or private object names
```

## Task 3: Candidate Preflight And Result Record

**Files:**
- Create: `docs/zh-Hans-backend-fixture-r3-preflight-results.md`

- [ ] **Step 1: Preflight all backend fixture candidates**

Run:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-01 --artifact /tmp/gui-bill-01-candidate.txt --markdown > /tmp/gui-bill-01-preflight.md
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-02 --artifact /tmp/gui-bill-02-candidate.txt --markdown > /tmp/gui-bill-02-preflight.md
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-CLOUD-01 --artifact /tmp/gui-cloud-01-candidate.txt --markdown > /tmp/gui-cloud-01-preflight.md
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-04 --artifact /tmp/gui-set-04-candidate.txt --markdown > /tmp/gui-set-04-preflight.md
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /tmp/gui-set-05-candidate.txt --markdown > /tmp/gui-set-05-preflight.md
```

Expected:

```text
each command exits 0
each markdown file contains candidate-ready-for-human-review
no markdown file contains raw URLs, token values, cookies, API keys, billing IDs, or private object names
```

- [ ] **Step 2: Create the preflight result record**

Create `docs/zh-Hans-backend-fixture-r3-preflight-results.md`:

````markdown
# zh-Hans Backend Fixture R3 Preflight Results

Date: 2026-06-03

## Scope

Rows:

- `GUI-BILL-01`
- `GUI-BILL-02`
- `GUI-CLOUD-01`
- `GUI-SET-04`
- `GUI-SET-05`

## Preflight Results

```text
GUI-BILL-01: candidate-ready-for-human-review
GUI-BILL-02: candidate-ready-for-human-review
GUI-CLOUD-01: candidate-ready-for-human-review
GUI-SET-04: candidate-ready-for-human-review
GUI-SET-05: candidate-ready-for-human-review
```

## Safety Review

```text
raw evidence stayed outside Git
candidate files stayed outside Git under /tmp
candidate text contained no callback URLs, endpoint URLs, tokens, cookies, API keys, secrets, billing IDs, team IDs, account identifiers, or private object names
fixture cleanup proof was present for every row
```

## Decision

```text
decision: ready-for-human-ledger-promotion-review
```

This document summarizes preflight only. It does not provide evidence, update the ledger, or clear blockers.
````

- [ ] **Step 3: Verify Task 3**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

## Task 4: Approved Artifact And Ledger Promotion

**Files:**
- Create: `artifacts/redacted/gui-bill-01.txt`
- Create: `artifacts/redacted/gui-bill-02.txt`
- Create: `artifacts/redacted/gui-cloud-01.txt`
- Create: `artifacts/redacted/gui-set-04.txt`
- Create: `artifacts/redacted/gui-set-05.txt`
- Modify: `resources/localization/zh-Hans-public-rc-evidence.toml`

- [ ] **Step 1: Stop for explicit promotion approval**

Before creating files under `artifacts/redacted/` or editing the evidence ledger, get explicit approval that:

```text
the reviewed redacted candidate text may be committed
the exact destination path is approved
cleanup proof text is approved
redaction statement is approved
notes text is approved
```

Expected:

```text
If approval is absent, stop with BLOCKED and do not edit artifacts/redacted or resources/localization/zh-Hans-public-rc-evidence.toml.
```

- [ ] **Step 2: Create approved redacted artifacts**

After explicit approval, create exactly these files from the approved redacted candidate text:

```text
artifacts/redacted/gui-bill-01.txt
artifacts/redacted/gui-bill-02.txt
artifacts/redacted/gui-cloud-01.txt
artifacts/redacted/gui-set-04.txt
artifacts/redacted/gui-set-05.txt
```

Expected:

```text
each file is reviewed redacted text only
no file contains raw screenshots, recordings, callback URLs, endpoint URLs, cookies, tokens, API keys, secrets, team IDs, billing IDs, account identifiers, or private object names
```

- [ ] **Step 3: Update backend fixture evidence rows**

In `resources/localization/zh-Hans-public-rc-evidence.toml`, update only these five rows:

```toml
[[evidence]]
row_id = "GUI-SET-04"
status = "provided"
evidence_paths = ["artifacts/redacted/gui-set-04.txt"]
cleanup_proof = "fixture reset proof captured; disposable AWS or Bedrock fixture reset; no production state was touched"
redaction = "account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, secrets, team IDs, billing IDs, and private object names removed"
notes = "backend fixture evidence approved for AWS Bedrock settings row"

[[evidence]]
row_id = "GUI-SET-05"
status = "provided"
evidence_paths = ["artifacts/redacted/gui-set-05.txt"]
cleanup_proof = "fixture reset proof captured; invalid credential fixture reset; no production state was touched"
redaction = "account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, secrets, team IDs, billing IDs, and private object names removed"
notes = "backend fixture evidence approved for invalid Bedrock credential row"

[[evidence]]
row_id = "GUI-BILL-01"
status = "provided"
evidence_paths = ["artifacts/redacted/gui-bill-01.txt"]
cleanup_proof = "fixture reset proof captured; billing or quota fixture reset; no production state was touched"
redaction = "account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, secrets, team IDs, billing IDs, and private object names removed"
notes = "backend fixture evidence approved for billing or quota modal row"

[[evidence]]
row_id = "GUI-BILL-02"
status = "provided"
evidence_paths = ["artifacts/redacted/gui-bill-02.txt"]
cleanup_proof = "fixture reset proof captured; build-plan migration flags reset; no production state was touched"
redaction = "account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, secrets, team IDs, billing IDs, and private object names removed"
notes = "backend fixture evidence approved for build-plan migration modal row"

[[evidence]]
row_id = "GUI-CLOUD-01"
status = "provided"
evidence_paths = ["artifacts/redacted/gui-cloud-01.txt"]
cleanup_proof = "fixture reset proof captured; cloud capacity or quota fixture reset; no production state was touched"
redaction = "account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, secrets, team IDs, billing IDs, and private object names removed"
notes = "backend fixture evidence approved for cloud capacity or quota modal row"
```

Preserve every non-backend row exactly as it was.

- [ ] **Step 4: Verify backend fixture promotion**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_public_rc_evidence_report.py --json > /tmp/warp-cn-r3-evidence-report.json
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
git diff --check
```

Expected:

```text
privacy guard exits 0
evidence report JSON shows backend_fixture ready count 5
strict evidence lint may still exit 1 because isolated_account and disposable_object rows are missing
strict evidence lint does not report GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01, GUI-SET-04, or GUI-SET-05 as missing evidence
git diff --check exits 0
```

## Task 5: R3 Completion Record

**Files:**
- Create: `docs/zh-Hans-backend-fixture-r3-completion.md`
- Modify: `docs/zh-Hans-official-release-next-development-tasks.md`

- [ ] **Step 1: Create the R3 completion record**

Create `docs/zh-Hans-backend-fixture-r3-completion.md`:

````markdown
# zh-Hans Backend Fixture R3 Completion

Date: 2026-06-03

## Scope

Rows:

- `GUI-BILL-01`
- `GUI-BILL-02`
- `GUI-CLOUD-01`
- `GUI-SET-04`
- `GUI-SET-05`

## Result

```text
backend_fixture evidence rows provided: 5
backend_fixture strict-artifact errors: 0
isolated_account rows: still missing
disposable_object rows: still missing
blocker registry status: unchanged
```

## Verification

```text
privacy guard: passed
evidence report JSON: backend_fixture ready count 5
strict evidence lint: expected failure only for non-backend rows
git diff --check: passed
```

## Next Stage

```text
next: R4 isolated account evidence closure
```
````

- [ ] **Step 2: Update next-development task index**

In `docs/zh-Hans-official-release-next-development-tasks.md`, update the R3 row to show:

```text
R3: backend fixture evidence closure complete; proceed to R4 isolated account evidence closure
```

- [ ] **Step 3: Verify Task 5**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

## Deferred Work

This plan does not:

- Use an isolated account.
- Delete, transfer, create, or mutate disposable objects.
- Run GUI smoke.
- Regenerate PNG assets.
- Run heavy Rust or bundle gates.
- Modify `resources/localization/zh-Hans-public-rc-blockers.toml`.
- Create tags, push, or publish releases.

Those belong to R4-R7 follow-up plans.

## Self-Review

Spec coverage:

- R3 backend fixture rows are all covered.
- Fixture owner approval, raw evidence review, candidate preflight, approved artifact creation, ledger update, and verification are separate gates.
- Protected operations stop unless explicit approval exists.

Placeholder scan:

- No placeholder file paths are used for repository destinations.
- Candidate preflight paths are temporary `/tmp` paths.

Type and command consistency:

- Evidence ledger uses `status = "provided"`, matching `script/zh_public_rc_evidence_lint.py`.
- Backend fixture row IDs match `resources/localization/zh-Hans-public-rc-blockers.toml`.
- Approved artifact paths match the missing-action packets.
