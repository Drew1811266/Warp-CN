# zh-Hans GUI 冒烟矩阵

本矩阵记录 Warp CN 汉化构建的视觉验证路径。它的作用是把已验证项、manual gate 和账号/状态依赖拆清楚，避免把构建成功或进程启动误认为 GUI 已验收。

基线日期：2026-05-31。

## 状态定义

| 状态 | 含义 |
| --- | --- |
| `verified` | 已在 GUI 中看到对应中文文案。 |
| `manual-gate` | 已有翻译和命令行验证，但需要真实交互或账号状态才能触发。 |
| `fixture-verified` | 已用本地或 debug-only fixture 看到对应中文文案，但该证据不能替代真实账号/服务状态证据。 |
| `automation-blocked` | 应用可启动，但窗口读取或截图自动化受本机环境限制。 |
| `needs-trigger` | 需要构造特定产品状态、错误状态或 feature flag 才能验证。 |
| `not-started` | 尚未开始 GUI 复验。 |

## 前置检查

每次 GUI 冒烟前先跑命令行 gate：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

启动本地 bundle：

```bash
open -n target/debug/bundle/osx/WarpOss.app
```

## Phase 5 GUI profile 与证据策略

Phase 5 开始，GUI 冒烟记录必须区分三类证据：

- `Computer Use state`: accessibility tree 中可读到的中文锚点，优先作为 `verified` 依据。
- `Screenshot`: 存放在 `docs/gui-smoke-artifacts/` 的截图路径，只能证明当时视觉状态；截图为空桌面或只显示进程启动不能作为业务路径 verified。
- `Process/bundle evidence`: `./script/run --dont-open`、`open -n`、`pgrep` 只能证明构建和启动，不证明 UI 已验收。

本地测试 profile 约定：

- 默认使用当前 `WarpOss` 本地 profile 做非破坏性 smoke。
- 涉及 endpoint、environment、auth secret、会话删除等 destructive confirmation 时，必须先创建可恢复/隔离测试对象，并在记录中写明对象类型。
- 不使用真实主账号做团队所有权转让、计费、额度、云端 Agent 等高风险测试。
- macOS 权限弹窗默认不授权，除非该轮测试明确需要对应权限；权限弹窗本身只记录为环境事件。

## Phase 7 profile isolation audit

审计日期：2026-05-31。

Phase 7 先审计 `WARP_DATA_PROFILE=zh-rc4`，再决定是否能安全创建 `zh-smoke-delete-endpoint`。结论是：debug profile 可隔离部分路径和 secure-storage 命名空间，但 macOS 上不是完整文件系统隔离。

| 项目 | Phase 7 分类 | 2026-05-31 结论 |
| --- | --- | --- |
| `ChannelState::data_profile()` | `profile-isolated` | 仅 debug build 读取 `WARP_DATA_PROFILE`；release build 返回 `None`。 |
| `ChannelState::data_domain()` | `profile-isolated` | debug profile 下会变成 `dev.warp.WarpOss-zh-rc4`。 |
| `warp_home_config_dir()` | `profile-isolated` | `WARP_DATA_PROFILE=zh-rc4 cargo test -p warp_core test_warp_home_config_dir_path` 通过，期望目录为 `~/.warp-oss-zh-rc4`。 |
| `data_dir()` | `shared-with-oss` | macOS 仍由 `macos_config_dir_name()` 返回 `~/.warp-oss`，不读取 profile。 |
| `config_local_dir()` | `shared-with-oss` | macOS 仍由 `macos_config_dir_name()` 返回 `~/.warp-oss`，不读取 profile。 |
| `cache_dir()` | `profile-isolated` | 走 profiled `ProjectDirs`，profile 下预期为 `~/Library/Application Support/dev.warp.WarpOss-zh-rc4`。 |
| `state_dir()` | `profile-isolated` | 走 profiled `ProjectDirs`，profile 下预期为 `~/Library/Application Support/dev.warp.WarpOss-zh-rc4`。 |
| `secure_state_dir()` | `unknown-until-runtime` | 如果 macOS app group 可用，会拼接 profiled project path；app group 是否可用需运行时确认。 |
| custom endpoint state | `profile-isolated` | `ApiKeyManager` 读写 secure storage key `AiApiKeys`，secure storage service name 来自 `ChannelState::data_domain()`。只有在 GUI 进程确实带 `WARP_DATA_PROFILE=zh-rc4` 启动时才可创建/删除 `zh-smoke-delete-endpoint`。 |

P7-M1 测试结果：

- `cargo test -p warp_core path`: 10 tests passed.
- `WARP_DATA_PROFILE=zh-rc4 cargo test -p warp_core test_warp_home_config_dir_path`: 1 test passed.

