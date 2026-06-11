# Warp CN zh-Hans Localization Functional Test Plan

Last updated: 2026-06-11

本方案用于系统排查 Warp CN 是否因为简体中文汉化而引入功能 bug。它不替代上游 Warp 的完整产品测试，而是专门验证：源码级汉化 overlay、术语选择、中文文本长度、占位符、命令/配置保留规则、GUI 可见文案和账号/云端状态文案，不会影响用户正常使用。

## 测试目标

1. 确认汉化不会改变功能行为、数据契约、命令语法、配置格式、搜索索引、账号状态、账单含义或安全提示。
2. 确认中文界面在核心工作流中可读、可点击、可搜索、可恢复，且不会因文本长度造成遮挡、截断、错位或不可操作。
3. 确认高风险功能在没有安全前置条件时保持阻断，不用真实主账号、真实账单、真实密钥或不可恢复对象冒险验证。
4. 为每次翻译更新、上游同步、发布候选和正式包提供可重复的分层测试门禁。

## 范围

必测范围：

- 启动、安装、更新、窗口、菜单、权限弹窗和退出。
- 首次启动、登录入口、浏览器回调、登录取消和登录失败。
- 终端输入、命令执行、block、复制粘贴、查找、历史、补全、快捷键、中文输入法组合输入。
- 标签页、窗格、窗口、新会话、session restore、launch config、tab config。
- 命令搜索、导航搜索、工作流搜索、历史搜索、中文查询和英文查询兼容。
- 设置页、主题、字体、键盘、隐私、AI、BYO API Key、AWS Bedrock、自定义推理 endpoint。
- Agent、web search、fetch、get-files、MCP、tool 状态、错误提示和停止/重试路径。
- Warp Drive、工作流、notebook、项目工作流、分享入口、终端分享。
- secret redaction、Keychain、managed secret、权限、隐私、安全模式。
- 账单、credit、quota、plan、team seat、Cloud、team ownership、删除/转让/撤销等高风险文案。
- packaging：debug bundle、release-lto bundle、DMG、ad-hoc 签名、版本元数据、首次打开。

不在本方案内直接改变的内容：

- 上游 Warp 本身已有的非汉化缺陷。
- 官方服务端可用性、计费真实扣费、生产团队权限变更。
- 没有隔离账号、后端 fixture、一次性对象时的 public-RC 升级结论。

## 汉化专属风险模型

| 风险 | 典型 bug | 必须验证 |
| --- | --- | --- |
| 占位符和格式损坏 | `{name}`、`%s`、markdown link、shortcut、URL 被改坏导致 panic 或错误显示 | 静态 manifest 校验、运行时触发对应文案 |
| 命令/配置被翻译 | shell 命令、CLI flag、TOML/YAML key、GraphQL/JSON field 被翻译导致执行失败 | risk register 审查、命令复制执行、配置加载 |
| 搜索索引失效 | action label 翻译后命令搜索找不到，或英文别名不可用 | 中文 query 和英文 query 双路径搜索 |
| 布局溢出 | 按钮、菜单、toast、modal、settings nav 因中文过长遮挡或无法点击 | GUI smoke、截图/可访问性锚点、窄窗口检查 |
| 语义误导 | 删除、转让、账单、权限、登录文案含义偏差导致用户误操作 | 高风险手工审查、cancel-first 验证、隔离对象 |
| 编码和字体问题 | 中文乱码、缺字、全角标点异常、复制粘贴丢字 | mojibake scan、GUI 可见锚点、终端输入输出 |
| 外部集成破坏 | provider/model/endpoint/API key 名称被改导致配置不可用 | provider ID 保留、mock/fixture、隔离账号 |
| 测试/日志误翻译 | fixture、snapshot、日志哨兵被翻译导致测试失效或诊断困难 | ignore 规则、cargo test、inventory 审查 |

判定原则：如果一个英文字符串参与行为、协议、存储、搜索 key、遥测、日志、测试 fixture 或外部系统契约，默认不翻译；只有确认它是用户可见展示文案时才翻译。

## 分层门禁

### L0 静态和脚本门禁

每次修改 manifest、术语表、忽略规则、汉化脚本或中文文档前后都运行：

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_mojibake_scan.py
python3 -m unittest discover -s script -p 'test_zh_*.py'
git diff --check
```

通过标准：

- manifest 结构有效，glossary 无禁用译法命中。
- dry-run 为 `would_change: 0`、`missing: 0`，或每一项 drift 都有解释。
- release preset 没有未审查的候选英文字符串。
- mojibake/layout scan 没有 actionable findings。
- Python 汉化工具单测通过。
- 没有提交隐私敏感产物或空白/换行问题。

### L1 Rust 编译和目标单测

每次上游同步、发布候选或涉及 Rust 字符串上下文的变更运行：

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
cargo fmt --check
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
cargo test -p warp settings
```

