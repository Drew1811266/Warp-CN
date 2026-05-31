# Warp zh-Hans 汉化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前 `drew/zh-Hans-localization` 分支从“首轮高可见界面汉化”推进到“可维护、可同步上游、核心界面广覆盖”的简体中文本地化版本。

**Architecture:** 延续当前本地 fork 方案，不引入运行时语言切换框架。所有翻译条目继续收敛在 `resources/localization/zh-Hans-overrides.toml`，由 `script/zh_apply_localization.py` 做精确替换；在大规模扩展翻译前，先补齐库存扫描、覆盖统计、漂移检测和验证流程。

**Tech Stack:** Rust UI 源码、Python 3 脚本、TOML manifest、`cargo fmt`、`cargo check`、局部 Rust 测试、`./script/run` 人工冒烟。

---

## 1. 当前基线

当前分支：`drew/zh-Hans-localization`。

当前已完成：

- 已建立本地汉化 manifest：`resources/localization/zh-Hans-overrides.toml`。
- 已建立应用脚本：`script/zh_apply_localization.py`。
- 已创建维护文档：`docs/zh-Hans-localization.md`。
- 已汉化 122 个精确字符串。
- 当前覆盖重点：
  - onboarding 首屏与主要流程。
  - 登录 / AI opt-out / 隐私设置。
  - 纵向标签栏部分标签。
  - 工作区部分搜索占位符和顶层入口。

当前验证命令已经通过：

```bash
python3 script/zh_apply_localization.py --dry-run
cargo fmt --check
git diff --check
```

当前未完成：

- 设置页大部分文案。
- 命令面板、命令搜索、slash menu。
- workspace 用户菜单、左右面板、toast。
- modal、确认框、主题、tab config、billing、terminal、Agent 面板。
- macOS 原生菜单。
- 覆盖率统计和候选字符串库存。

## 2. 总体策略

实施分三条线并行推进，但提交时按阶段顺序落地：

1. **工具链线**
   - 加固替换脚本。
   - 增加候选字符串库存扫描。
   - 增加覆盖率统计。
   - 降低后续大规模 manifest 维护风险。

2. **翻译覆盖线**
   - 按界面入口分批翻译。
   - 每批只覆盖一组用户路径。
   - 每批有独立验证和提交。

3. **验证发布线**
   - 每批跑 dry-run、格式检查和针对性 compile/test。
   - 大阶段完成后跑人工冒烟。
   - 建立本地 release checklist。

不做的事：

- 不引入完整 i18n runtime。
- 不新增语言设置 UI。
- 不翻译 telemetry event、settings key、command id、binding id、URL、文件路径、模型 ID、协议字段。
- 不翻译用户生成内容、终端输出、代码片段、配置示例里的 key。

## 3. 里程碑总览

| 里程碑 | 目标 | 预计提交 | 完成判定 |
| --- | --- | ---: | --- |
| M0 | 固化基线 | 1 | 当前状态可复现，文档记录清楚 |
| M1 | 工具链加固 | 2 | 有 summary、库存扫描、覆盖统计 |
| M2 | 完成 onboarding/auth | 1 | 新用户路径基本中文 |
| M3 | 完成 workspace shell | 1 | 主菜单、面板、常见 toast 中文 |
| M4 | 完成搜索类入口 | 1 | command palette/search/slash menu 中文 |
| M5 | 完成 settings 核心页 | 1 | 设置导航与高频设置项中文 |
| M6 | 完成高级设置页 | 1 | AI/Code/MCP/Billing/Environment 中文 |
| M7 | 完成 modals/toasts/panels | 1-2 | 常见弹窗、确认框、Agent/terminal 面板中文 |
| M8 | 发布验收 | 1 | 覆盖率、编译、人工冒烟均记录 |

建议总提交数：9 到 11 个。不要把所有翻译压成一个大提交。

## 4. 每批固定执行流程

每个翻译批次都按同一套流程执行：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset <preset> > /tmp/zh-<preset>.md
```

然后人工审查 `/tmp/zh-<preset>.md` 里的 `candidate` 行，只挑本批范围内的用户可见文案加入 manifest。

应用翻译：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
```

