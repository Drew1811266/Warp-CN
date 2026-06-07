# zh-Hans Self-Defined Complete Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship Warp CN 0.19 as a self-defined Simplified Chinese localization complete release, without waiting for Warp official approval and without claiming official status.

**Architecture:** Keep the existing public-RC blocker registry intact for future higher-assurance evidence work. Add a separate self-defined release path that validates core localization, GUI readability, packaging, and clear known limitations for official backend and high-risk object paths.

**Tech Stack:** Rust workspace, TOML localization manifests, Python validation scripts, macOS GUI smoke workflow, GitHub release documentation.

---

## File Structure

- Create: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`
  - Final executable checklist for the 0.19 self-defined release.
- Modify: `docs/zh-Hans-release-notes-0.19-draft.md`
  - Reword from public-RC waiting state to self-defined complete release draft.
- Modify: `README.md`
  - Add the self-defined release plan and checklist to the maintenance document index.
- Modify or create: `docs/zh-Hans-gui-smoke-matrix.md`
  - Record current-cycle GUI smoke scope and results.
- Modify or create: `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`
  - Index current-cycle GUI artifacts without committing raw private evidence.
- Modify or create: `docs/zh-Hans-onboarding-visual-regeneration-plan.md`
  - Track onboarding static PNG replacement or known limitation decision.
- Do not modify: `resources/localization/zh-Hans-public-rc-blockers.toml`
  - Keep public-RC blocker truth intact.
- Do not modify without reviewed evidence: `resources/localization/zh-Hans-public-rc-evidence.toml`
  - Do not mark public-RC evidence as provided for self-defined release.

### Task 1: Freeze Self-Defined Release Scope

**Files:**
- Modify: `README.md`
- Modify: `docs/zh-Hans-release-notes-0.19-draft.md`
- Create: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`

- [ ] **Step 1: Add README index links**

Add these entries under `README.md` section `维护文档`:

```markdown
- `docs/zh-Hans-self-defined-complete-release-plan.md`：Warp CN 0.19 自定义汉化完成版目标、验收标准和官方后端范围声明。
- `docs/superpowers/plans/2026-06-06-zh-Hans-self-defined-complete-release.md`：0.19 自定义汉化完成版后续开发任务计划。
- `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`：0.19 自定义汉化完成版最终冻结 checklist。
```

- [ ] **Step 2: Create checklist skeleton**

Create `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md` with:

```markdown
# Warp CN 0.19 自定义汉化完成版 Checklist

日期：2026-06-06

## Release Identity

- [ ] 发行名称使用 `Warp CN 0.19 自定义汉化完成版`。
- [ ] README 明确写明非官方 Warp 中文版本。
- [ ] Release notes 明确写明不代表 Warp 官方发布。
- [ ] public-RC blocker 未被伪造清零。

## Localization Gates

- [ ] `python3 script/zh_apply_localization.py --validate-manifest` 通过。
- [ ] `python3 script/zh_apply_localization.py --check-glossary` 通过。
- [ ] `python3 script/zh_apply_localization.py --metadata-summary` 通过。
- [ ] `python3 script/zh_apply_localization.py --dry-run --summary` 显示 `would_change: 0` 和 `missing: 0`。
- [ ] `python3 script/zh_localization_inventory.py --preset release --coverage` 显示 release coverage 100.0%。

## GUI Gates

- [ ] 当前周期启动界面已验证。
- [ ] 工作区 shell、tab、命令面板已验证。
- [ ] Settings 核心页已验证。
- [ ] 常见弹窗和危险确认取消路径已验证。
- [ ] 官方后端状态路径已列入 known limitations 或后续 public-RC evidence lane。

## Packaging Gates

- [ ] `python3 script/privacy_guard.py --all-tracked` 通过。
- [ ] `git diff --check` 通过。
- [ ] low-load gate 允许 heavy gate。
- [ ] `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp` 通过。
- [ ] 本地启动或 bundle 验证通过。

## Publication Gates

- [ ] 用户批准 tag。
- [ ] 用户批准 push。
- [ ] 用户批准 GitHub release。
```

- [ ] **Step 3: Reword release notes draft**

In `docs/zh-Hans-release-notes-0.19-draft.md`, replace the current public-RC waiting-state framing with this status block:

```markdown
Status: self-defined-complete-release-draft

## 说明

这份文档是 Warp CN 自定义汉化完成版发行说明草稿。它不是 Warp 官方发行说明，
不代表 Warp 官方发布、官方中文版本、官方标签、官方推送或官方 release。
```

- [ ] **Step 4: Verify wording**

Run:

```bash
rg -n "官方中文版本|Warp 官方发布|public-RC readiness|official release" README.md docs/zh-Hans-release-notes-0.19-draft.md docs/zh-Hans-self-defined-complete-release-checklist-0.19.md
```

Expected: every match is either a disclaimer or a statement that the release is not official.

