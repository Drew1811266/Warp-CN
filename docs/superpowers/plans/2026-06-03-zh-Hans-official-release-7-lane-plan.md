# zh-Hans Official Release 7-Lane Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute the seven formal-release lanes needed to move Warp CN from RC38 local-use readiness to a releasable Simplified Chinese fork release.

**Architecture:** Treat public GitHub as a routing record only and keep sensitive approval, raw evidence, account data, and object details outside Git. Each lane produces a concrete artifact: private approval references, reviewed redacted evidence, closed blocker rows, prepared isolated/disposable test objects, translation quality gates, packaging gates, and final release material.

**Tech Stack:** Markdown runbooks, Python localization/evidence scripts, TOML evidence ledgers, Rust/Cargo build gates, Git/GitHub release tooling.

---

## File Structure

- Modify `README.md` to expose the 7-lane guide in the maintenance-doc index.
- Create `docs/zh-Hans-official-release-7-lane-development-guide.md` as the human-facing execution guide.
- Create this plan at `docs/superpowers/plans/2026-06-03-zh-Hans-official-release-7-lane-plan.md`.
- Do not modify `resources/localization/zh-Hans-public-rc-evidence.toml` until reviewed redacted evidence exists.
- Do not modify `resources/localization/zh-Hans-public-rc-blockers.toml` until strict artifact lint supports blocker closure.
- Do not create `artifacts/redacted/*` from this planning task.

### Task 1: Publish the 7-Lane Development Guide

**Files:**
- Create: `docs/zh-Hans-official-release-7-lane-development-guide.md`
- Modify: `README.md`

- [ ] **Step 1: Check current workspace state**

Run:

```bash
git status --short --branch
```

Expected:

```text
branch is codex/zh-Hans-post-rc26-execution
workspace may already contain uncommitted release-planning docs
```

- [ ] **Step 2: Create the guide**

Create `docs/zh-Hans-official-release-7-lane-development-guide.md` with sections for:

```text
purpose
current baseline
formal release completion criteria
lane overview
Lane 1 private approval routing
Lane 2 evidence and redaction
Lane 3 blocker row closure
Lane 4 isolated account and disposable object preparation
Lane 5 translation completeness and quality
Lane 6 packaging and release engineering
Lane 7 release notes and acceptance
recommended execution order
Subagent-Driven dispatch matrix
global no-go rules
```

- [ ] **Step 3: Add README entry**

Add this bullet under `## 维护文档` in `README.md`:

```markdown
- `docs/zh-Hans-official-release-7-lane-development-guide.md`：正式汉化发行版 7 条 lane 的执行入口，覆盖私有审批、证据脱敏、blocker 关闭、测试环境、翻译质量、打包发布和最终验收。
```

