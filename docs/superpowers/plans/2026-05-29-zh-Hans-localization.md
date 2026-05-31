# zh-Hans Localization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the local `drew/zh-Hans-localization` branch from a first-pass Chinese UI fork to a maintainable, broadly covered Simplified Chinese build.

**Architecture:** Keep the current local-fork strategy: translations live in `resources/localization/zh-Hans-overrides.toml` and are applied by `script/zh_apply_localization.py`. Before expanding the manifest substantially, add inventory and validation tooling so future upstream syncs expose drift, untranslated high-value UI strings, and accidental non-UI rewrites.

**Tech Stack:** Rust UI source, Python 3 tooling, TOML manifest, `cargo fmt`, targeted `cargo check`/integration tests, manual app smoke testing through `./script/run`.

---

## Current Baseline

The branch currently has 122 manifest replacements across these high-visibility areas:

- `crates/onboarding/src/slides/*.rs`
- `app/src/auth/login_slide.rs`
- `app/src/workspace/view.rs`
- `app/src/workspace/view/vertical_tabs.rs`

Current validation passes:

```bash
python3 script/zh_apply_localization.py --dry-run
cargo fmt --check
git diff --check
```

The explicit scope note in `docs/zh-Hans-localization.md` says the first pass covers onboarding, login / AI opt-out, vertical tabs labels, search placeholders, and top-level navigation labels. It also names the next priority areas: settings pages, command palette entries, modals, and toast messages.

## Principles

1. Preserve Warp behavior. Translation changes must not alter actions, telemetry names, persisted settings keys, command IDs, URLs, model IDs, or config schema values.
2. Prefer manifest-driven exact replacements for local fork maintainability. Do not build a full runtime i18n framework unless the local fork starts needing language switching.
3. Translate user-visible UI only. Leave logs, test names, telemetry event labels, binding IDs, internal pane type keys, config keys, and generated protocol fields in English unless they are rendered directly to users.
4. Keep English product names when they are brands or established feature names: Warp, Warp Drive, Warp Agent, Codex, Claude Code, Gemini, MCP, GitHub, Slack.
5. Use concise Simplified Chinese UI copy. Avoid literal long translations that overflow small menu, button, pill, tooltip, or tab containers.
6. Validate every batch with the manifest dry-run, formatting, and at least one targeted compile/test command.

## Translation Glossary

Use this table before adding new replacements:

| English | zh-Hans |
| --- | --- |
| Settings | 设置 |
| Keyboard shortcuts | 键盘快捷键 |
| Billing and usage | 账单与用量 |
| Upgrade | 升级 |
| Sign up | 注册 |
| Log out | 退出登录 |
| Documentation | 文档 |
| Feedback | 反馈 |
| What's new | 新增内容 |
| Update Warp | 更新 Warp |
| View Warp logs | 查看 Warp 日志 |
| Invite a friend | 邀请朋友 |
| Agent conversations | Agent 对话 |
| Project explorer | 项目浏览器 |
| Global search | 全局搜索 |
| Tools panel | 工具面板 |
| Command Search | 命令搜索 |
| Command Palette | 命令面板 |
| No results found | 未找到结果 |
| Search your history, workflows, and more | 搜索历史、工作流等 |
| Search for a command | 搜索命令 |
| Back | 返回 |
| Next | 下一步 |
| Cancel | 取消 |
| Save | 保存 |
| Create | 创建 |
| Delete | 删除 |
| Remove | 移除 |
| Open | 打开 |
| Close | 关闭 |
| Learn more | 了解更多 |
| View | 查看 |
| Undo | 撤销 |
| Copy | 复制 |
| Paste | 粘贴 |
| Retry | 重试 |
| Continue | 继续 |
| Subscribe | 订阅 |
| Free | 免费 |
| Loading... | 正在加载... |
| Unable to load | 无法加载 |

## File Ownership Map

### Tooling And Documentation

