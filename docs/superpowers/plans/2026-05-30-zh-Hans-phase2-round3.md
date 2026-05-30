# Warp CN Phase 2 Round 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the next high-visible zh-Hans localization slice for launch modals, credit/plan modals, Agent tips, conversation details, and remaining destructive confirmations.

**Architecture:** Continue the manifest-driven localization workflow. Add exact `path`/`source`/`target` entries to `resources/localization/zh-Hans-overrides.toml`, apply them with `script/zh_apply_localization.py`, then verify each slice with dry-run, coverage, focused string checks, formatting, and `cargo check -p warp`.

**Tech Stack:** Rust UI code, TOML localization manifest, Python localization scripts, Cargo formatting/check/test commands, macOS `WarpOss.app` bundle gate.

---

## Current Baseline

Baseline captured on 2026-05-30 after Phase 2 Round 2:

```text
entries: 2400
files: 176
already_applied: 2385
would_change: 0
missing: 0
```

Coverage baseline:

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| `workspace` | 495 | 475 | 51.0% |
| `settings` | 1163 | 867 | 57.3% |
| `modals` | 573 | 5865 | 8.9% |
| `release` | 2642 | 7281 | 26.6% |

Round 3 focuses on visible surfaces that remain English after Round 2:

- Oz, OpenWarp, and orchestration launch modals.
- Free-tier credit and Build plan migration modals.
- Agent tips shown in the Agent UI.
- Cloud conversation details side panel.
- CLI install prompts and destructive settings confirmations.

Round 3 excludes:

- Telemetry, debug logs, protocol IDs, YAML export labels, test-only strings, and search keywords.
- Theme names, product names that read better in English, command syntax, URLs, file extensions, and config keys.
- Broad terminal/AI diagnostic internals that inflate `modals` coverage without improving visible UI.

## File Structure

### Manifest

- Modify: `resources/localization/zh-Hans-overrides.toml`
  - Append Round 3 entries in task order.
  - Use one exact `[[replace]]` per `path`/`source`.
  - Preserve placeholders such as `{price}`, `{command}`, `{url}`, `{branch}`, `{artifact_uid}`, and `<keybinding>`.

### Source Files Modified by Apply Script

- `app/src/workspace/view/launch_modal/oz_launch.rs`
- `app/src/workspace/view/openwarp_launch_modal/view.rs`
- `app/src/workspace/view/orchestration_launch_modal/view.rs`
- `app/src/workspace/view/free_tier_limit_hit_modal.rs`
- `app/src/workspace/view/build_plan_migration_modal.rs`
- `app/src/ai/agent_tips.rs`
- `app/src/ai/conversation_details_panel.rs`
- `app/src/workspace/cli_install.rs`
- `app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs`
- `app/src/settings_view/transfer_ownership_confirmation_modal.rs`

### Documentation

- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-localization-phase2.md`

## Task 0: Commit the Round 3 Plan

**Files:**

- Create: `docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round3.md`

- [ ] **Step 1: Verify the plan file exists**

Run:

```bash
test -s docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round3.md
```

Expected: exit code 0.

- [ ] **Step 2: Scan for planning placeholders**

Run:

```bash
rg -n 'T[B]D|T[O]DO|implement late[r]|fill in detail[s]|Similar t[o]|probabl[y]' docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round3.md
```

Expected: exit code 1 with no matches.

- [ ] **Step 3: Verify diff hygiene**

Run:

```bash
git diff --check
```

Expected: exit code 0.

- [ ] **Step 4: Commit the plan**

Run:

```bash
git add docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round3.md
git commit -m "docs: plan phase 2 round 3 zh-Hans localization"
```

Expected: one commit containing only the Round 3 plan file.

## Task 1: Translate Launch Modals

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/workspace/view/launch_modal/oz_launch.rs`
- Modify after apply: `app/src/workspace/view/openwarp_launch_modal/view.rs`
- Modify after apply: `app/src/workspace/view/orchestration_launch_modal/view.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"Introducing Oz"|"Infinitely scalable coding agent"|"Next: \\{\\}"|"Try it out"|"Skip for now"|"Sync conversations to cloud"|"Warp is now open-source"|"Visit the repo"|"Orchestrate any agent, anywhere"|"Learn more"|"Close"' app/src/workspace/view/launch_modal/oz_launch.rs app/src/workspace/view/openwarp_launch_modal/view.rs app/src/workspace/view/orchestration_launch_modal/view.rs resources/localization/zh-Hans-overrides.toml
```

