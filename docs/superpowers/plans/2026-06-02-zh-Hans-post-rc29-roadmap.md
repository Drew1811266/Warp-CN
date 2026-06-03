# zh-Hans Post-RC29 Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC29 local-use readiness toward a public-RC candidate without overheating the local machine or mutating unsafe external state.

**Architecture:** Treat the localization overlay as already clean and shift work to evidence recovery, public-RC prerequisite clearing, and optional upstream ancestry alignment. Every phase writes a standalone `docs/zh-Hans-localization-phaseNNN.md` record with an explicit qualification review before continuing.

**Tech Stack:** Git, Python localization scripts, Rust/Cargo for Warp validation, macOS bundle/GUI smoke, Computer Use for accessibility evidence, Markdown evidence records.

---

## Current Baseline

RC29 status:

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
onboarding PNGs: 54 total, 50 deferred visual-residue assets
upstream stable source-tree parity: yes
upstream stable ancestry containment: no
```

Heat-safety rule:

```text
Run heavy Rust, bundle, or GUI commands only after two load probes 60 seconds apart.
Continue heavy work only if load average is below 2.50 on both probes and no desktop/security/helper process is already consuming sustained high CPU.
When the threshold is not met, record a qualified heat-safety defer and continue to the next non-heavy phase.
```

## File Structure

- Create `docs/zh-Hans-localization-phase212.md` through `docs/zh-Hans-localization-phase219.md` for post-RC29 execution evidence.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc30.md` only after Phase 219 freeze.
- Modify `README.md` only during Phase 219 if RC30 is frozen.
- Modify `docs/zh-Hans-localization.md` only during Phase 219 if RC30 is frozen.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` when GUI, public-RC, or PNG status changes.
- Modify `docs/zh-Hans-upstream-sync.md` only if upstream ancestry policy or branch execution changes.
- Do not modify `resources/localization/zh-Hans-overrides.toml` unless a phase finds real source-string drift.
- Do not modify `app/assets/async/png/onboarding/**/*.png` unless the user explicitly approves the asset-only branch.
- Do not stage, commit, push, merge, rebase, or mutate tags unless the user explicitly asks for publication or integration.

### Task 1: Phase 212 Branch Hygiene And Evidence Index

**Files:**
- Create: `docs/zh-Hans-localization-phase212.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect current worktree scope**

Run:

```bash
git status --short --branch
git diff --stat
git diff --check
```

Expected:

```text
git diff --check exits 0
worktree shows RC27-RC29 evidence docs and existing documentation updates
no PNG or account/backend artifact is dirty
```

- [ ] **Step 2: Confirm no tracked secret or raw GUI artifact slipped in**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git status --short -- '*.png' 'docs/gui-smoke-artifacts/**'
```

Expected:

```text
privacy_guard.py exits 0
PNG/artifact status is empty unless a prior approved evidence file is intentionally tracked
```

- [ ] **Step 3: Write Phase 212 record**

Create `docs/zh-Hans-localization-phase212.md` with this structure:

```markdown
# zh-Hans Localization Phase 212

Date: 2026-06-02

## Scope

Phase 212 audits the post-RC29 evidence branch before any new execution.

This phase does not stage, commit, push, merge, rebase, create a worktree,
mutate tags, build a bundle, launch GUI, use accounts, create backend fixtures,
touch billing/cloud state, or modify PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
git diff --check: passed
privacy guard: passed
PNG/artifact dirtiness: none
```

## Decision

```text
decision: keep-current-branch-as-evidence-branch
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 212
status: qualified-branch-hygiene
safe to continue to Phase 213: yes
```
```

- [ ] **Step 4: Update localization index**

In `docs/zh-Hans-localization.md`, add one status bullet after the RC29 bullet:

```markdown
- Phase 212 records post-RC29 branch hygiene and confirms that integration or publication requires explicit user approval.
```

- [ ] **Step 5: Verify Task 1**

Run:

```bash
git diff --check
python3 script/privacy_guard.py --all-tracked
```

Expected:

```text
both commands exit 0
```

### Task 2: Phase 213 Quiet-Window Heavy Validation

**Files:**
- Create: `docs/zh-Hans-localization-phase213.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Capture two load probes**

Run:

```bash
printf 'probe_time_1='; date '+%Y-%m-%d %H:%M:%S %Z'
pgrep -afil 'cargo|rustc|warp-oss|terminal-server|script/run|WarpOss.app' || true
uptime
pmset -g therm 2>/dev/null || true
ps -axo pid,pcpu,comm | sort -nr -k2 | head -n 12
sleep 60
printf 'probe_time_2='; date '+%Y-%m-%d %H:%M:%S %Z'
pgrep -afil 'cargo|rustc|warp-oss|terminal-server|script/run|WarpOss.app' || true
uptime
pmset -g therm 2>/dev/null || true
ps -axo pid,pcpu,comm | sort -nr -k2 | head -n 12
```

Expected safe condition:

```text
load averages stay below 2.50 on both probes
no cargo/rustc/warp process is already active
no thermal or performance warning is recorded
top CPU list does not show sustained desktop/security/helper pressure
```

- [ ] **Step 2: If probes are unsafe, write heat-safety defer**

Create `docs/zh-Hans-localization-phase213.md`:

```markdown
# zh-Hans Localization Phase 213

Date: 2026-06-02

## Scope

Phase 213 checks whether RC30 heavy validation can run safely.

## Decision

```text
decision: skip-heavy-validation-for-heat-safety
Rust compile: not run
bundle build: not run
GUI launch: not run
```

## Qualification Review

```text
phase: 213
status: qualified-heavy-gate-deferred
safe to continue to Phase 214: yes
```
```

- [ ] **Step 3: If probes are safe, run serial Rust validation**

Run:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

Expected:

```text
command exits 0
warnings are recorded as existing warnings unless new errors appear
```

- [ ] **Step 4: If Rust validation passes, run fresh bundle**

Run:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
target/debug/bundle/osx/WarpOss.app is created or refreshed
command exits 0
```

- [ ] **Step 5: Record Phase 213 result**

If Step 3 and Step 4 passed, create `docs/zh-Hans-localization-phase213.md` with:

```markdown
# zh-Hans Localization Phase 213

Date: 2026-06-02

## Decision

```text
decision: heavy-validation-passed
Rust compile: passed
fresh bundle: passed
```

## Qualification Review

```text
phase: 213
status: qualified-heavy-gate-passed
safe to continue to Phase 214: yes
```
```

- [ ] **Step 6: Update GUI matrix**

Append to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## 2026-06-02 P213 heavy validation

Phase 213 status: `qualified-heavy-gate-passed` or `qualified-heavy-gate-deferred`.

- Two load probes were captured before heavy validation.
- Rust compile and bundle status are recorded in `docs/zh-Hans-localization-phase213.md`.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was touched.
```

- [ ] **Step 7: Verify Task 2**

Run:

```bash
git diff --check
```

Expected:

```text
command exits 0
```

### Task 3: Phase 214 No-Account Current-Cycle GUI Smoke

**Files:**
- Create: `docs/zh-Hans-localization-phase214.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Check Phase 213 dependency**

Run:

```bash
rg -n "fresh bundle: passed|bundle build: not run|fresh bundle: not run" docs/zh-Hans-localization-phase213.md
```

Expected:

```text
continue GUI only if Phase 213 says fresh bundle passed
otherwise write a no-fresh-bundle defer
```

- [ ] **Step 2: If no fresh bundle exists, write Phase 214 defer**

Create `docs/zh-Hans-localization-phase214.md`:

```markdown
# zh-Hans Localization Phase 214

Date: 2026-06-02

## Decision

```text
decision: skip-no-account-gui-smoke-no-fresh-bundle
GUI launch: not run
rows promoted: none
```

## Qualification Review

```text
phase: 214
status: qualified-gui-smoke-deferred
safe to continue to Phase 215: yes
```
```