按批次跑目标验证，例如：

```bash
cargo check -p onboarding
cargo check -p app
cargo test -p app command_palette
cargo test -p app settings_view
```

提交前检查：

```bash
git diff --stat
git diff --check
git status --short
```

提交粒度：

```bash
git add <本批文件>
git commit -m "<type>: <scope>"
```

## 5. M0 固化当前基线

### 目标

让当前状态变成可追踪起点，后续每次扩展都能知道覆盖范围和验证状态。

### 修改文件

- `docs/zh-Hans-localization.md`

### 执行步骤

- [ ] 在 `docs/zh-Hans-localization.md` 增加 `Status` 段落。

建议内容：

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

- [ ] 运行验证：

```bash
python3 script/zh_apply_localization.py --dry-run
cargo fmt --check
git diff --check
```

- [ ] 提交：

```bash
git add docs/zh-Hans-localization.md
git commit -m "docs: record zh-Hans localization baseline"
```

### 验收标准

- 文档明确当前覆盖范围。
- 三个验证命令均退出 0。

## 6. M1 工具链加固

### 目标

在继续扩大翻译前，先解决两个维护风险：

- 当前替换器可能匹配注释中的双引号字符串。
- 后续 manifest 规模变大后，需要知道哪些 UI 字符串还没覆盖。

### 修改文件

- `script/zh_apply_localization.py`
- `script/zh_localization_inventory.py`
- `docs/zh-Hans-localization.md`

### 6.1 加固 apply 脚本

- [ ] 在 `replace_rust_string_literals` 中跳过 `//` 行注释。
- [ ] 跳过 `/* ... */` 块注释。
- [ ] 跳过 Rust char literal，例如 `'x'`。
- [ ] 增加 manifest 重复项检测，重复 `(path, source)` 直接报错。
- [ ] 增加 `--summary` 输出。

`--summary` 目标输出：

```text
entries: 122
files: 10
already_applied: 122
would_change: 0
missing: 0
```

