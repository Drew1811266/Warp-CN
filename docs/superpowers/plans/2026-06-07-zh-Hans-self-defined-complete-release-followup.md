# zh-Hans Self-Defined Complete Release Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the remaining Warp CN 0.19 self-defined Simplified Chinese localization release work after removing the low-load development constraint.

**Architecture:** Keep the existing public-RC evidence registry intact and finish a separate self-defined release path. Run heavy validation directly, document GUI smoke and known limitations, then freeze release notes and checklist without publishing until the user explicitly approves tag, push, and GitHub release actions.

**Tech Stack:** Rust workspace, Python localization validation scripts, TOML localization manifests, macOS GUI smoke workflow, Markdown release documentation, GitHub release preparation.

---

## File Structure

- Create: `docs/zh-Hans-packaging-preflight-2026-06-07.md`
  - Records direct heavy validation after the low-load constraint was cancelled.
- Modify: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`
  - Updates packaging, GUI, and publication gate state.
- Modify: `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`
  - Records current-cycle GUI smoke results without private raw evidence.
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
  - Keeps GUI scope and known limitations aligned with current evidence.
- Modify: `docs/zh-Hans-onboarding-visual-regeneration-plan.md`
  - Records onboarding static asset replacement or limitation decision.
- Modify: `docs/zh-Hans-release-notes-0.19-draft.md`
  - Freezes release wording, scope, and known limitations.
- Inspect only: `resources/localization/zh-Hans-public-rc-blockers.toml`
  - Do not clear or rewrite public-RC blockers for this self-defined release.
- Inspect only: `resources/localization/zh-Hans-public-rc-evidence.toml`
  - Do not mark evidence `provided` without reviewed evidence.

### Task 1: Direct Heavy Validation Preflight

**Files:**
- Create: `docs/zh-Hans-packaging-preflight-2026-06-07.md`
- Modify: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`

- [ ] **Step 1: Run privacy and whitespace preflight**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
privacy_guard: pass
diff_check: pass
```

- [ ] **Step 2: Run Rust workspace package check directly**

Run:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

Expected:

```text
Finished `dev` profile
```

If it fails, copy only the non-secret command summary and the first actionable compiler error into `docs/zh-Hans-packaging-preflight-2026-06-07.md`. Do not paste tokens, account identifiers, private URLs, or local-only secrets.

- [ ] **Step 3: Run local launch command directly**

Run:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
launch_check: pass
```

If the command prints a different success marker, record the exact non-secret success line in the preflight document. If it fails, record the non-secret failure summary and create a follow-up repair row in the checklist.

- [ ] **Step 4: Create the 2026-06-07 preflight record**

Create `docs/zh-Hans-packaging-preflight-2026-06-07.md` with this structure:

````markdown
# zh-Hans Packaging Preflight - 2026-06-07

## Scope

Warp CN 0.19 self-defined complete release packaging preflight after the low-load development constraint was cancelled.

## Commands

```text
python3 script/privacy_guard.py --all-tracked
git diff --check
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

## Result

```text
privacy_guard: pass
diff_check: pass
cargo_check: pass
launch_check: pass
```

## Notes

Low-load gate is not required for this run after the 2026-06-07 policy update.
````

If a command fails, keep the passing lines and set the failed line to the exact blocked status below:

```text
cargo_check: blocked-with-actionable-error
launch_check: blocked-with-actionable-error
```

- [ ] **Step 5: Update checklist packaging state**

In `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`, set `cargo_check` and `bundle_or_launch` to the actual result:

```text
cargo_check: pass
bundle_or_launch: pass
```

If either command fails, use:

```text
cargo_check: blocked-with-actionable-error
bundle_or_launch: blocked-with-actionable-error
```

### Task 2: Current-Cycle GUI Smoke

**Files:**
- Modify: `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Modify: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`

- [ ] **Step 1: Launch the app for manual smoke**

Run:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected: Warp launches or prepares the app without requiring private account credentials.

- [ ] **Step 2: Validate app launch**

Inspect the launch screen. Update the GUI index row:

```markdown
| GUI-SD-01 | App launch | pass | current-cycle reviewer note: launch screen Chinese copy readable; no obvious layout break |
```

If launch fails, use:

```markdown
| GUI-SD-01 | App launch | blocked-with-reason | current-cycle reviewer note: launch blocked by packaging preflight failure recorded in `docs/zh-Hans-packaging-preflight-2026-06-07.md` |
```

- [ ] **Step 3: Validate workspace shell and tabs**

Inspect workspace shell, tab labels, and command output surroundings. Update the GUI index row:

```markdown
| GUI-SD-03 | Workspace shell | pass | current-cycle reviewer note: shell chrome, tabs, and nearby actions Chinese copy readable |
```

- [ ] **Step 4: Validate command palette**

Open the command palette and inspect search input, empty state, and visible result rows. Update the GUI index row:

```markdown
| GUI-SD-04 | Command palette | pass | current-cycle reviewer note: command palette visible strings readable; no obvious truncation |
```

- [ ] **Step 5: Validate Settings core pages**

Inspect core Settings pages that do not require account mutations. Update the GUI index row:

```markdown
| GUI-SD-05 | Settings core pages | pass | current-cycle reviewer note: core settings labels and descriptions readable; no obvious truncation |
```

- [ ] **Step 6: Validate AI settings entry without credentials**

Open AI settings entry points without entering API keys, cookies, tokens, or cloud credentials. Update the GUI index row:

```markdown
| GUI-SD-06 | AI settings entry | pass | current-cycle reviewer note: AI settings entry readable; no private credentials entered |
```

- [ ] **Step 7: Validate dangerous confirmation cancel path**

Open only the confirmation dialog for a high-risk action and cancel it. Do not delete, transfer, purchase, bind billing, or mutate real remote objects. Update the GUI index row:

```markdown
| GUI-SD-07 | Dangerous confirmation cancel path | pass | current-cycle reviewer note: cancel path readable; no real mutation executed |
```

- [ ] **Step 8: Update checklist GUI state**

In `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`, check the GUI rows that passed:

```markdown
- [x] 当前周期启动界面已验证。
- [x] 工作区 shell、tab、命令面板已验证。
- [x] Settings 核心页已验证。
- [x] 常见弹窗和危险确认取消路径已验证。
- [x] 官方后端状态路径已列入 known limitations 或后续 public-RC evidence lane。
```

### Task 3: Onboarding Static Asset Decision

**Files:**
- Modify: `docs/zh-Hans-onboarding-visual-regeneration-plan.md`
- Modify: `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`
- Modify: `docs/zh-Hans-release-notes-0.19-draft.md`

- [ ] **Step 1: Inspect current onboarding asset plan**

Run:

```bash
rg -n "pending-replacement|known limitation|phase30|onboarding" docs/zh-Hans-onboarding-visual-regeneration-plan.md docs/zh-Hans-gui-smoke-artifact-index-0.19.md docs/zh-Hans-release-notes-0.19-draft.md
```

Expected: the current rows identify onboarding assets that still need replacement or explicit limitation wording.

- [ ] **Step 2: Choose the 0.19-safe asset decision**

Use this release-safe decision unless the replacement images are actually regenerated during execution:

```markdown
## 0.19 Static Asset Release Decision