Expected: target strings appear in the source files, and no identical `path`/`source` pair already exists in `resources/localization/zh-Hans-overrides.toml`.

- [ ] **Step 2: Append launch modal manifest entries**

Append:

```toml
[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Introducing Oz"
target = "介绍 Oz"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Infinitely scalable coding agent — run in local sessions or in the cloud."
target = "可无限扩展的编码 Agent，可在本地会话或云端运行。"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Cloud agents"
target = "云端 Agent"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Agent automations"
target = "Agent 自动化"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Agent management"
target = "Agent 管理"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "A little gift"
target = "一点小礼物"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Launch credits"
target = "发布赠送额度"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Break out of your laptop with cloud agents"
target = "用云端 Agent 突破本机限制"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Orchestrate agents, turning Skills into automations"
target = "编排 Agent，将 Skills 变成自动化"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Track local and cloud agents seamlessly"
target = "无缝跟踪本地和云端 Agent"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "1,000 free cloud agent credits when you upgrade to Warp Build"
target = "升级到 Warp Build 即可获得 1,000 点免费云端 Agent 额度"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Use cloud agents to run many agents in parallel, keep agents working when you close your laptop, or start agents programmatically. Plus, you can check on their work through the web."
target = "使用云端 Agent 并行运行多个 Agent，在你合上笔记本后仍继续工作，或通过程序启动 Agent。你还可以通过网页查看它们的进展。"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Oz agents can be defined using the standard Skills format. You can use the built in scheduler to setup agents to run autonomously at set intervals, or use the Oz SDK or API to programmatically start and manage Oz agents."
target = "Oz Agent 可使用标准 Skills 格式定义。你可以用内置调度器设置 Agent 按固定间隔自主运行，也可以用 Oz SDK 或 API 以编程方式启动和管理 Oz Agent。"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "View all of your agents across local and cloud sessions in the Warp app or at [oz.warp.dev](https://oz.warp.dev). Join live agent sessions, continue tasks locally, and steer agents with one click."
target = "在 Warp 应用或 [oz.warp.dev](https://oz.warp.dev) 查看本地和云端会话中的所有 Agent。你可以加入实时 Agent 会话、本地继续任务，并一键引导 Agent。"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Upgrade to Build this month and receive 1,000 extra credits to try using Oz. Credits are only eligible for Oz runs in Warp-hosted cloud environments."
target = "本月升级到 Build，即可获得 1,000 点额外额度来试用 Oz。该额度仅适用于 Warp 托管云环境中的 Oz 运行。"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Next: {}"
target = "下一步：{}"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Try it out"
target = "试试看"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Skip for now"
target = "暂时跳过"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Sync conversations to cloud"
target = "将对话同步到云端"

[[replace]]
path = "app/src/workspace/view/launch_modal/oz_launch.rs"
source = "Agent conversations stored in the cloud can be shared with anyone with one click, and allow conversations to be continued across devices and on logout."
target = "存储在云端的 Agent 对话可一键共享给任何人，并支持跨设备或退出登录后继续对话。"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "Contribute"
target = "参与贡献"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "Warp's client code is now open source. Get started by using the /feedback skill to open an issue, and follow the contribution guidelines here."
target = "Warp 客户端代码现已开源。你可以先使用 /feedback skill 创建 issue，并在这里查看贡献指南。"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "here"
target = "这里"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "Open Automated Development"
target = "开放式自动化开发"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "The Warp repo is managed by an agent-first workflow powered by Oz, our cloud agent orchestration platform."
target = "Warp 仓库由 Agent-first 工作流管理，该工作流由我们的云端 Agent 编排平台 Oz 提供支持。"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "Introducing 'auto (open-weights)'"
target = "介绍 'auto (open-weights)'"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "We've added a new auto model that picks the best open weight model for a task, like Kimi or MiniMax."
target = "我们新增了一个 auto 模型，可为任务选择最合适的开放权重模型，例如 Kimi 或 MiniMax。"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "Visit the repo"
target = "访问仓库"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "New"
target = "新增"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "Warp is now open-source"
target = "Warp 现已开源"

[[replace]]
path = "app/src/workspace/view/openwarp_launch_modal/view.rs"
source = "You, our community, can participate in building Warp using an agent-first workflow."
target = "你和整个社区都可以使用 Agent-first 工作流参与构建 Warp。"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Run any agent harness in the cloud"
target = "在云端运行任何 Agent harness"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Use Oz to spin up Claude Code or Codex agents in the cloud; Oz will help you track and steer the agents."
target = "使用 Oz 在云端启动 Claude Code 或 Codex Agent；Oz 会帮助你跟踪并引导这些 Agent。"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Multi-agent orchestration"
target = "多 Agent 编排"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Warp Agents will now orchestrate swarms of subagents, allowing you to parallelize tasks."
target = "Warp Agent 现在可以编排多个子 Agent，让你并行处理任务。"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Agent Memory"
target = "Agent 记忆"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Agents will now store and access long-term memories, enabling self-improvement over time."
target = "Agent 现在可以存储并访问长期记忆，从而随着时间自我改进。"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Research preview"
target = "研究预览"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Learn more"
target = "了解更多"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Close"
target = "关闭"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "New"
target = "新增"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "Orchestrate any agent, anywhere"
target = "随时随地编排任何 Agent"

[[replace]]
path = "app/src/workspace/view/orchestration_launch_modal/view.rs"
source = "We've made major improvements to Warp's cloud agent orchestration platform, Oz."
target = "我们对 Warp 的云端 Agent 编排平台 Oz 做了重大改进。"
```

