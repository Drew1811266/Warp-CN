# Warp CN Phase 2 Round 2 Localization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the next Phase 2 zh-Hans localization slice by translating visible Appearance command-palette actions, conversation list actions, cloud-agent capacity messaging, AWS credential errors, and environment deletion confirmation while preserving internal tokens and search metadata.

**Architecture:** Continue the manifest-driven local fork. Add exact replacements to `resources/localization/zh-Hans-overrides.toml`, apply them with `script/zh_apply_localization.py`, then verify with inventory coverage, Rust formatting, focused tests, and release docs. Treat GUI automation as a release gate; if the local `WarpOss` window is still unreadable, record a manual gate instead of claiming visual success.

**Tech Stack:** Rust UI source, Python 3 localization scripts, TOML translation manifest, Cargo checks/tests, macOS `WarpOss.app` smoke testing.

---

## Scope

This round is intentionally narrower than “translate every remaining candidate”. It targets strings that are visible to users in command palette actions, menus, toasts, modals, and credential error messages.

Do not translate:

- Theme names such as `Aurora`, `Classic 1`, `Glow`, `Warp 1`.
- Settings search keyword blobs such as `window opacity transparency`.
- Examples and placeholders such as `aws login`, `sk-...`, `{value}%`, `${price}/month`.
- Debug logs, telemetry event names, test text, serialized status keys, or command/filter syntax.

## File Map

- Modify: `resources/localization/zh-Hans-overrides.toml`
  - Add all new exact string replacements.
- Modify after apply: `app/src/settings_view/appearance_page.rs`
  - Appearance command-palette toggle suffixes.
- Modify after apply: `app/src/workspace/view/conversation_list/view.rs`
  - Conversation list overflow menu and delete toasts.
- Modify after apply: `app/src/workspace/view.rs`
  - Conversation delete failure/success toasts.
- Modify after apply: `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs`
  - Cloud agent capacity and credit limit modal copy.
- Modify after apply: `app/src/ai/aws_credentials.rs`
  - User-facing AWS credential error messages.
- Modify after apply: `app/src/settings_view/delete_environment_confirmation_dialog.rs`
  - Delete environment confirmation dialog.
- Modify: `docs/zh-Hans-localization.md`
  - Update final manifest, coverage, validation, GUI gate notes.
- Modify: `docs/zh-Hans-localization-phase2.md`
  - Add Round 2 execution results.
- Modify: `README.md`
  - Update status numbers and Round 2 summary.