For Warp CN 0.19 self-defined complete release, onboarding static PNG English residue is treated as `known-limitation-documented`. Source-level UI localization remains complete, but inherited static onboarding images may still need future regeneration.
```

- [ ] **Step 3: Update GUI-SD-02**

Set the GUI index row to:

```markdown
| GUI-SD-02 | Onboarding visible copy | known-limitation | static onboarding PNG residue documented in `docs/zh-Hans-onboarding-visual-regeneration-plan.md`; source-level UI localization remains complete |
```

- [ ] **Step 4: Update release notes known limitations**

Add this known limitation to `docs/zh-Hans-release-notes-0.19-draft.md`:

```markdown
- Onboarding static PNG assets may retain inherited English text until the visual asset regeneration lane completes; source-level zh-Hans overlay remains clean.
```

### Task 4: Release Notes and Checklist Freeze

**Files:**
- Modify: `docs/zh-Hans-release-notes-0.19-draft.md`
- Modify: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`
- Modify: `README.md`

- [ ] **Step 1: Verify non-official wording**

Run:

```bash
rg -n "官方中文版本|官方发布|official|self-defined|自定义汉化完成版" README.md docs/zh-Hans-release-notes-0.19-draft.md docs/zh-Hans-self-defined-complete-release-checklist-0.19.md
```

Expected: every official-status match is either a disclaimer or a scope boundary.

- [ ] **Step 2: Freeze release notes status**

Set the release notes status to:

```text
Status: self-defined-complete-release-freeze-candidate
```

- [ ] **Step 3: Freeze checklist current stop point**

Update the checklist stop point after all completed gates:

```text
privacy_guard: pass
git diff --check: pass
dry_run: would_change 0, missing 0
release_inventory: coverage 100.0%
low_load_gate: no-longer-required-after-2026-06-07
cargo_check: pass
bundle_or_launch: pass
gui_smoke: pass
publication: not approved
```

If a validation lane is blocked, keep the passing lines and use these exact blocked lines for the affected lane:

```text
cargo_check: blocked-with-actionable-error
bundle_or_launch: blocked-with-actionable-error
gui_smoke: known-limitations-documented
```

- [ ] **Step 4: Run documentation consistency checks**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
privacy_guard: pass
diff_check: pass
```

### Task 5: Git Hygiene and Release Approval Hold

**Files:**
- Inspect: working tree
- Modify only if needed: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`

- [ ] **Step 1: Inspect dirty worktree**

Run:

```bash
git status --short
```

Expected: all changes can be explained as docs, validation scripts, or generated audit/test artifacts.

- [ ] **Step 2: Classify changes before staging**

Record this grouping in the final execution summary:

```text
release_docs: README and docs/zh-Hans-* release planning files
validation_scripts: script/zh_* and script/test_zh_* changes already present in working tree
public_rc_registry: unchanged unless separately approved
publication: not approved
```

- [ ] **Step 3: Hold publication gates**

Do not run these commands without explicit user approval:

```bash
git tag
git push
gh release create
```

Expected checklist state:

```markdown
- [ ] 用户批准 tag。
- [ ] 用户批准 push。
- [ ] 用户批准 GitHub release。
```

## Self-Review

- Spec coverage: low-load cancellation is handled by Task 1; GUI smoke by Task 2; onboarding assets by Task 3; release docs by Task 4; publication hold by Task 5.
- Placeholder scan: no unresolved placeholders or generic “write tests” step remains.
- Registry safety: public-RC blocker and evidence ledgers are inspect-only for this plan.