- [ ] **Step 3: Apply launch modal translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: dry-run reports `would_change: 43`, `missing: 0`; apply lists the three launch modal files.

- [ ] **Step 4: Verify launch modal slice**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset workspace --coverage
rg -n '介绍 Oz|将对话同步到云端|Warp 现已开源|随时随地编排任何 Agent|Introducing Oz|Sync conversations to cloud|Warp is now open-source|Orchestrate any agent, anywhere' app/src/workspace/view/launch_modal/oz_launch.rs app/src/workspace/view/openwarp_launch_modal/view.rs app/src/workspace/view/orchestration_launch_modal/view.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports `would_change: 0`, `missing: 0`; focused `rg` returns Chinese targets and no English launch-modal sources; `cargo check -p warp` exits 0 with only known warnings.

- [ ] **Step 5: Commit launch modal localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace/view/launch_modal/oz_launch.rs app/src/workspace/view/openwarp_launch_modal/view.rs app/src/workspace/view/orchestration_launch_modal/view.rs
git commit -m "feat: localize launch modals"
```

Expected: one focused launch modal commit.

## Task 2: Translate Credit and Plan Modals

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/workspace/view/free_tier_limit_hit_modal.rs`
- Modify after apply: `app/src/workspace/view/build_plan_migration_modal.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n 'You’re out of credits|To continue using AI|The Build plan is \\$\\{price\\}/month|Auto-reload|Get Started|Welcome to Warp Build|Build comes with|Oops, something went wrong' app/src/workspace/view/free_tier_limit_hit_modal.rs app/src/workspace/view/build_plan_migration_modal.rs resources/localization/zh-Hans-overrides.toml
```

Expected: target strings appear in source files, and no identical `path`/`source` pair already exists.

- [ ] **Step 2: Append credit and plan modal entries**

Append:

```toml
[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "You’re out of credits"
target = "你的额度已用完"

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "To continue using AI, please upgrade your plan."
target = "若要继续使用 AI，请升级你的方案。"

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "The Build plan is ${price}/month which includes everything in the free tier plus:"
target = "Build 方案为 ${price}/月，包含免费层级的所有内容，并额外提供："

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "The Build plan includes everything in the free tier plus:"
target = "Build 方案包含免费层级的所有内容，并额外提供："

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "{} Credits per month"
target = "每月 {} 点额度"

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "Extended Credits per month"
target = "每月扩展额度"

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "Access to frontier OpenAI, Anthropic, and Google models"
target = "访问前沿 OpenAI、Anthropic 和 Google 模型"

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "Access to "
target = "可使用 "

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "Reload Credits"
target = "Reload 额度"

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "Extended cloud agents access"
target = "扩展云端 Agent 访问权限"

[[replace]]
path = "app/src/workspace/view/free_tier_limit_hit_modal.rs"
source = "Upgrade plan"
target = "升级方案"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Failed to enable auto-reload. Please try updating your settings in Billing & usage."
target = "无法启用自动充值。请尝试在“账单与用量”中更新设置。"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "${} / {} credits"
target = "${} / {} 点额度"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Auto-reload"
target = "自动充值"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Saving..."
target = "正在保存..."

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Get Started"
target = "开始使用"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Use auto-reload to never miss a beat."
target = "使用自动充值，避免中断。"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Auto-reload will automatically purchase credits at your selected rate when your account balance reaches 100 credits. Your monthly spend limit is set at your legacy plan's monthly cost and can be updated in Settings > Billing & usage."
target = "当你的账号余额降至 100 点额度时，自动充值会按你选择的档位自动购买额度。你的月度支出限制会设置为旧方案的月度费用，并可在“设置 > 账单与用量”中更新。"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Welcome to the New Business Plan"
target = "欢迎使用新的 Business 方案"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Welcome to Warp Build"
target = "欢迎使用 Warp Build"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Your workspace has been updated to the new Warp Business Plan as the legacy Business plan is sunset."
target = "由于旧版 Business 方案即将下线，你的工作区已更新到新的 Warp Business 方案。"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Your workspace has been updated to the Warp Build Plan as the legacy Pro, Turbo, and Lightspeed plans are sunset."
target = "由于旧版 Pro、Turbo 和 Lightspeed 方案即将下线，你的工作区已更新到 Warp Build 方案。"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "The new Business plan is a primarily usage-based plan, starting at:"
target = "新的 Business 方案主要按用量计费，起价为："

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Warp Build is a primarily usage-based plan, starting at:"
target = "Warp Build 主要按用量计费，起价为："

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "${} per user per month"
target = "每位用户每月 ${}"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "${} per user per month for annual plans"
target = "年度方案每位用户每月 ${}"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "The new Business plan comes with:"
target = "新的 Business 方案包含："

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Build comes with:"
target = "Build 包含："

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "{} base credits per month"
target = "每月 {} 点基础额度"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Access to Reload credits and volume-based discounts"
target = "可使用 Reload 额度和基于用量的折扣"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Bring your own API key"
target = "自带 API key"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "SAML-based SSO"
target = "基于 SAML 的 SSO"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Automatically enforced team-wide Zero Data Retention"
target = "自动强制执行团队范围的零数据保留"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "And more..."
target = "以及更多..."

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Learn more on our "
target = "在我们的 "

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "pricing page"
target = "价格页面"

[[replace]]
path = "app/src/workspace/view/build_plan_migration_modal.rs"
source = "Oops, something went wrong; your team data could not be found."
target = "出错了，无法找到你的团队数据。"
```

- [ ] **Step 3: Apply credit and plan modal translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: dry-run reports `would_change: 37`, `missing: 0`; apply lists both plan/credit modal files.

- [ ] **Step 4: Verify credit and plan slice**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset workspace --coverage
rg -n '你的额度已用完|Build 方案为 \\$\\{price\\}/月|自动充值|欢迎使用 Warp Build|You’re out of credits|Auto-reload|Welcome to Warp Build' app/src/workspace/view/free_tier_limit_hit_modal.rs app/src/workspace/view/build_plan_migration_modal.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports `would_change: 0`, `missing: 0`; focused `rg` returns Chinese targets and no English sources from this task.

- [ ] **Step 5: Commit credit and plan modal localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace/view/free_tier_limit_hit_modal.rs app/src/workspace/view/build_plan_migration_modal.rs
git commit -m "feat: localize credit and plan modals"
```

Expected: one focused credit/plan modal commit.

## Task 3: Translate Agent Tips

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/ai/agent_tips.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '`/` to open the slash-command menu|`/plan` <prompt>|Store reusable workflows|Drag an image into the pane|Use `AGENTS.md` or `CLAUDE.md`|Hold <keybinding> to speak your prompt' app/src/ai/agent_tips.rs resources/localization/zh-Hans-overrides.toml
```