### Task 2: Run Lightweight Localization Rescan

**Files:**
- Modify or create: `docs/zh-Hans-translation-rescan-2026-06-06.md`

- [ ] **Step 1: Run manifest validation**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
```

Expected:

```text
manifest validation passed
glossary check passed
would_change: 0
missing: 0
coverage: 100.0%
```

- [ ] **Step 2: Run focused unit tests**

Run:

```bash
python3 -m unittest \
  script/test_zh_apply_localization.py \
  script/test_zh_localization_inventory.py \
  script/test_zh_export_locale.py \
  script/test_zh_full_translation_audit.py \
  script/test_zh_mojibake_scan.py
```

Expected: all tests pass.

- [ ] **Step 3: Record rescan result**

Create `docs/zh-Hans-translation-rescan-2026-06-06.md` with:

````markdown
# zh-Hans Translation Rescan - 2026-06-06

## Purpose

Validate Warp CN 0.19 self-defined complete release localization health.

## Commands

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_full_translation_audit.py script/test_zh_mojibake_scan.py
```

## Result

```text
status: pending-run
```

## Release Interpretation

This rescan validates the self-defined localization release. It does not clear public-RC backend fixture, isolated account, or disposable object evidence rows.
````

Replace `pending-run` with the actual pass/fail summary after running the commands.

### Task 3: Define GUI Smoke Scope for Self-Defined Release

**Files:**
- Modify or create: `docs/zh-Hans-gui-smoke-matrix.md`
- Create: `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`

- [ ] **Step 1: Add self-defined GUI matrix section**

Add this table to `docs/zh-Hans-gui-smoke-matrix.md`:

```markdown
## 0.19 Self-Defined Complete Release GUI Scope

| Area | Required for 0.19 | Evidence Type | Official backend required |
| --- | --- | --- | --- |
| App launch | yes | current-cycle screenshot or reviewer note | no |
| Onboarding visible copy | yes | screenshot or static asset decision | no |
| Workspace shell | yes | screenshot or reviewer note | no |
| Command palette | yes | screenshot or reviewer note | no |
| Settings core pages | yes | screenshot or reviewer note | no |
| AI settings entry | yes | screenshot or reviewer note | no |
| Login callback | no | known limitation or isolated account lane | no official approval, but requires isolated account |
| Billing / quota / Cloud | no | known limitation | yes |
| Delete / transfer real objects | no | cancel-first proof only | no official approval, but requires disposable object approval |
```

- [ ] **Step 2: Create artifact index**

Create `docs/zh-Hans-gui-smoke-artifact-index-0.19.md` with:

```markdown
# zh-Hans GUI Smoke Artifact Index - 0.19

## Scope

This index records current-cycle GUI smoke evidence for Warp CN 0.19 self-defined complete release. Do not commit raw private screenshots, recordings, account identifiers, callback URLs, endpoint URLs, billing IDs, team IDs, tokens, cookies, or magic links.

## Required Rows

| ID | Area | Status | Artifact or Reviewer Note |
| --- | --- | --- | --- |
| GUI-SD-01 | App launch | pending | pending current-cycle validation |
| GUI-SD-02 | Onboarding visible copy | pending | pending current-cycle validation |
| GUI-SD-03 | Workspace shell | pending | pending current-cycle validation |
| GUI-SD-04 | Command palette | pending | pending current-cycle validation |
| GUI-SD-05 | Settings core pages | pending | pending current-cycle validation |
| GUI-SD-06 | AI settings entry | pending | pending current-cycle validation |
| GUI-SD-07 | Dangerous confirmation cancel path | pending | pending current-cycle validation |

## Known Limitations

Billing, Cloud quota, official backend capacity, real team ownership transfer, real secret deletion, real environment deletion, and real endpoint deletion are not required for 0.19 self-defined complete release.
```

- [ ] **Step 3: Verify no private artifact paths were added**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
```

Expected: pass.

### Task 4: Handle Onboarding Static PNG English Residue

**Files:**
- Modify: `docs/zh-Hans-onboarding-visual-regeneration-plan.md`
- Modify: `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`

- [ ] **Step 1: Classify onboarding assets**

Run:

```bash
rg -n "onboarding|welcome|theme|agent|customize|english|英文|PNG|png" docs/zh-Hans-onboarding-visual-regeneration-plan.md docs/gui-smoke-artifacts README.md
```

Expected: list of current onboarding PNG references and known residue notes.

- [ ] **Step 2: Pick one of three decisions per asset**

Record each asset in `docs/zh-Hans-onboarding-visual-regeneration-plan.md` using:

```markdown
| Asset | Decision | Required Action |
| --- | --- | --- |
| docs/gui-smoke-artifacts/phase30/p30-onboarding-welcome-local-fixture.png | replace | regenerate current-cycle zh-Hans screenshot |
| docs/gui-smoke-artifacts/phase30/p30-onboarding-theme-choice.png | replace | regenerate current-cycle zh-Hans screenshot |
| docs/gui-smoke-artifacts/phase30/p30-onboarding-agent-choice.png | replace | regenerate current-cycle zh-Hans screenshot |
```

Allowed decisions are `replace`, `crop-or-retire`, and `known-limitation`.

- [ ] **Step 3: Reflect decision in artifact index**

For `GUI-SD-02` in `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`, set status to one of:

```text
pending-replacement
passed-current-cycle
known-limitation-documented
```

### Task 5: Run Low-Load and Packaging Gate

**Files:**
- Create: `docs/zh-Hans-packaging-preflight-2026-06-06.md`
- Modify: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`

