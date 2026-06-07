# zh-Hans Official Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC38 local-use readiness to a formally releasable Simplified Chinese fork release with complete evidence, GUI, asset, build, and publication gates.

**Architecture:** Keep source-level localization state in `resources/localization/*.toml` and release evidence state in the public-RC blocker/evidence registries. Split the remaining work into independently verifiable lanes: backend fixtures, isolated account flows, disposable object flows, GUI smoke, visual assets, upstream freshness, packaging, and publication. Each lane produces reviewed redacted artifacts before any blocker or release status is promoted.

**Tech Stack:** Rust/Cargo workspace, Python localization and evidence scripts, TOML manifest/ledger files, Markdown release records, Git/GitHub release tags, heat-safe local build gates, privacy guard.

---

## Current Baseline

```text
branch: codex/zh-Hans-post-rc26-execution
version: 0.18
latest RC: 2026-06-03 RC38
decision: ready-for-local-use-with-fixture-evidence
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 8574 covered, 2 candidates, 100.0%
public-RC blockers: 11
ready evidence rows: 0
strict evidence lint: expected fail until evidence exists
```

## File Structure

- Modify `docs/zh-Hans-official-release-development-plan.md` when release criteria or lane sequencing changes.
- Modify `README.md` to keep the maintenance-doc index discoverable.
- Modify `docs/zh-Hans-localization.md` when a new RC, phase, or release lane is completed.
- Modify `resources/localization/zh-Hans-public-rc-evidence.toml` only after reviewed redacted evidence exists and explicit approval is given.
- Modify `resources/localization/zh-Hans-public-rc-blockers.toml` only when a blocker is truly cleared and strict evidence lint supports the change.
- Create `docs/zh-Hans-public-rc-backend-fixture-execution.md` for backend fixture row execution.
- Create `docs/zh-Hans-public-rc-isolated-account-execution.md` for isolated account row execution.
- Create `docs/zh-Hans-public-rc-disposable-object-execution.md` for disposable object row execution.
- Create `docs/zh-Hans-release-candidate-2026-06-03-formal.md` only during final release freeze.
- Create `docs/zh-Hans-official-release-checklist-0.19.md` only when all public-RC blockers have evidence.
- Create `docs/zh-Hans-release-notes-0.19.md` only after the version number is selected and publication is approved.
- Do not create raw screenshots, recordings, account identifiers, callback URLs, cookies, tokens, endpoint URLs, team IDs, or private object names inside the repository.
- Do not stage, commit, push, tag, or publish without explicit user approval.

### Task 1: Freeze Official Release Planning Docs

**Files:**
- Create: `docs/zh-Hans-official-release-development-plan.md`
- Create: `docs/superpowers/plans/2026-06-03-zh-Hans-official-release-plan.md`
- Modify: `README.md`

- [ ] **Step 1: Verify the current localization baseline**

Run:

```bash
git status --short --branch
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
```

Expected:

```text
branch is codex/zh-Hans-post-rc26-execution
manifest validation passed
glossary check passed
entries: 7943
dry-run reports would_change: 0
dry-run reports missing: 0
release coverage reports 8574 covered, 2 candidates, 100.0%
public-RC blocker total is 11
```

- [ ] **Step 2: Create the formal release development plan**

Create `docs/zh-Hans-official-release-development-plan.md` with these sections:

```markdown
# Warp CN 正式汉化发行版开发计划

日期：2026-06-03

## 目标定义

本计划的目标是把 Warp CN 从 `ready-for-local-use-with-fixture-evidence`
推进到可公开发布的正式汉化发行版。

## 当前基线

记录 version、RC38、manifest entries、release coverage、public-RC blockers、
ready evidence rows。

## 正式发行准入标准

列出 overlay、full audit、strict evidence lint、GUI smoke、PNG、heavy gate、
upstream freshness、release notes、tag/push approval 的准入条件。

## 工作流总览

按 Evidence Governance、Backend Fixture Lane、Isolated Account Lane、
Disposable Object Lane、GUI Smoke Lane、Visual Asset Lane、Upstream Freshness
Lane、Packaging Lane、Publication Lane 分解。

## No-Go 规则

明确禁止主账号、真实凭据、真实 billing/cloud/team mutation、原始证据入库和
未经批准发布。
```

- [ ] **Step 3: Add README discoverability**

Add this bullet to the maintenance docs section in `README.md`:

```markdown
- `docs/zh-Hans-official-release-development-plan.md`：正式汉化发行版目标、准入标准、public-RC lane 和发布路线图。
```

- [ ] **Step 4: Verify docs-only planning changes**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
privacy_guard.py exits 0
git diff --check exits 0
```

### Task 2: Create Backend Fixture Execution Doc

**Files:**
- Create: `docs/zh-Hans-public-rc-backend-fixture-execution.md`
- Modify: `docs/zh-Hans-official-release-development-plan.md`

- [ ] **Step 1: Generate backend fixture queue packets**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture > /tmp/warp-cn-backend-fixture-queue.md
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture > /tmp/warp-cn-backend-fixture-actions.md
```

Expected:

```text
/tmp/warp-cn-backend-fixture-queue.md contains GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01, GUI-SET-04, GUI-SET-05
/tmp/warp-cn-backend-fixture-actions.md contains artifact paths for those five rows
```

- [ ] **Step 2: Create backend fixture execution doc**

Create `docs/zh-Hans-public-rc-backend-fixture-execution.md` with:

```markdown
# zh-Hans Public-RC Backend Fixture Execution

## Scope

Rows: `GUI-BILL-01`, `GUI-BILL-02`, `GUI-CLOUD-01`, `GUI-SET-04`,
`GUI-SET-05`.

## Safety

Do not buy credits, attach payment methods, expose billing IDs, consume real
quota, use real AWS credentials, or enter real provider credentials.

## Evidence Commands

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
```