验证：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
python3 script/zh_apply_localization.py --dry-run --summary
git diff --check
cargo fmt --check
```

提交：

```bash
git add script/zh_apply_localization.py
git commit -m "chore: harden zh-Hans localization apply script"
```

### 6.2 新增库存扫描脚本

- [ ] 新建 `script/zh_localization_inventory.py`。
- [ ] 支持扫描 Rust 普通字符串字面量。
- [ ] 支持跳过注释。
- [ ] 支持排除测试、模型数据、bundled resources。
- [ ] 支持读取 manifest，标记已覆盖项。
- [ ] 默认输出 Markdown 表格。

基本命令：

```bash
python3 script/zh_localization_inventory.py app/src/settings_view app/src/search crates/onboarding/src
```

输出列：

```markdown
| status | path | line | literal |
| --- | --- | ---: | --- |
```

状态：

- `covered-source`
- `covered-target`
- `candidate`

支持 preset：

```bash
python3 script/zh_localization_inventory.py --preset onboarding
python3 script/zh_localization_inventory.py --preset workspace
python3 script/zh_localization_inventory.py --preset search
python3 script/zh_localization_inventory.py --preset settings
python3 script/zh_localization_inventory.py --preset modals
```

preset 范围：

| preset | 范围 |
| --- | --- |
| onboarding | `crates/onboarding/src`, `app/src/auth` |
| workspace | `app/src/workspace`, `app/src/app_menus.rs`, `app/src/menu.rs` |
| search | `app/src/search` |
| settings | `app/src/settings_view` |
| modals | `app/src/auth`, `app/src/billing`, `app/src/themes`, `app/src/tab_configs`, `app/src/drive`, `app/src/terminal`, `app/src/ai` |

验证：

```bash
python3 script/zh_localization_inventory.py --preset onboarding | head -n 40
python3 script/zh_localization_inventory.py --preset settings | head -n 40
python3 script/zh_apply_localization.py --dry-run --summary
git diff --check
```

提交：

```bash
git add script/zh_localization_inventory.py docs/zh-Hans-localization.md
git commit -m "chore: add zh-Hans localization inventory tool"
```

### 6.3 覆盖率统计

- [ ] 给库存脚本增加 `--coverage`。

命令：

```bash
python3 script/zh_localization_inventory.py --preset settings --coverage
```

输出：

```text
preset: settings
covered: <number>
candidates: <number>
coverage: <percent>
```

验收标准：

- 五个 preset 都能输出候选清单。
- 五个 preset 都能输出 coverage。
- apply 脚本 summary 显示 `missing: 0`。

## 7. M2 完成 onboarding/auth 汉化

### 目标

让新用户从启动、选择使用方式、登录、隐私设置、跳过 AI/Drive、token fallback 的路径基本都是中文。

### 修改文件

- `resources/localization/zh-Hans-overrides.toml`
- `crates/onboarding/src/slides/free_user_no_ai_slide.rs`
- `crates/onboarding/src/callout/view.rs`
- `crates/onboarding/src/components/onboarding_callout.rs`
- `app/src/auth/paste_auth_token_modal.rs`
- `app/src/auth/auth_view_body.rs`
- `app/src/auth/auth_view_modal.rs`
- `app/src/auth/login_failure_notification.rs`
- `app/src/auth/login_error_modal.rs`
- `app/src/auth/auth_override_warning_body.rs`

### 执行步骤

- [ ] 生成候选清单：

```bash
python3 script/zh_localization_inventory.py --preset onboarding > /tmp/zh-onboarding.md
```

- [ ] 优先处理 `free_user_no_ai_slide.rs` 中的剩余英文：
  - `Back`
  - `Next`
  - `Get Warping`
  - `Subscribe`
  - `Free`
  - plan/paywall benefit copy。

- [ ] 处理 auth modal：
  - paste auth token modal。
  - login error modal。
  - login failure notification。
  - auth override warning。
  - browser login fallback。

- [ ] 应用和验证：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo check -p onboarding
cargo check -p app
```

- [ ] 提交：

```bash
git add resources/localization/zh-Hans-overrides.toml crates/onboarding/src app/src/auth docs/zh-Hans-localization.md
git commit -m "feat: expand zh-Hans onboarding and auth copy"
```

### 人工验收

- 新安装首次打开。
- Agent 路径 onboarding。
- Terminal-only 路径 onboarding。
- 浏览器登录路径。
- token paste fallback。
- privacy settings。
- disable AI / disable Warp Drive 确认框。

## 8. M3 完成 workspace shell 与菜单汉化

### 目标

让用户进入主界面后最常看到的 shell、用户菜单、左右面板、纵向标签栏、常见 toast 和更新提示变成中文。

### 修改文件

- `resources/localization/zh-Hans-overrides.toml`
- `app/src/workspace/view.rs`
- `app/src/workspace/view/vertical_tabs.rs`
- `app/src/workspace/view/left_panel.rs`
- `app/src/workspace/view/right_panel.rs`
- `app/src/workspace/view/conversation_list/view.rs`
- `app/src/workspace/close_session_confirmation_dialog.rs`
- `app/src/workspace/rewind_confirmation_dialog.rs`
- `app/src/workspace/toast_stack.rs`
- `app/src/app_menus.rs`
- `app/src/menu.rs`
- `crates/warpui/src/platform/mac/menus.rs`

### 执行步骤

- [ ] 生成候选清单：

```bash
python3 script/zh_localization_inventory.py --preset workspace > /tmp/zh-workspace.md
```

- [ ] 处理 `Workspace::user_menu_items`：
  - `What's new` -> `新增内容`
  - `Keyboard shortcuts` -> `键盘快捷键`
  - `Documentation` -> `文档`
  - `Feedback` -> `反馈`
  - `View Warp logs` -> `查看 Warp 日志`
  - `Sign up` -> `注册`
  - `Billing and usage` -> `账单与用量`
  - `Upgrade` -> `升级`
  - `Invite a friend` -> `邀请朋友`
  - `Log out` -> `退出登录`