- [ ] **Step 1: Run privacy and whitespace checks**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected: both pass.

- [ ] **Step 2: Run low-load gate**

Run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Expected:

```text
decision: run-heavy-gate
```

If the decision is `defer-heavy-gate`, record the output and stop before Rust build.

- [ ] **Step 3: Run Rust check only when low-load gate passes**

Run:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

Expected: command exits 0.

- [ ] **Step 4: Record packaging result**

Create `docs/zh-Hans-packaging-preflight-2026-06-06.md` with:

````markdown
# zh-Hans Packaging Preflight - 2026-06-06

## Scope

Warp CN 0.19 self-defined complete release packaging preflight.

## Commands

```text
python3 script/privacy_guard.py --all-tracked
git diff --check
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

## Result

```text
privacy_guard: pending-run
diff_check: pending-run
low_load_gate: pending-run
cargo_check: pending-run
```

## Notes

Rust check is skipped when low-load gate returns defer-heavy-gate.
````

Replace each `pending-run` with actual result after execution.

### Task 6: Rewrite Release Notes for 0.19

**Files:**
- Modify: `docs/zh-Hans-release-notes-0.19-draft.md`

- [ ] **Step 1: Replace release blocker section**

Replace the old `Release Blockers` section with:

```markdown
## Known Limitations

Warp CN 0.19 自定义汉化完成版不声称以下官方后端或高风险对象路径已完成 full public-RC evidence closure：

- Billing、credits、quota、build-plan migration。
- Cloud capacity 或官方后端容量状态。
- AWS Bedrock 真实凭据和真实 provider credential。
- 真实 team ownership transfer。
- 真实 managed secret、environment、endpoint 删除。
- 个人主账号 login callback 和认证材料。

这些路径保留在 public-RC evidence registry 中，作为未来更高等级验证路线。它们不是 0.19 自定义汉化完成版的硬阻塞。
```

- [ ] **Step 2: Add completed scope section**

Add:

```markdown
## Completed Scope

- 简体中文源码级 overlay 保持干净。
- 高频用户界面、设置、工作区、命令面板、常见弹窗和核心 Agent 文案已纳入汉化清单。
- 发行说明明确非官方 fork 边界。
- 官方后端状态和高风险对象路径按 known limitations 管理。
```

- [ ] **Step 3: Verify no official claim**

Run:

```bash
rg -n "官方中文版本|官方发布|official Warp release|public-RC readiness" docs/zh-Hans-release-notes-0.19-draft.md
```

Expected: every match is a disclaimer or known limitation.

### Task 7: Final Freeze and User Approval Gate

**Files:**
- Modify: `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`
- Modify: `README.md`

- [ ] **Step 1: Run final lightweight checks**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
```

Expected:

```text
privacy_guard: pass
git diff --check: pass
would_change: 0
missing: 0
coverage: 100.0%
```

- [ ] **Step 2: Verify release docs are linked**

Run:

```bash
rg -n "self-defined|自定义汉化完成版|0.19" README.md docs/zh-Hans-self-defined-complete-release-plan.md docs/zh-Hans-release-notes-0.19-draft.md docs/zh-Hans-self-defined-complete-release-checklist-0.19.md
```

Expected: README links the plan and checklist; release notes and checklist use self-defined complete release wording.

- [ ] **Step 3: Stop before publication**

Do not run these commands until the user explicitly approves publication:

```bash
git tag 0.19
git push github main
git push github 0.19
gh release create 0.19
```

Expected: no tag, push, or release happens during planning or validation.

## Self-Review

Spec coverage:

- The plan no longer treats Warp official approval as a hard blocker for the self-defined release.
- The plan preserves public-RC blocker registry integrity for future higher-assurance work.
- The plan defines concrete localization, GUI, asset, packaging, documentation, and publication gates.

Placeholder scan:

- The plan uses explicit pending statuses only in files that must later be filled with command output.
- No task asks an implementer to invent unspecified checks.

Risk review:

- Real accounts, real billing, real cloud capacity, real secrets, real endpoints, and real teams remain no-go unless separately approved.
- Publication commands are listed but gated behind explicit user approval.
