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
| `blocked-no-isolated-account` | public-RC 行需要隔离测试账号；当前没有可用账号或不能使用主账号。 |
| `blocked-no-backend-fixture` | public-RC 行需要后端、计费、AWS、容量或错误状态 fixture；当前未提供。 |
| `blocked-no-disposable-object` | public-RC 行需要精确命名的 disposable endpoint/environment/secret/team；当前对象不存在或未确认。 |
| `ready-with-prerequisites` | 执行步骤已定义，但必须先满足对应前置条件。 |
| `verified-current-cycle` | 当前 RC 周期已用合规证据验证。 |

## RC20 public-RC blocker registry

RC20 起，以下三类 public-RC blocked 状态的机器可读来源是：

```text
resources/localization/zh-Hans-public-rc-blockers.toml
script/zh_public_rc_status.py
```

当前 registry 总数为 11：

```text
blocked-no-isolated-account: 3
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
```

矩阵中的 blocked 行不能只靠 fixture 或源码检查升级；必须同时更新
registry、阶段记录和对应的 redacted GUI/backend/account 证据。

## 0.19 Self-Defined Complete Release GUI Scope

| Area | Required for 0.19 | Evidence Type | Official backend required |
| --- | --- | --- | --- |
| App launch | yes | current-cycle screenshot or reviewer note | no |
| Onboarding visible copy | yes | screenshot or static asset decision | no |
| Workspace shell | yes | screenshot or reviewer note | no |
| Command search（界面文案：命令搜索） | yes | screenshot or reviewer note | no |
| Settings core pages | yes | screenshot or reviewer note | no |
| AI settings entry | yes | screenshot or reviewer note | no |
| Login callback | no | known limitation or isolated account lane | no official approval, but requires isolated account |
| Billing / quota / Cloud | no | known limitation | yes |
| Delete / transfer real objects | no | cancel-first proof only | no official approval, but requires disposable object approval |

## 0.19 Current-Cycle GUI Smoke Result - 2026-06-07

| Area | Canonical Status | Reviewer Note |
| --- | --- | --- |
| App launch | verified-current-cycle | `WarpOss.app` opened foreground `~` workspace and `设置` windows; no raw screenshot is committed. |
| Workspace shell | verified-current-cycle | New workspace window `~` displayed `搜索标签页...`, `新会话`, and accessibility text `输入 shell 命令` / `命令输入`; no shell command was executed. |
| Command search（界面文案：命令搜索） | verified-current-cycle | `视图 > 命令搜索` opened a panel with `命令搜索`, `我想找...`, `历史记录`, `示例查询`, and `搜索历史记录、工作流等`. |
| Settings core pages | verified-current-cycle | Settings navigation and core labels were visible and readable in Chinese. |
| AI settings entry | verified-current-cycle | `Warp Agent` settings page was visible with AI labels and descriptions; no private credentials were entered. |
| Dangerous confirmation cancel path | blocked-no-disposable-object | No approved disposable object exists for this cycle, so no real destructive dialog was opened and no mutation was attempted. |

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

## Phase 10 证据卫生规则

Phase 10 起，GUI 证据还必须遵守 `docs/zh-Hans-evidence-policy.md`：

- 不再提交原始全屏桌面截图或录屏。
- 优先记录 Computer Use/accessibility tree 中看到的中文锚点。
- 截图只作为辅助证据，提交前必须裁剪或脱敏。
- 账号、邮箱、团队名、API key、token、magic link、本地路径、浏览器状态和无关系统弹窗必须脱敏。
- debug-only fixture 证据只能标记为 `fixture-verified`，不能升级为 public-RC `verified`。
- 已经进入 Git 历史的早期截图需要单独的历史清理任务；普通后续删除不能从已发布 tag/history 中移除它们。

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

## Phase 76 public-RC evidence dry-run package

审计日期：2026-06-02。

Phase 76 没有启动 GUI，也没有触碰账号、后端、账单、云环境、团队、
managed secret、自定义端点或任何 destructive state。该阶段只把 public-RC
剩余 blocker 的证据采集流程整理成可执行包。

证据目录：

- `docs/gui-smoke-artifacts/phase76/`

默认 profile：

```text
zh-rc15-public-rc-dry-run
```

状态保持：

| Row | Phase 76 status | Evidence requirement |
| --- | --- | --- |
| `GUI-AUTH-01` | `blocked-until-isolated-account` | 需要隔离测试账号和浏览器 callback。 |
| `GUI-SET-03` | `blocked-until-isolated-account-state` | 需要能看到 AI settings、Build plan、API key、自定义推理的隔离账号状态。 |
| `GUI-SET-04` | `blocked-until-disposable-aws-profile` | 需要 disposable AWS/Bedrock profile 或明确 fixture。 |
| `GUI-SET-05` | `blocked-until-invalid-credential-fixture` | 需要不会访问真实凭据的 invalid Bedrock fixture。 |
| `GUI-SET-06` | `blocked-until-disposable-environment` | 需要名为 `zh-smoke-delete-environment` 的 disposable cloud environment。 |
| `GUI-WS-04` | `blocked-until-disposable-secret` | 需要名为 `zh-smoke-delete-secret` 的 disposable managed auth secret。 |
| `GUI-WS-06` | `fixture-verified-only` | fixture 已验证渲染；public RC 仍需要不带 fixture env 的隔离账号路径。 |
| `GUI-WS-07` | `blocked-until-disposable-team` | 需要名为 `zh-smoke-public-rc-team` 的 disposable owner test team 和明确批准。 |
| `GUI-BILL-01` | `blocked-until-safe-billing-state` | 需要不会购买/消耗真实额度的 billing fixture 或测试账号状态。 |
| `GUI-BILL-02` | `blocked-until-backend-billing-state` | 需要 backend test team 的 Build plan migration 状态。 |
| `GUI-CLOUD-01` | `blocked-until-capacity-fixture` | 需要 cloud capacity/quota fixture 或 backend test state。 |

Phase 76 不能把任何行升级为 `verified`。后续只有在 cropped/redacted
截图、accessibility anchors、cleanup proof 全部满足且证据类型为
`real-account-evidence` 时，public-RC 行才能升级。

## Phase 83 RC16 public-RC prerequisites

审计日期：2026-06-02。

Phase 83 没有启动 GUI，也没有触碰账号、后端、账单、云环境、团队、
managed secret、自定义端点或任何 destructive state。它只把 RC16
public-RC 行整理为精确前置条件。

主文档：

- `docs/zh-Hans-public-rc-prerequisites-rc16.md`

| Row | Phase 83 status | Required prerequisite |
| --- | --- | --- |
| `GUI-AUTH-01` | `blocked-no-isolated-account` | 隔离 browser-login 测试账号。 |
| `GUI-SET-03` | `blocked-no-isolated-account` | 可见 AI settings、Build plan、API key、自定义推理和模型 UI 的隔离账号。 |
| `GUI-SET-04` | `blocked-no-backend-fixture` | Disposable AWS/Bedrock profile 或明确 fixture。 |
| `GUI-SET-05` | `blocked-no-backend-fixture` | 不会访问真实凭据的 invalid Bedrock fixture。 |
| `GUI-SET-06` | `blocked-no-disposable-object` | 精确命名为 `zh-smoke-delete-environment` 的 disposable cloud environment。 |
| `GUI-WS-04` | `blocked-no-disposable-object` | 精确命名为 `zh-smoke-delete-secret` 的 disposable managed auth secret。 |
| `GUI-WS-06` | `blocked-no-isolated-account` | custom inference enabled 的隔离账号和 `zh-smoke-delete-endpoint`。 |
| `GUI-WS-07` | `blocked-no-disposable-object` | 精确命名为 `zh-smoke-public-rc-team` 的 owner test team 和明确批准。 |
| `GUI-BILL-01` | `blocked-no-backend-fixture` | 不购买、不消耗真实额度的 billing/quota fixture 或测试账号状态。 |
| `GUI-BILL-02` | `blocked-no-backend-fixture` | 带 `sunsetted_to_build_ts` 的 backend test team 状态。 |
| `GUI-CLOUD-01` | `blocked-no-backend-fixture` | controlled capacity/quota backend state 或 local fixture。 |

这些行均未升级为 `verified-current-cycle`。升级前必须具备当前周期的
cropped/redacted screenshot、accessibility anchors、process/profile proof 和
cleanup proof。

## Phase 89 low-risk local GUI smoke preparation

审计日期：2026-06-02。

Phase 89 did not build the bundle or open the GUI because this run is following
a heat-safety policy. It prepared the no-account/no-backend local smoke slice in
`docs/gui-smoke-artifacts/phase89/README.md`.

Safe rows for a later local run:

```text
GUI-BASE-01
GUI-BASE-02
GUI-BASE-03
GUI-BASE-04
GUI-BASE-05
GUI-ONB-01
GUI-ONB-02
GUI-AUTH-03
GUI-SET-01
GUI-SET-02
GUI-WS-08
```

The following public-RC rows remain excluded from low-risk local smoke because
they require isolated account/backend fixtures or disposable objects:

```text
GUI-AUTH-01
GUI-SET-03
GUI-SET-04
GUI-SET-05
GUI-SET-06
GUI-WS-04
GUI-WS-06
GUI-WS-07
GUI-BILL-01
GUI-BILL-02
GUI-CLOUD-01
```

## Phase 90 isolated account check

审计日期：2026-06-02。

Phase 90 checked for the required `zh-rc16-test-account` profile and found no
local profile directories. It did not launch the GUI, open a browser, attempt
login, read secrets, or touch a custom endpoint.

Rows remaining blocked:

```text
GUI-AUTH-01: blocked-no-isolated-account
GUI-SET-03: blocked-no-isolated-account
GUI-WS-06: blocked-no-isolated-account
```

## Phase 91 backend and disposable fixture check

审计日期：2026-06-02。

Phase 91 checked for required backend, billing, cloud, AWS, team, managed-secret,
and disposable-object fixtures. It did not create, delete, or mutate any object.

Rows remaining blocked:

```text
GUI-SET-04: blocked-no-backend-fixture
GUI-SET-05: blocked-no-backend-fixture
GUI-SET-06: blocked-no-disposable-object
GUI-WS-04: blocked-no-disposable-object
GUI-WS-07: blocked-no-disposable-object
GUI-BILL-01: blocked-no-backend-fixture
GUI-BILL-02: blocked-no-backend-fixture
GUI-CLOUD-01: blocked-no-backend-fixture
```

## Phase 121 no-account GUI smoke decision

审计日期：2026-06-02。

Phase 121 did not launch GUI because Phase 120 skipped the current-cycle bundle
gate for heat-safety. It checked for active `warp-oss`, `terminal-server`, or
`WarpOss.app` processes and found none. No no-account GUI rows were promoted to
`verified-current-cycle`, and no account, token, backend, billing, cloud,
managed-secret, endpoint, team, or destructive state was touched.

Rows preserved for the next safe GUI run:

```text
GUI-BASE-01
GUI-BASE-02
GUI-BASE-03
GUI-BASE-04
GUI-BASE-05
GUI-ONB-01
GUI-ONB-02
GUI-AUTH-02
GUI-AUTH-03
GUI-SET-01
GUI-SET-02
GUI-WS-01
GUI-WS-02
GUI-WS-03
GUI-WS-08
GUI-AGENT-01
```

## Phase 123 fixture GUI evidence decision

审计日期：2026-06-02。

Phase 123 did not launch GUI. Phase 122 added a debug/test-only
`WARP_CN_AGENT_LIFECYCLE_SMOKE` lifecycle seed helper, but it is not yet wired
into a GUI smoke launch path. `GUI-AGENT-03` therefore remains `needs-trigger`;
no row was promoted to `fixture-verified`, and the public-RC blocker registry was
unchanged.

## Phase 130 no-GUI lifecycle fixture evidence

审计日期：2026-06-02。

Phase 130 records source-anchor evidence only. Phase 129 added a debug/test-only
model probe for `WARP_CN_AGENT_LIFECYCLE_SMOKE` that exposes deterministic
state query params, localized labels, and lifecycle metadata without starting a
real Agent run or GUI. Targeted Rust tests passed for inert unset/false-like
values and truthy localized lifecycle output.

This is `fixture-prep` evidence, not GUI evidence. `GUI-AGENT-03` remains
`needs-trigger` until a future safe bundle/GUI or accessibility pass captures
the lifecycle labels in a rendered Agent surface. No public-RC blocker was
cleared.

## Phase 131 heat-safe GUI reattempt

审计日期：2026-06-02。

Phase 131 found no active `cargo`, `rustc`, `warp-oss`, `terminal-server`,
`script/run`, or `WarpOss.app` process and no macOS thermal warning. It still
skipped `cargo check -p warp`, bundle generation, and GUI launch because the
system load was already around `3.13 3.64 3.58` and WindowServer/Codex processes
were actively consuming CPU. No GUI row was promoted, and
`WARP_CN_AGENT_LIFECYCLE_SMOKE` was not used in a GUI launch.

## Phase 137 heat-safe no-account GUI decision

审计日期：2026-06-02。

Phase 137 did not launch GUI. Phase 136 did not produce a fresh bundle because
the machine was already under elevated desktop/Codex load, and the second probe
still showed load averages around `3.45 3.59 3.53` with WindowServer and Codex
CPU activity. No no-account GUI row was promoted, and
`WARP_CN_AGENT_LIFECYCLE_SMOKE` was not used in a GUI launch.

## Phase 138 lifecycle fixture feasibility

审计日期：2026-06-02。

Phase 138 chose to keep `WARP_CN_AGENT_LIFECYCLE_SMOKE` as source-anchor
evidence only. The current rendered lifecycle path still depends on
`WaitingForSession` and `ProgressUpdated` model/view state, while Phase 136/137
did not provide a fresh safe bundle/GUI run. `GUI-AGENT-03` remains
`needs-trigger`; no row was promoted to `fixture-verified`.

## Phase 140 public-RC prerequisite refresh

审计日期：2026-06-02。

Phase 140 reran the machine-readable public-RC blocker summary and found the
same 11 blockers: 5 backend fixture rows, 3 disposable object rows, and 3
isolated account rows. No isolated account, backend fixture, disposable object
approval, cleanup proof, or current-cycle GUI/accessibility evidence was
available, so no row was promoted.

## Phase 147 heat-safe no-account GUI decision

审计日期：2026-06-02。

Phase 147 did not launch GUI. Phase 145 skipped the current-cycle full compile
for heat safety, and Phase 146 therefore could not produce a fresh bundle. The
only bundle found was the older `target/debug/bundle/osx/WarpOss.app` from
2026-06-01 21:53:26, so reusing it would not create valid current-cycle RC24
evidence. No `warp-oss`, `terminal-server`, or `WarpOss.app` process was
running after the gate.

No no-account GUI row was promoted. Existing historical GUI evidence remains
unchanged, and public-RC rows remain blocked by account/backend/disposable
object prerequisites.

## Phase 148 Agent lifecycle rendered fixture decision

审计日期：2026-06-02。

Phase 148 chose Option A: keep `WARP_CN_AGENT_LIFECYCLE_SMOKE` as
source-anchor-only evidence. Phase 147 did not launch GUI and no fresh
current-cycle bundle exists, so Option B could not expose rendered lifecycle
labels through the existing app path. Option C would require a new narrow Rust
render harness; no already-proven harness exists in this cycle, so source
changes were deferred.

`GUI-AGENT-03` remains `needs-trigger`. It cannot be promoted without
current-cycle accessibility anchors or cropped/redacted evidence for the
rendered lifecycle labels.

## Phase 158 Agent lifecycle deferred record

审计日期：2026-06-02。

Phase 158 executed the Phase 157 Option A decision. It made no source changes,
did not run a lifecycle render harness, and did not launch GUI. Low-load
manifest, glossary, dry-run, Rust formatting, and diff whitespace checks passed.

`GUI-AGENT-03` remains `needs-trigger` with source-anchor-only evidence. A
future promotion still requires rendered current-cycle accessibility anchors or
cropped/redacted GUI evidence for every required lifecycle label.

## Phase 159 public-RC registry and evidence readiness refresh

审计日期：2026-06-02。

Phase 159 reran the public-RC blocker registry and found the same 11 blockers:
5 backend fixture rows, 3 disposable object rows, and 3 isolated account rows.
No exact current-cycle isolated account, backend fixture, disposable object,
cleanup proof, or GUI/accessibility evidence was available, so no public-RC row
was promoted.

## Phase 160 isolated account evidence gate

审计日期：2026-06-02。

Phase 160 reviewed `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`.
The runbook defines the account label `zh-rc19-test-account` and evidence rules,
but it does not provide an actual isolated account, browser callback, custom
inference state, or disposable endpoint. No login was attempted and no main
account was used.

`GUI-AUTH-01`, `GUI-SET-03`, and `GUI-WS-06` remain
`blocked-no-isolated-account`.

## Phase 161 backend fixture and disposable object gate

审计日期：2026-06-02。

Phase 161 reviewed `docs/zh-Hans-backend-fixture-contract-rc19.md`. The
contract defines fixture names and cleanup requirements, but this execution
context did not provide fixture owners, live backend fixture state, exact
disposable objects, or cleanup proof. No backend, billing, cloud, secret,
environment, endpoint, or team operation was run.

`GUI-SET-04`, `GUI-SET-05`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`
remain `blocked-no-backend-fixture`. `GUI-SET-06`, `GUI-WS-04`, and
`GUI-WS-07` remain `blocked-no-disposable-object`.

## Phase 149 Agent lifecycle deferred record

审计日期：2026-06-02。

Phase 149 executed the Phase 148 Option A decision. It made no source changes,
did not run a lifecycle render harness, and did not launch GUI. Low-load
manifest, glossary, dry-run, Rust formatting, and diff whitespace checks passed.

`GUI-AGENT-03` remains `needs-trigger` with source-anchor-only evidence. A
future promotion still requires rendered current-cycle accessibility anchors or
cropped/redacted GUI evidence for every required lifecycle label.

## Phase 150 public-RC external evidence refresh

审计日期：2026-06-02。

Phase 150 reran the public-RC blocker registry and found the same 11 blockers:
5 backend fixture rows, 3 disposable object rows, and 3 isolated account rows.
No isolated account, backend fixture, disposable object approval, cleanup proof,
or current-cycle GUI/accessibility evidence was available, so no public-RC row
was promoted.

## Phase 156 heat-safe no-account GUI decision

审计日期：2026-06-02。

Phase 156 did not launch GUI. Phase 154 skipped the current-cycle full compile
for heat safety, and Phase 155 therefore could not produce a fresh bundle. The
only bundle found was the older `target/debug/bundle/osx/WarpOss.app` from
2026-06-01 21:53:26, so reusing it would not create valid current-cycle RC25
evidence. No `warp-oss`, `terminal-server`, or `WarpOss.app` process was
running after the gate.

No no-account GUI row was promoted. Existing historical GUI evidence remains
unchanged, and public-RC rows remain blocked by account/backend/disposable
object prerequisites.

## Phase 157 Agent lifecycle rendered fixture decision

审计日期：2026-06-02。

Phase 157 chose Option A: keep `WARP_CN_AGENT_LIFECYCLE_SMOKE` as
source-anchor-only evidence. Phase 156 did not launch GUI and no fresh
current-cycle bundle exists, so Option B could not expose rendered lifecycle
labels through the existing app path. Option C would require a new narrow Rust
render harness; no already-proven harness exists in this cycle, so source
changes were deferred.

`GUI-AGENT-03` remains `needs-trigger`. It cannot be promoted without
current-cycle accessibility anchors or cropped/redacted evidence for the
rendered lifecycle labels.

## Phase 169 heat-safe no-account GUI decision

审计日期：2026-06-02。

Phase 169 did not launch GUI. Phase 167 skipped the current-cycle full compile
because Phase 166 did not find a quiet window, and Phase 168 therefore did not
produce a fresh bundle. The only bundle found was the older
`target/debug/bundle/osx/WarpOss.app` from 2026-06-01 21:53:26, so reusing it
would not create valid current-cycle RC26 evidence. No `warp-oss`,
`terminal-server`, or `WarpOss.app` process was running after the gate.

No no-account GUI row was promoted. Existing historical GUI evidence remains
unchanged, and public-RC rows remain blocked by account/backend/disposable
object prerequisites.

## Phase 170 Agent lifecycle rendered fixture decision

审计日期：2026-06-02。

Phase 170 chose Option A: keep `WARP_CN_AGENT_LIFECYCLE_SMOKE` as
source-anchor-only evidence. Phase 169 did not launch GUI and no fresh
current-cycle bundle exists, so Option B cannot expose rendered lifecycle labels
through the existing app path. Option C would require adding or proving a narrow
Rust render harness in this cycle; no existing proven harness was found, and no
new source changes were made.

`GUI-AGENT-03` remains `needs-trigger`. It cannot be promoted without
current-cycle accessibility anchors or cropped/redacted evidence for the
rendered lifecycle labels.

## Phase 171 Agent lifecycle source-only execution

审计日期：2026-06-02。

Phase 171 executed the Phase 170 Option A decision. It made no source changes,
did not run a lifecycle render harness, and did not launch GUI. Low-load
manifest, glossary, dry-run, Rust formatting, and diff whitespace checks passed.

`GUI-AGENT-03` remains `needs-trigger` with source-anchor-only evidence. A
future promotion still requires rendered current-cycle accessibility anchors or
cropped/redacted GUI evidence for every required lifecycle label.

## Phase 172 public-RC registry and handoff refresh

审计日期：2026-06-02。

Phase 172 reran the public-RC blocker registry in JSON mode and found the same
11 blockers: 5 backend fixture rows, 3 disposable object rows, and 3 isolated
account rows. The current handoff documents remain
`docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md` and
`docs/zh-Hans-backend-fixture-contract-rc19.md`.

No exact current-cycle isolated account, backend fixture, disposable object,
cleanup proof, or GUI/accessibility evidence was available, so no public-RC row
was promoted.

## Phase 173 static onboarding PNG asset gate

审计日期：2026-06-02。

Phase 173 rechecked onboarding PNG status without modifying assets. The
inventory still contains 54 PNGs: 12 root-level onboarding PNGs, 16
`agent_intention` root PNGs, 10 `terminal_intention` root PNGs, 8
`agent_intention/theme` PNGs, and 8 `terminal_intention/theme` PNGs. `git
status --short -- '*.png'` and `git diff --name-only -- '*.png'` returned no
output.

The Phase 45/61 asset policy still applies: static onboarding screenshots remain
visual residue until an approved reversible asset-only regeneration branch is
created. No GUI row was promoted by Phase 173.

## Phase 179 no-account GUI smoke skip

审计日期：2026-06-02。

Phase 179 did not launch GUI because Phase 178 did not produce a fresh
current-cycle bundle. `target/debug/bundle/osx/WarpOss.app` exists, but its
mtime is `Jun 1 21:53:26 2026`, so it is historical bundle evidence rather than
post-RC26 current-cycle evidence.

No `warp-oss`, `terminal-server`, or `WarpOss.app` process was running aside
from the probe shell itself. No GUI row was promoted, no account/backend state
was touched, and no historical bundle was reused as current-cycle evidence.

## Phase 180 isolated-account lane

审计日期：2026-06-02。

Phase 180 reviewed the isolated-account lane for `GUI-AUTH-01`, `GUI-SET-03`,
and `GUI-WS-06`. No isolated test account, browser callback evidence, AI
settings account state, custom-inference-enabled account, disposable
`zh-smoke-delete-endpoint`, or cleanup proof was provided in the execution
context.

No browser auth was launched, no account was used, no endpoint was created or
deleted, and the user's main account was not used. These rows remain
`blocked-no-isolated-account`.

## Phase 181 backend fixture lane

审计日期：2026-06-02。

Phase 181 reviewed backend fixture prerequisites for `GUI-SET-04`,
`GUI-SET-05`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`. No fixture
owner, allowed mutation list, reset procedure, redaction plan, teardown date, or
production-safety proof was provided.