- [ ] **Step 4: Verify docs-only changes**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
privacy_guard exits 0
git diff --check exits 0
```

### Task 2: Execute Lane 1 Private Approval Routing

**Files:**
- Read: `docs/zh-Hans-official-release-7-lane-development-guide.md`
- Read: `/tmp/warp-cn-backend-fixture-intake/owner-approval-request.md`
- Read: `/tmp/warp-cn-backend-fixture-intake/intake-readme.md`

- [ ] **Step 1: Confirm public routing record**

Run:

```bash
gh issue view 12129 --repo warpdotdev/warp --comments --json state,comments,url
```

Expected:

```text
latest comments confirm this is not a public Warp client bug
routing recommends private support/internal owner channels
```

- [ ] **Step 2: Prepare private support request**

Use the body from:

```text
/tmp/warp-cn-backend-fixture-intake/owner-approval-request.md
```

Prepend this routing note before sending through the private channel:

```text
Public GitHub issue #12129 confirmed this is not a public Warp client bug and
should be routed through private support/internal owner channels. No raw fixture
data, account identifiers, backend object details, or evidence should be shared
in GitHub.
```

- [ ] **Step 3: Record only the redacted approval reference**

After the private channel responds, record only this shape in a follow-up release
doc or status note:

```text
approval_channel: private-support-or-internal-owner
approval_reference: <case-id-or-redacted-thread-reference>
approved_rows: GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01, GUI-SET-04, GUI-SET-05
raw_evidence_review_required: true
redacted_artifact_review_required: true
cleanup_proof_required: true
```

Do not commit raw support messages or sensitive owner content.

### Task 3: Execute Lane 2 Evidence and Redaction

**Files:**
- Read: `docs/zh-Hans-evidence-policy.md`
- Read: `docs/zh-Hans-official-release-7-lane-development-guide.md`
- Future modify only after approval: `artifacts/redacted/*.txt`

- [ ] **Step 1: Create Git-outside candidates only after approval**

Expected candidate paths:

```text
/tmp/gui-auth-01-candidate.txt
/tmp/gui-set-03-candidate.txt
/tmp/gui-ws-06-candidate.txt
/tmp/gui-set-06-candidate.txt
/tmp/gui-ws-04-candidate.txt
/tmp/gui-ws-07-candidate.txt
/tmp/gui-bill-01-candidate.txt
/tmp/gui-bill-02-candidate.txt
/tmp/gui-cloud-01-candidate.txt
/tmp/gui-set-04-candidate.txt
/tmp/gui-set-05-candidate.txt
```

- [ ] **Step 2: Preflight each candidate**

Run:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-AUTH-01 --artifact /tmp/gui-auth-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-03 --artifact /tmp/gui-set-03-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-06 --artifact /tmp/gui-ws-06-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-06 --artifact /tmp/gui-set-06-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-04 --artifact /tmp/gui-ws-04-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-07 --artifact /tmp/gui-ws-07-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-01 --artifact /tmp/gui-bill-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-02 --artifact /tmp/gui-bill-02-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-CLOUD-01 --artifact /tmp/gui-cloud-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-04 --artifact /tmp/gui-set-04-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /tmp/gui-set-05-candidate.txt --markdown
```

Expected:

```text
each row returns candidate-ready-for-human-review or equivalent accepted status
any rejected row stops that row until fixed
```

- [ ] **Step 3: Promote only reviewed redacted artifacts**

Allowed Git paths after review:

```text
artifacts/redacted/gui-auth-01.txt
artifacts/redacted/gui-set-03.txt
artifacts/redacted/gui-ws-06.txt
artifacts/redacted/gui-set-06.txt
artifacts/redacted/gui-ws-04.txt
artifacts/redacted/gui-ws-07.txt
artifacts/redacted/gui-bill-01.txt
artifacts/redacted/gui-bill-02.txt
artifacts/redacted/gui-cloud-01.txt
artifacts/redacted/gui-set-04.txt
artifacts/redacted/gui-set-05.txt
```

### Task 4: Execute Lane 3 Blocker Row Closure

**Files:**
- Modify after reviewed evidence only: `resources/localization/zh-Hans-public-rc-evidence.toml`
- Modify after strict lint supports closure only: `resources/localization/zh-Hans-public-rc-blockers.toml`

- [ ] **Step 1: Review current blocker queues**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
```

Expected:

```text
backend_fixture: GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01, GUI-SET-04, GUI-SET-05
isolated_account: GUI-AUTH-01, GUI-SET-03, GUI-WS-06
disposable_object: GUI-SET-06, GUI-WS-04, GUI-WS-07
```

- [ ] **Step 2: Update evidence ledger only with reviewed artifacts**

For each row, update `resources/localization/zh-Hans-public-rc-evidence.toml`
with the exact artifact path, redaction reviewer, cleanup proof reference, and
status required by the existing ledger schema.

- [ ] **Step 3: Verify blocker closure**

Run:

```bash
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py --json
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected after all 11 rows are complete:

```text
strict artifact lint exits 0
privacy guard exits 0
git diff --check exits 0
```

### Task 5: Execute Lane 4 Isolated Account and Disposable Object Preparation

**Files:**
- Read: `docs/zh-Hans-public-rc-isolated-account-execution.md`
- Read: `docs/zh-Hans-public-rc-disposable-object-execution.md`
- Read: `docs/zh-Hans-public-rc-independent-lanes-execution.md`

- [ ] **Step 1: Verify isolated account packet requirements**

Required text:

```text
isolated account is not the user's main account
login flow is approved for public-RC evidence capture
Settings > AI visibility is approved
custom inference endpoint test object is named zh-smoke-delete-endpoint
logout or profile cleanup proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

- [ ] **Step 2: Verify disposable object packet requirements**

Required text:

```text
object exists and is disposable
object name exactly matches the allowlist
cancel-first path is approved
delete or transfer path is explicitly approved
cleanup absence or restoration proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

- [ ] **Step 3: Confirm no real object will be touched**

Allowed object names only:

```text
zh-smoke-delete-environment
zh-smoke-delete-secret
zh-smoke-public-rc-team
zh-smoke-delete-endpoint
```

Expected:

```text
no personal account
no real team
no real secret
no real environment
no real endpoint
no real billing or cloud capacity mutation
```

### Task 6: Execute Lane 5 Translation Completeness and Quality

**Files:**
- Read: `resources/localization/zh-Hans-overrides.toml`
- Read: `resources/localization/zh-Hans-glossary.toml`
- Read: `docs/zh-Hans-translation-rescan-2026-06-03.md`

- [ ] **Step 1: Run localization quality gates**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_public_rc_evidence_candidate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py
```

Expected before evidence closure:

```text
manifest and glossary pass
dry-run would_change: 0
dry-run missing: 0
release coverage: 100.0%
strict artifact lint fails only because evidence is still missing
unit tests pass
```

Expected after evidence closure:

```text
all commands exit 0
```

### Task 7: Execute Lane 6 Packaging and Release Engineering

**Files:**
- Read: `docs/zh-Hans-packaging-preflight-2026-06-03.md`
- Future create after execution: `docs/zh-Hans-release-candidate-2026-06-03-formal.md`

- [ ] **Step 1: Run low-load gate**

Run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Expected:

```text
decision: run-heavy-gate
```

- [ ] **Step 2: Run heavy gate only after explicit approval**

Run:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
cargo check exits 0
bundle command exits 0
privacy guard exits 0
git diff --check exits 0
```

### Task 8: Execute Lane 7 Release Notes and Acceptance

**Files:**
- Read: `docs/zh-Hans-release-notes-0.19-draft.md`
- Create after all gates pass: `docs/zh-Hans-release-notes-0.19.md`
- Create after all gates pass: `docs/zh-Hans-official-release-checklist-0.19.md`
- Modify after all gates pass: `README.md`

- [ ] **Step 1: Promote release notes draft only after all gates pass**

Required final fields:

```text
scope: Simplified Chinese localization fork
not official Warp release: true
source overlay status: clean
public-RC evidence status: complete
backend fixture approval: private route, redacted reference only
GUI smoke status: complete
packaging status: complete
known limitations: upstream official i18n still pending
support boundary: Warp official services remain upstream-controlled
```

- [ ] **Step 2: Verify final go/no-go checklist**

Required pass list:

```text
manifest validation: pass
glossary check: pass
dry-run would_change: 0
dry-run missing: 0
release inventory: 100.0%
public-RC evidence strict lint: pass
privacy guard: pass
unit tests: pass
low-load gate: pass
cargo check: pass
bundle build: pass
GUI launch: pass
release notes: final
README status: final
tag approval: explicit user approval
push approval: explicit user approval
GitHub release approval: explicit user approval
```

- [ ] **Step 3: Run publication commands only after explicit user approval**

Commands that require explicit approval:

```bash
git tag 0.19
git push github main
git push github 0.19
gh release create 0.19
```

Expected:

```text
tag, remote branch, remote tag, and GitHub release point to the same approved release state
```