- Modify: `script/zh_apply_localization.py`
  - Keep exact replacement behavior.
  - Add safer parsing/validation before manifest scale increases.
- Create: `script/zh_localization_inventory.py`
  - Extract likely user-visible English Rust string literals from selected source paths.
  - Exclude comments, logs, tests, telemetry-only strings, config keys, URLs, file paths, and generated data where possible.
- Modify: `resources/localization/zh-Hans-overrides.toml`
  - Add new replacements in batches grouped by file.
  - Add optional metadata only if the apply script supports it.
- Modify: `docs/zh-Hans-localization.md`
  - Keep the current workflow updated with new inventory/check commands and phase status.

### Phase 1 High-Value Remaining Onboarding/Auth

- Modify: `crates/onboarding/src/slides/free_user_no_ai_slide.rs`
- Modify: `crates/onboarding/src/callout/view.rs`
- Modify: `crates/onboarding/src/components/onboarding_callout.rs`
- Modify: `app/src/auth/paste_auth_token_modal.rs`
- Modify: `app/src/auth/auth_view_body.rs`
- Modify: `app/src/auth/auth_view_modal.rs`
- Modify: `app/src/auth/login_failure_notification.rs`
- Modify: `app/src/auth/login_error_modal.rs`
- Modify: `app/src/auth/auth_override_warning_body.rs`

### Phase 2 Workspace Shell And Navigation

- Modify: `app/src/workspace/view.rs`
- Modify: `app/src/workspace/view/vertical_tabs.rs`
- Modify: `app/src/workspace/view/left_panel.rs`
- Modify: `app/src/workspace/view/right_panel.rs`
- Modify: `app/src/workspace/view/conversation_list/view.rs`
- Modify: `app/src/workspace/close_session_confirmation_dialog.rs`
- Modify: `app/src/workspace/rewind_confirmation_dialog.rs`
- Modify: `app/src/workspace/toast_stack.rs`
- Modify: `app/src/app_menus.rs`
- Modify: `app/src/menu.rs`
- Modify: `crates/warpui/src/platform/mac/menus.rs`

### Phase 3 Search Surfaces

- Modify: `app/src/search/command_palette/view.rs`
- Modify: `app/src/search/command_palette/zero_state.rs`
- Modify: `app/src/search/command_palette/zero_state/items.rs`
- Modify: `app/src/search/command_palette/navigation/*.rs`
- Modify: `app/src/search/command_palette/new_session/*.rs`
- Modify: `app/src/search/command_palette/repos/*.rs`
- Modify: `app/src/search/command_search/view.rs`
- Modify: `app/src/search/command_search/zero_state.rs`
- Modify: `app/src/search/command_search/*/*search_item.rs`
- Modify: `app/src/search/ai_context_menu/**/*.rs`
- Modify: `app/src/search/slash_command_menu/**/*.rs`

### Phase 4 Settings

- Modify: `app/src/settings_view/mod.rs`
- Modify: `app/src/settings_view/nav.rs`
- Modify: `app/src/settings_view/settings_page.rs`
- Modify: `app/src/settings_view/main_page.rs`
- Modify: `app/src/settings_view/appearance_page.rs`
- Modify: `app/src/settings_view/features_page.rs`
- Modify: `app/src/settings_view/keybindings.rs`
- Modify: `app/src/settings_view/privacy_page.rs`
- Modify: `app/src/settings_view/ai_page.rs`
- Modify: `app/src/settings_view/code_page.rs`
- Modify: `app/src/settings_view/warp_drive_page.rs`
- Modify: `app/src/settings_view/warpify_page.rs`
- Modify: `app/src/settings_view/mcp_servers/**/*.rs`
- Modify: `app/src/settings_view/billing_and_usage*.rs`
- Modify: `app/src/settings_view/billing_and_usage/**/*.rs`

### Phase 5 Modals, Toasts, And Feature-Specific Panels