- [ ] **Step 3: If fresh bundle exists, launch no-account GUI**

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

- [ ] **Step 4: Capture safe GUI anchors**

Use Computer Use to inspect `WarpOss`. Record only redacted text anchors in the phase doc. Do not save raw full-screen screenshots.

Expected anchors:

```text
Chinese menu labels such as 文件, 编辑, 视图, 标签页, 窗口, 帮助
one no-account shell or onboarding anchor if visible
no account identifiers, tokens, callback URLs, or private team names
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

- [ ] **Step 6: Write Phase 214 result**

Create `docs/zh-Hans-localization-phase214.md` with:

```markdown
# zh-Hans Localization Phase 214

Date: 2026-06-02

## Decision

```text
decision: no-account-gui-smoke-passed
GUI launch: passed
safe anchors: recorded
public-RC rows promoted: none
```

## Qualification Review

```text
phase: 214
status: qualified-no-account-gui-smoke
safe to continue to Phase 215: yes
```
```

- [ ] **Step 7: Update GUI matrix and verify**

Append the Phase 214 outcome to `docs/zh-Hans-gui-smoke-matrix.md`, then run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Phase 215 Isolated Account Prerequisite Gate

**Files:**
- Create: `docs/zh-Hans-localization-phase215.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Read: `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`
- Read: `resources/localization/zh-Hans-public-rc-blockers.toml`

- [ ] **Step 1: Recheck isolated account blocker rows**

Run:

```bash
python3 script/zh_public_rc_status.py
rg -n "GUI-AUTH-01|GUI-SET-03|GUI-WS-06" resources/localization/zh-Hans-public-rc-blockers.toml docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md
```

Expected:

```text
GUI-AUTH-01, GUI-SET-03, and GUI-WS-06 remain blocked unless an isolated account is explicitly provided
```

- [ ] **Step 2: If no isolated account is provided, write safe blocker record**

Create `docs/zh-Hans-localization-phase215.md`:

```markdown
# zh-Hans Localization Phase 215

Date: 2026-06-02

## Decision

```text
decision: isolated-account-prerequisites-still-blocked
GUI-AUTH-01: blocked-no-isolated-account
GUI-SET-03: blocked-no-isolated-account
GUI-WS-06: blocked-no-isolated-account
account used: none
```

## Qualification Review

```text
phase: 215
status: qualified-isolated-account-blocked
safe to continue to Phase 216: yes
```
```

- [ ] **Step 3: If an isolated account is explicitly provided, run only non-destructive login smoke**

Before any login interaction, confirm the account is not the user's main account and has no production billing/team ownership risk. Then run the documented login path from `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`.

Expected evidence:

```text
redacted login/callback GUI anchors
redacted Settings > AI anchors
logout or profile cleanup proof
no real endpoint, API key, team ownership, billing, or production object mutation
```

- [ ] **Step 4: Verify Task 4**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_public_rc_status.py
git diff --check
```

Expected:

```text
privacy and diff checks exit 0
public-RC status reflects either unchanged blockers or documented registry updates with matching evidence
```

### Task 5: Phase 216 Backend Fixture Contract Gate

**Files:**
- Create: `docs/zh-Hans-localization-phase216.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Read: `docs/zh-Hans-backend-fixture-contract-rc19.md`
- Read: `resources/localization/zh-Hans-public-rc-blockers.toml`

- [ ] **Step 1: Recheck backend fixture blocker rows**

Run:

```bash
python3 script/zh_public_rc_status.py
rg -n "GUI-SET-04|GUI-SET-05|GUI-BILL-01|GUI-BILL-02|GUI-CLOUD-01" resources/localization/zh-Hans-public-rc-blockers.toml docs/zh-Hans-backend-fixture-contract-rc19.md
```