## Phase 189 no-account GUI smoke skip

审计日期：2026-06-02。

Phase 189 did not launch GUI. Phase 188 skipped the fresh bundle build under
heat-safety rules after two probes remained above load 3 with WindowServer
around 43% CPU and active Codex/Finder CPU usage. The only app bundle remained
the historical `target/debug/bundle/osx/WarpOss.app` from 2026-06-01 21:53:26,
so it was not eligible as post-RC27 current-cycle evidence.

No no-account GUI row was promoted. Existing historical GUI evidence remains
unchanged, and public-RC rows remain blocked by account/backend/disposable
object prerequisites.

## Phase 190-195 public-RC external prerequisite lanes

审计日期：2026-06-02。

Phase 190 prepared the isolated-account package and kept `GUI-AUTH-01`,
`GUI-SET-03`, and `GUI-WS-06` blocked because no isolated account credential,
browser callback proof, custom inference state, disposable
`zh-smoke-delete-endpoint`, cleanup proof, or execution approval was available.

Phase 191 respected that blocker and did not launch browser auth, use the main
account, or mutate endpoints.

Phase 192 hardened the backend fixture contract and kept `GUI-SET-04`,
`GUI-SET-05`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` blocked because
no fixture owner, reset procedure, teardown date, or production-safety proof was
available.

Phase 193 respected that blocker and did not contact backend services, enter
credentials, buy credits, consume quota, or mutate billing/cloud/team state.

Phase 194 prepared the disposable-object package and kept `GUI-SET-06`,
`GUI-WS-04`, and `GUI-WS-07` blocked because exact disposable object existence,
disposability, cleanup proof, and explicit destructive-action approval were not
available.

Phase 195 respected that blocker and did not open destructive confirmations,
delete objects, transfer ownership, or touch production state.

## Phase 196 Agent lifecycle render follow-up

审计日期：2026-06-02。

Phase 196 reviewed the source harness for `WARP_CN_AGENT_LIFECYCLE_SMOKE` and
confirmed the localized lifecycle labels remain present in
`app/src/ai/ambient_agents/task.rs`: `排队中`, `等待中`, `已分配`, `进行中`,
`已完成`, `失败`, `错误`, `已阻塞`, and `已取消`.

No rendered GUI evidence was produced because Phase 188 did not produce a fresh
bundle and Phase 189 did not launch GUI. `GUI-AGENT-03` remains
`needs-trigger`; source harness evidence was not promoted as public-RC proof.

No AWS/Bedrock credential path, billing/quota path, cloud capacity path, or
Build plan backend state was touched. These rows remain
`blocked-no-backend-fixture`.

## Phase 182 disposable-object lane

审计日期：2026-06-02。

Phase 182 reviewed disposable-object prerequisites for `GUI-SET-06`,
`GUI-WS-04`, and `GUI-WS-07`. No exact allowlisted
`zh-smoke-delete-environment`, `zh-smoke-delete-secret`, or
`zh-smoke-public-rc-team` object was provided, and no destructive approval or
cleanup proof was available.

No environment delete confirmation, managed-secret delete confirmation, or team
ownership transfer confirmation was opened. No object was deleted or
transferred. These rows remain `blocked-no-disposable-object`.

## Phase 183 Agent lifecycle source harness

审计日期：2026-06-02。

Phase 183 reviewed `AmbientAgentTaskState` display labels and ran:

```bash
CARGO_BUILD_JOBS=1 cargo test -j 1 -p warp lifecycle_smoke_fixture -- --nocapture
```

The targeted source-harness tests passed: 4 passed, 0 failed, 4715 filtered
out. The existing `WARP_CN_AGENT_LIFECYCLE_SMOKE` fixture remains inert without
a truthy env value and covers `排队中`, `等待中`, `已分配`, `进行中`,
`已完成`, `失败`, `错误`, `已阻塞`, and `已取消`.

This is source-harness evidence only. No GUI or accessibility evidence was
produced, so `GUI-AGENT-03` remains `needs-trigger`.

## Phase 184 onboarding PNG asset lane

审计日期：2026-06-02。

Phase 184 rechecked static onboarding PNG assets. `git status --short --
'*.png'` and `git diff --name-only -- '*.png'` produced no output, and
`app/assets/async/png/onboarding` still contains 54 PNGs. The authorization
package still requires the asset-only branch
`codex/zh-Hans-onboarding-assets-rc20`, design/product approval, contact sheets,
binary scope proof, and visual QA before PNG regeneration.

No PNG files were changed. Static onboarding image residue remains
`blocked-no-asset-approval`.

## 基础工作区

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-BASE-01 | macOS 菜单栏 | 启动 `WarpOss.app` 后查看系统菜单栏 | 无 | `文件`、`编辑`、`视图`、`标签页`、`块`、`窗口`、`帮助` | `verified` | 2026-06-01 P38 | Computer Use 在当前源构建中读取到 `文件`、`编辑`、`视图`、`标签页`、`块`、`AI`、`Drive`、`窗口`、`帮助`；截图见 `docs/gui-smoke-artifacts/phase38/p38-main-window-current-source.png`。 |
| GUI-BASE-02 | 工作区全局搜索 | 打开基础工作区并聚焦全局搜索入口 | 无 | 全局搜索占位符为中文 | `verified` | 2026-06-01 P19 | P19 低负载复验在隔离 `zh-p19-lowload` profile 中打开命令面板，显示 `搜索命令`、`文件`、`操作`、`会话`、`启动配置` 和 `打开主题选择器`。截图见 `docs/gui-smoke-artifacts/phase19/p19-command-palette-readable.png`。 |
| GUI-BASE-03 | 新会话入口 | 打开基础工作区 | 无 | 新建会话/终端入口为中文 | `verified` | 2026-05-31 P7-M4 | 当前 horizontal tab UI 的 `+` 菜单显示 `终端`，系统 `文件` 菜单显示 `新建终端标签页`；这不是历史 `新会话` 文案，但入口已中文化。截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-new-session-menu.png` 和 `docs/gui-smoke-artifacts/phase7/p7-m4-file-menu.png`。 |
| GUI-BASE-04 | 终端-only 工作区 | 首次启动选择 terminal-only 或跳过 Agent 路径 | fresh profile | 中文工作区入口 | `verified` | 2026-06-01 P38 | 当前源构建使用 `zh-rc10-local-fixture`，在 onboarding 中选择禁用 AI 后进入主窗口；截图见 `docs/gui-smoke-artifacts/phase38/p38-main-window-current-source.png`。 |
| GUI-BASE-05 | 命令面板筛选标签 | 打开命令面板 | 无 | `文件`、`操作`、`会话`、`启动配置` | `verified` | 2026-05-31 P7-M4 | `Cmd-P` 当前周期显示 `搜索命令`、`文件`、`操作`、`会话`、`启动配置` 和 `打开主题选择器`；截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-command-palette.png`。 |

## Onboarding 与登录

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-ONB-01 | Fresh onboarding: Agent path | 清空本地用户状态后首次启动，选择 Agent 路径 | fresh profile | 欢迎、Agent 选择、模型/自主程度等中文 | `verified` | 2026-06-01 P38 | 当前源构建截图覆盖欢迎页、Agent 选择、个性化、第三方 Agent、主题选择；静态产品预览 PNG 仍作为 `visual-residue` 单独跟踪。截图见 `docs/gui-smoke-artifacts/phase38/p38-onboarding-welcome-current-source.png` 等。 |
| GUI-ONB-02 | Fresh onboarding: terminal-only path | 清空本地用户状态后首次启动，选择 terminal-only | fresh profile | 不启用 AI、终端路径中文 | `verified` | historical GUI smoke | 建议在下个 release 重新跑。 |
| GUI-ONB-03 | HOA onboarding | 触发新功能/HOA 引导 | 需要对应 feature state | 垂直标签页、Agent 收件箱、标签页配置等中文 | `manual-gate` | Phase 2 first pass | 自动化未稳定触发。 |
| GUI-AUTH-01 | 浏览器登录 | fresh/logged-out profile 中进入 `login_slide.rs`，点击浏览器登录并完成回流 | 需要隔离测试账号、可打开浏览器、可接收 auth callback；不使用主账号 | 登录、授权回流、错误 fallback 中文 | `blocked-no-isolated-account` | 2026-06-02 Phase 160 | 账号和浏览器回流依赖；当前没有可用隔离测试账号，不能使用主账号。 |
| GUI-AUTH-02 | Token paste fallback | fresh/logged-out profile 中进入浏览器已打开状态，点击 token 粘贴入口或粘贴无效 redirect URL | 本地可用无效 token 触发错误；完整成功路径仍需测试账号 | token 粘贴、重试、错误提示中文 | `needs-trigger` | 2026-05-30 P5-M4 | 组件路径：`login_slide.rs`、`paste_auth_token_modal.rs`、`login_failure_notification.rs`；无效 token 错误可本地构造，但仍需可见 GUI。 |
| GUI-AUTH-03 | 隐私设置与跳过登录 | fresh profile onboarding 中打开隐私设置，或在登录页触发跳过登录确认 | 需要 fresh profile；不需要真实账号 | 隐私设置、跳过登录确认中文 | `verified` | 2026-06-01 P38 | 当前源构建在 `zh-rc10-local-fixture` 中看到 `开始使用 AI`、`禁用 AI 功能`、禁用 AI 确认、`暂时跳过` 等中文；截图见 `docs/gui-smoke-artifacts/phase38/p38-onboarding-ai-enable-skip-login-current-source.png` 和 `p38-disable-ai-confirmation-current-source.png`。 |

## 设置页

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-SET-01 | Settings shell | 打开设置页并切换 Account、Appearance、Features、Privacy、AI、Code、MCP、Billing、Environments | 部分页面需要登录 | 设置导航和页面标题中文 | `verified` | 2026-06-01 P38 | 当前源构建复验设置页 `账户`、`Warp Agent`、`隐私`，侧栏中文锚点可读；截图见 `docs/gui-smoke-artifacts/phase38/p38-settings-account-current-source.png`、`p38-settings-agent-current-source.png` 和 `p38-settings-privacy-current-source.png`。 |
| GUI-SET-02 | Appearance command actions | 打开 Appearance 或命令面板中相关动作 | 无 | Appearance 动作标签中文，搜索关键词不被破坏 | `manual-gate` | Round 2 | `dim inactive panes` 等搜索 tag 仍保留英文。 |
| GUI-SET-03 | AI settings deep paths | 打开 AI 设置，查看 Build 方案、BYO API keys、自定义端点 | 登录或对应 plan 状态 | Build 方案、API 密钥、自定义端点中文 | `blocked-no-isolated-account` | 2026-06-02 Phase 160 | 需要隔离账号和 plan 状态；当前没有可用隔离测试账号。 |
| GUI-SET-04 | AWS Bedrock credentials | 打开 AI 设置中的 AWS Bedrock 凭据区域 | AWS/Bedrock 配置状态 | AWS Bedrock 凭据、登录命令、AWS Profile、刷新中文 | `blocked-no-backend-fixture` | 2026-06-02 Phase 161 | 需要 disposable AWS/Bedrock profile 或明确 fixture；当前未提供。 |
| GUI-SET-05 | AWS credential errors | 构造 Bedrock 凭据错误 | AWS/Bedrock 错误状态 | AWS 凭据错误中文 | `blocked-no-backend-fixture` | 2026-06-02 Phase 161 | 需要不会访问真实凭据的 invalid Bedrock fixture；当前未提供。 |
| GUI-SET-06 | Environment deletion confirmation | Settings > Environments 中编辑可删环境并点击 `删除环境` | 需要隔离的 cloud environment 测试对象；不能使用真实生产环境 | `删除环境？`、`确定要移除 … 环境吗？`、`删除环境`、`取消` | `blocked-no-disposable-object` | 2026-06-02 Phase 161 | 源码路径已复查：`update_environment_form.rs` 触发，`delete_environment_confirmation_dialog.rs` 渲染；当前缺少精确命名为 `zh-smoke-delete-environment` 的 disposable 对象。 |

## 工作区、会话与确认框

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-WS-01 | 工作区左右面板 | 打开左侧/右侧面板、工具面板、用户菜单 | 视入口而定 | Agent 对话、Warp Drive、工具面板等中文 | `manual-gate` | Phase 2 | 基础入口已部分验证，深层菜单未完整复验。 |
| GUI-WS-02 | 会话列表菜单和删除 toast | 打开会话列表，对会话执行菜单/删除操作 | 有会话历史 | 菜单项、删除 toast 中文 | `manual-gate` | Round 2 | 需要可删除测试会话。 |
| GUI-WS-03 | Rewind 搜索提示和确认 | 触发 terminal rewind 或回退确认 | 有可 rewind 会话 | rewind 搜索和确认说明中文 | `manual-gate` | Phase 2 first pass | 需要构造历史命令状态。 |
| GUI-WS-04 | Auth-secret 删除确认 | Agent auth secret selector 中删除 managed auth secret | 需要隔离 managed auth secret；不能删除真实密钥 | `删除密钥`、`确定要删除 … 吗？`、`删除`、`取消` | `blocked-no-disposable-object` | 2026-06-02 Phase 161 | 源码路径已复查：`auth_secret_selector.rs` 打开删除动作，`delete_auth_secret_confirmation_dialog.rs` 渲染；当前缺少精确命名为 `zh-smoke-delete-secret` 的 disposable managed auth secret。 |
| GUI-WS-05 | CLI 管理员权限提示 | 安装/卸载 Oz CLI 命令 | macOS 权限提示 | 管理员权限提示中文 | `manual-gate` | Round 3 | AppleScript 字符串已通过编译验证，仍需视觉确认。 |
| GUI-WS-06 | Remove endpoint confirmation | Settings > AI > 自定义推理中编辑并移除自定义 endpoint | Public-RC 需要隔离测试账号；fixture smoke 可使用 `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`，但不能替代真实账号证据 | `移除端点？`、`确定要移除此端点吗？`、`移除端点`、`取消` | `blocked-no-isolated-account` | 2026-06-02 Phase 160 | P9-M4 使用 debug-only in-memory fixture 预置 `zh-smoke-delete-endpoint`，验证了列表显示、编辑弹窗、取消删除后保留、最终删除和 `端点已移除` toast。该历史 fixture 证据不能升级为 public-RC 证据；当前仍缺少不带 fixture env 的隔离测试账号和 disposable endpoint。 |
| GUI-WS-07 | Transfer ownership confirmation | 转让团队所有权 | 团队 owner 账号 | 转让确认中文 | `blocked-no-disposable-object` | 2026-06-02 Phase 161 | 高风险路径，必须测试账号隔离；当前缺少精确命名为 `zh-smoke-public-rc-team` 的 owner test team 和明确批准。 |
| GUI-WS-08 | 标签页右键菜单 | 右键当前会话标签页 | 无 | `共享会话`、`复制标签页标题`、`重命名标签页`、`关闭标签页`、`关闭其他标签页`、`关闭右侧标签页`、`另存为新配置` | `verified` | 2026-05-31 P7-M4 | 当前 `zh-rc4` profile 使用 horizontal tab UI；右键当前标签页显示 `共享会话`、`复制标签页标题`、`重命名标签页`、`左移标签页`、`关闭标签页`、`关闭其他标签页`、`关闭右侧标签页`、`另存为新配置` 和颜色选项。截图见 `docs/gui-smoke-artifacts/phase7/p7-m4-tab-context-menu.png`。 |

## 云端、Billing 与 Launch Modals

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-CLOUD-01 | 云端 Agent 容量弹窗 | Cloud Mode ambient agent 触发 `ConcurrentLimit` 或 paid-plan out-of-credits 触发 `OutOfCredits` | 需要 CloudMode、ambient agent、服务端 at-capacity/Quota 状态或受控 mock；不使用主账号额度做验证 | 容量、点数、升级提示中文 | `blocked-no-backend-fixture` | 2026-06-02 Phase 161 | 需要 controlled capacity/quota backend state 或 local fixture；当前未提供。 |
| GUI-BILL-01 | 额度耗尽/额度弹窗 | `BuyCreditsBanner` 显示 `OutOfCredits` 或 `MonthlyLimitReached` | 需要 workspace 允许购买 add-on credits、无剩余额度/bonus、auto reload 状态或受控 model fixture；不消费真实主账号额度 | 额度、自动充值、方案说明中文 | `blocked-no-backend-fixture` | 2026-06-02 Phase 161 | 需要 safe quota/billing fixture 或 disposable billing test account；当前未提供。 |
| GUI-BILL-02 | Build 方案迁移弹窗 | 打开 `BuildPlanMigrationModal` 或满足 one-time modal 条件 | 需要已登录团队管理员、team service agreement 带 `sunsetted_to_build_ts`、未 dismiss；可考虑开发动作强制打开但不能作为公开账号证据 | Build 方案迁移说明中文 | `blocked-no-backend-fixture` | 2026-06-02 Phase 161 | 需要 backend test team with `sunsetted_to_build_ts`；当前未提供。 |
| GUI-LAUNCH-01 | Oz/OpenWarp/orchestration launch modals | 触发 launch modal | feature/version 状态 | launch modal 标题、按钮、说明中文 | `manual-gate` | Round 3 | 需要对应 feature 状态。 |

## Agent 与 Warp on Web

| ID | 路径 | 触发条件 | 账号/状态需求 | 期望中文锚点 | 当前状态 | 最近记录 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-AGENT-01 | Agent tips | 打开 Agent 输入区域并触发 tips | Agent enabled | tips、快捷提示中文 | `manual-gate` | Round 3 | 需要确认不会遮挡输入。 |
| GUI-AGENT-02 | Conversation details panel | 打开 Agent conversation details | 有 Agent 对话 | metadata、状态、操作中文 | `manual-gate` | Round 3 | 需要测试对话。 |
| GUI-AGENT-03 | Agent conversation status labels | 触发 task/conversation queued、pending、in progress、done、failed、blocked、cancelled | 需要 Agent 任务生命周期状态或 model fixture；不依赖破坏性账号操作 | `排队中`、`等待中`、`进行中`、`已完成`、`失败`、`已阻塞`、`已取消` | `needs-trigger` | 2026-06-02 Phase 171 | Phase 129/130 已提供 debug/test-only model probe 和 Rust 测试 source-anchor 证据；Phase 171 执行 Phase 170 Option A，未改源码、未启动 GUI、未运行 render harness，继续保持 source-anchor-only。 |
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

## 2026-06-02 Phase 67 public-RC evidence package

Phase 67 did not launch GUI or touch account/backend state. It refreshed the
public-RC evidence package after RC13 and kept fixture evidence separate from
true isolated-account evidence.

Rows still blocked for public RC:

| Row | Required evidence | Current Phase 67 status |
| --- | --- | --- |
| `GUI-AUTH-01` | Isolated account browser login and auth callback | `blocked-until-isolated-account` |
| `GUI-SET-03` | Real-account AI settings, Build plan/API key/custom inference state | `blocked-until-isolated-account-state` |
| `GUI-SET-04` | Disposable AWS/Bedrock profile | `blocked-until-disposable-aws-profile` |
| `GUI-SET-05` | Invalid Bedrock credential fixture | `blocked-until-invalid-credential-fixture` |
| `GUI-SET-06` | Disposable cloud environment deletion confirmation | `blocked-until-disposable-environment` |
| `GUI-WS-04` | Disposable managed auth secret deletion confirmation | `blocked-until-disposable-secret` |
| `GUI-WS-06` | Disposable custom endpoint removal without fixture env | `fixture-verified-only` |
| `GUI-WS-07` | Disposable team ownership transfer confirmation | `blocked-until-disposable-team` |
| `GUI-BILL-01` | Safe billing/quota state | `blocked-until-safe-billing-state` |
| `GUI-BILL-02` | Backend Build-plan migration state | `blocked-until-backend-billing-state` |
| `GUI-CLOUD-01` | Safe cloud capacity/quota state | `blocked-until-capacity-fixture` |

Public RC cannot be marked `verified` from fixture evidence alone. Cropped or
redacted screenshots and cleanup proof are required for every disposable object
path before promotion.
- GUI 自动化读取窗口超时但没有人工视觉确认。

## 2026-06-01 P18 RC7 evidence decision

RC7 status: `ready-for-local-use-source-level`.

- Phase 13-17 source passes completed and raised release-preset coverage to `4746 covered / 4147 candidates = 53.4%`.
- Low-load and compile gates passed: manifest validation, glossary, dry-run, locale JSON/YAML export, Python localization tests, `cargo fmt --check`, `git diff --check`, and `cargo check -p warp`.
- No GUI row is promoted to `verified` in P18, because this pass did not capture current-cycle visual screenshots for account/state paths.
- Existing historical GUI evidence remains unchanged for base workspace, command palette, settings shell, and tab context menu.
- `GUI-WS-06` remains fixture-level only for custom endpoint deletion; public RC still requires a no-fixture isolated test-account run.
- Browser login, token fallback, Billing, Cloud capacity, Agent lifecycle/error states, environment deletion, and auth-secret deletion remain manual or fixture gates.
- P18 did not use the user's main account, real billing quota, real production cloud environment, real auth secret, or real team ownership state.

## 2026-06-01 P19 low-load GUI evidence recovery

Phase 19 status: `qualified-low-load-gui-source-fix`.

- Used existing `target/debug/bundle/osx/WarpOss.app`; did not run bundle rebuild.
- Launched the app directly with `WARP_DATA_PROFILE=zh-p19-lowload`, `WARP_SKIP_COMMON_SKILLS_INSTALL=1`, and `nice -n 10`.
- Computer Use successfully read the `WarpOss` window and menu bar.
- Current-cycle screenshots captured:
  - `docs/gui-smoke-artifacts/phase19/p19-settings-agent-readable.png`
  - `docs/gui-smoke-artifacts/phase19/p19-command-palette-readable.png`
  - `docs/gui-smoke-artifacts/phase19/p19-warp-drive-english-residue.png`
- Re-verified current-cycle GUI anchors for `GUI-BASE-02` and `GUI-SET-01`.
- Found a logged-out Warp Drive settings page residue: `To use Warp Drive, please create an account.`, `Sign up`, and the Warp Drive description were still English in `app/src/settings_view/warp_drive_page.rs`.
- Added Phase 19 manifest entries and applied source replacements for those Warp Drive strings.
- Did not rebuild the bundle after this source fix to respect the low-load requirement; visual after-fix confirmation is deferred to the next bundle/GUI gate.
- `GUI-ONB-01`, `GUI-AUTH-02`, `GUI-AUTH-03`, `GUI-AGENT-01`, `GUI-AGENT-03`, `GUI-AGENT-04`, and `GUI-AGENT-05` remain blocked or needs-trigger because they require fresh onboarding state, token fallback trigger, Agent input/conversation fixtures, lifecycle fixtures, error fixtures, or environment modal fixtures.
- No main account, real billing quota, cloud environment, secret, or team ownership state was used.
- The P19 `WarpOss` and child `terminal-server` processes were stopped after evidence capture.

## 2026-06-01 P20 public-RC gate runbook

Phase 20 status: `qualified-runbook-only`.

- Added `docs/zh-Hans-public-rc-gate-runbook.md`.
- The runbook defines isolated profiles, disposable object names, screenshot/evidence labels, allowed actions, cleanup rules, and stop conditions for Auth, Settings/AI, custom inference, environment deletion, auth-secret deletion, Billing, Cloud, launch modal, and Agent lifecycle rows.
- `GUI-WS-06` remains fixture-only until an isolated account proves the no-fixture custom endpoint path.
- No public-RC row is promoted in Phase 20; this phase prepares safe execution and prevents accidental use of main accounts, billing quota, production cloud objects, real secrets, or team ownership state.

## 2026-06-01 P21 terminal backlog source pass

Phase 21 status: `qualified-terminal-backlog-pass`.

- Added terminal-focused manifest entries for `terminal/view.rs`, Agent tips, model selector, context menu, SSH errors, and shared-session viewer errors.
- Raised terminal preset coverage from `18.1%` to `37.5%`.
- Raised release preset coverage to `58.5%`.
- Dry-run is clean with `would_change: 0` and `missing: 0`.
- Python localization tests, `cargo fmt --check`, and `git diff --check` passed after mechanical formatting.
- No GUI row is promoted by this source-only pass.

## 2026-06-01 P22 settings/workspace source pass

Phase 22 status: `qualified-settings-workspace-pass`.

- Added Settings and Workspace manifest entries for Teams, Referrals, Appearance search/control terms, global search, right-panel unavailable reasons, and selected workspace toasts/errors.
- Raised Settings coverage from `76.6%` to `87.5%`.
- Raised Workspace coverage from `75.6%` to `94.3%`.
- Raised release preset coverage to `62.8%`.
- Dry-run is clean with `would_change: 0` and `missing: 0`.
- Python localization tests, `cargo fmt --check`, and `git diff --check` passed after mechanical formatting.
- No GUI row is promoted by this source-only pass.

## 2026-06-01 P23 AI SDK/editor/environment source pass

Phase 23 status: `qualified-ai-sdk-editor-environment-pass`.

- Added AI-focused manifest entries for Agent SDK environment setup, Agent Code diff application, execution profile editor, secret/environment CLI, integration output, requested command view, conversation errors, and Codex harness messages.
- Raised AI root coverage from `42.1%` to `56.0%`.
- Raised modals preset coverage to `52.6%`.
- Raised release preset coverage to `66.9%`.
- Dry-run is clean with `would_change: 0` and `missing: 0`.
- Python localization tests, `cargo fmt --check`, and `git diff --check` passed after mechanical formatting.
- No GUI row is promoted by this source-only pass.

## 2026-06-01 P24/P25 metadata migration and RC8 gate

Phase 24/25 status: `qualified-rc8-source-gate`.

- Added missing manifest `context/status` metadata to older entries and raised both fields to `100.0%` coverage.
- Created `docs/zh-Hans-release-candidate-2026-06-01-rc8.md`.
- RC8 release preset coverage is `66.9%`.
- Final dry-run is clean with `would_change: 0` and `missing: 0`.
- Locale JSON/YAML exports, JSON parse, Python localization tests, `cargo fmt --check`, `git diff --check`, and `cargo check -j 2 -p warp` passed.
- `cargo check -j 2 -p warp` only reports existing unused-variable warnings.
- RC8 remains `ready-for-local-use-source-level`, not `ready-for-public-rc`, because account/state GUI rows still require isolated test-account or fixture evidence.

## 2026-06-01 P26 public-RC readiness

Phase 26 status: `qualified-public-rc-readiness`.

- Added post-RC8 execution batches to `docs/zh-Hans-public-rc-gate-runbook.md`.
- Added profile names for `zh-rc9-local-fixture`, `zh-rc9-agent-fixture`, `zh-rc9-test-account`, `zh-rc9-server-state`, and `zh-rc9-aws-fixture`.
- Confirmed local-fixture rows can proceed only if GUI automation can read target UI.
- Confirmed `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06`, `GUI-SET-06`, `GUI-WS-04`, and `GUI-WS-07` remain blocked until an isolated test account and disposable objects exist.
- Confirmed `GUI-CLOUD-01`, `GUI-BILL-01`, `GUI-BILL-02`, `GUI-LAUNCH-01`, `GUI-ONB-03`, and `GUI-WEB-01` require backend, feature, billing, route, or server-state fixtures.
- No GUI row is promoted by this readiness-only phase.
- No source files, accounts, billing quota, cloud environment, secrets, or team ownership state were touched.

## 2026-06-01 P27 terminal backlog source pass

Phase 27 status: `qualified-terminal-backlog-pass-3-low-load`.

- Added Terminal-focused manifest entries across input, events, available shells, CLI Agent, local TTY shell, Claude/Gemini plugin managers, session/model errors, shared-session sharer errors, and terminal init bindings.
- Added `77` translated visible/user-facing strings and `207` reviewed preserves for shell commands, parser/protocol/debug strings, environment variables, product names, and test fixtures.
- Raised Terminal preset coverage from `37.5%` to `52.1%`.
- Raised release preset coverage from `66.9%` to `70.7%`.
- Phase 27 scoped dry-run is clean with `would_change: 0` and `missing: 0`.
- Manifest validation, glossary check, Python localization tests, `cargo fmt --check`, and `git diff --check` passed.
- Full-manifest dry-run is deferred to the Phase 32 RC9 gate because the local machine became hot during full scanning.
- No GUI row is promoted by this source-only pass.

## 2026-06-01 P28 AI/Agent backlog source pass

Phase 28 status: `qualified-ai-agent-backlog-pass-2-low-load`.

- Added AI/Agent manifest entries across Agent SDK CLI output, execution profiles, orchestration controls, usage details, run-agent cards, prompt alerts, remote search errors, LLM availability messages, rules UI, and selected diagnostics.
- Added `240` translated visible/user-facing strings and `117` reviewed preserves for provider CLI output matching, prompt/tool contracts, schema keys, IDs, test fixtures, filenames, command templates, and diagnostics.
- Raised AI root coverage from `56.0%` to `70.9%`.
- Raised modals preset coverage from `58.6%` to `65.8%`.
- Raised release preset coverage from `70.7%` to `75.2%`.
- Phase 28 scoped dry-run is clean with `would_change: 0` and `missing: 0`.
- Manifest validation, glossary check, Python localization tests, `cargo fmt --check`, and `git diff --check` passed.
- Full-manifest dry-run is deferred to the Phase 32 RC9 gate because repeated full scans caused local overheating.
- No GUI row is promoted by this source-only pass.

## 2026-06-01 P29 settings/modals source pass

Phase 29 status: `qualified-settings-modals-cleanup-low-load`.

- Added Settings-focused manifest entries across AI settings, shared blocks, code settings, external editor settings, environment forms, MCP settings, privacy regex, billing state labels, custom inference examples, and Settings navigation labels.
- Added `125` translated visible/searchable/modal-facing strings and `41` reviewed preserves for examples, date formats, IDs, commands, search tags, and diagnostics.
- Raised Settings preset coverage from `87.5%` to `96.3%`.
- Modals preset remains above target at `65.8%`.
- Raised release preset coverage from `75.2%` to `77.2%`.
- Phase 29 scoped dry-run is clean with `would_change: 0` and `missing: 0`.
- Manifest validation, glossary check, Python localization tests, `cargo fmt --check`, and `git diff --check` passed.
- Full-manifest dry-run is deferred to the Phase 32 RC9 gate because repeated full scans caused local overheating.
- No GUI row is promoted by this source-only pass.

## 2026-06-01 P30 low-load GUI evidence pass

Phase 30 status: `qualified-gui-evidence-low-load-with-residue`.

- Reused `target/debug/bundle/osx/WarpOss.app` with `WARP_DATA_PROFILE=zh-rc9-local-fixture`; no rebuild was performed.
- Captured current-cycle screenshots under `docs/gui-smoke-artifacts/phase30/`.
- Verified fresh onboarding and local no-login flow were reachable in the isolated profile.
- `GUI-ONB-01`: `fixture-evidence-with-residue`; onboarding text is Chinese, but static product preview imagery still contains embedded English and the reused bundle showed pre-Phase-28 `auto (cost-efficient)` residue.
- `GUI-AUTH-03`: `fixture-evidence`; `隐私设置`, `服务条款`, `禁用 AI 功能`, and disable-AI confirmation were visible in Chinese.
- `GUI-WS-01`: `accessibility-evidence` + `cropped-screenshot-evidence`; main window, left panel, top search, and Settings navigation were readable in Chinese.
- `GUI-SET-03`: `local-fixture-only`; logged-out Settings > Agent was readable, but isolated account evidence is still required for Build plan/API key/custom endpoint state.
- `GUI-AUTH-02`, `GUI-WS-02`, `GUI-WS-03`, `GUI-WS-05`, and `GUI-AGENT-01` through `GUI-AGENT-05` remain blocked or partial because token fallback, disposable session history, rewind history, admin prompt, Agent tips, Agent conversation, lifecycle, error, and environment modal fixtures were unavailable.
- No public-RC row is promoted by Phase 30.
- No account, billing quota, cloud environment, secret, production object, or team ownership state was touched.

## 2026-06-01 P31 isolated test-account public-RC pass

Phase 31 status: `qualified-public-rc-account-state-blocked`.

- Public-RC account/state rows were audited against `docs/zh-Hans-public-rc-gate-runbook.md`.
- `GUI-AUTH-01` remains `blocked-external-state`: missing isolated test account and browser auth callback.
- `GUI-SET-03` remains `blocked-external-state`: missing isolated account for real AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-06` remains `blocked-external-state`: missing disposable cloud environment `zh-smoke-delete-environment`.
- `GUI-WS-04` remains `blocked-external-state`: missing disposable managed auth secret `zh-smoke-delete-secret`.
- `GUI-WS-06` remains `blocked-external-state`: missing isolated account/custom inference state and disposable endpoint `zh-smoke-delete-endpoint`.
- `GUI-WS-07` remains `blocked-external-state`: missing disposable owner test team `zh-smoke-public-rc-team`.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain `blocked-external-state`: missing safe billing/quota/backend fixtures.
- No public-RC row is promoted by Phase 31.
- No account, billing quota, cloud environment, secret, production object, or team ownership state was touched.