## Candidate Preflight

Run one row at a time against an existing reviewed redacted candidate file
outside Git:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-01 --artifact /tmp/gui-bill-01-candidate.txt --markdown
```

Repeat for `GUI-BILL-02`, `GUI-CLOUD-01`, `GUI-SET-04`, and `GUI-SET-05`.

Final approved destinations after explicit approval only:

- `artifacts/redacted/gui-bill-01.txt`
- `artifacts/redacted/gui-bill-02.txt`
- `artifacts/redacted/gui-cloud-01.txt`
- `artifacts/redacted/gui-set-04.txt`
- `artifacts/redacted/gui-set-05.txt`
```

- [ ] **Step 3: Verify backend fixture doc**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 3: Create Isolated Account Execution Doc

**Files:**
- Create: `docs/zh-Hans-public-rc-isolated-account-execution.md`
- Modify: `docs/zh-Hans-official-release-development-plan.md`

- [ ] **Step 1: Generate isolated account queue packets**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account > /tmp/warp-cn-isolated-account-queue.md
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account > /tmp/warp-cn-isolated-account-actions.md
```

Expected:

```text
/tmp/warp-cn-isolated-account-queue.md contains GUI-AUTH-01, GUI-SET-03, GUI-WS-06
/tmp/warp-cn-isolated-account-actions.md contains artifact paths for those three rows
```

- [ ] **Step 2: Create isolated account execution doc**

Create `docs/zh-Hans-public-rc-isolated-account-execution.md` with:

```markdown
# zh-Hans Public-RC Isolated Account Execution

## Scope

Rows: `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06`.

## Safety

Use only an isolated test account. Do not use the user's main account. Do not
store account identifiers, cookies, tokens, magic links, callback URLs, endpoint
URLs, or private profile names in Git.

## Evidence Commands

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account
```

## Candidate Preflight

Run one row at a time against an existing reviewed redacted candidate file
outside Git:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-AUTH-01 --artifact /tmp/gui-auth-01-candidate.txt --markdown
```

Repeat for `GUI-SET-03` and `GUI-WS-06`.

Final approved destinations after explicit approval only:

- `artifacts/redacted/gui-auth-01.txt`
- `artifacts/redacted/gui-set-03.txt`
- `artifacts/redacted/gui-ws-06.txt`
```

- [ ] **Step 3: Verify isolated account doc**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Create Disposable Object Execution Doc

**Files:**
- Create: `docs/zh-Hans-public-rc-disposable-object-execution.md`
- Modify: `docs/zh-Hans-official-release-development-plan.md`

- [ ] **Step 1: Generate disposable object queue packets**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object > /tmp/warp-cn-disposable-object-queue.md
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object > /tmp/warp-cn-disposable-object-actions.md
```

Expected:

```text
/tmp/warp-cn-disposable-object-queue.md contains GUI-SET-06, GUI-WS-04, GUI-WS-07
/tmp/warp-cn-disposable-object-actions.md contains artifact paths for those three rows
```

- [ ] **Step 2: Create disposable object execution doc**

Create `docs/zh-Hans-public-rc-disposable-object-execution.md` with:

```markdown
# zh-Hans Public-RC Disposable Object Execution

## Scope

Rows: `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07`.

## Safety

Cancel first. Delete, transfer, or mutate only exact allowlisted disposable
objects after explicit approval. Do not touch real teams, secrets, endpoints, or
environments.

## Allowlisted Names

- `zh-smoke-delete-environment`
- `zh-smoke-delete-secret`
- `zh-smoke-public-rc-team`

## Evidence Commands

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
```

## Candidate Preflight

Run one row at a time against an existing reviewed redacted candidate file
outside Git:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-06 --artifact /tmp/gui-set-06-candidate.txt --markdown
```

Repeat for `GUI-WS-04` and `GUI-WS-07`.

Final approved destinations after explicit approval only:

- `artifacts/redacted/gui-set-06.txt`
- `artifacts/redacted/gui-ws-04.txt`
- `artifacts/redacted/gui-ws-07.txt`
```

- [ ] **Step 3: Verify disposable object doc**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

## Deferred Follow-Up Plans

This execution plan intentionally stops after R1/R2 documentation. The following
work requires reviewed evidence or explicit approval and must be split into
separate follow-up plans before execution:

- Evidence ledger promotion for reviewed redacted artifacts.
- Public-RC blocker status changes.
- GUI launch, current-cycle smoke evidence, PNG asset changes, Rust heavy gate,
  and bundle refresh.
- Version bump, release notes, tag creation, push, or GitHub release.

Do not use this plan to mutate `resources/localization/zh-Hans-public-rc-evidence.toml`,
mutate `resources/localization/zh-Hans-public-rc-blockers.toml`, create
`artifacts/redacted/` files, run GUI evidence collection, or publish a release.

## Self-Review

Spec coverage:

- Formal release planning is covered by Task 1 and the roadmap document.
- R2 public-RC lane preparation is covered by Tasks 2, 3, and 4.
- Safety boundaries are covered in every lane execution document.
- Evidence promotion, GUI, asset, heavy gate, and publication are explicitly deferred.

Placeholder scan:

- No placeholder markers or unspecified artifact names remain.
- Future release records use a concrete filename in this plan.

Type and command consistency:

- All referenced scripts exist in the current repository.
- Evidence row IDs match `resources/localization/zh-Hans-public-rc-blockers.toml`.
- The app package command uses `cargo check -p warp`, not the obsolete `cargo check -p app`.