通过标准：

- 编译无新增错误。
- 搜索、设置、命令面板相关测试不因中文 label 或保留英文 key 改动失败。
- 如果测试失败，先判定是否由汉化破坏契约，再区分上游既有问题。

### L2 Warp 集成测试

使用 `crates/integration` 的 Builder/TestStep 框架，优先覆盖不依赖真实账号和后端的本地功能：

```bash
cargo run -p integration --bin integration -- test_single_command
cargo run -p integration --bin integration -- test_open_and_close_settings
cargo run -p integration --bin integration -- test_open_and_close_context_menu_with_keybinding
cargo run -p integration --bin integration -- test_command_search_loads_history
cargo run -p integration --bin integration -- test_loading_project_workflows
cargo run -p integration --bin integration -- test_secret_is_obfuscated_on_copy
cargo run -p integration --bin integration -- test_restore_snapshot_with_settings_page
```

推荐新增或补强的汉化专属集成测试：

| Test ID | 目标 | 自动断言 |
| --- | --- | --- |
| `test_zh_command_palette_chinese_labels` | 打开命令搜索，中文 label 可见且 action 可执行 | 搜索“设置”“新会话”等中文锚点后执行，窗口/状态变化正确 |
| `test_zh_command_palette_english_aliases` | 汉化后英文 action/query 仍可发现核心命令 | 搜索 `settings`、`new session` 等英文 query 不退化 |
| `test_zh_settings_core_pages_open` | 设置核心页中文导航不影响页面切换 | 外观、AI、键盘、隐私页可打开，当前 section 正确 |
| `test_zh_terminal_cjk_input_roundtrip` | 中文输入和命令输出不乱码 | 固定中文输出后 block 文本匹配 |
| `test_zh_copy_command_preserves_executable_tokens` | 带中文说明的可复制命令仍保留可执行 token | 复制命令中 flag、path、provider ID 未被翻译 |
| `test_zh_settings_error_banner` | settings.toml 错误提示中文显示但修复流程正常 | 错误 banner 出现、修复后消失 |
| `test_zh_secret_and_ai_redaction_copy` | secret 文案汉化不影响 redaction | secret 检测、tooltip、安全模式、AI 输入脱敏仍正确 |

集成测试要求：

- 新测试放在 `crates/integration/src/test/`，并注册到 `crates/integration/src/bin/integration.rs`。
- UI 行为测试加入 `crates/integration/tests/integration/ui_tests.rs`。
- shell 相关测试加入 `crates/integration/tests/integration/shell_integration_tests.rs`。
- 断言应检查行为和状态，不只检查中文文本存在。

### L3 GUI 冒烟和视觉验收

每次发布候选至少覆盖 `docs/zh-Hans-gui-smoke-matrix.md` 的个人使用版必测范围：

| Area | 操作 | 通过标准 |
| --- | --- | --- |
| App launch | 打开 debug 或 release bundle | 主窗口出现，菜单可见，无空白窗口，无启动崩溃 |
| Onboarding | 首启或隔离 profile 打开 onboarding | 中文锚点可读，按钮可点击，登录入口不误导 |
| Workspace shell | 新会话中输入普通命令和中文文本 | 命令执行、输入焦点、复制粘贴、block 显示正常 |
| Command search | 打开命令搜索，分别搜中文和英文 | 中文界面可搜索，英文核心 query 不失效 |
| Settings core | 打开设置并切换核心页 | 导航、标题、按钮不遮挡，设置值可保存 |
| AI settings | 打开 AI/BYO key/custom endpoint 区域 | provider/model/API key/endpoint 标识保留，说明文案清楚 |
| Dangerous cancel path | 只在有一次性对象时打开确认框并取消 | 删除/转让/撤销文案准确，取消不改变对象 |

证据规则：

- 优先记录 Computer Use/accessibility tree 可读到的中文锚点。
- 截图只作为辅助证据，必须裁剪和脱敏。
- 不提交原始全屏桌面截图、录屏、账号、邮箱、token、API key、本地路径或真实团队信息。
- fixture-only 证据只能标记为 `fixture-verified`，不能升级为 public-RC `verified`。

### L4 隔离账号、后端 fixture 和一次性对象门禁

以下功能只有满足安全前置条件才执行真实路径：