## 2026-06-01 P32 review/freeze/RC9 gate

Phase 32 status: `qualified-rc9-gate`.

- Created `docs/zh-Hans-release-candidate-2026-06-01-rc9.md`.
- RC9 decision is `ready-for-local-use-with-fixture-evidence`.
- Public RC remains not ready because isolated account/state evidence is still unavailable.
- Final manifest state: `6294` entries, `301` files, `would_change: 0`, `missing: 0`.
- Metadata remains complete: manifest `context/status` coverage is `100.0%`.
- Final source coverage: onboarding `100.0%`, workspace `94.3%`, search `100.0%`, settings `96.3%`, modals `65.8%`, release `77.2%`, terminal `52.1%`, AI/Agent `70.9%`.
- Locale JSON/YAML exports completed and JSON parsed.
- Python localization tests passed: `19` tests.
- `cargo fmt --check`, `git diff --check`, and `cargo check -j 2 -p warp` passed.
- Rust warnings are unchanged existing unused-variable warnings in `scp_fallback.rs` and `slash_commands/mod.rs`.
- The full dry-run was run through a throttled wrapper to reduce heat; the Python summary was clean, and no manifest drift or replacement failure was reported.

## 2026-06-01 P37 GUI fixture and visual residue preparation

Phase 37 status: `qualified-gui-fixture-visual-residue-prep`.