## Task 1: Translate Appearance Command-Palette Toggle Labels

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/settings_view/appearance_page.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"compact mode"|"themes: sync with OS"|"cursor blink"|"jump to bottom of block button"|"block dividers"|"dim inactive panes"|"open new windows with custom size"|"window blur acrylic texture"|"tools panel visibility across tabs"|"agent font matching terminal font"|"notebook font size matching terminal font size"|"tab indicators"|"focus follows mouse"|"zen mode"|"vertical tab layout"|"show vertical tabs panel in restored windows"|"latest user prompt as conversation title in tab names"|"ligature rendering"|"preserve active tab color for new tabs"|"custom padding in alt-screen"' app/src/settings_view/appearance_page.rs resources/localization/zh-Hans-overrides.toml
```

Expected: every source appears in `app/src/settings_view/appearance_page.rs`; none appears as a `source =` entry in `resources/localization/zh-Hans-overrides.toml`.

- [ ] **Step 2: Append manifest entries**

Append exactly:

```toml
[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "compact mode"
target = "紧凑模式"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "themes: sync with OS"
target = "主题：跟随系统"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "cursor blink"
target = "光标闪烁"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "jump to bottom of block button"
target = "跳到底部按钮"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "block dividers"
target = "块分隔线"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "dim inactive panes"
target = "调暗非活动窗格"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "open new windows with custom size"
target = "使用自定义尺寸打开新窗口"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "window blur acrylic texture"
target = "窗口亚克力模糊纹理"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "tools panel visibility across tabs"
target = "跨标签页保持工具面板可见状态"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "agent font matching terminal font"
target = "Agent 字体跟随终端字体"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "notebook font size matching terminal font size"
target = "Notebook 字号跟随终端字号"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "tab indicators"
target = "标签页指示器"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "focus follows mouse"
target = "焦点跟随鼠标"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "zen mode"
target = "禅模式"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "vertical tab layout"
target = "垂直标签页布局"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "show vertical tabs panel in restored windows"
target = "在恢复的窗口中显示垂直标签页面板"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "latest user prompt as conversation title in tab names"
target = "用最新用户提示词作为标签页会话标题"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "ligature rendering"
target = "连字渲染"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "preserve active tab color for new tabs"
target = "新标签页沿用活动标签页颜色"

[[replace]]
path = "app/src/settings_view/appearance_page.rs"
source = "custom padding in alt-screen"
target = "备用屏幕自定义内边距"
```

- [ ] **Step 3: Apply translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: the apply command lists `app/src/settings_view/appearance_page.rs`.

- [ ] **Step 4: Verify Appearance slice**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset settings --coverage
rg -n '"Aurora"|"Classic 1"|"Glow"|"Warp 1"|window opacity transparency|\{value\}%' app/src/settings_view/appearance_page.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports `would_change: 0` and `missing: 0`; theme names, search keywords, and `{value}%` remain unchanged; `cargo check -p warp` exits 0 with only known unused-variable warnings.

- [ ] **Step 5: Commit Appearance labels**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/settings_view/appearance_page.rs
git commit -m "feat: localize appearance command actions"
```

## Task 2: Translate Conversation List Actions And Delete Toasts

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/workspace/view/conversation_list/view.rs`
- Modify after apply: `app/src/workspace/view.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"Conversations cannot be deleted while in progress\\."|"Conversation"|"This conversation cannot be deleted"|"Share conversation"|"Fork in new pane"|"Fork in new tab"|"Failed to delete conversation\\. Please exit the agent view and try again\\."|"Conversation deleted"' app/src/workspace/view/conversation_list/view.rs app/src/workspace/view.rs resources/localization/zh-Hans-overrides.toml
```

Expected: every source appears in workspace source; none appears as a duplicate `source =` entry in the manifest.

- [ ] **Step 2: Append manifest entries**

Append exactly:

```toml
[[replace]]
path = "app/src/workspace/view/conversation_list/view.rs"
source = "Conversations cannot be deleted while in progress."
target = "进行中的对话无法删除。"

[[replace]]
path = "app/src/workspace/view/conversation_list/view.rs"
source = "Conversation"
target = "对话"

[[replace]]
path = "app/src/workspace/view/conversation_list/view.rs"
source = "This conversation cannot be deleted"
target = "此对话无法删除"

[[replace]]
path = "app/src/workspace/view/conversation_list/view.rs"
source = "Share conversation"
target = "共享对话"

[[replace]]
path = "app/src/workspace/view/conversation_list/view.rs"
source = "Fork in new pane"
target = "在新窗格中 fork"

[[replace]]
path = "app/src/workspace/view/conversation_list/view.rs"
source = "Fork in new tab"
target = "在新标签页中 fork"

[[replace]]
path = "app/src/workspace/view.rs"
source = "Failed to delete conversation. Please exit the agent view and try again."
target = "删除对话失败。请退出 Agent 视图后重试。"

[[replace]]
path = "app/src/workspace/view.rs"
source = "Conversation deleted"
target = "对话已删除"
```

- [ ] **Step 3: Apply translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: the apply command lists `app/src/workspace/view/conversation_list/view.rs` and `app/src/workspace/view.rs`.

- [ ] **Step 4: Verify workspace slice**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: all commands exit 0; dry-run reports no pending changes and no missing entries.

- [ ] **Step 5: Commit conversation list localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace/view/conversation_list/view.rs app/src/workspace/view.rs
git commit -m "feat: localize conversation list actions"
```

## Task 3: Translate Cloud Agent Capacity Modal

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"Concurrent cloud agent limit reached"|"This cloud run is queued because your team has reached the maximum number of concurrent cloud agents\\. It will start automatically when another cloud run finishes\\."|"You'"'"'re out of AI credits"|"This cloud run stopped because your team has used all available AI credits for the current billing period\\."|" Upgrade your plan for more concurrent cloud agents\\."|" Upgrade your plan to continue running cloud agents\\."|"Paid plans include everything in your free trial plus:"|"The Business plan includes everything on your current plan plus:"|"Extended AI credits per month"|"Bring your own API key"|"Upgrade plan"|"Open billing"' app/src/workspace/view/cloud_agent_capacity_modal/mod.rs resources/localization/zh-Hans-overrides.toml
```

Expected: every source appears in `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs`; none appears as a duplicate manifest source.

- [ ] **Step 2: Append manifest entries**

Append exactly:

```toml
[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "Concurrent cloud agent limit reached"
target = "已达到并发云端 Agent 上限"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "This cloud run is queued because your team has reached the maximum number of concurrent cloud agents. It will start automatically when another cloud run finishes."
target = "由于你的团队已达到并发云端 Agent 数量上限，此云端运行已排队。其他云端运行完成后，它会自动开始。"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "You're out of AI credits"
target = "AI 点数已用完"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "This cloud run stopped because your team has used all available AI credits for the current billing period."
target = "由于你的团队已用完当前计费周期内的全部 AI 点数，此云端运行已停止。"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = " Upgrade your plan for more concurrent cloud agents."
target = "升级方案以获得更多并发云端 Agent。"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = " Upgrade your plan to continue running cloud agents."
target = "升级方案以继续运行云端 Agent。"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "Paid plans include everything in your free trial plus:"
target = "付费方案包含免费试用中的所有内容，并额外提供："

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "The Business plan includes everything on your current plan plus:"
target = "Business 方案包含当前方案中的所有内容，并额外提供："

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "Extended AI credits per month"
target = "每月扩展 AI 点数"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "Bring your own API key"
target = "自带 API key"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "Upgrade plan"
target = "升级方案"

[[replace]]
path = "app/src/workspace/view/cloud_agent_capacity_modal/mod.rs"
source = "Open billing"
target = "打开账单"
```

Do not add entries for strings containing `${price}/month`, `2x`, or `5x`; those combine dynamic pricing or multiplier values that need separate UI review before translation.

- [ ] **Step 3: Apply translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: the apply command lists `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs`.

- [ ] **Step 4: Verify cloud modal slice**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
rg -n '"2x"|"5x"|\$\{price\}/month' app/src/workspace/view/cloud_agent_capacity_modal/mod.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports no pending changes; the dynamic multiplier/pricing strings remain unchanged; `cargo check -p warp` exits 0 with only known warnings.

- [ ] **Step 5: Commit cloud modal localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace/view/cloud_agent_capacity_modal/mod.rs
git commit -m "feat: localize cloud agent capacity modal"
```

## Task 4: Translate AWS Credential Errors And Environment Delete Dialog

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/ai/aws_credentials.rs`
- Modify after apply: `app/src/settings_view/delete_environment_confirmation_dialog.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"No AWS credentials configured"|"Failed to load AWS credentials: \\{msg\\}"|"The default AWS profile"|"the default AWS profile"|"AWS credentials were not found for \\{\\}\\. Log in with the AWS CLI or update your AWS credentials configuration, then refresh\\."|"Timed out while loading AWS credentials\\. Refresh and try again\\."|"\\{\\} is invalid or incomplete in your local AWS configuration\\. Update your AWS profile settings and credentials, then refresh\\."|"Unable to load AWS credentials from your configured provider\\. Refresh your AWS login and try again\\."|"Unexpected error while loading AWS credentials\\. Refresh your AWS login and try again\\."|"Unable to load AWS credentials\\. Refresh your AWS login and try again\\."|"Cancel"|"Delete environment"|"Are you sure you want to remove the \\{\\} environment\\?"|"Delete environment\\?"' app/src/ai/aws_credentials.rs app/src/settings_view/delete_environment_confirmation_dialog.rs resources/localization/zh-Hans-overrides.toml
```

Expected: every source appears in source files; no duplicate manifest source exists for these exact path/source pairs.

- [ ] **Step 2: Append manifest entries**

Append exactly:

```toml
[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "No AWS credentials configured"
target = "未配置 AWS 凭据"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "Failed to load AWS credentials: {msg}"
target = "无法加载 AWS 凭据：{msg}"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "The default AWS profile"
target = "默认 AWS 配置档"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "the default AWS profile"
target = "默认 AWS 配置档"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "AWS credentials were not found for {}. Log in with the AWS CLI or update your AWS credentials configuration, then refresh."
target = "未找到 {} 的 AWS 凭据。请使用 AWS CLI 登录，或更新你的 AWS 凭据配置后刷新。"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "Timed out while loading AWS credentials. Refresh and try again."
target = "加载 AWS 凭据超时。请刷新后重试。"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "{} is invalid or incomplete in your local AWS configuration. Update your AWS profile settings and credentials, then refresh."
target = "{} 在本地 AWS 配置中无效或不完整。请更新 AWS 配置档设置和凭据后刷新。"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "Unable to load AWS credentials from your configured provider. Refresh your AWS login and try again."
target = "无法从已配置的提供方加载 AWS 凭据。请刷新 AWS 登录后重试。"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "Unexpected error while loading AWS credentials. Refresh your AWS login and try again."
target = "加载 AWS 凭据时发生意外错误。请刷新 AWS 登录后重试。"

[[replace]]
path = "app/src/ai/aws_credentials.rs"
source = "Unable to load AWS credentials. Refresh your AWS login and try again."
target = "无法加载 AWS 凭据。请刷新 AWS 登录后重试。"

[[replace]]
path = "app/src/settings_view/delete_environment_confirmation_dialog.rs"
source = "Cancel"
target = "取消"

[[replace]]
path = "app/src/settings_view/delete_environment_confirmation_dialog.rs"
source = "Delete environment"
target = "删除环境"

[[replace]]
path = "app/src/settings_view/delete_environment_confirmation_dialog.rs"
source = "Are you sure you want to remove the {} environment?"
target = "确定要移除 {} 环境吗？"

[[replace]]
path = "app/src/settings_view/delete_environment_confirmation_dialog.rs"
source = "Delete environment?"
target = "删除环境？"
```

- [ ] **Step 3: Apply translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: the apply command lists `app/src/ai/aws_credentials.rs` and `app/src/settings_view/delete_environment_confirmation_dialog.rs`.

- [ ] **Step 4: Verify credential/dialog slice**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
rg -n 'AWS CLI|AWS profile|AWS 配置档|默认 AWS 配置档' app/src/ai/aws_credentials.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports no pending changes; AWS product terms remain recognizable; `cargo check -p warp` exits 0 with only known warnings.

- [ ] **Step 5: Commit credential and dialog localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/ai/aws_credentials.rs app/src/settings_view/delete_environment_confirmation_dialog.rs
git commit -m "feat: localize credential and environment dialogs"
```

## Task 5: Record Round 2 Release Audit

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-localization-phase2.md`
- Modify: `README.md`

- [ ] **Step 1: Run final command-line audit**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected: all commands exit 0. Known unused-variable warnings in `scp_fallback.rs` and `slash_commands/mod.rs` are acceptable only if unchanged.

- [ ] **Step 2: Try GUI smoke once**

Run:

```bash
osascript -e 'tell application id "dev.warp.WarpOss" to quit' >/dev/null 2>&1 || true
open -n target/debug/bundle/osx/WarpOss.app
```

Check these paths in the app if the window is usable:

- Command palette Appearance actions show Chinese suffixes after `启用` or `停用`.
- Conversation list overflow menu shows `共享对话`, `在新窗格中 fork`, `在新标签页中 fork`.
- Cloud agent capacity modal copy is Chinese if the debug path or real account state can trigger it.
- Delete environment confirmation dialog shows Chinese title, body, and buttons.

If the window is still unreadable through automation, capture the exact error and write it as a manual gate.

- [ ] **Step 3: Update docs**

Update `docs/zh-Hans-localization.md`:

- Set manifest count and dry-run summary to the final `zh_apply_localization.py --dry-run --summary` output.
- Set coverage snapshot to the final six preset outputs.
- Add Round 2 covered areas: Appearance command actions, conversation list actions, cloud agent capacity modal, AWS credential errors, environment deletion dialog.
- Add GUI smoke result or manual gate.

Update `docs/zh-Hans-localization-phase2.md`:

- Add `第二阶段第二轮执行结果`.
- Record each Round 2 task commit hash.
- Record final coverage numbers.
- Record skipped dynamic strings: theme names, search keywords, `${price}/month`, `2x`, `5x`, example values.

Update `README.md`:

- Update manifest count, files count, coverage table, and milestone summary.
- Keep the current distinction between command-line validation and GUI/manual gates.

- [ ] **Step 4: Validate docs and commit**

Run:

```bash
rg -n 'T''BD|TO''DO|implement lat''er|fill in det''ails|Similar t''o|probab''ly' README.md docs/zh-Hans-localization.md docs/zh-Hans-localization-phase2.md
git diff --check
git status --short
```

Expected: the `rg` command exits 1 with no matches; `git diff --check` exits 0; only planned docs are modified.

Commit:

```bash
git add docs/zh-Hans-localization.md docs/zh-Hans-localization-phase2.md README.md
git commit -m "docs: record phase 2 round 2 zh-Hans audit"
```

## Task 6: Push Round 2 To GitHub

**Files:** no file edits.

- [ ] **Step 1: Verify local status**

Run:

```bash
git status -sb
git log --oneline --decorate -10
git log --oneline github/main..HEAD
```

Expected: current branch is ahead of `github/main` only by Round 2 commits. Old untracked `docs/superpowers/plans/2026-05-29-zh-Hans-localization*.md` files may remain untracked and must not be staged unless the user asks.

- [ ] **Step 2: Push to GitHub main**

Run:

```bash
git push github HEAD:main
```

Expected: push exits 0 and updates `Drew1811266/Warp-CN` `main`.

- [ ] **Step 3: Confirm remote**

Run:

```bash
git ls-remote github refs/heads/main
git rev-parse HEAD
gh repo view Drew1811266/Warp-CN --json nameWithOwner,defaultBranchRef,url
```

Expected: remote `main` hash equals local `HEAD`, and repo URL is `https://github.com/Drew1811266/Warp-CN`.

## Self-Review

Spec coverage:

- GUI manual gate from Round 1 is preserved in Task 5 instead of claimed as complete.
- Appearance work targets command-palette strings generated by `ToggleSettingActionPair::new`; theme names and keyword blobs stay unchanged.
- Workspace work targets visible menu/toast strings in the conversation list.
- Cloud work targets visible capacity modal strings and avoids dynamic price/multiplier fragments.
- Credential work targets user-facing AWS error messages and one destructive environment confirmation dialog.
- Release audit and GitHub push are explicit tasks.

Placeholder scan:

- No placeholder tasks are included.
- Every translation task includes exact TOML entries, exact commands, and expected results.

Consistency check:

- All source paths match the current inventory/source reads.
- Verification commands use the current app package name `warp`.
- The plan keeps the existing manifest-driven architecture and avoids runtime localization changes.