Expected:

```text
five backend fixture rows remain blocked unless a safe fixture is explicitly provided
```

- [ ] **Step 2: If no safe fixture is provided, write blocker record**

Create `docs/zh-Hans-localization-phase216.md`:

```markdown
# zh-Hans Localization Phase 216

Date: 2026-06-02

## Decision

```text
decision: backend-fixture-prerequisites-still-blocked
GUI-SET-04: blocked-no-backend-fixture
GUI-SET-05: blocked-no-backend-fixture
GUI-BILL-01: blocked-no-backend-fixture
GUI-BILL-02: blocked-no-backend-fixture
GUI-CLOUD-01: blocked-no-backend-fixture
fixture used: none
```

## Qualification Review

```text
phase: 216
status: qualified-backend-fixture-blocked
safe to continue to Phase 217: yes
```
```

- [ ] **Step 3: If fixture is provided, validate it before GUI use**

Run only fixture-local checks defined by `docs/zh-Hans-backend-fixture-contract-rc19.md`. Do not enter real credentials.

Expected evidence:

```text
fixture name and scope are documented
fixture reset path is documented
no real AWS, billing, quota, or cloud capacity state is used
```

- [ ] **Step 4: Verify Task 5**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_public_rc_status.py
git diff --check
```

Expected:

```text
privacy and diff checks exit 0
public-RC status matches evidence
```

### Task 6: Phase 217 Disposable Object Gate

**Files:**
- Create: `docs/zh-Hans-localization-phase217.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Read: `docs/zh-Hans-backend-fixture-contract-rc19.md`
- Read: `resources/localization/zh-Hans-public-rc-blockers.toml`

- [ ] **Step 1: Recheck disposable object blocker rows**

Run:

```bash
python3 script/zh_public_rc_status.py
rg -n "GUI-SET-06|GUI-WS-04|GUI-WS-07|zh-smoke-delete-environment|zh-smoke-delete-secret|zh-smoke-public-rc-team" resources/localization/zh-Hans-public-rc-blockers.toml docs/zh-Hans-backend-fixture-contract-rc19.md
```

Expected:

```text
three disposable object rows remain blocked unless exact allowlisted disposable objects are provided
```

- [ ] **Step 2: If no disposable object approval exists, write blocker record**

Create `docs/zh-Hans-localization-phase217.md`:

```markdown
# zh-Hans Localization Phase 217

Date: 2026-06-02

## Decision

```text
decision: disposable-object-prerequisites-still-blocked
GUI-SET-06: blocked-no-disposable-object
GUI-WS-04: blocked-no-disposable-object
GUI-WS-07: blocked-no-disposable-object
object mutation: none
```

## Qualification Review

```text
phase: 217
status: qualified-disposable-object-blocked
safe to continue to Phase 218: yes
```
```

- [ ] **Step 3: If approval exists, verify exact object names before interaction**

Use only these names:

```text
environment: zh-smoke-delete-environment
managed secret: zh-smoke-delete-secret
owner test team: zh-smoke-public-rc-team
```

Expected before destructive GUI interaction:

```text
object exists and is disposable
cleanup path is documented
user explicitly approved cancel/delete or transfer test
```

- [ ] **Step 4: Verify Task 6**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_public_rc_status.py
git diff --check
```

Expected:

```text
privacy and diff checks exit 0
public-RC status matches evidence
```

### Task 7: Phase 218 PNG Asset Branch Decision

**Files:**
- Create: `docs/zh-Hans-localization-phase218.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Read: `docs/zh-Hans-onboarding-visual-regeneration-plan.md`
- Read: `docs/zh-Hans-onboarding-visual-script-package.md`
- Read: `docs/zh-Hans-onboarding-asset-authorization-rc20.md`

- [ ] **Step 1: Recheck PNG dirtiness and inventory**

Run:

```bash
git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
find app/assets/async/png/onboarding -name '*.png' | wc -l
```

Expected:

```text
PNG status is empty
PNG diff is empty
onboarding PNG count is 54
```

- [ ] **Step 2: If no design/product approval exists, write defer**

Create `docs/zh-Hans-localization-phase218.md`:

```markdown
# zh-Hans Localization Phase 218

Date: 2026-06-02

## Decision

```text
decision: defer-png-asset-branch
accepted decorative/brand assets: 4
deferred visual-residue assets: 50
PNG modified: no
```

## Qualification Review

```text
phase: 218
status: qualified-png-asset-branch-deferred
safe to continue to Phase 219: yes
```
```

- [ ] **Step 3: If approval exists, create asset-only branch**

Run only after explicit user approval:

```bash
git switch -c codex/zh-Hans-onboarding-assets-rc30
```

Expected:

```text
new branch is codex/zh-Hans-onboarding-assets-rc30
dirty scope is limited to app/assets/async/png/onboarding/**/*.png plus required evidence docs
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

### Task 8: Phase 219 RC30 Freeze

**Files:**
- Create: `docs/zh-Hans-localization-phase219.md`
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc30.md`
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
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py
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
cargo fmt --check exits 0
git diff --check exits 0
```

- [ ] **Step 2: Record heavy gate status from Phase 213**

Run:

```bash
rg -n "Rust compile|fresh bundle|GUI launch|status:" docs/zh-Hans-localization-phase213.md docs/zh-Hans-localization-phase214.md
```

Expected:

```text
RC30 release record accurately says whether heavy and GUI gates passed or were heat-safety deferred
```

- [ ] **Step 3: Create RC30 release record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc30.md` with these sections:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC30

Date: 2026-06-02

## Scope

RC30 covers Phases 212 through 219.

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
```

## Public-RC Status

```text
public-RC blockers: 11 unless Phase 215, 216, or 217 provides matching evidence and registry updates
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready unless all blockers, fresh bundle, GUI, and PNG/asset evidence are cleared
```
```

- [ ] **Step 4: Update README and localization index**

Update `README.md`:

```text
最后核验记录：`2026-06-02 RC30`
```

Update `docs/zh-Hans-localization.md`:

```markdown
Last verified release audit: 2026-06-02 RC30, generated on 2026-06-02 Asia/Shanghai.

- RC30 decision: `ready-for-local-use-with-fixture-evidence`; public RC remains blocked unless Phase 215 through Phase 218 cleared every required evidence gate.
```

- [ ] **Step 5: Create Phase 219 freeze record**

Create `docs/zh-Hans-localization-phase219.md`:

```markdown
# zh-Hans Localization Phase 219

Date: 2026-06-02

## Decision

```text
decision: rc30-freeze
public RC: not ready unless all evidence gates passed
```

## Qualification Review

```text
phase: 219
status: qualified-rc30-freeze
all roadmap phases complete: yes
```
```

- [ ] **Step 6: Final verification**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 script/privacy_guard.py --all-tracked
git diff --check
git status --short --branch
```

Expected:

```text
validation passes
dry-run would_change is 0
dry-run missing is 0
public-RC blocker total is explicit
privacy guard exits 0
diff check exits 0
status shows only planned documentation/evidence changes unless explicitly approved source or asset work happened
```

## Self-Review

Spec coverage:

```text
post-RC29 branch hygiene: Task 1
low-load heavy validation: Task 2
GUI evidence recovery: Task 3
isolated account blockers: Task 4
backend fixture blockers: Task 5
disposable object blockers: Task 6
PNG asset branch decision: Task 7
RC30 freeze: Task 8
```

Placeholder scan:

```text
No task uses placeholder markers or undefined external code.
All commands and expected outcomes are explicit.
```

Risk boundary:

```text
No stage/commit/push/merge/rebase/tag mutation is planned without explicit user approval.
No real account, billing, cloud, secret, endpoint, or team state is touched unless the matching prerequisite is explicitly provided and documented.
```