- Located the static onboarding preview asset roots used by Phase 30 screenshots:
  - `app/assets/async/png/onboarding/welcome_agent.png`
  - `app/assets/async/png/onboarding/welcome_terminal.png`
  - `app/assets/async/png/onboarding/agent_intention/`
  - `app/assets/async/png/onboarding/terminal_intention/`
  - `app/assets/async/png/onboarding/thirdparty_*.png`
- Confirmed those embedded English previews are PNG content residue, not Rust string manifest drift.
- Added `zh-rc10-local-fixture`, `zh-rc10-agent-fixture`, `zh-rc10-test-account`, `zh-rc10-server-state`, and `zh-rc10-aws-fixture` to the public-RC runbook.
- Defined Phase 38 fixture labels for current-source logged-out onboarding, token fallback, local Agent fixture states, and static imagery.
- No public-RC row is promoted by Phase 37.
- No source fixture code was added in this phase; debug-only fixture implementation remains a Phase 38/39 prerequisite if GUI automation cannot naturally trigger the row.

## 2026-06-01 P38 current-source GUI smoke

Phase 38 status: `qualified-current-source-gui-smoke-low-load`.

- Rebuilt `target/debug/bundle/osx/WarpOss.app` from current source with `CARGO_BUILD_JOBS=2` and `nice -n 10`.
- Launched with `WARP_DATA_PROFILE=zh-rc10-local-fixture`; `warp-oss` and child `terminal-server` were reniced to `15` and stopped after capture.
- Captured current-source screenshots under `docs/gui-smoke-artifacts/phase38/`.
- Promoted current-source local evidence:
  - `GUI-BASE-01`: `accessibility-evidence`; menu bar showed `文件`、`编辑`、`视图`、`标签页`、`块`、`AI`、`Drive`、`窗口`、`帮助`.
  - `GUI-BASE-04`: `cropped-screenshot-evidence`; disabling AI reached the Chinese main window.
  - `GUI-ONB-01`: `cropped-screenshot-evidence`; welcome, Agent choice, customization, third-party Agent, and theme screens were visible in Chinese.
  - `GUI-AUTH-03`: `cropped-screenshot-evidence`; disable-AI confirmation and skip flow were visible in Chinese.
  - `GUI-SET-01`: `cropped-screenshot-evidence`; Account, Warp Agent, and Privacy settings were visible in Chinese.