| 功能 | 前置条件 | 禁止事项 |
| --- | --- | --- |
| 登录和浏览器回调 | 隔离测试账号、可清理浏览器状态 | 不使用主账号 magic link 或真实私有会话 |
| Billing / quota / plan | 不扣费、不购买、不消耗真实额度的 fixture 或测试账号状态 | 不触发真实购买、升级、自动续费 |
| Cloud capacity | 可控 capacity/quota 后端状态 | 不制造真实容量压力 |
| Team ownership transfer | 精确命名的一次性 owner test team 和明确批准 | 不操作真实团队 |
| Managed secret | `zh-smoke-delete-secret` 一次性 secret | 不删除真实 secret |
| Environment deletion | `zh-smoke-delete-environment` 一次性 environment | 不删除真实环境 |
| Custom inference endpoint | custom inference enabled 隔离账号和 `zh-smoke-delete-endpoint` | 不删除真实 endpoint，不猜测凭据 |
| AWS Bedrock | disposable profile 或 invalid credential fixture | 不访问真实 AWS 凭据 |

没有前置条件时，测试结论必须是 `blocked-no-isolated-account`、`blocked-no-backend-fixture` 或 `blocked-no-disposable-object`，不能写成通过。

## 功能测试矩阵

| 功能域 | 汉化风险 | 自动化覆盖 | GUI/手工覆盖 | Release 必须结论 |
| --- | --- | --- | --- | --- |
| 启动和安装 | app 名称、版本、权限文案、bundle 资源缺失 | `cargo check -p warp`、`./script/run --dont-open`、packaging 脚本 | 打开 app、权限弹窗、菜单栏 | 可启动、可关闭、无空白主窗口 |
| Onboarding/Auth | 登录入口、取消、错误、回调文案误导 | manifest/glossary、登录相关单测 | 隔离 profile 首启；有账号时验证回调 | 无账号路径安全，账号路径需隔离证据 |
| Workspace terminal | 中文输入、prompt、block、复制命令、快捷键 | shell integration tests、secret tests、restore tests | 输入中文、执行命令、复制粘贴、查找 | 核心终端使用不退化 |
| Shell integration | bootstrap、history、completion、OSC、SSH 文案或脚本被翻译 | `shell_integration_tests.rs` 矩阵 | bash/zsh/fish/pwsh 代表性手工路径 | 可启动 shell，补全/历史/SSH 不因汉化破坏 |
| Command search | label 翻译影响 action lookup 或英文 query | command palette/search 测试、新增 zh/English alias 测试 | 搜中文和英文核心命令 | 搜索可用，动作可执行 |
| Settings | 导航过长、配置 key/provider ID 被翻译、保存失败 | settings、settings file、settings private/hot reload tests | 外观、AI、键盘、隐私、terminal 切换 | 设置可打开、可保存、无布局阻断 |
| AI/Agent | model/provider/tool 名被翻译，API key 误导，状态文案错误 | redaction tests、agent/tool 状态定向测试 | BYO key/custom endpoint/Agent 状态只用安全 fixture | 标识符保留，敏感输入不泄露 |
| Workflows/Drive/Notebooks | YAML key、workflow 命令、项目工作流路径被翻译 | workflow integration tests、restore tests | 创建/打开个人 workflow、项目 workflow | 工作流加载和执行不受影响 |
| Tabs/Panes/Windows | 菜单、drag、关闭确认文案影响操作 | UI integration tests、session restoration | 多 tab、多 pane、关闭、恢复 | 常用窗口管理正常 |
| Secrets/Privacy | secret 文案误导、安全模式失效、Keychain key 被翻译 | `test_secret_*`、privacy guard | secret tooltip、复制、AI 输入脱敏 | secret 不泄露，Keychain/storage key 不变 |
| Sharing/Cloud/Team | 真实外部状态、所有权、删除、分享文案高风险 | 仅 fixture/mock 或阻断状态检查 | 只用隔离账号和一次性对象 | 没有安全前置条件时保持 blocked |
| Billing/Quota | 费用、额度、计划、席位文案误导 | public-RC blocker/evidence scripts | 只用 billing fixture 或测试账号 | 不触发真实扣费，文案需 owner review |
| Errors/Offline/Recovery | 错误原因翻译不准确，重试/取消路径失效 | targeted unit/integration tests | 断网、无效配置、服务失败 fixture | 错误提示可理解，恢复动作有效 |
| Accessibility/Layout | 中文过长、焦点顺序、可访问文本缺失 | mojibake scan、截图/recording hooks | 窄窗口、高 DPI、键盘导航 | 无遮挡、无乱码、可访问锚点存在 |
| Packaging/Release | release bundle 资源、版本、签名、DMG 安装问题 | package script、checksum、privacy guard | 安装 DMG、首次打开、隔离标记处理 | release 包可安装和启动 |