Expected: target strings appear in `app/src/ai/agent_tips.rs`, and no identical `path`/`source` pair already exists.

- [ ] **Step 2: Append Agent tip entries**

Append:

```toml
[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/` to open the slash-command menu and access quick agent actions."
target = "使用 `/` 打开斜杠命令菜单并访问快速 Agent 操作。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/plan` <prompt> to create a plan for the agent before executing."
target = "使用 `/plan` <prompt> 先为 Agent 创建计划再执行。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "<keybinding> to open the Command Palette and access Warp actions and shortcuts."
target = "使用 <keybinding> 打开命令面板，访问 Warp 操作和快捷键。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Store reusable workflows, notebooks, and prompts in your"
target = "将可复用的工作流、Notebook 和提示词存入你的"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Enter a new prompt to redirect the agent while it's running."
target = "输入新的提示词，可在 Agent 运行时重定向它。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "<keybinding> to attach the prior command output as agent context."
target = "使用 <keybinding> 将上一条命令输出附加为 Agent 上下文。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/init` to index the repo so the agent can understand your codebase."
target = "使用 `/init` 索引仓库，让 Agent 理解你的代码库。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Drag an image into the pane to attach it as agent context."
target = "将图片拖入窗格，可作为 Agent 上下文附加。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Prompt the agent to control interactive tools like node, python, postgres, gdb, or vim."
target = "提示 Agent 控制 node、python、postgres、gdb 或 vim 等交互式工具。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/add-mcp` to add an MCP server to your workspace."
target = "使用 `/add-mcp` 向工作区添加 MCP 服务器。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/create-environment` to turn a repo into a remote docker environment an agent can run in."
target = "使用 `/create-environment` 将仓库转换为 Agent 可运行的远程 Docker 环境。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/add-prompt` to create a reusable prompt for repeatable workflows."
target = "使用 `/add-prompt` 创建可复用提示词，以支持重复工作流。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/add-rule` to create a global agent rule."
target = "使用 `/add-rule` 创建全局 Agent 规则。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/fork` to create a fresh copy of the current conversation, optionally with a new prompt."
target = "使用 `/fork` 创建当前对话的新副本，并可附加新的提示词。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/new` to start a new agent conversation with clean context."
target = "使用 `/new` 以干净上下文开始新的 Agent 对话。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/compact` to summarize the current conversation and free up space in the context window."
target = "使用 `/compact` 总结当前对话，并释放上下文窗口空间。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/usage` to show your current AI credits usage."
target = "使用 `/usage` 查看当前 AI 额度用量。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Use the `oz` command to run an Oz agent in headless mode, useful for remote machines."
target = "使用 `oz` 命令以 headless 模式运行 Oz Agent，适合远程机器。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Right-click selected text to attach it as agent context."
target = "右键点击选中文本，可将其附加为 Agent 上下文。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Use `AGENTS.md` or `CLAUDE.md` to apply project-scoped rules."
target = "使用 `AGENTS.md` 或 `CLAUDE.md` 应用项目范围规则。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Paste a URL to attach that webpage as context for the agent."
target = "粘贴 URL，可将该网页作为 Agent 上下文附加。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Warpify a remote SSH session to enable Oz inside that environment."
target = "Warpify 远程 SSH 会话，以便在该环境中启用 Oz。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "`/init` to generate a `WARP.md` file and define project rules for the agent."
target = "使用 `/init` 生成 `WARP.md` 文件，并为 Agent 定义项目规则。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "<keybinding> to auto-approve the agent's commands and diffs for the rest of the session."
target = "使用 <keybinding> 在本会话剩余时间内自动批准 Agent 的命令和 diff。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Type `&` or use the handoff chip to move a local conversation to the cloud."
target = "输入 `&` 或使用 handoff chip 将本地对话移至云端。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Enable desktop notifications to get an alert when an agent needs your attention."
target = "启用桌面通知，当 Agent 需要你关注时即可收到提醒。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "<keybinding> to cancel the current agent task."
target = "使用 <keybinding> 取消当前 Agent 任务。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Open palette"
target = "打开面板"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Warp Drive."
target = "Warp Drive。"