- Static onboarding preview PNGs still contain embedded English UI and remain `visual-residue`; this is not source string manifest drift.
- The current-source smoke initially showed server/cache-provided `auto (cost-efficient)` model metadata. Source and manifest already translated this string, so Phase 38 added a narrow runtime display-name mapping in `app/src/ai/llms.rs` plus a focused unit test. A second GUI launch after the fix was `automation-blocked` on this desktop, so the fix is accepted by source inspection and unit test rather than a second screenshot.
- `GUI-SET-03` remains blocked for public-RC evidence because real Build plan/API key/custom endpoint state requires an isolated account.
- `GUI-AUTH-01`, `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-06`, `GUI-WS-07`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain blocked until Phase 39 prerequisites exist.
- No main account, billing quota, cloud environment, secret, production object, or team ownership state was touched.

## 2026-06-01 P39 isolated account and backend-state audit

Phase 39 status: `qualified-public-rc-account-state-blocked`.

- Audited the public-RC rows against `docs/zh-Hans-public-rc-gate-runbook.md`.
- Did not run account/backend GUI interactions because no disposable test account, test team, safe billing/quota state, disposable endpoint, disposable cloud environment, disposable managed secret, or cleanup path was available.
- `GUI-AUTH-01` remains `blocked-external-state`: missing isolated test account and browser auth callback.
- `GUI-SET-03` remains `blocked-external-state`: missing isolated account for real AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-06` remains `blocked-external-state`: missing disposable cloud environment `zh-smoke-delete-environment`.
- `GUI-WS-04` remains `blocked-external-state`: missing disposable managed auth secret `zh-smoke-delete-secret`.
- `GUI-WS-06` remains `blocked-external-state`: missing isolated account/custom inference state and disposable endpoint `zh-smoke-delete-endpoint`.
- `GUI-WS-07` remains `blocked-external-state`: missing disposable owner test team `zh-smoke-public-rc-team`.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain `blocked-external-state`: missing safe billing/quota/backend fixtures.
- `GUI-SET-04` and `GUI-SET-05` remain `blocked-external-state`: missing explicit disposable AWS/Bedrock profile or invalid credential fixture.
- No public-RC row is promoted by Phase 39.
- No account, billing quota, cloud environment, secret, production object, or team ownership state was touched.

## 2026-06-02 P40 review/freeze/RC10 gate

Phase 40 status: `qualified-rc10-gate`.

- Created `docs/zh-Hans-release-candidate-2026-06-01-rc10.md`.
- RC10 decision is `ready-for-local-use-with-fixture-evidence`.
- Public RC remains not ready because isolated account/state evidence is still unavailable.
- Final manifest state: `6786` entries, `342` files, `would_change: 0`, `missing: 0`.
- Metadata remains complete: manifest `context/status` coverage is `100.0%`.
- Final source coverage: onboarding `100.0%`, workspace `99.9%`, search `100.0%`, settings `99.9%`, modals `73.1%`, release `83.1%`, terminal `61.2%`, AI/Agent `78.0%`.
- Locale JSON/YAML exports completed and JSON parsed.
- Python localization tests passed: `19` tests.
- `cargo fmt --check`, `git diff --check`, and `cargo check -j 2 -p warp` passed.
- Rust warnings are unchanged existing unused-variable warnings in `scp_fallback.rs` and `slash_commands/mod.rs`.
- The full dry-run was run through a throttled Python wrapper to reduce heat; the Python summary was clean, and no manifest drift or replacement failure was reported.

## 2026-06-02 P44 auth-secret and Agent fixture audit

Phase 44 status: `qualified-auth-secret-ftux-source-and-agent-fixture-blockers`.

- Auth-secret FTUX source copy is translated in `app/src/terminal/view/ambient_agent/auth_secret_ftux_view.rs`: placeholder, save failure, empty-name validation, success toast, credential description, encryption copy, learn-more link, team sharing, optional-field suffix, and buttons.
- Agent task/notification copy is translated in `app/src/ai/ambient_agents/task.rs` and `app/src/ai/agent_management/agent_management_model.rs`: task completion/cancellation/error notifications, task source labels, and cancel-task toasts.
- No GUI launch was attempted in this phase because the laptop heat constraint favors source/fixture audit first, and no safe Agent fixture hook was found that could exercise the rows without account/backend state.
- Existing debug GUI fixture support remains limited to custom inference endpoint smoke via `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`; there is no corresponding `WARP_CN_AGENT_*` or profile-seeded fixture for Agent tips, conversation details, lifecycle states, stream errors, or Agent Assisted Environment fallback.
- `GUI-AUTH-02` remains `needs-trigger`: invalid token fallback is locally constructible in principle, but no visible GUI/token-paste fixture hook exists in current source.
- `GUI-WS-04` remains `blocked-external-state`: auth-secret deletion still requires disposable managed secret `zh-smoke-delete-secret` or a dedicated fixture; Phase 44 only translated auth-secret FTUX source copy and did not create/delete secrets.
- `GUI-AGENT-01` remains `manual-gate`: missing an env-gated Agent tips fixture that opens the Agent input area and exposes overlap/accessibility evidence.
- `GUI-AGENT-02` remains `manual-gate`: missing a disposable local Agent conversation fixture that can open the details panel with safe metadata.
- `GUI-AGENT-03` remains `needs-trigger`: source status labels are translated, but GUI evidence still needs a lifecycle fixture covering queued, pending, in progress, done, failed, blocked, and cancelled.
- `GUI-AGENT-04` remains `needs-trigger`: missing controlled web/AWS/quota/stream-error fixtures; do not consume main-account quota or credentials.
- `GUI-AGENT-05` remains `needs-trigger`: missing an environment-modal fixture that triggers Agent Assisted Environment fallback copy.
- No account, billing quota, cloud object, managed secret, production object, or team state was touched.

## 2026-06-02 P45 static onboarding visual asset decision

Phase 45 status: `qualified-static-onboarding-visual-residue-deferred`.

- Reviewed all `54` onboarding PNGs through source mapping and local contact sheets.
- Accepted `4` assets as `accepted-decorative-or-brand-art`: `hoa_welcome_banner.png`, `onboarding_bg.png`, `openwarp_launch_banner.png`, and `orchestration_launch_banner.png`.
- Classified `50` assets as `defer-to-design-regeneration` because they contain embedded English UI, terminal/code/editor preview text, notification text, toolbar text, or sidebar labels.
- Affected source surfaces are onboarding intention, customization, third-party Agent, theme picker, and login right-panel visuals.
- No PNG was modified in this phase. RC11 must continue to describe these screenshots as `visual-residue`, not manifest/source drift.
- Follow-up requires a reversible asset branch, regenerated Chinese-localized preview art, before/after screenshots, and confirmation that no unrelated binary assets changed.

## 2026-06-02 P46 public-RC external-state evidence pass

Phase 46 status: `qualified-public-rc-account-state-blocked`.

- Followed `docs/zh-Hans-public-rc-gate-runbook.md` and stopped before GUI/account/backend interaction because the required disposable prerequisites were unavailable.
- No GUI launch was attempted, and no account, billing quota, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- `GUI-AUTH-01` remains `blocked-external-state`: missing isolated test account and browser auth callback.
- `GUI-SET-03` remains `blocked-external-state`: missing isolated account for AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-04` and `GUI-SET-05` remain `blocked-external-state`: missing explicit disposable AWS/Bedrock profile or invalid credential fixture.
- `GUI-SET-06` remains `blocked-external-state`: missing disposable cloud environment `zh-smoke-delete-environment`.
- `GUI-WS-04` remains `blocked-external-state`: missing disposable managed auth secret `zh-smoke-delete-secret` or dedicated fixture.
- `GUI-WS-06` remains `blocked-external-state`: missing isolated account/custom inference state and disposable endpoint `zh-smoke-delete-endpoint`.
- `GUI-WS-07` remains `blocked-external-state`: missing disposable owner test team `zh-smoke-public-rc-team`.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain `blocked-external-state`: missing safe billing/quota/backend fixtures.
- No row was promoted to public-RC `verified`; public RC remains blocked by current-cycle external-state evidence.