执行约束：

- P7-M5 可以尝试 `zh-smoke-delete-endpoint`，但前提是 P7-M2 证明 GUI 进程以 `zh-rc4` profile 启动并且 UI 可见。
- 如果 GUI 进程没有 profile，或 profile 传播无法确认，则不得创建或删除 custom endpoint。
- `data_dir()` 和 `config_local_dir()` 仍共享 `~/.warp-oss`，所以任何会改写 settings、themes、workflows、tab configs、user preferences 的 GUI 操作都不能视为完整隔离。

P7-M2 launch 记录：

- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` 通过并生成 `target/debug/bundle/osx/WarpOss.app`。
- 使用 `launchctl setenv WARP_DATA_PROFILE zh-rc4` 后 `open -n target/debug/bundle/osx/WarpOss.app`，随后 `launchctl unsetenv WARP_DATA_PROFILE`；`launchctl getenv WARP_DATA_PROFILE` 返回空值。
- `pgrep -afil 'target/debug/bundle/osx/WarpOss.app|warp-oss|terminal-server'` 找到 `warp-oss` pid `80871` 和 `terminal-server` pid `80874`。
- `ps eww -p 80871` 确认 GUI 进程包含 `WARP_DATA_PROFILE=zh-rc4`。
- 首次截图 `docs/gui-smoke-artifacts/phase7/p7-m2-launch.png` 显示 macOS 权限弹窗：`“WarpOss”想访问其他 App 的数据。` 本轮按策略点击 `不允许`，没有授权。
- 权限弹窗拒绝后的截图：`docs/gui-smoke-artifacts/phase7/p7-m2-after-permission-deny.png`，显示 `欢迎使用 Warp`、`开始使用` 和底部 `登录`。
- `/usr/bin/log show --last 5m --predicate 'process == "warp-oss"' --style compact` 输出到 `docs/gui-smoke-artifacts/phase7/p7-m2-warp-oss.log.txt`，共 111 行；日志包含 AppIntents/linkd 错误和 app group lookup 成功，但没有阻止窗口显示。
- Computer Use 对 `WarpOss` 成功返回窗口状态，读取到菜单栏 `文件`、`编辑`、`视图`、`标签页`、`块`、`AI`、`Drive`、`窗口`、`帮助`。
- P7-M2 launch classification: `interactive-profile-ready`。

## Phase 8 evidence path selection

审计日期：2026-05-31。

Phase 8 的目标是验证 `GUI-WS-06` custom endpoint 删除确认，但该路径必须使用隔离测试账号或等价 fixture，因为 `UserWorkspaces::is_custom_inference_enabled()` 对 anonymous/logged-out 用户返回 false。

```text
P8 evidence path: no-test-account
```

结论：

- 当前执行上下文没有提供隔离测试账号或可用 fixture。
- 本轮不会猜测凭据，也不会使用主账号。
- 不创建 `zh-smoke-delete-endpoint`。
- 不打开 remove endpoint confirmation。
- 不删除任何 endpoint。
- P8-M3 到 P8-M6 的 public-RC GUI 证据路径延期。
- 下一步可做 debug-only custom inference fixture，用于验证翻译渲染和截图流程；但该 fixture 不能单独作为 `ready-for-public-rc` 证据。

## Phase 9 custom inference fixture boundary

审计日期：2026-05-31。

Phase 9 重新复核了 custom inference 的三个 gate：

- `UserWorkspaces::is_custom_inference_enabled()` 对 anonymous/logged-out 用户返回 false，且企业 workspace 还受 enterprise flag、Warp Plan 或 dogfood 状态约束。
- `AISettingsPageView::can_use_custom_inference_controls()` 同时要求 `FeatureFlag::CustomInferenceEndpoints`、AI 可用和 custom inference 可用，控制 add/edit/remove 动作。
- `AISettingsWidget::render_provider_keys_section()` 控制 Settings > AI 是否渲染 `自定义推理`、`添加自定义端点`、endpoint 列表和 fallback toggle。

Fixture strategy:

```text
Add a debug_assertions-only env-gated override controlled by WARP_CN_CUSTOM_INFERENCE_SMOKE=1. The fixture may render and enable custom inference controls, seed one in-memory disposable endpoint, and avoid Keychain/App Group prompts for localization smoke only. Fixture evidence is non-public and cannot mark GUI-WS-06 verified.
```

证据规则：

- Fixture 成功后，`GUI-WS-06` 最多记录为 `fixture-verified` 或在 notes 中记录 `fixture-evidence`。
- `ready-for-public-rc` 仍必须来自不带 `WARP_CN_CUSTOM_INFERENCE_SMOKE` 的隔离测试账号路径。
- 不使用主账号，不猜测登录凭据，不删除除 `zh-smoke-delete-endpoint` 之外的 endpoint。
- Fixture endpoint 只在当前 debug 进程内存中存在；重启后只有再次带上 env gate 才会重新播种。

## 基础工作区

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-BASE-01 | macOS 菜单栏 | 启动 `WarpOss.app` 后查看系统菜单栏 | 无 | `文件`、`编辑`、`视图`、`标签页`、`块`、`窗口`、`帮助` | `verified` | 2026-05-31 P7-M4 | Computer Use 当前周期读取到 `文件`、`编辑`、`视图`、`标签页`、`块`、`AI`、`Drive`、`窗口`、`帮助`；截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-workspace.png`。 |
| GUI-BASE-02 | 工作区全局搜索 | 打开基础工作区并聚焦全局搜索入口 | 无 | 全局搜索占位符为中文 | `verified` | 2026-05-31 P7-M4 | `Cmd-P` 当前周期显示 `搜索命令`，并显示中文筛选 chip；截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-command-palette.png`。 |
| GUI-BASE-03 | 新会话入口 | 打开基础工作区 | 无 | 新建会话/终端入口为中文 | `verified` | 2026-05-31 P7-M4 | 当前 horizontal tab UI 的 `+` 菜单显示 `终端`，系统 `文件` 菜单显示 `新建终端标签页`；这不是历史 `新会话` 文案，但入口已中文化。截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-new-session-menu.png` 和 `docs/gui-smoke-artifacts/phase7/p7-m4-file-menu.png`。 |
| GUI-BASE-04 | 终端-only 工作区 | 首次启动选择 terminal-only 或跳过 Agent 路径 | fresh profile | 中文工作区入口 | `verified` | historical GUI smoke | 需在新 profile 下复验一次。 |
| GUI-BASE-05 | 命令面板筛选标签 | 打开命令面板 | 无 | `文件`、`操作`、`会话`、`启动配置` | `verified` | 2026-05-31 P7-M4 | `Cmd-P` 当前周期显示 `搜索命令`、`文件`、`操作`、`会话`、`启动配置` 和 `打开主题选择器`；截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-command-palette.png`。 |

## Onboarding 与登录

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-ONB-01 | Fresh onboarding: Agent path | 清空本地用户状态后首次启动，选择 Agent 路径 | fresh profile | 欢迎、Agent 选择、模型/自主程度等中文 | `manual-gate` | Phase 2 | 需要真实交互式桌面会话。 |
| GUI-ONB-02 | Fresh onboarding: terminal-only path | 清空本地用户状态后首次启动，选择 terminal-only | fresh profile | 不启用 AI、终端路径中文 | `verified` | historical GUI smoke | 建议在下个 release 重新跑。 |
| GUI-ONB-03 | HOA onboarding | 触发新功能/HOA 引导 | 需要对应 feature state | 垂直标签页、Agent 收件箱、标签页配置等中文 | `manual-gate` | Phase 2 first pass | 自动化未稳定触发。 |
| GUI-AUTH-01 | 浏览器登录 | fresh/logged-out profile 中进入 `login_slide.rs`，点击浏览器登录并完成回流 | 需要隔离测试账号、可打开浏览器、可接收 auth callback；不使用主账号 | 登录、授权回流、错误 fallback 中文 | `manual-gate` | 2026-05-30 P5-M4 | 账号和浏览器回流依赖；当前本机 GUI 窗口不可见/不可读，不能证明回流 UI。 |
| GUI-AUTH-02 | Token paste fallback | fresh/logged-out profile 中进入浏览器已打开状态，点击 token 粘贴入口或粘贴无效 redirect URL | 本地可用无效 token 触发错误；完整成功路径仍需测试账号 | token 粘贴、重试、错误提示中文 | `needs-trigger` | 2026-05-30 P5-M4 | 组件路径：`login_slide.rs`、`paste_auth_token_modal.rs`、`login_failure_notification.rs`；无效 token 错误可本地构造，但仍需可见 GUI。 |
| GUI-AUTH-03 | 隐私设置与跳过登录 | fresh profile onboarding 中打开隐私设置，或在登录页触发跳过登录确认 | 需要 fresh profile；不需要真实账号 | 隐私设置、跳过登录确认中文 | `manual-gate` | 2026-05-30 P5-M4 | 本地可触发，但会改变 onboarding/profile 状态；需隔离 profile 和可见 GUI。 |

## 设置页

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-SET-01 | Settings shell | 打开设置页并切换 Account、Appearance、Features、Privacy、AI、Code、MCP、Billing、Environments | 部分页面需要登录 | 设置导航和页面标题中文 | `verified` | 2026-05-31 P7-M4 | 通过右上角菜单进入 `设置`，当前周期看到 `账户`、`Agent`、`代码`、`云平台`、`团队`、`外观`、`功能`、`键盘快捷键`、`Warpify`、`推荐`、`Warp Drive`、`隐私`、`关于` 等导航。截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-settings-shell.png`。 |
| GUI-SET-02 | Appearance command actions | 打开 Appearance 或命令面板中相关动作 | 无 | Appearance 动作标签中文，搜索关键词不被破坏 | `manual-gate` | Round 2 | `dim inactive panes` 等搜索 tag 仍保留英文。 |
| GUI-SET-03 | AI settings deep paths | 打开 AI 设置，查看 Build 方案、BYO API keys、自定义端点 | 登录或对应 plan 状态 | Build 方案、API 密钥、自定义端点中文 | `manual-gate` | Phase 2 first pass | 需要账号和 plan 状态。 |
| GUI-SET-04 | AWS Bedrock credentials | 打开 AI 设置中的 AWS Bedrock 凭据区域 | AWS/Bedrock 配置状态 | AWS Bedrock 凭据、登录命令、AWS Profile、刷新中文 | `manual-gate` | Phase 2 / Round 2 | 需要凭据或错误状态。 |
| GUI-SET-05 | AWS credential errors | 构造 Bedrock 凭据错误 | AWS/Bedrock 错误状态 | AWS 凭据错误中文 | `needs-trigger` | Round 2 / Round 4 | 需要可重复错误触发方式。 |
| GUI-SET-06 | Environment deletion confirmation | Settings > Environments 中编辑可删环境并点击 `删除环境` | 需要隔离的 cloud environment 测试对象；不能使用真实生产环境 | `删除环境？`、`确定要移除 … 环境吗？`、`删除环境`、`取消` | `manual-gate` | 2026-05-31 P6-M3 | 源码路径已复查：`update_environment_form.rs` 触发，`delete_environment_confirmation_dialog.rs` 渲染；P6-M3 未尝试删除，因为 P6-M2 为 `automation-blocked`，且没有隔离 cloud environment 对象。 |