## A/B 回归策略

发布候选时增加一次汉化版与英文基线的行为对照：

1. 选择同一 upstream base commit 或同一 tag。
2. 在英文基线和 Warp CN 汉化版上运行同一组非账号集成测试。
3. 对 GUI smoke 使用同一操作脚本，只比较行为、状态、可点击性和错误恢复，不要求文案相同。
4. 如果汉化版失败而英文基线通过，优先检查 manifest 条目、术语表、忽略规则、占位符和被翻译的内部 key。
5. 如果两边都失败，归为上游或环境问题，但仍记录是否有中文文案加重误导。

最低 A/B 样本：

- `test_single_command`
- `test_open_and_close_settings`
- `test_open_and_close_context_menu_with_keybinding`
- `test_command_search_loads_history`
- `test_secret_is_obfuscated_on_copy`
- GUI：启动、工作区输入、命令搜索、设置、AI 设置入口。

## 执行节奏

| 时机 | 必跑 | 可延期 |
| --- | --- | --- |
| 单个翻译条目修改 | L0、相关文件上下文 review | Rust 编译、GUI |
| 一个功能域汉化完成 | L0、相关 inventory preset、目标 Rust tests、目标 GUI smoke | 全量 integration |
| 上游同步后 | L0、manifest drift、inventory presets、L1、核心 L2 | L4 外部状态 |
| 发布候选 | L0、L1、核心 L2、L3、packaging smoke | L4 仅在前置条件满足时 |
| 公开 RC 或外部分享 | L0-L4 全部，证据包、隐私检查、blocked registry 更新 | 不允许跳过安全前置条件 |

## 缺陷分级

| 等级 | 定义 | 示例 | 发布决策 |
| --- | --- | --- | --- |
| P0 | 汉化导致崩溃、数据丢失、真实扣费、密钥泄露、删除/转让误操作 | 占位符 panic、删除按钮语义反转、API key 泄露 | 阻断发布 |
| P1 | 核心功能无法正常使用 | 命令搜索不可用、设置打不开、终端中文输入乱码 | 阻断发布候选 |
| P2 | 功能可用但明显误导或影响效率 | 文案含义偏差、按钮过长遮挡、英文 query 失效 | 发布前修复或明确记录 |
| P3 | 低频文案、轻微排版或有意保留英文解释不足 | tooltip 略长、非核心页面残留英文 | 可延期 |
| Blocked | 缺少隔离账号、fixture 或一次性对象，无法安全验证 | billing、team transfer、cloud quota | 不算通过，保留 blocker |

## 证据记录模板

每轮测试记录建议使用以下结构：

```markdown
# zh-Hans Functional Test Run - <date>

Branch:
Commit:
Build:
Tester:
Scope:

## Gates

| Gate | Command | Result | Notes |
| --- | --- | --- | --- |
| L0 manifest | `python3 script/zh_apply_localization.py --validate-manifest` | pass/fail | |
| L1 check | `cargo check -p warp` | pass/fail/deferred | |
| L2 integration | `<test names>` | pass/fail/deferred | |
| L3 GUI | `<matrix rows>` | verified/blocked | |

## Findings

| ID | Severity | Area | Symptom | Evidence | Owner decision |
| --- | --- | --- | --- | --- | --- |

## Blocked Rows

| Row | Reason | Required prerequisite |
| --- | --- | --- |

## Release Decision

accepted / accepted-with-known-blockers / blocked
```

## 完成标准

个人使用版可以接受的完成标准：

- L0 全部通过。
- L1 至少 `cargo check -p warp` 通过，或因机器负载明确延期并保留记录。
- 核心 L2 集成测试通过，或每个失败项证明不是汉化导致。
- L3 覆盖启动、工作区、命令搜索、设置和 AI 设置入口。
- P0/P1 为 0；P2 有修复计划或明确接受说明。
- L4 高风险外部状态如果没有安全前置条件，必须保留 blocker，不得冒险验证。

公开 RC 或外部发布需要更高标准：

- L0-L3 全部通过且有当前周期证据。
- L4 所有 blocker 用隔离账号、后端 fixture 或一次性对象关闭。
- 证据遵守 `docs/zh-Hans-evidence-policy.md`，不提交原始敏感截图/录屏。
- `resources/localization/zh-Hans-public-rc-blockers.toml` 和 `resources/localization/zh-Hans-public-rc-evidence.toml` 与实际状态一致。