## 2026-06-02 P53 visual and public-RC blocker refresh

Phase 53 status: `qualified-visual-public-rc-blocker-refresh`.

- Rechecked onboarding PNG inventory: total remains `54`, with `16` agent customization, `10` terminal customization, `8` agent theme, and `8` terminal theme PNGs.
- Phase 45 asset policy still applies: `4` decorative/brand assets accepted, `50` screenshot/static-art assets remain `defer-to-design-regeneration`.
- No PNG was modified; visual residue remains bitmap content, not manifest/source drift.
- No GUI launch was attempted, and no account, billing quota, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- Public-RC blocker status is unchanged from Phase 46: `GUI-AUTH-01`, `GUI-SET-03`, `GUI-SET-04`, `GUI-SET-05`, `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-06`, `GUI-WS-07`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain `blocked-external-state`.
- No row was promoted to public-RC `verified`.

## 2026-06-02 P61 visual and public-RC preflight

Phase 61 status: `qualified-visual-public-rc-preflight`.

- Rechecked onboarding PNG inventory: total remains `54`, with `12` root-level onboarding PNGs, `16` `agent_intention` root PNGs, `10` `terminal_intention` root PNGs, `8` `agent_intention/theme` PNGs, and `8` `terminal_intention/theme` PNGs.
- Phase 45/53 asset policy still applies: `4` decorative/brand assets accepted, `50` screenshot/static-art assets remain `defer-to-design-regeneration`.
- Created `docs/zh-Hans-onboarding-visual-regeneration-plan.md` to define the reversible asset-only branch, before/after comparison, dimensions/filename checks, and design approval requirements.
- No PNG was modified; visual residue remains bitmap content, not manifest/source drift.
- No GUI launch was attempted, and no account, billing quota, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- Public-RC blocker status remains unchanged: `GUI-AUTH-01`, `GUI-SET-03`, `GUI-SET-04`, `GUI-SET-05`, `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-06`, `GUI-WS-07`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain `blocked-external-state`.
- No row was promoted to public-RC `verified`.

## 2026-06-02 P96 low-risk GUI smoke heat-safe defer

Phase 96 status: `qualified-with-heat-safety-gui-defer`.

- Reviewed the RC18 low-risk GUI smoke candidate list: `GUI-BASE-01`, `GUI-BASE-02`, `GUI-BASE-03`, `GUI-BASE-04`, `GUI-BASE-05`, `GUI-ONB-01`, `GUI-ONB-02`, `GUI-AUTH-03`, `GUI-SET-01`, `GUI-SET-02`, and `GUI-WS-08`.
- Did not launch GUI or build a bundle because the active goal requires avoiding local performance pressure after severe machine heating.
- Created `docs/gui-smoke-artifacts/phase96/README.md` as the Phase 96 artifact index.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- Public-RC blocker status is unchanged: `GUI-AUTH-01`, `GUI-SET-03`, `GUI-SET-04`, `GUI-SET-05`, `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-06`, `GUI-WS-07`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain blocked until isolated accounts, backend fixtures, or disposable objects exist.
- No row was promoted to current-cycle public-RC `verified`.

## 2026-06-02 P105 low-risk GUI smoke heat-safe defer

Phase 105 status: `qualified-with-heat-safety-gui-defer`.

- Reviewed the RC19 low-risk GUI smoke candidate list: `GUI-BASE-01`, `GUI-BASE-02`, `GUI-BASE-03`, `GUI-BASE-04`, `GUI-BASE-05`, `GUI-ONB-01`, `GUI-ONB-02`, `GUI-AUTH-03`, `GUI-SET-01`, `GUI-SET-02`, and `GUI-WS-08`.
- Did not build a bundle or launch GUI because the active goal requires avoiding local performance pressure after severe machine heating.
- Did not create a new ignored artifact directory because no screenshots or accessibility snapshots were captured.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- Public-RC blocker status is unchanged: `GUI-AUTH-01`, `GUI-SET-03`, `GUI-SET-04`, `GUI-SET-05`, `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-06`, `GUI-WS-07`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain blocked until isolated accounts, backend fixtures, or disposable objects exist.
- No row was promoted to current-cycle public-RC `verified`.

## 2026-06-02 P207 fresh bundle heat-safe defer

Phase 207 status: `qualified-with-heat-safety-bundle-defer`.

- Ran two lightweight load probes 60 seconds apart before attempting a fresh bundle.
- No `cargo`, `rustc`, `warp-oss`, `terminal-server`, `script/run`, or `WarpOss.app` workload was active other than the probe shell.
- System load stayed around `2.30` to `2.69`, while WindowServer, Codex helper processes, Finder, syspolicyd, and trustd showed notable CPU use.
- `pmset -g therm` reported no recorded thermal or performance warning, but the active CPU profile was not quiet enough for a conservative bundle retry.
- Did not run `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`.
- Did not launch `target/debug/bundle/osx/WarpOss.app`.
- No screenshot, accessibility snapshot, account state, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No row was promoted to current-cycle public-RC `verified`; GUI evidence remains dependent on a later quiet-window fresh bundle or an approved external prerequisite path.

## 2026-06-02 P208 no-account GUI smoke deferred

Phase 208 status: `qualified-gui-smoke-deferred-by-phase207`.

- Reviewed the no-account GUI smoke dependency after Phase 207.
- Did not run no-account GUI smoke because the current cycle did not produce a fresh bundle.
- Did not reuse historical screenshots or accessibility snapshots as current-cycle evidence.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No row was promoted to current-cycle public-RC `verified`.

## 2026-06-02 P209 public-RC prerequisite refresh

Phase 209 status: `qualified-public-rc-prerequisites-refreshed`.

- Re-ran `python3 script/zh_public_rc_status.py`.
- Registry total remains `11` public-RC blockers: `3` isolated account blockers, `5` backend fixture blockers, and `3` disposable object blockers.
- No isolated test account, backend fixture contract, safe billing/quota state, disposable AWS/Bedrock fixture, disposable cloud environment, disposable managed secret, disposable endpoint, or disposable owner test team was provided in this cycle.
- No registry row was downgraded or promoted.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- Public RC remains blocked.

## 2026-06-02 P210 onboarding PNG asset branch decision

Phase 210 status: `qualified-png-asset-branch-deferred`.

- Checked PNG dirtiness; `git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'` and `git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'` produced no output.
- Rechecked onboarding PNG inventory; total remains `54`.
- Existing asset policy still applies: `4` decorative/brand assets accepted, `50` screenshot/static-art assets remain deferred for design-approved regeneration.
- Did not create an asset-only branch because no design/product approval was provided for RC29.
- Did not modify, generate, stage, or commit any PNG.
- Visual residue status is unchanged and cannot be promoted by RC29.

## 2026-06-02 P213 heavy validation

Phase 213 status: `qualified-heavy-gate-deferred`.