## 工作区、会话与确认框

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-WS-01 | 工作区左右面板 | 打开左侧/右侧面板、工具面板、用户菜单 | 视入口而定 | Agent 对话、Warp Drive、工具面板等中文 | `manual-gate` | Phase 2 | 基础入口已部分验证，深层菜单未完整复验。 |
| GUI-WS-02 | 会话列表菜单和删除 toast | 打开会话列表，对会话执行菜单/删除操作 | 有会话历史 | 菜单项、删除 toast 中文 | `manual-gate` | Round 2 | 需要可删除测试会话。 |
| GUI-WS-03 | Rewind 搜索提示和确认 | 触发 terminal rewind 或回退确认 | 有可 rewind 会话 | rewind 搜索和确认说明中文 | `manual-gate` | Phase 2 first pass | 需要构造历史命令状态。 |
| GUI-WS-04 | Auth-secret 删除确认 | Agent auth secret selector 中删除 managed auth secret | 需要隔离 managed auth secret；不能删除真实密钥 | `删除密钥`、`确定要删除 … 吗？`、`删除`、`取消` | `manual-gate` | 2026-05-31 P6-M3 | 源码路径已复查：`auth_secret_selector.rs` 打开删除动作，`delete_auth_secret_confirmation_dialog.rs` 渲染；P6-M3 阻塞于 `automation-blocked` 和缺少隔离 managed auth secret。 |
| GUI-WS-05 | CLI 管理员权限提示 | 安装/卸载 Oz CLI 命令 | macOS 权限提示 | 管理员权限提示中文 | `manual-gate` | Round 3 | AppleScript 字符串已通过编译验证，仍需视觉确认。 |
| GUI-WS-06 | Remove endpoint confirmation | Settings > AI > 自定义推理中编辑并移除自定义 endpoint | Public-RC 需要隔离测试账号；fixture smoke 可使用 `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`，但不能替代真实账号证据 | `移除端点？`、`确定要移除此端点吗？`、`移除端点`、`取消` | `fixture-verified` | 2026-05-31 P9-M5 | P9-M4 使用 debug-only in-memory fixture 预置 `zh-smoke-delete-endpoint`，验证了列表显示、编辑弹窗、取消删除后保留、最终删除和 `端点已移除` toast。截图：`docs/gui-smoke-artifacts/phase9/p9-m4-fixture-endpoint-seeded.png`、`p9-m4-fixture-edit-modal.png`、`p9-m4-fixture-remove-confirmation.png`、`p9-m4-fixture-after-cancel.png`、`p9-m4-fixture-after-remove.png`。P9-M5 尝试不带 fixture env 的真实路径，但当前没有隔离测试账号；`zh-rc6` 进程只带 `WARP_DATA_PROFILE=zh-rc6`，无 `WARP_CN_CUSTOM_INFERENCE_SMOKE`，并触发 Keychain/App 数据权限提示，均已拒绝。该行仍不能升级为 `verified`，public-RC 仍要求不带 fixture env 的隔离测试账号路径。 |
| GUI-WS-07 | Transfer ownership confirmation | 转让团队所有权 | 团队 owner 账号 | 转让确认中文 | `manual-gate` | Round 3 | 高风险路径，必须测试账号隔离。 |
| GUI-WS-08 | 标签页右键菜单 | 右键当前会话标签页 | 无 | `共享会话`、`复制标签页标题`、`重命名标签页`、`关闭标签页`、`关闭其他标签页`、`关闭右侧标签页`、`另存为新配置` | `verified` | 2026-05-31 P7-M4 | 当前 `zh-rc4` profile 使用 horizontal tab UI；右键当前标签页显示 `共享会话`、`复制标签页标题`、`重命名标签页`、`左移标签页`、`关闭标签页`、`关闭其他标签页`、`关闭右侧标签页`、`另存为新配置` 和颜色选项。截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-tab-context-menu.png`。 |

## 云端、Billing 与 Launch Modals

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-CLOUD-01 | 云端 Agent 容量弹窗 | Cloud Mode ambient agent 触发 `ConcurrentLimit` 或 paid-plan out-of-credits 触发 `OutOfCredits` | 需要 CloudMode、ambient agent、服务端 at-capacity/Quota 状态或受控 mock；不使用主账号额度做验证 | 容量、点数、升级提示中文 | `needs-trigger` | 2026-05-30 P5-M4 | 路径：`ambient_agent/model.rs`、`ambient_agent/view_impl.rs`、`cloud_agent_capacity_modal/mod.rs`；仍有定价/倍数英文残留，需先可重复触发。 |
| GUI-BILL-01 | 额度耗尽/额度弹窗 | `BuyCreditsBanner` 显示 `OutOfCredits` 或 `MonthlyLimitReached` | 需要 workspace 允许购买 add-on credits、无剩余额度/bonus、auto reload 状态或受控 model fixture；不消费真实主账号额度 | 额度、自动充值、方案说明中文 | `needs-trigger` | 2026-05-30 P5-M4 | 路径：`request_usage_model.rs`、`terminal/buy_credits_banner.rs`；可用模型测试验证条件，GUI 需隔离账号状态。 |
| GUI-BILL-02 | Build 方案迁移弹窗 | 打开 `BuildPlanMigrationModal` 或满足 one-time modal 条件 | 需要已登录团队管理员、team service agreement 带 `sunsetted_to_build_ts`、未 dismiss；可考虑开发动作强制打开但不能作为公开账号证据 | Build 方案迁移说明中文 | `needs-trigger` | 2026-05-30 P5-M4 | 路径：`one_time_modal_model.rs`、`build_plan_migration_modal.rs`；核心 copy 已中文化，但触发依赖服务端 billing 状态。 |
| GUI-LAUNCH-01 | Oz/OpenWarp/orchestration launch modals | 触发 launch modal | feature/version 状态 | launch modal 标题、按钮、说明中文 | `manual-gate` | Round 3 | 需要对应 feature 状态。 |

## Agent 与 Warp on Web

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-AGENT-01 | Agent tips | 打开 Agent 输入区域并触发 tips | Agent enabled | tips、快捷提示中文 | `manual-gate` | Round 3 | 需要确认不会遮挡输入。 |
| GUI-AGENT-02 | Conversation details panel | 打开 Agent conversation details | 有 Agent 对话 | metadata、状态、操作中文 | `manual-gate` | Round 3 | 需要测试对话。 |
| GUI-AGENT-03 | Agent conversation status labels | 触发 task/conversation queued、pending、in progress、done、failed、blocked、cancelled | 需要 Agent 任务生命周期状态或 model fixture；不依赖破坏性账号操作 | `排队中`、`等待中`、`进行中`、`已完成`、`失败`、`已阻塞`、`已取消` | `needs-trigger` | 2026-05-30 P5-M5 | P5-M5 已替换 status display 层、pending query badge 和 history status；GUI 仍需构造生命周期状态复验。 |
| GUI-AGENT-04 | Agent error residue | 触发 web search/fetch、AWS Bedrock、quota 或 Agent stream error fallback | 错误状态、mock/failure fixture 或隔离测试账号；不应使用主账号配额耗尽做测试 | 错误提示中文 | `needs-trigger` | 2026-05-30 P5-M4 | 需要把 web/AWS/quota 错误拆成单独 fixture；本轮只记录门禁，不追加批量翻译。 |
| GUI-AGENT-05 | Agent Assisted Environment fallback | 打开环境创建/编辑弹窗并触发 fallback 文案 | 环境功能状态 | fallback 文案中文 | `needs-trigger` | Round 4 | Round 4 未触发对应状态。 |
| GUI-WEB-01 | Warp on Web home | 打开 Warp on Web home | web/home 可达状态 | home copy 中文 | `needs-trigger` | Round 4 | Round 4 未触发该页面。 |

## 2026-05-30 P4-M5 记录

- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` 成功生成并签名 `target/debug/bundle/osx/WarpOss.app`。
- `open -n target/debug/bundle/osx/WarpOss.app` 成功启动本地 bundle，`warp-oss` 和 `terminal-server` 进程均可见。
- Computer Use 读取窗口并确认基础工作区中文锚点、设置 shell、命令面板和垂直标签页右键菜单。
- 本轮发现 `app/src/tab.rs` 右键菜单英文残留后已补齐 manifest 并复验：`Share session`、`Copy pane title`、`Copy working directory`、`Rename tab`、`Close tab`、`Close other tabs`、`Close Tabs Below`、`Save as new config` 等已显示为中文。
- 重建后 macOS 曾弹出 `WarpOss` 访问其他 App 数据的系统权限提示。本轮未授予该权限；提示关闭后 GUI 可继续读取。
- Destructive confirmation 仍未自动触发：当前本地 profile 没有可安全删除的 endpoint、environment、auth secret 或 team ownership 测试对象，相关路径继续保留为 `manual-gate`。