- [ ] 处理主界面面板按钮：
  - `Agent management panel` -> `Agent 管理面板`
  - `Tabs panel` -> `标签页面板`
  - `Project explorer` -> `项目浏览器`
  - `Global search` -> `全局搜索`
  - `Agent conversations` -> `Agent 对话`
  - `Tools panel` -> `工具面板`
  - `Close panel` -> `关闭面板`

- [ ] 处理 conversation list：
  - 搜索框。
  - 空状态。
  - 新建对话。
  - 删除 / 分享 / fork 菜单。

- [ ] 处理更新和 toast：
  - `Update Warp`
  - `Update and relaunch Warp`
  - `Update Warp manually`
  - `Warp updated!`
  - `Learn more`
  - `View changelog`
  - `Undo`

- [ ] 处理 macOS 菜单中可见英文，但不要翻译 action id 或系统保留项。

- [ ] 应用和验证：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo check -p app
```

- [ ] 提交：

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace app/src/app_menus.rs app/src/menu.rs crates/warpui/src/platform/mac/menus.rs
git commit -m "feat: expand zh-Hans workspace shell copy"
```

### 人工验收

- 主界面用户菜单。
- 左面板按钮 tooltip。
- 右面板按钮 tooltip。
- conversation list 搜索、右键菜单。
- update toast。
- vertical tabs 设置弹窗。
- macOS 应用菜单。

## 9. M4 完成搜索入口汉化

### 目标

覆盖用户高频输入入口：command palette、command search、AI context menu、slash command menu。

### 修改文件

- `resources/localization/zh-Hans-overrides.toml`
- `app/src/search/command_palette/**/*.rs`
- `app/src/search/command_search/**/*.rs`
- `app/src/search/ai_context_menu/**/*.rs`
- `app/src/search/slash_command_menu/**/*.rs`

### 执行步骤

- [ ] 生成候选清单：

```bash
python3 script/zh_localization_inventory.py --preset search > /tmp/zh-search.md
```

- [ ] 处理基础 chrome：
  - `Search for a command` -> `搜索命令`
  - `No results found` -> `未找到结果`
  - `Search your history, workflows, and more` -> `搜索历史、工作流等`
  - `Command Search` -> `命令搜索`
  - `Command Palette` -> `命令面板`

- [ ] 处理 zero-state：
  - suggested actions。
  - recently used。
  - empty state。
  - helper copy。

- [ ] 处理各数据源静态标签：
  - notebooks。
  - workflows。
  - env var collections。
  - repos。
  - files。
  - navigation。
  - launch configs。

- [ ] 保留用户内容：
  - 用户命令历史不翻译。
  - 文件名不翻译。
  - workflow/notebook 自定义标题不翻译。
  - shell command 不翻译。

- [ ] 应用和验证：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo test -p app command_palette
cargo test -p app command_search
```

- [ ] 提交：

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/search
git commit -m "feat: expand zh-Hans search surface copy"
```

### 人工验收

- 打开 command palette。
- 搜索一个命令。
- 搜索一个文件。
- 打开 command search。
- 输入无结果查询。
- 打开 slash command menu。
- 打开 AI context menu。

## 10. M5 完成 settings 核心页汉化

### 目标

设置页是剩余最大用户可见区域。先完成导航、搜索、footer、Account、Appearance、Features、Keybindings、Privacy、Warpify 等核心页。

### 修改文件

- `resources/localization/zh-Hans-overrides.toml`
- `app/src/settings_view/mod.rs`
- `app/src/settings_view/nav.rs`
- `app/src/settings_view/settings_page.rs`
- `app/src/settings_view/main_page.rs`
- `app/src/settings_view/appearance_page.rs`
- `app/src/settings_view/features_page.rs`
- `app/src/settings_view/keybindings.rs`
- `app/src/settings_view/privacy_page.rs`
- `app/src/settings_view/warpify_page.rs`
- `app/src/settings_view/settings_file_footer.rs`

### 执行步骤

- [ ] 生成候选清单：

```bash
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
```