- Modify: `app/src/themes/*modal*.rs`
- Modify: `app/src/themes/*body*.rs`
- Modify: `app/src/tab_configs/*modal*.rs`
- Modify: `app/src/billing/*modal*.rs`
- Modify: `app/src/billing/*body*.rs`
- Modify: `app/src/drive/**/*.rs`
- Modify: `app/src/terminal/**/*modal*.rs`
- Modify: `app/src/terminal/input/**/*.rs`
- Modify: `app/src/ai/blocklist/**/*.rs`
- Modify: `app/src/ai/agent_management/**/*.rs`

## Execution Plan

### Task 1: Lock The Baseline

**Files:**

- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Record the current validated baseline**

Add a short status section to `docs/zh-Hans-localization.md`:

```markdown
## Status

Last verified baseline: 2026-05-29.

- Manifest entries: 122.
- Covered areas: onboarding slides, login / AI opt-out, vertical tabs labels, selected search placeholders, selected top-level navigation labels.
- Validation:
  - `python3 script/zh_apply_localization.py --dry-run`
  - `cargo fmt --check`
  - `git diff --check`
```

- [ ] **Step 2: Run the baseline commands**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run
cargo fmt --check
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 3: Commit**

```bash
git add docs/zh-Hans-localization.md
git commit -m "docs: record zh-Hans localization baseline"
```

### Task 2: Harden The Replacement Script

**Files:**

- Modify: `script/zh_apply_localization.py`
- Test: `script/zh_apply_localization.py --dry-run`

- [ ] **Step 1: Add comment-aware Rust string scanning**

Update `replace_rust_string_literals` so it skips:

- `// line comments`
- `/* block comments */`
- Rust char literals such as `'x'`

It should still replace normal Rust double-quoted literals. Raw strings can be left unsupported in this task because the current manifest targets normal string literals.

- [ ] **Step 2: Add manifest duplicate detection**

In `load_manifest`, reject duplicate `(path, source)` pairs. This prevents later batches from silently adding conflicting targets.

Expected error shape:

```text
resources/localization/zh-Hans-overrides.toml:<line>: duplicate replacement for <path> <source>
```

- [ ] **Step 3: Add `--summary`**

Add a CLI flag:

```bash
python3 script/zh_apply_localization.py --summary
```

Expected output format:

```text
entries: 122
files: 10
already_applied: 122
would_change: 0
missing: 0
```