## 2026-05-30 P5-M2 记录

- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` 成功生成并签名 `target/debug/bundle/osx/WarpOss.app`。
- `open -n target/debug/bundle/osx/WarpOss.app` 启动后，`warp-oss` 和 `terminal-server` 进程可见。
- Computer Use 对 `WarpOss` 连续两次读取窗口状态均超时：`Computer Use server error -10005: timeoutReached`。
- AppleScript `tell application id "dev.warp.WarpOss" to activate` 超时：`AppleEvent已超时。 (-1712)`。
- 截图证据：
  - `docs/gui-smoke-artifacts/2026-05-30-p5-m2-desktop.png`
  - `docs/gui-smoke-artifacts/2026-05-30-p5-m2-after-activate.png`
- 两张截图都只显示桌面壁纸，没有可见 `WarpOss` 窗口。因此本轮只证明 bundle 和进程启动，不新增业务路径 `verified`。
- P5-M2 的结论是 `automation-blocked` 证据流程已落档；后续 GUI 验证应优先复用 P4-M5 已证明可读窗口的交互式桌面状态，或先解决当前窗口不可见/激活超时问题。

## 2026-05-30 P5-M3 destructive confirmation review

- `GUI-WS-06` custom endpoint 删除路径：`app/src/settings_view/ai_page.rs` 中 `CustomEndpointModalEvent::RemoveEndpoint` 会调用 `show_remove_custom_endpoint_confirmation_dialog`，再由 `app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs` 渲染 `移除端点？`、说明文案、endpoint 名称、model chips、`取消` 和 `移除端点`。复验需要启用 custom inference 的测试 profile，并先创建可恢复 endpoint。
- `GUI-SET-06` environment 删除路径：`app/src/settings_view/update_environment_form.rs` 的 `删除环境` 按钮触发删除事件，`app/src/settings_view/environments_page.rs` 打开确认流程，`app/src/settings_view/delete_environment_confirmation_dialog.rs` 渲染 `删除环境？`、`确定要移除 … 环境吗？`、`取消` 和 `删除环境`。复验需要隔离 cloud environment 对象。
- `GUI-WS-04` auth secret 删除路径：`app/src/terminal/view/ambient_agent/auth_secret_selector.rs` 的 `DeleteSecret` 操作打开 `app/src/terminal/view/ambient_agent/delete_auth_secret_confirmation_dialog.rs`。P5-M3 发现该确认框标题和按钮仍为 `Delete secret`、`Cancel`、`Delete`，已补入 manifest 并替换为 `删除密钥`、`取消`、`删除`。
- 本轮没有把上述路径标为 `verified`：P5-M2 已证明当前本机 `WarpOss` 窗口不可见/不可读，且当前 profile 没有隔离 endpoint、environment、auth secret 测试对象。P5-M3 的达标结果是把每个 manual gate 的具体对象、触发路径和剩余阻塞写清楚，并修复了一个源码级英文残留。

## 2026-05-30 P5-M4 account/state gate decomposition

- Auth gate 分为三类：`GUI-AUTH-01` 需要隔离测试账号和浏览器 auth callback；`GUI-AUTH-02` 的无效 token 错误可以本地构造，但成功登录仍需测试账号；`GUI-AUTH-03` 只需 fresh profile，但必须隔离 onboarding/profile 状态。
- Cloud gate 分为两类：`ConcurrentLimit` 来自 cloud ambient agent at-capacity 事件，`OutOfCredits` 来自 paid-plan quota/credits 状态。两者都不能靠普通 bundle gate 验证，需要服务端状态或受控 fixture。
- Billing gate 分为两类：`BuyCreditsBanner` 由 `AIRequestUsageModel::compute_buy_addon_credits_banner_display_state` 决定，可先用模型测试覆盖条件；`BuildPlanMigrationModal` 由 logged-in team admin + `sunsetted_to_build_ts` + 未 dismiss 状态触发。
- Agent status gate 已定位到 display 层：`AgentRunDisplayStatus`、`AmbientAgentTaskState`、pending query badge 和 history status。它们是 P5-M5 的合适小切片，但 GUI verified 仍需要能构造 queued/running/failed/done/blocked/cancelled 状态。
- 本轮没有新增 GUI `verified`，因为 P5-M4 的目标是把账号、Billing、Cloud、Agent 状态门禁拆成可执行触发条件和剩余阻塞，不消耗真实主账号额度或团队状态。

## 2026-05-30 P5-M5 Agent status slice

- 已将 `app/src/ai/agent_conversations_model.rs` 中 `AgentRunDisplayStatus` 的短标签替换为中文：`排队中`、`等待中`、`已分配`、`进行中`、`已完成`、`失败`、`错误`、`已阻塞`、`已取消`。
- 已将 `app/src/ai/ambient_agents/task.rs` 中 `AmbientAgentTaskState` 的短标签替换为同一套中文术语。
- 已将 `app/src/ai/blocklist/block/pending_user_query_block.rs` 的 pending query badge 替换为 `排队中`。
- 已将 `app/src/ai/blocklist/history_model.rs` 的 history status 替换为 `已成功完成`、`等待中`、`用户已取消`、`失败`。
- 这些变更属于源码级可见标签修复，不等同于 GUI verified；`GUI-AGENT-03` 仍需构造 Agent 生命周期状态或 model fixture 后复验。

## 2026-05-31 P6-M2 GUI automation recovery

Phase 6 GUI profile status: `automation-blocked`.

- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` 成功生成并签名 `target/debug/bundle/osx/WarpOss.app`。
- `open -n target/debug/bundle/osx/WarpOss.app` 返回成功，`pgrep -afil 'warp-oss|terminal-server'` 能看到 `warp-oss` 和 `terminal-server`。
- Computer Use 对 `WarpOss` 和 bundle id `dev.warp.WarpOss` 均超时：`Computer Use server error -10005: timeoutReached`。
- 系统截图显示 macOS 弹窗：`你不能打开应用程序 “WarpOss”，因为它没有响应。`
- 截图证据：`docs/gui-smoke-artifacts/phase6/p6-m2-warp-oss-not-responding-2026-05-31.png`
- `osascript` 能确认前台进程为 `warp-oss`，但 `System Events` 不能取得 `menu bar 1 of process "WarpOss"`，窗口列表为空。
- `/usr/bin/log show --last 3m --predicate 'process == "warp-oss"' --style compact` 未返回可用 app 日志。
- 结论：P6-M2 只证明 bundle gate 和进程启动，不证明任何业务 GUI 路径。当前 profile/窗口状态不能作为 destructive confirmation、账号、Billing、Cloud 或 Agent GUI verified 的依据。