- [ ] 处理 settings sidebar：
  - `Agents` -> `Agent`
  - `Code` -> `代码`
  - `Cloud platform` -> `云平台`
  - `Billing and usage` -> `账单与用量`
  - `Keyboard shortcuts` -> `键盘快捷键`
  - `Shared blocks` -> `共享块`
  - `MCP Servers` -> `MCP 服务器`
  - `Profiles` -> `配置档`
  - `Knowledge` -> `知识`
  - `Third party CLI agents` -> `第三方 CLI Agent`
  - `Indexing and projects` -> `索引与项目`
  - `Editor and Code Review` -> `编辑器与代码审查`
  - `Environments` -> `环境`

- [ ] 处理 settings 搜索：
  - placeholder。
  - no results。
  - 匹配高亮周边说明。

- [ ] 处理 settings file footer：
  - 打开文件。
  - 修复提示。
  - 错误提示。

- [ ] 处理核心页面静态标签：
  - Account。
  - Appearance。
  - Features。
  - Keybindings。
  - Privacy。
  - Warpify。

- [ ] 应用和验证：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo test -p app settings_view
cargo test -p app settings
```

- [ ] 提交：

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/settings_view
git commit -m "feat: expand zh-Hans settings core copy"
```

### 人工验收

- 打开 Settings。
- 逐个点击 sidebar 一级项。
- 使用 settings 搜索。
- 修改一个 dropdown。
- 修改一个 toggle。
- 打开 keybindings 页面。
- 打开 privacy 页面。

## 11. M6 完成高级 settings 汉化

### 目标

覆盖设置页内较复杂的产品区域：AI/Agent、Code、MCP、Billing、Environments、Platform、Execution Profile。

### 修改文件

- `resources/localization/zh-Hans-overrides.toml`
- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/code_page.rs`
- `app/src/settings_view/mcp_servers/**/*.rs`
- `app/src/settings_view/mcp_servers_page.rs`
- `app/src/settings_view/billing_and_usage_page.rs`
- `app/src/settings_view/billing_and_usage_page_v2.rs`
- `app/src/settings_view/billing_and_usage/**/*.rs`
- `app/src/settings_view/environments_page.rs`
- `app/src/settings_view/platform_page.rs`
- `app/src/settings_view/platform/**/*.rs`
- `app/src/settings_view/execution_profile_view.rs`
- `app/src/settings_view/update_environment_form.rs`

### 执行步骤

- [ ] 复用 settings inventory：

```bash
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
```

- [ ] 处理 AI/Agent 设置：
  - profile。
  - model。
  - autonomy。
  - MCP。
  - knowledge。
  - third-party CLI agents。

- [ ] 处理 Code 设置：
  - indexing。
  - project rules。
  - editor。
  - code review。
  - execution profile。

- [ ] 处理 MCP 设置：
  - gallery。
  - install。
  - update。
  - remove。
  - logs。
  - config editor 周边提示。

- [ ] 处理 Billing：
  - usage。
  - plan。
  - overage。
  - API keys。
  - credits。

- [ ] 处理 Environments / Platform：
  - 环境列表。
  - 创建 / 更新环境。
  - handoff environment。
  - API key modal。

- [ ] 不翻译：
  - 模型名称。
  - API 参数名。
  - CLI binary 名称。
  - JSON key。
  - package/server id。
  - 动态后端返回的产品或团队名称。

- [ ] 应用和验证：

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

- [ ] 提交：

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/settings_view
git commit -m "feat: expand zh-Hans advanced settings copy"
```

### 人工验收

- 打开 Warp Agent 设置。
- 打开 Profiles。
- 打开 MCP servers。
- 打开 Code indexing。
- 打开 Billing and usage。
- 打开 Environments。
- 打开 API key 页面或 modal。

## 12. M7 完成 modals、toast、terminal、Agent 面板汉化

### 目标

覆盖高频弹窗、破坏性确认框、主题配置、tab config、terminal 分享、Agent 操作面板等剩余散点。

### 修改文件