- [ ] **Step 4: Verify idempotence**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
python3 script/zh_apply_localization.py --dry-run --summary
git diff --check
cargo fmt --check
```

Expected: no failures. The second summary should still report `missing: 0`.

- [ ] **Step 5: Commit**

```bash
git add script/zh_apply_localization.py
git commit -m "chore: harden zh-Hans localization apply script"
```

### Task 3: Add A Localization Inventory Tool

**Files:**

- Create: `script/zh_localization_inventory.py`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Create the inventory script**

The script should:

- Read Rust files under user-selected roots.
- Extract normal Rust double-quoted string literals.
- Skip comments.
- Skip paths containing `_tests.rs`, `/tests/`, `test_data`, `models/onnx`, `resources/bundled`.
- Skip strings that match URLs, keybinding IDs, telemetry event names, file paths, all-caps constants, empty strings, and strings without alphabetic characters.
- Mark whether each literal already appears as a `source` or `target` in `resources/localization/zh-Hans-overrides.toml`.
- Print Markdown by default.

Required command:

```bash
python3 script/zh_localization_inventory.py app/src/settings_view app/src/search crates/onboarding/src
```

Required output columns:

```markdown
| status | path | line | literal |
| --- | --- | ---: | --- |
```

Statuses:

- `covered-source`
- `covered-target`
- `candidate`

- [ ] **Step 2: Add focused presets**

Support these flags:

```bash
python3 script/zh_localization_inventory.py --preset onboarding
python3 script/zh_localization_inventory.py --preset workspace
python3 script/zh_localization_inventory.py --preset search
python3 script/zh_localization_inventory.py --preset settings
python3 script/zh_localization_inventory.py --preset modals
```

Preset roots:

- `onboarding`: `crates/onboarding/src`, `app/src/auth`
- `workspace`: `app/src/workspace`, `app/src/app_menus.rs`, `app/src/menu.rs`
- `search`: `app/src/search`
- `settings`: `app/src/settings_view`
- `modals`: `app/src/auth`, `app/src/billing`, `app/src/themes`, `app/src/tab_configs`, `app/src/drive`, `app/src/terminal`, `app/src/ai`

- [ ] **Step 3: Document the inventory workflow**

Add to `docs/zh-Hans-localization.md`:

````markdown
## Inventory workflow

```bash
python3 script/zh_localization_inventory.py --preset onboarding > /tmp/zh-onboarding.md
python3 script/zh_localization_inventory.py --preset workspace > /tmp/zh-workspace.md
python3 script/zh_localization_inventory.py --preset search > /tmp/zh-search.md
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
python3 script/zh_localization_inventory.py --preset modals > /tmp/zh-modals.md
```

Review only `candidate` rows. Add manifest entries in small batches and rerun `zh_apply_localization.py --dry-run --summary`.
````

- [ ] **Step 4: Verify**

Run:

```bash
python3 script/zh_localization_inventory.py --preset onboarding | head -n 40
python3 script/zh_localization_inventory.py --preset settings | head -n 40
python3 script/zh_apply_localization.py --dry-run --summary
git diff --check
```

Expected: inventory prints Markdown tables and apply summary reports `missing: 0`.

- [ ] **Step 5: Commit**

```bash
git add script/zh_localization_inventory.py docs/zh-Hans-localization.md
git commit -m "chore: add zh-Hans localization inventory tool"
```

### Task 4: Finish Onboarding And Auth

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify: `crates/onboarding/src/slides/free_user_no_ai_slide.rs`
- Modify: `crates/onboarding/src/callout/view.rs`
- Modify: `crates/onboarding/src/components/onboarding_callout.rs`
- Modify: `app/src/auth/paste_auth_token_modal.rs`
- Modify: `app/src/auth/auth_view_body.rs`
- Modify: `app/src/auth/auth_view_modal.rs`
- Modify: `app/src/auth/login_failure_notification.rs`
- Modify: `app/src/auth/login_error_modal.rs`
- Modify: `app/src/auth/auth_override_warning_body.rs`

- [ ] **Step 1: Generate inventory**

Run:

```bash
python3 script/zh_localization_inventory.py --preset onboarding > /tmp/zh-onboarding.md
```

- [ ] **Step 2: Translate `free_user_no_ai_slide.rs` first**

Add manifest entries for the remaining visible plan and paywall copy. Known candidates include:

- `Access to frontier OpenAI, Anthropic, and Google models`
- `Access to Reload credits and volume-based discounts`
- `Extended cloud agents access`
- `Highest codebase indexing limits`
- `Unlimited Warp Drive objects and collaboration`
- `Private email support`
- `Unlimited cloud conversation storage`
- `Classic terminal with third-party agents`
- `A modern terminal that supports third-party agents (Claude Code, Codex, Gemini CLI) and classic terminal workflows.`
- `Free`
- `Subscribe`

- [ ] **Step 3: Translate auth modal copy**

Add manifest entries for paste-token, login error, login failure, auth view, and override-warning modals. Keep auth token field names understandable: use `认证令牌` for `Auth Token`, `粘贴` for `Paste`, and `浏览器登录` for browser login copy where space is tight.

- [ ] **Step 4: Apply and format**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
```

- [ ] **Step 5: Compile touched crates**

Run:

```bash
cargo check -p onboarding
cargo check -p app
```

Expected: both commands exit 0. If `cargo check -p app` is too slow or blocked by local dependencies, record the exact failure in `docs/zh-Hans-localization.md`.

- [ ] **Step 6: Commit**