## 2026-05-31 P6-M3 destructive confirmation blockers

- `GUI-WS-06` custom endpoint 删除是最低风险 destructive path，但本轮未触发：P6-M2 已证明当前 `WarpOss` 为 `automation-blocked`，且当前 profile 没有可删除的 `zh-smoke-delete-endpoint` 隔离对象。
- `GUI-WS-06` 源码锚点已复查：`ai_page.rs` 的 `CustomEndpointModalEvent::RemoveEndpoint` 会打开 `remove_custom_endpoint_confirmation_dialog.rs`，其中已有 `移除端点？`、`确定要移除此端点吗？之后你将无法在 Agent 会话中使用它的模型。`、`取消`、`移除端点`。
- `GUI-SET-06` environment 删除未继续尝试：只有在 endpoint 删除验证成功后才考虑 environment 删除；当前还缺少隔离 cloud environment 对象，且 GUI 自动化阻塞。
- `GUI-SET-06` 源码锚点已复查：`update_environment_form.rs`、`environments_page.rs`、`delete_environment_confirmation_dialog.rs` 中已有 `删除环境`、`删除环境？`、`确定要移除 ... 环境吗？`、`取消`。
- `GUI-WS-04` auth-secret 删除仍阻塞：当前没有隔离 managed auth secret，不能触碰真实密钥；GUI 自动化同样阻塞。
- `GUI-WS-04` 源码锚点已复查：`auth_secret_selector.rs` 打开删除动作，`delete_auth_secret_confirmation_dialog.rs` 中已有 `删除密钥`、`确定要删除 ... 吗？此操作无法撤销。任何引用此密钥的 Agent 或环境都将无法再访问它。`、`取消`、`删除`。
- 本轮没有删除真实 endpoint、cloud environment 或 secret，也没有把任何 destructive confirmation 标记为 `verified`。