- `resources/localization/zh-Hans-overrides.toml`
- `app/src/themes`
- `app/src/tab_configs`
- `app/src/billing`
- `app/src/drive`
- `app/src/terminal`
- `app/src/ai`
- `app/src/workspace/view`

### 执行步骤

- [ ] 生成候选清单：

```bash
python3 script/zh_localization_inventory.py --preset modals > /tmp/zh-modals.md
```

- [ ] 先处理通用按钮：
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

- [ ] 处理破坏性确认框：

```bash
rg --files app/src | rg '(confirmation|delete|remove|deletion|destructive).*\\.rs$'
```

对删除、重置、撤销、关闭会话这类文案使用明确中文，不弱化风险。

- [ ] 处理主题相关 modal：
  - create theme。
  - delete theme。
  - image state。

- [ ] 处理 tab configs：
  - new worktree modal。
  - session config modal。
  - params modal。
  - action sidecar。

- [ ] 处理 terminal：
  - context menu。
  - share modal。
  - role change modal。
  - auto reload modal。
  - slash command view。
  - inline menu。

- [ ] 处理 Agent：
  - agent input footer。
  - orchestration controls。
  - setup command block。
  - auth secret selector。
  - notification toast。
  - permission/confirmation copy。

- [ ] 应用和验证：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
cargo check -p app
```

- [ ] 提交：

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/themes app/src/tab_configs app/src/billing app/src/drive app/src/terminal app/src/ai app/src/workspace/view
git commit -m "feat: expand zh-Hans modal toast and agent copy"
```

### 人工验收

- 创建主题。
- 删除主题。
- 新建 tab config。
- 新建 worktree config。
- 关闭 session。
- rewind 确认。
- terminal context menu。
- share modal。
- Agent toolbar。
- Agent 权限确认。

## 13. M8 发布验收

### 目标

形成一个可重复的本地中文版本发布检查流程。

### 修改文件

- `docs/zh-Hans-localization.md`
- `script/zh_localization_inventory.py`

### 执行步骤

- [ ] 在文档中加入 release checklist。