```bash
git add resources/localization/zh-Hans-overrides.toml crates/onboarding/src app/src/auth docs/zh-Hans-localization.md
git commit -m "feat: expand zh-Hans onboarding and auth copy"
```

### Task 5: Translate Workspace Shell And Menus

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify: `app/src/workspace/view.rs`
- Modify: `app/src/workspace/view/vertical_tabs.rs`
- Modify: `app/src/workspace/view/left_panel.rs`
- Modify: `app/src/workspace/view/right_panel.rs`
- Modify: `app/src/workspace/view/conversation_list/view.rs`
- Modify: `app/src/workspace/close_session_confirmation_dialog.rs`
- Modify: `app/src/workspace/rewind_confirmation_dialog.rs`
- Modify: `app/src/workspace/toast_stack.rs`
- Modify: `app/src/app_menus.rs`
- Modify: `app/src/menu.rs`
- Modify: `crates/warpui/src/platform/mac/menus.rs`

- [ ] **Step 1: Generate inventory**

Run:

```bash
python3 script/zh_localization_inventory.py --preset workspace > /tmp/zh-workspace.md
```

- [ ] **Step 2: Translate top-level user menu**

Prioritize the block around `Workspace::user_menu_items` in `app/src/workspace/view.rs`. Known labels:

- `What's new` -> `新增内容`
- `Keyboard shortcuts` -> `键盘快捷键`
- `Documentation` -> `文档`
- `Feedback` -> `反馈`
- `View Warp logs` -> `查看 Warp 日志`
- `Sign up` -> `注册`
- `Billing and usage` -> `账单与用量`
- `Invite a friend` -> `邀请朋友`
- `Log out` -> `退出登录`

- [ ] **Step 3: Translate panel and toolbar labels**

Known labels:

- `Agent management panel` -> `Agent 管理面板`
- `Tabs panel` -> `标签页面板`
- `Project explorer` -> `项目浏览器`
- `Global search` -> `全局搜索`
- `Agent conversations` -> `Agent 对话`
- `Tools panel` -> `工具面板`
- `Some features may be unavailable offline` -> `部分功能离线时可能不可用`

- [ ] **Step 4: Translate conversation list and panel actions**

Known labels:

- `Search` -> `搜索`
- `No conversations yet` -> `暂无对话`
- `New conversation` -> `新建对话`
- `Delete` -> `删除`
- `Share conversation` -> `分享对话`
- `Fork in new pane` -> `在新窗格中分叉`
- `Fork in new tab` -> `在新标签页中分叉`
- `Close panel` -> `关闭面板`
- `Code review` -> `代码审查`

- [ ] **Step 5: Translate update and common toast copy**

Known labels:

- `Update Warp` -> `更新 Warp`
- `Update and relaunch Warp` -> `更新并重启 Warp`
- `Update Warp manually` -> `手动更新 Warp`
- `Warp updated!` -> `Warp 已更新！`
- `Learn more` -> `了解更多`
- `View changelog` -> `查看更新日志`
- `View` -> `查看`
- `Undo` -> `撤销`

- [ ] **Step 6: Apply, format, compile**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo check -p app
```

- [ ] **Step 7: Commit**

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace app/src/app_menus.rs app/src/menu.rs crates/warpui/src/platform/mac/menus.rs
git commit -m "feat: expand zh-Hans workspace shell copy"
```

### Task 6: Translate Command Palette, Command Search, And Slash Menus

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify: `app/src/search/command_palette/**/*.rs`
- Modify: `app/src/search/command_search/**/*.rs`
- Modify: `app/src/search/ai_context_menu/**/*.rs`
- Modify: `app/src/search/slash_command_menu/**/*.rs`

- [ ] **Step 1: Generate inventory**

Run:

```bash
python3 script/zh_localization_inventory.py --preset search > /tmp/zh-search.md
```

- [ ] **Step 2: Translate core palette chrome**

Known labels:

- `Search for a command` -> `搜索命令`
- `No results found` -> `未找到结果`
- `Search your history, workflows, and more` -> `搜索历史、工作流等`
- `No results found.` -> `未找到结果。`
- `Command Search` -> `命令搜索`
- `Search saved prompts` -> `搜索已保存提示词`

- [ ] **Step 3: Translate zero-state and category labels**

Review:

- `app/src/search/command_palette/zero_state.rs`
- `app/src/search/command_palette/zero_state/items.rs`
- `app/src/search/command_search/zero_state.rs`
- `app/src/search/ai_context_menu/view.rs`

Keep user content and command text untouched. Translate only static UI titles, category labels, helper copy, and empty-state copy.

- [ ] **Step 4: Translate fallback labels**

Known labels:

- `Untitled` -> `未命名`
- `Notebook:` -> `笔记本：`
- `Workflow:` -> `工作流：`
- `Environment Variables` -> `环境变量`

- [ ] **Step 5: Apply, format, compile, run focused tests**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo test -p app command_palette
cargo test -p app command_search
```

Expected: tests pass or unsupported local test prerequisites are documented.

- [ ] **Step 6: Commit**

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/search
git commit -m "feat: expand zh-Hans search surface copy"
```

### Task 7: Translate Settings Navigation And Core Pages

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify: `app/src/settings_view/mod.rs`
- Modify: `app/src/settings_view/nav.rs`
- Modify: `app/src/settings_view/settings_page.rs`
- Modify: `app/src/settings_view/main_page.rs`
- Modify: `app/src/settings_view/appearance_page.rs`
- Modify: `app/src/settings_view/features_page.rs`
- Modify: `app/src/settings_view/keybindings.rs`
- Modify: `app/src/settings_view/privacy_page.rs`
- Modify: `app/src/settings_view/warpify_page.rs`

- [ ] **Step 1: Generate inventory**

Run:

```bash
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
```

- [ ] **Step 2: Translate settings sidebar labels**

Known `SettingsSection` labels:

- `Billing and usage` -> `账单与用量`
- `Keyboard shortcuts` -> `键盘快捷键`
- `Shared blocks` -> `共享块`
- `MCP Servers` -> `MCP 服务器`
- `Warp Drive` -> `Warp Drive`
- `Warp Agent` -> `Warp Agent`
- `Profiles` -> `配置档`
- `MCP servers` -> `MCP 服务器`
- `Knowledge` -> `知识`
- `Third party CLI agents` -> `第三方 CLI Agent`
- `Indexing and projects` -> `索引与项目`
- `Editor and Code Review` -> `编辑器与代码审查`
- `Environments` -> `环境`
- `Oz Cloud API Keys` -> `Oz Cloud API 密钥`
- `Agents` -> `Agent`
- `Code` -> `代码`
- `Cloud platform` -> `云平台`

- [ ] **Step 3: Translate settings search and footer chrome**

Review `app/src/settings_view/mod.rs`, `nav.rs`, `settings_page.rs`, and `settings_file_footer.rs`. Translate visible search placeholders, filter empty states, footer buttons, settings file errors, and "Open file" / "Fix with Oz" style actions.

- [ ] **Step 4: Translate core page labels**

Prioritize high-frequency pages:

- Account: `app/src/settings_view/main_page.rs`
- Appearance: `app/src/settings_view/appearance_page.rs`
- Features: `app/src/settings_view/features_page.rs`
- Keybindings: `app/src/settings_view/keybindings.rs`
- Privacy: `app/src/settings_view/privacy_page.rs`
- Warpify: `app/src/settings_view/warpify_page.rs`

- [ ] **Step 5: Apply, format, compile, run settings tests**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo test -p app settings_view
cargo test -p app settings
```

- [ ] **Step 6: Commit**

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/settings_view
git commit -m "feat: expand zh-Hans settings copy"
```