## 2026-05-31 P6-M4 fixture ownership map

Owner categories:

- `local-fixture`: can be triggered with a fresh/local profile, model fixture, fake token, local test conversation, or controlled mock state.
- `test-account`: requires an isolated account or team that is safe to sign in with and mutate.
- `server-state`: requires backend quota, billing, capacity, team agreement, or service-side feature state.
- `manual-only`: high-risk or platform/permission path that should not be automated without a dedicated manual test plan.

| Row | Owner category | Concrete trigger | Remaining blocker |
| --- | --- | --- | --- |
| GUI-ONB-01 | `local-fixture` | Fresh profile selects Agent onboarding path | P6-M2 `automation-blocked`; needs isolated profile reset. |
| GUI-ONB-03 | `server-state` | HOA/feature state exposes the launch/onboarding modal | Need feature/version state fixture. |
| GUI-AUTH-01 | `test-account` | Logged-out fresh profile uses browser auth and receives callback | Needs isolated auth account and visible GUI. |
| GUI-AUTH-02 | `local-fixture` | Paste invalid redirect/token to force fallback/error UI | Needs visible GUI; successful auth remains covered by `GUI-AUTH-01`. |
| GUI-AUTH-03 | `local-fixture` | Fresh profile opens privacy settings or skip-login confirmation | Needs visible GUI and disposable profile. |
| GUI-SET-03 | `test-account` | Test account with AI settings, plan state, BYO keys, and custom endpoint UI enabled | Needs isolated account/plan state; do not use main account. |
| GUI-SET-04 | `manual-only` | AWS/Bedrock credential settings with disposable AWS profile | Needs explicit credentials test plan; do not touch real credentials. |
| GUI-SET-05 | `local-fixture` | Invalid Bedrock credential/profile fixture to force error UI | Needs fixture path and visible GUI. |
| GUI-CLOUD-01 | `server-state` | Cloud ambient agent receives `ConcurrentLimit` or `OutOfCredits` | Needs quota/capacity service state or a controlled mock. |
| GUI-BILL-01 | `local-fixture` | Model fixture covers `BuyCreditsBanner` display conditions | Public GUI evidence still needs test account with safe quota state. |
| GUI-BILL-02 | `server-state` | Team service agreement includes `sunsetted_to_build_ts` and modal is not dismissed | Needs backend billing/team state; dev action alone is not public evidence. |
| GUI-AGENT-01 | `local-fixture` | Agent-enabled fresh/local profile opens tips near the input | Needs visible GUI and overlap check. |
| GUI-AGENT-02 | `local-fixture` | Disposable local/fixture Agent conversation opens details panel | Needs test conversation fixture. |
| GUI-AGENT-03 | `local-fixture` | Model/fixture conversations cover queued, pending, running, done, failed, blocked, cancelled | Source labels are translated; GUI evidence still needs lifecycle fixture. |
| GUI-AGENT-04 | `local-fixture` | Mocked web/AWS/quota/stream errors exercise fallback copy | Quota/AWS account variants may require `test-account` or `server-state`; do not consume main quota. |
| GUI-AGENT-05 | `local-fixture` | Environment modal fixture triggers Agent Assisted Environment fallback | Needs environment feature state and visible GUI. |
| GUI-WEB-01 | `server-state` | Warp on Web home route reachable with expected home state | Needs web/home availability and a route fixture. |

## 记录规则

每次执行 GUI 冒烟后更新对应行的状态和最近记录。失败项必须记录：

- 触发路径。
- 看到的英文原文或异常状态。
- 是否需要账号、服务端状态、feature flag 或测试数据。
- 截图或窗口读取失败的原因。

不能把以下结果写成 `verified`：

- 只完成 `./script/run --dont-open` bundle gate。
- 只看到 `warp-oss` 或 `terminal-server` 进程启动。
- 只通过 dry-run、coverage、编译或单元测试。
- GUI 自动化读取窗口超时但没有人工视觉确认。