必须包含：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
cargo fmt --check
git diff --check
cargo check -p onboarding
cargo check -p app
./script/run
```

- [ ] 执行完整命令集。
- [ ] 记录失败项和原因。
- [ ] 如果 `cargo check -p app` 因本地环境失败，记录 exact output，并跑可用的窄测试替代。
- [ ] 运行人工冒烟。

人工冒烟路径：

- fresh onboarding：Agent 路径。
- fresh onboarding：Terminal-only 路径。
- login：browser login。
- login：token paste fallback。
- login：privacy settings。
- workspace：用户菜单。
- workspace：left/right panel。
- workspace：vertical tabs。
- search：command palette。
- search：command search。
- search：slash command。
- settings：Account、Appearance、Features、Privacy、AI、Code、MCP、Billing、Environments。
- modals/toasts：update toast、destructive dialog、theme modal、tab config modal、terminal share modal。

- [ ] 提交：

```bash
git add docs/zh-Hans-localization.md script/zh_localization_inventory.py
git commit -m "docs: add zh-Hans localization release checklist"
```

## 14. 术语与风格规则

必须统一：

| English | 中文 |
| --- | --- |
| Settings | 设置 |
| Keyboard shortcuts | 键盘快捷键 |
| Billing and usage | 账单与用量 |
| Workspace | 工作区 |
| Project explorer | 项目浏览器 |
| Global search | 全局搜索 |
| Tools panel | 工具面板 |
| Agent conversations | Agent 对话 |
| Command Palette | 命令面板 |
| Command Search | 命令搜索 |
| Workflow | 工作流 |
| Notebook | 笔记本 |
| Environment | 环境 |
| Execution Profile | 执行配置 |
| API Key | API 密钥 |
| Secret | 密钥 |
| Privacy | 隐私 |
| Telemetry | 遥测 |
| Code review | 代码审查 |
| Indexing | 索引 |

保留英文：

- Warp
- Warp Drive
- Warp Agent
- Codex
- Claude Code
- Gemini
- MCP
- GitHub
- Slack
- OAuth
- API
- CLI
- URL
- JSON

短标签优先：

- `未找到结果` 优先于 `没有找到任何结果`。
- `新建对话` 优先于 `创建新的对话`。
- `退出登录` 优先于 `注销当前账号`。
- `账单与用量` 优先于 `账单和使用情况`。

## 15. 分工建议

如果使用多 agent 或多人并行：

| 角色 | 负责范围 | 写入边界 |
| --- | --- | --- |
| Tooling | 脚本和文档 | `script/zh_*.py`, `docs/zh-Hans-localization.md` |
| Onboarding/Auth | 新用户路径 | `crates/onboarding/src`, `app/src/auth` |
| Workspace | 主界面 shell | `app/src/workspace`, `app/src/app_menus.rs`, `app/src/menu.rs` |
| Search | 搜索与命令入口 | `app/src/search` |
| Settings Core | settings 导航与核心页 | `app/src/settings_view/{mod.rs,nav.rs,settings_page.rs,main_page.rs,appearance_page.rs,features_page.rs,keybindings.rs,privacy_page.rs,warpify_page.rs}` |
| Settings Advanced | AI/Code/MCP/Billing/Env | `app/src/settings_view/ai_page.rs`, `code_page.rs`, `mcp_servers*`, `billing*`, `environments*`, `platform*` |
| Modal/Agent/Terminal | 弹窗和剩余面板 | `app/src/themes`, `app/src/tab_configs`, `app/src/drive`, `app/src/terminal`, `app/src/ai` |
| Verifier | 验证与冒烟 | 不写业务代码，只更新验证记录 |

并行规则：

- 不同角色不要同时改 `resources/localization/zh-Hans-overrides.toml` 的同一区段。
- 每个角色先在自己的文件范围内收集候选，再由一个集成者合并 manifest。
- 集成者每次合并后运行 `python3 script/zh_apply_localization.py --dry-run --summary`。

## 16. 回滚与上游同步策略

### 单批回滚

每个里程碑独立提交，所以回滚优先用普通 revert：

```bash
git revert <commit>
```

不要用 `git reset --hard`，除非明确决定丢弃整个分支上的本地工作。

### 上游同步

每次同步上游后：

```bash
git switch drew/zh-Hans-localization
git fetch origin
git merge origin/master
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt --check
git diff --check
```

如果 dry-run 出现 missing：

1. 打开报错文件。
2. 找到上游新文案。
3. 更新 manifest 的 `source`。
4. 重新 dry-run。

## 17. 最终验收标准

功能性：

- onboarding/auth 主路径没有明显英文静态 UI。
- workspace shell 主入口没有明显英文静态 UI。
- command palette/search/slash menu 主界面没有明显英文静态 UI。
- settings 主要页面没有明显英文静态 UI。
- 常见 modal/toast 没有明显英文静态 UI。

工程性：

- `python3 script/zh_apply_localization.py --dry-run --summary` 通过。
- 五个 preset 的 coverage 可输出。
- `cargo fmt --check` 通过。
- `git diff --check` 通过。
- `cargo check -p onboarding` 通过。
- `cargo check -p app` 通过，或本地环境问题有精确记录。
- 人工冒烟路径已执行并记录。

可维护性：

- 所有翻译在 manifest 中可追踪。
- 文档记录同步上游流程。
- 每批提交范围清晰。
- 没有翻译 telemetry、settings key、action id、binding id、配置 key、URL 或用户内容。

## 18. 推荐立即开始的第一组任务

先执行 M0 和 M1，不要直接继续翻译。

启动命令：

```bash
python3 script/zh_apply_localization.py --dry-run
cargo fmt --check
git diff --check
```

然后依次实现：

1. `docs/zh-Hans-localization.md` 增加当前 status。
2. `script/zh_apply_localization.py` 增加 comment-aware scanner、duplicate detection、`--summary`。
3. `script/zh_localization_inventory.py` 增加 inventory 和 preset。
4. 文档加入 inventory workflow。

这组完成后，后面的翻译扩展会更稳，且每次同步上游都能快速判断漂移和遗漏。