### Task 8: Translate Agent, Code, MCP, Billing, And Environment Settings

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify: `app/src/settings_view/ai_page.rs`
- Modify: `app/src/settings_view/code_page.rs`
- Modify: `app/src/settings_view/mcp_servers/**/*.rs`
- Modify: `app/src/settings_view/billing_and_usage*.rs`
- Modify: `app/src/settings_view/billing_and_usage/**/*.rs`
- Modify: `app/src/settings_view/environments_page.rs`
- Modify: `app/src/settings_view/platform_page.rs`
- Modify: `app/src/settings_view/platform/**/*.rs`
- Modify: `app/src/settings_view/execution_profile_view.rs`
- Modify: `app/src/settings_view/update_environment_form.rs`

- [ ] **Step 1: Use the existing settings inventory**

Run:

```bash
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
```

- [ ] **Step 2: Translate AI / Agent settings**

Translate section labels, descriptions, buttons, dropdown labels, empty states, model endpoint modals, and CLI agent instructions. Keep model names, vendor names, API parameter names, CLI binary names, and config snippets unchanged.

- [ ] **Step 3: Translate Code settings**

Translate code indexing, project rules, editor, code review, and execution profile copy. Keep setting keys and config-file examples unchanged.

- [ ] **Step 4: Translate MCP settings**

Translate gallery/install/update/remove UI copy. Keep MCP server package names, command names, JSON config keys, and server identifiers unchanged.

- [ ] **Step 5: Translate billing and environment settings**

Translate plan, usage, overage, API key, environment, and cloud platform labels. Keep currency symbols, plan SKU names, product identifiers, API key token examples, and server-provided dynamic text unchanged.

- [ ] **Step 6: Apply and test**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo test -p app ai_page
cargo test -p app mcp_servers
cargo test -p app billing_and_usage
cargo test -p app environments_page
```

- [ ] **Step 7: Commit**

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/settings_view
git commit -m "feat: expand zh-Hans advanced settings copy"
```

### Task 9: Translate Modals, Toasts, And Terminal/Agent Panels

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify: `app/src/themes`
- Modify: `app/src/tab_configs`
- Modify: `app/src/billing`
- Modify: `app/src/drive`
- Modify: `app/src/terminal`
- Modify: `app/src/ai`
- Modify: `app/src/workspace/view/*.rs`

- [ ] **Step 1: Generate modal inventory**

Run:

```bash
python3 script/zh_localization_inventory.py --preset modals > /tmp/zh-modals.md
```

- [ ] **Step 2: Translate common modal actions first**

Common labels:

- `Cancel` -> `取消`
- `Save` -> `保存`
- `Create` -> `创建`
- `Delete` -> `删除`
- `Remove` -> `移除`
- `Open` -> `打开`
- `Close` -> `关闭`
- `Make default` -> `设为默认`
- `Edit config` -> `编辑配置`
- `Set up` -> `设置`
- `View logs` -> `查看日志`

- [ ] **Step 3: Translate destructive confirmation dialogs**

Review all files matching:

```bash
rg --files app/src | rg '(confirmation|delete|remove|deletion|destructive).*\\.rs$'
```

For destructive actions, keep Chinese copy explicit and conservative. Example: translate `Delete` as `删除`, not `移除`, when the underlying operation deletes user data.

- [ ] **Step 4: Translate terminal and Agent visible panels**

Prioritize:

- `app/src/terminal/input/slash_commands`
- `app/src/terminal/input/inline_menu`
- `app/src/terminal/view/context_menu.rs`
- `app/src/ai/blocklist/agent_view`
- `app/src/ai/blocklist/inline_action`
- `app/src/ai/agent_management`

Keep shell commands, code, command history, AI-generated content, user prompts, and file paths untouched.

- [ ] **Step 5: Apply and test**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo check -p app
```

- [ ] **Step 6: Commit**

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/themes app/src/tab_configs app/src/billing app/src/drive app/src/terminal app/src/ai app/src/workspace/view
git commit -m "feat: expand zh-Hans modal toast and agent copy"
```

### Task 10: Add Coverage Reporting And Release Checklist

**Files:**

- Modify: `script/zh_localization_inventory.py`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Add coverage counts**