[[replace]]
path = "app/src/ai/agent_tips.rs"
source = "Hold <keybinding> to speak your prompt directly to the agent."
target = "按住 <keybinding> 可直接对 Agent 说出你的提示词。"
```

- [ ] **Step 3: Apply Agent tip translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: dry-run reports `would_change: 30`, `missing: 0`; apply lists `app/src/ai/agent_tips.rs`.

- [ ] **Step 4: Verify Agent tips**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset modals --coverage
rg -n '斜杠命令菜单|将可复用的工作流|将图片拖入窗格|使用 `AGENTS.md`|按住 <keybinding>|`/` to open the slash-command menu|Drag an image into the pane|Use `AGENTS.md`' app/src/ai/agent_tips.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports `would_change: 0`, `missing: 0`; focused `rg` returns Chinese targets and no English sources from this task.

- [ ] **Step 5: Commit Agent tip localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/ai/agent_tips.rs
git commit -m "feat: localize agent tips"
```

Expected: one focused Agent tips commit.

## Task 4: Translate Conversation Details Panel

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/ai/conversation_details_panel.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"Conversation"|"Cloud agent run"|"Continue locally"|"Fork this conversation locally"|"View in Oz"|"Copied branch name"|"Initial query"|"Environment setup commands"|"Environment details"|"Run ID"' app/src/ai/conversation_details_panel.rs resources/localization/zh-Hans-overrides.toml
```

Expected: target strings appear in `app/src/ai/conversation_details_panel.rs`, and no identical `path`/`source` pair already exists.

- [ ] **Step 2: Append conversation details entries**

Append:

```toml
[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Conversation"
target = "对话"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Cloud agent run"
target = "云端 Agent 运行"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Copy"
target = "复制"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Continue locally"
target = "在本地继续"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Fork this conversation locally"
target = "在本地 fork 此对话"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "View in Oz"
target = "在 Oz 中查看"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "View this run in the Oz web app"
target = "在 Oz Web 应用中查看此次运行"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Copied branch name"
target = "已复制分支名称"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Created by {} • {}"
target = "由 {} 创建 • {}"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Error"
target = "错误"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Status"
target = "状态"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Open in Oz"
target = "在 Oz 中打开"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Open in GitHub"
target = "在 GitHub 中打开"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Initial query"
target = "初始查询"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Artifacts"
target = "产物"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Environment setup commands"
target = "环境设置命令"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Environment details"
target = "环境详情"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Name: {environment_name}"
target = "名称：{environment_name}"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Image"
target = "镜像"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Directory"
target = "目录"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Conversation ID"
target = "对话 ID"

[[replace]]
path = "app/src/ai/conversation_details_panel.rs"
source = "Run ID"
target = "运行 ID"
```

- [ ] **Step 3: Apply conversation details translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: dry-run reports `would_change: 22`, `missing: 0`; apply lists `app/src/ai/conversation_details_panel.rs`.

- [ ] **Step 4: Verify conversation details panel**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset modals --coverage
rg -n '云端 Agent 运行|在本地继续|已复制分支名称|环境设置命令|环境详情|Cloud agent run|Continue locally|Copied branch name|Environment setup commands|Environment details' app/src/ai/conversation_details_panel.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports `would_change: 0`, `missing: 0`; focused `rg` returns Chinese targets and no English sources from this task.

- [ ] **Step 5: Commit conversation details localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/ai/conversation_details_panel.rs
git commit -m "feat: localize conversation details panel"
```

Expected: one focused conversation details commit.

## Task 5: Translate CLI Prompts and Destructive Confirmations

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/workspace/cli_install.rs`
- Modify after apply: `app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs`
- Modify after apply: `app/src/settings_view/transfer_ownership_confirmation_modal.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n 'administrator privileges to install|administrator privileges to uninstall|Installation cancelled by user|Uninstallation cancelled by user|Remove endpoint|Are you sure you want to remove this endpoint|transfer team ownership|Transfer' app/src/workspace/cli_install.rs app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs app/src/settings_view/transfer_ownership_confirmation_modal.rs resources/localization/zh-Hans-overrides.toml
```

Expected: target strings appear in the source files, and no identical `path`/`source` pair already exists.

- [ ] **Step 2: Append CLI and confirmation entries**

Append:

```toml
[[replace]]
path = "app/src/workspace/cli_install.rs"
source = "do shell script \"ln -sf {escaped_source} {escaped_target}\" with prompt \"Warp needs administrator privileges to install the command in /usr/local/bin.\" with administrator privileges"
target = "do shell script \"ln -sf {escaped_source} {escaped_target}\" with prompt \"Warp 需要管理员权限才能将命令安装到 /usr/local/bin。\" with administrator privileges"

[[replace]]
path = "app/src/workspace/cli_install.rs"
source = "do shell script \"rm {escaped_target}\" with prompt \"Warp needs administrator privileges to uninstall the command from /usr/local/bin.\" with administrator privileges"
target = "do shell script \"rm {escaped_target}\" with prompt \"Warp 需要管理员权限才能从 /usr/local/bin 卸载该命令。\" with administrator privileges"

[[replace]]
path = "app/src/workspace/cli_install.rs"
source = "Installation cancelled by user."
target = "用户已取消安装。"

[[replace]]
path = "app/src/workspace/cli_install.rs"
source = "Uninstallation cancelled by user."
target = "用户已取消卸载。"

[[replace]]
path = "app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs"
source = "Cancel"
target = "取消"

[[replace]]
path = "app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs"
source = "Remove endpoint"
target = "移除端点"

[[replace]]
path = "app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs"
source = "Are you sure you want to remove this endpoint? You won't be able to use its models in your agent sessions moving forward."
target = "确定要移除此端点吗？之后你将无法在 Agent 会话中使用它的模型。"

[[replace]]
path = "app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs"
source = "Remove endpoint?"
target = "移除端点？"

[[replace]]
path = "app/src/settings_view/transfer_ownership_confirmation_modal.rs"
source = "Are you sure you want to transfer team ownership to {}? You will no longer be the owner and will not be able to take any administrative actions for this team."
target = "确定要将团队所有权转让给 {} 吗？你将不再是所有者，也无法对此团队执行任何管理操作。"

[[replace]]
path = "app/src/settings_view/transfer_ownership_confirmation_modal.rs"
source = "Cancel"
target = "取消"

[[replace]]
path = "app/src/settings_view/transfer_ownership_confirmation_modal.rs"
source = "Transfer"
target = "转让"
```

- [ ] **Step 3: Apply CLI and confirmation translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: dry-run reports `would_change: 11`, `missing: 0`; apply lists the CLI and confirmation files.

- [ ] **Step 4: Verify CLI prompts and confirmations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
rg -n 'Warp 需要管理员权限|用户已取消安装|移除端点|团队所有权|administrator privileges to install|Remove endpoint|transfer team ownership' app/src/workspace/cli_install.rs app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs app/src/settings_view/transfer_ownership_confirmation_modal.rs
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: dry-run reports `would_change: 0`, `missing: 0`; focused `rg` returns Chinese targets and no English sources from this task.

- [ ] **Step 5: Commit CLI and confirmation localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace/cli_install.rs app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs app/src/settings_view/transfer_ownership_confirmation_modal.rs
git commit -m "feat: localize cli and confirmation prompts"
```

Expected: one focused CLI/confirmation commit.

## Task 6: Record Round 3 Release Audit

**Files:**

- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-localization-phase2.md`

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

Expected:

- Dry-run reports `would_change: 0`, `missing: 0`.
- Coverage numbers are captured for docs.
- `cargo check -p warp` exits 0 with only known unused-variable warnings.
- `cargo test -p warp_search_core` passes.
- `cargo test -p warp command_palette` passes.
- Bundle gate creates and signs `target/debug/bundle/osx/WarpOss.app`.

- [ ] **Step 2: Attempt GUI smoke once**

Run:

```bash
open -na "target/debug/bundle/osx/WarpOss.app"
sleep 5
pgrep -fl WarpOss
```

Then use Computer Use or an interactive desktop session to inspect:

- Oz launch modal.
- OpenWarp launch modal.
- Orchestration launch modal.
- Free-tier credit modal.
- Build plan migration modal.
- Agent tips.
- Conversation details panel.
- Remove custom endpoint confirmation.
- Transfer ownership confirmation.
- CLI install admin prompt.

Expected: if GUI automation times out, record the process state and the timeout as a manual gate in docs.

- [ ] **Step 3: Update docs with Round 3 results**

Update:

- `README.md`: current audit date, manifest count, file count, coverage table, completed Round 3 scope, manual gates.
- `docs/zh-Hans-localization.md`: Round 3 execution record, skipped strings, command outputs, GUI gate.
- `docs/zh-Hans-localization-phase2.md`: Round 3 result section and rationality review.

Expected documented facts:

- Exact final dry-run summary.
- Exact final coverage table.
- Commit hashes for Task 0 through Task 5.
- Known retained strings: command syntax, product names, debug logs, telemetry, YAML export labels, URLs, paths, settings search keywords.
- GUI smoke result.

- [ ] **Step 4: Verify docs**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
rg -n 'T[B]D|T[O]DO|implement late[r]|fill in detail[s]|Similar t[o]|probabl[y]' README.md docs/zh-Hans-localization.md docs/zh-Hans-localization-phase2.md
git diff --check
```

Expected:

- Dry-run reports `would_change: 0`, `missing: 0`.
- Placeholder scan exits 1 with no matches.
- `git diff --check` exits 0.

- [ ] **Step 5: Commit Round 3 audit docs**

Run:

```bash
git add README.md docs/zh-Hans-localization.md docs/zh-Hans-localization-phase2.md
git commit -m "docs: record phase 2 round 3 zh-Hans audit"
```

Expected: one focused docs commit.

## Task 7: Push Round 3 to GitHub

**Files:**

- No file edits.

- [ ] **Step 1: Verify local branch and outgoing commits**

Run:

```bash
git status -sb
git log --oneline --decorate -10
git log --oneline github/main..HEAD
```

Expected:

- Only old unrelated untracked plan files may remain untracked:
  - `docs/superpowers/plans/2026-05-29-zh-Hans-localization-execution-plan.md`
  - `docs/superpowers/plans/2026-05-29-zh-Hans-localization.md`
- Outgoing commits are the Round 3 plan, Round 3 localization commits, and Round 3 audit docs.

- [ ] **Step 2: Push to GitHub main**

Run:

```bash
git push github HEAD:main
```

Expected: remote `main` updates from the previous commit to the new Round 3 audit commit.

- [ ] **Step 3: Confirm remote state**

Run:

```bash
git ls-remote github refs/heads/main
git rev-parse HEAD
gh repo view Drew1811266/Warp-CN --json nameWithOwner,defaultBranchRef,url
```

Expected:

- `git ls-remote github refs/heads/main` hash matches `git rev-parse HEAD`.
- `gh repo view` reports `Drew1811266/Warp-CN`, default branch `main`, and URL `https://github.com/Drew1811266/Warp-CN`.

## Self-Review

### Spec Coverage

- Launch modals are covered by Task 1.
- Credit and plan modals are covered by Task 2.
- Agent tips are covered by Task 3.
- Conversation details are covered by Task 4.
- CLI prompts and destructive confirmations are covered by Task 5.
- Release audit, GUI gate, docs, and push are covered by Tasks 6 and 7.

### Placeholder Scan

The plan avoids placeholder instructions and includes exact files, exact commands, exact manifest entries, and expected verification outputs.

### Type and Placeholder Consistency

All manifest entries preserve Rust placeholders and UI placeholders:

- `{price}`, `{command}`, `{url}`, `{branch}`, `{artifact_uid}`, `{environment_name}`.
- `{}` positional placeholders.
- `<keybinding>` in Agent tips.
- Inline command syntax such as `/plan`, `/init`, `/add-mcp`, `/usage`, `AGENTS.md`, and `CLAUDE.md`.

No task translates telemetry IDs, debug state names, YAML export metadata, theme names, URLs, or command parser tokens.