- Captured two load probes 60 seconds apart before attempting RC30 heavy validation.
- No `cargo`, `rustc`, `warp-oss`, `terminal-server`, `script/run`, or `WarpOss.app` workload was active other than the probe shell.
- Probe 1 load was `3.44 3.63 3.21`; Probe 2 load was `2.31 3.23 3.09`.
- `pmset -g therm` reported no recorded thermal or performance warning, but WindowServer, Finder, trustd, and Codex helper processes showed sustained CPU pressure.
- Did not run `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`.
- Did not run `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`.
- Did not launch `target/debug/bundle/osx/WarpOss.app`.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was touched.

## 2026-06-02 P214 no-account GUI smoke deferred

Phase 214 status: `qualified-gui-smoke-deferred`.

- Checked the Phase 213 dependency and found `fresh bundle: not run`.
- Did not run no-account GUI smoke because the current cycle did not produce a fresh bundle.
- Did not reuse historical screenshots or accessibility snapshots as current-cycle evidence.
- No screenshot, accessibility snapshot, account state, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No row was promoted to current-cycle public-RC `verified`.

## 2026-06-02 P215 isolated account prerequisite gate

Phase 215 status: `qualified-isolated-account-blocked`.

- Re-ran `python3 script/zh_public_rc_status.py`.
- `GUI-AUTH-01`, `GUI-SET-03`, and `GUI-WS-06` remain `blocked-no-isolated-account`.
- No isolated test account was provided for RC30.
- Did not log in, start a browser callback, paste tokens, inspect Settings > AI with account state, create a disposable custom inference endpoint, or delete any endpoint.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No isolated-account row was promoted.

## 2026-06-02 P216 backend fixture prerequisite gate

Phase 216 status: `qualified-backend-fixture-blocked`.

- Re-ran `python3 script/zh_public_rc_status.py`.
- `GUI-SET-04`, `GUI-SET-05`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01` remain `blocked-no-backend-fixture`.
- No safe AWS/Bedrock, invalid credential, billing/quota, Build plan migration, or cloud capacity fixture was provided for RC30.
- Did not enter real provider credentials, attach payment state, consume quota, create cloud capacity state, or mutate backend test state.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No backend fixture row was promoted.

## 2026-06-02 P217 disposable object prerequisite gate

Phase 217 status: `qualified-disposable-object-blocked`.

- Re-ran `python3 script/zh_public_rc_status.py`.
- `GUI-SET-06`, `GUI-WS-04`, and `GUI-WS-07` remain `blocked-no-disposable-object`.
- No disposable environment named `zh-smoke-delete-environment`, disposable managed secret named `zh-smoke-delete-secret`, or disposable owner test team named `zh-smoke-public-rc-team` was provided or approved for RC30.
- Did not create, delete, cancel-delete, or transfer any environment, managed secret, endpoint, team, production object, or ownership state.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No disposable-object row was promoted.

## 2026-06-02 P218 onboarding PNG asset branch decision

Phase 218 status: `qualified-png-asset-branch-deferred`.

- Checked PNG dirtiness; `git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'` and `git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'` produced no output.
- Rechecked onboarding PNG inventory; total remains `54`.
- Existing asset policy still applies: `4` decorative/brand assets accepted, `50` screenshot/static-art assets remain deferred for design-approved regeneration.
- Did not create an asset-only branch because no design/product approval was provided for RC30.
- Did not modify, generate, stage, or commit any PNG.
- Visual residue status is unchanged and cannot be promoted by RC30.

## 2026-06-02 P223 heavy validation with helper

Phase 223 status: `qualified-heavy-gate-deferred`.

- The low-load helper decided whether Rust compile and bundle were safe.
- Helper output: Probe 1 load `2.75 2.82 2.90`, Probe 2 load `2.31 2.70 2.85`.
- Helper decision was `defer-heavy-gate` because both probes exceeded the `2.50` threshold.
- Did not run `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`.
- Did not run `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`.
- Did not launch `target/debug/bundle/osx/WarpOss.app`.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was touched.

## 2026-06-02 P224 current-cycle GUI smoke deferred

Phase 224 status: `qualified-gui-smoke-deferred`.

- Checked the Phase 223 dependency and found `fresh bundle: not run`.
- Did not run current-cycle GUI smoke because the current cycle did not produce a fresh bundle.
- Did not reuse historical screenshots or accessibility snapshots as current-cycle evidence.
- No screenshot, accessibility snapshot, account state, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No row was promoted to current-cycle public-RC `verified`.

## 2026-06-02 P225 public-RC action package

Phase 225 status: `qualified-public-rc-action-package`.

- Re-ran `python3 script/zh_public_rc_status.py`; public-RC blocker total remains `11`.
- Created `docs/zh-Hans-public-rc-action-package-rc31.md`.
- The action package groups required inputs into isolated account, backend fixture, disposable object, visual asset, and heavy validation categories.
- No registry row was changed or promoted.
- No account, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.

## 2026-06-02 P233 asset preflight

Phase 233 status: `qualified-asset-approval-preflight`.

- Checked PNG dirtiness; `git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'` and `git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'` produced no output.
- Onboarding PNG inventory remains `54` total, with `50` deferred screenshot/static-art assets and `4` accepted decorative/brand assets.
- No design/product approval was provided for an asset-only branch in this phase.
- Did not modify, generate, stage, or commit any PNG.
- Asset regeneration remains `blocked-no-asset-approval`.

## 2026-06-02 P234 heavy gate

Phase 234 status: `qualified-heavy-gate-decision`.

- Ran `python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25`.
- Helper output: Probe 1 load `3.75 3.54 3.02` with `WindowServer 44.7%`; Probe 2 load `4.99 3.88 3.17` with `mds_stores 124.0%` and `WindowServer 45.0%`.
- Helper decision was `defer-heavy-gate`.
- Did not run `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`.
- Did not run `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`.
- Did not launch `target/debug/bundle/osx/WarpOss.app`.
- GUI launch remains blocked because this phase did not produce a fresh bundle.

## 2026-06-02 P235 RC32 freeze

Phase 235 status: `qualified-rc32-freeze`.

- Final low-load validation kept manifest validation, glossary, dry-run, release coverage, public-RC status, privacy guard, Python tests, `cargo fmt --check`, and `git diff --check` clean.
- `script/zh_public_rc_evidence_lint.py` returned the expected blocker signal: `ready_rows: 0`, `errors: 11`, `decision: fail`, `exit_code: 1`.
- No current-cycle GUI smoke was run because Phase 234 did not produce a fresh bundle.
- No screenshot, accessibility snapshot, account state, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No row was promoted to current-cycle public-RC `verified`.

## 2026-06-02 P241 asset and GUI dependency recheck

Phase 241 status: `qualified-asset-gui-dependency-recheck`.

- PNG status remained clean.
- Asset regeneration remains blocked without an explicitly approved asset-only branch.
- Fresh bundle dependency remains `skipped-with-heat-safety`.
- GUI smoke remains blocked because no current-cycle fresh bundle exists.

## 2026-06-02 P242 heavy gate

Phase 242 status: `qualified-heavy-gate-decision`.

- Ran `python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25`.
- Helper output: Probe 1 load `2.20 2.56 2.69` with `WindowServer 42.5%` and `Codex (Service) 31.1%`; Probe 2 load `2.61 2.60 2.69` with `WindowServer 44.7%`.
- Helper decision was `defer-heavy-gate`.
- Did not run `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`.
- Did not run `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`.
- Did not launch `target/debug/bundle/osx/WarpOss.app`.
- GUI launch remains blocked because this phase did not produce a fresh bundle.

## 2026-06-02 P243 RC33 freeze

Phase 243 status: `qualified-rc33-freeze`.

- Final low-load validation kept manifest validation, glossary, dry-run, release coverage, public-RC status, public-RC evidence report, privacy guard, Python tests, `cargo fmt --check`, and `git diff --check` clean.
- `script/zh_public_rc_evidence_report.py` reported `ready_rows: 0` and `decision: blocked`.
- `script/zh_public_rc_evidence_lint.py --strict-artifacts` returned the expected blocker signal: `ready_rows: 0`, `errors: 11`, `decision: fail`, `exit_code: 1`.
- No current-cycle GUI smoke was run because Phase 242 did not produce a fresh bundle.
- No screenshot, accessibility snapshot, account state, backend fixture, billing/quota state, cloud object, managed secret, custom endpoint, production object, or team ownership state was read, created, modified, or deleted.
- No row was promoted to current-cycle public-RC `verified`.

## RC34 Pre-Heavy-Gate Refresh

```text
asset lane: blocked-no-asset-approval
PNG changes: none
fresh bundle: pending-low-load-gate
GUI launch: blocked-no-fresh-bundle
```

## RC35 Heavy Validation Retry

```text
fresh bundle: passed
GUI launch: pending-explicit-gui-smoke-approval
```

## RC34 Heavy Validation Retry

```text
fresh bundle: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```

## RC35 Lane And Asset Refresh

```text
asset lane: blocked-no-asset-approval
PNG changes: none
fresh bundle: pending-low-load-gate
GUI launch: blocked-no-fresh-bundle
```

## RC36 Filtered Evidence Packetization

```text
filtered action packets: available
backend_fixture rows: 5 missing
disposable_object rows: 3 missing
isolated_account rows: 3 missing
GUI launch: pending explicit GUI smoke approval
PNG assets: unchanged
```

## RC36 Heavy Validation Retry

```text
low-load gate: defer-heavy-gate
fresh bundle: skipped-with-heat-safety
GUI launch: pending explicit GUI smoke approval
```

## RC37 Evidence Queue Planning

```text
evidence queue: available
backend_fixture queue rows: 5
disposable_object queue rows: 3
isolated_account queue rows: 3
GUI launch: pending explicit GUI smoke approval
PNG assets: unchanged
```

## RC37 Heavy Validation Retry

```text
low-load gate: defer-heavy-gate
fresh bundle: skipped-with-heat-safety
GUI launch: pending explicit GUI smoke approval
```

## RC38 Evidence Candidate Preflight

RC38 adds `script/zh_public_rc_evidence_candidate.py` so redacted text
candidates can be machine-checked before any ledger update is proposed.

```text
candidate preflight: available
public-RC blockers: 11
ready evidence rows: 0
rows promoted in RC38: 0
GUI launch in RC38: not run unless separately approved
```

Candidate preflight does not collect evidence and does not replace GUI, account,
fixture, cleanup, or strict artifact-lint requirements.

## RC38 Heavy Validation Retry

```text
low-load gate: run-heavy-gate
cargo check -j 1 -p warp: passed with existing unused-variable warnings
script/run --dont-open: passed with existing unused-variable warnings
fresh bundle: refreshed
bundle path: target/debug/bundle/osx/WarpOss.app
GUI launch: not run
```

The heavy gate refreshed the local bundle under low-load conditions. It did not
open the app and does not provide current-cycle GUI, account, fixture, cleanup,
or public-RC evidence.