Add:

```bash
python3 script/zh_localization_inventory.py --preset settings --coverage
```

Expected output:

```text
preset: settings
covered: <number>
candidates: <number>
coverage: <percent>
```

- [ ] **Step 2: Add release checklist**

Add this to `docs/zh-Hans-localization.md`:

````markdown
## Local release checklist

- `python3 script/zh_apply_localization.py --dry-run --summary`
- `python3 script/zh_localization_inventory.py --preset onboarding --coverage`
- `python3 script/zh_localization_inventory.py --preset workspace --coverage`
- `python3 script/zh_localization_inventory.py --preset search --coverage`
- `python3 script/zh_localization_inventory.py --preset settings --coverage`
- `python3 script/zh_localization_inventory.py --preset modals --coverage`
- `cargo fmt --check`
- `git diff --check`
- `cargo check -p onboarding`
- `cargo check -p app`
- `./script/run`

Manual smoke paths:

- Fresh onboarding: terminal-only path and Agent path.
- Login flow: browser login, token paste fallback, privacy settings, skip/disable confirmation.
- Workspace shell: user menu, left/right panels, vertical tabs, conversation list.
- Search: command palette, command search, slash commands, AI context menu.
- Settings: sidebar search, Account, Appearance, Features, Privacy, AI, Code, MCP, Billing, Environments.
- Modals/toasts: update toast, destructive dialogs, theme modal, tab config modal, terminal share modal.
````

- [ ] **Step 3: Verify**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
cargo fmt --check
git diff --check
```

- [ ] **Step 4: Commit**

```bash
git add script/zh_localization_inventory.py docs/zh-Hans-localization.md
git commit -m "docs: add zh-Hans localization release checklist"
```

## Acceptance Criteria

- `python3 script/zh_apply_localization.py --dry-run --summary` reports `missing: 0`.
- Inventory coverage reports exist for onboarding, workspace, search, settings, and modals.
- High-value user-visible strings are translated in:
  - onboarding and auth flows
  - workspace top-level menus and panels
  - command palette and command search
  - settings navigation and core pages
  - common modals and toasts
- `cargo fmt --check` passes.
- `git diff --check` passes.
- `cargo check -p onboarding` passes.
- `cargo check -p app` passes, or any local-only dependency blocker is documented with exact output and a narrower passing command.
- Manual app smoke test covers every path listed in the release checklist.
- No translated string changes telemetry IDs, setting keys, action IDs, command IDs, config examples, or user-generated content.

## Risks And Mitigations

- **Risk: exact string replacement changes comments or non-UI literals.**
  - Mitigation: harden the scanner to skip comments, use inventory exclusions, and review every manifest candidate.
- **Risk: translated labels overflow compact UI.**
  - Mitigation: keep concise glossary terms, manually smoke small surfaces such as buttons, menu items, pills, and vertical tabs.
- **Risk: upstream changes cause silent missed translations.**
  - Mitigation: `--dry-run --summary` must fail on missing source strings unless the target is already applied.
- **Risk: settings/config examples get translated accidentally.**
  - Mitigation: exclude code blocks, config key strings, and examples during inventory review; keep manifest entries exact and file-scoped.
- **Risk: search quality changes if action names or searchable labels are translated.**
  - Mitigation: only translate rendered labels where acceptable; keep command/action IDs and keybinding names unchanged. Run command palette and command search tests.
- **Risk: server-provided English remains visible.**
  - Mitigation: classify dynamic server content separately; do not fake translations for server values in this local fork unless a local mapping already exists.

## Suggested Batch Order

1. Tooling hardening and inventory.
2. Onboarding/auth completion.
3. Workspace shell/menu completion.
4. Search surfaces.
5. Settings navigation/core pages.
6. Advanced settings.
7. Modals/toasts/terminal/Agent panels.
8. Coverage reporting and release checklist.

This order keeps visible progress high while reducing risk before touching the largest string surfaces.
