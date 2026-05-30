# Warp CN

Warp CN 是基于 [Warp](https://github.com/warpdotdev/warp) 开源客户端的简体中文本地化分支，目标是在 Warp 官方尚未提供完整应用语言切换和本地化框架之前，为中文用户提供一个可构建、可维护、可继续跟进上游的汉化版本。

> [!IMPORTANT]
> 本仓库不是 Warp 官方发行版，也不代表 Warp 官方中文版本。它是面向中文用户的社区本地化 fork。上游功能、协议、云服务、账号体系和许可证仍以 Warp 官方项目为准。

## 项目目标

本项目的核心目标不是做一次性的源码替换，而是建立一套可以长期维护的汉化流程：

- 覆盖高频、可见、影响使用体验的英文界面。
- 保持与上游 Warp 开源仓库同步的能力。
- 用清单化方式管理翻译，避免散落修改导致后续难以维护。
- 通过脚本验证上游字符串漂移，减少升级后翻译失效。
- 保留完整构建、审计、冒烟测试记录，方便后续迭代。

当前汉化主要覆盖 macOS 开源客户端中的高可见 UI。部分内部日志、协议字段、测试文本、调试信息和低频路径不会优先翻译。

## 当前状态

最近一次 release audit：`2026-05-30`

| 项目 | 状态 |
| --- | --- |
| 翻译清单条目 | `2556` |
| 已纳入清单的源码文件 | `186` |
| dry-run 校验 | `missing: 0` |
| 主要构建包 | `warp` |
| 可运行 bundle | `target/debug/bundle/osx/WarpOss.app` |
| 主要维护文档 | [`docs/zh-Hans-localization.md`](docs/zh-Hans-localization.md) |

覆盖率快照：

| 预设 | 已覆盖 | 候选 | 覆盖率 |
| --- | ---: | ---: | ---: |
| `onboarding` | 266 | 55 | 82.9% |
| `workspace` | 584 | 391 | 59.9% |
| `search` | 267 | 26 | 91.1% |
| `settings` | 1172 | 856 | 57.8% |
| `modals` | 635 | 5371 | 10.6% |
| `release` | 2802 | 6678 | 29.6% |

这些数字来自仓库内的本地化 inventory 脚本。覆盖率不是“整仓中文化百分比”，而是对选定高可见源代码区域中“可能用户可见字符串”的粗略审计指标。

## 已汉化范围

第一阶段已完成 M0-M8 里程碑。第二阶段第一轮深度覆盖、Round 2、Round 3 和 Round 4 切片也已完成，重点把审计口径降噪，并补齐 HOA onboarding、AI 设置深层路径、BYO API keys、AWS Bedrock、终端 rewind、auth-secret 删除确认、Appearance 命令面板开关、会话列表操作、云端 Agent 容量弹窗、AWS 凭据错误、环境删除确认、launch modals、额度/方案弹窗、Agent tips、conversation details panel、CLI 管理员权限提示、破坏性确认文案、Warp on Web home、Agent 状态/错误残留和环境弹窗 fallback 文案。

当前重点覆盖以下路径：

- 首次启动和 onboarding 流程。
- 登录、AI 启用/禁用、匿名使用提示。
- 工作区 shell、左侧标签页、菜单栏和常见工作区入口。
- 命令面板、命令搜索、斜杠命令和搜索筛选标签。
- 设置页核心区域和高级设置区域。
- 主题、标签页配置、Warp Drive、共享会话等常见模态框。
- Agent 管理、Agent 输入面板、常见 toast 和确认弹窗。
- 部分终端共享、会话、工作流、Notebook、环境变量相关文本。
- HOA onboarding、垂直标签页介绍、Agent inbox 介绍和 tab config 引导。
- AI 设置中的 Build 方案提示、自带 API keys、AWS Bedrock 凭据和登录命令设置。
- 终端 rewind 搜索提示和 auth-secret 删除确认说明。
- Appearance 命令面板动作标签、会话列表菜单/删除 toast、云端 Agent 容量与点数提示、AWS 凭据错误和环境删除确认框。
- Oz / OpenWarp / orchestration launch modals、额度耗尽和 Build 方案迁移弹窗。
- Agent tips、conversation details panel、CLI 安装/卸载管理员权限提示、移除 endpoint 和转让团队所有权确认框。
- Warp on Web home、Agent conversation 状态标签、AWS Bedrock 凭据错误、web search/fetch 失败提示和 Agent Assisted Environment fallback 文案。

历史 GUI 冒烟测试已确认：

- 终端-only 路径可以进入中文工作区。
- 菜单栏显示中文：`文件`、`编辑`、`视图`、`标签页`、`块`、`窗口`、`帮助` 等。
- 全局搜索占位符显示中文。
- 命令面板占位符和筛选标签显示中文，例如 `文件`、`操作`、`会话`、`启动配置`。

第二阶段本机自动 GUI 冒烟已多次尝试。2026-05-30 的 `WarpOss` bundle 构建、签名和进程启动通过；Round 4 使用 `open -n target/debug/bundle/osx/WarpOss.app` 可启动主进程和 `terminal-server`，Computer Use 已能读取窗口状态，并确认菜单栏、搜索占位符和“新会话”等基础工作区入口显示中文。HOA onboarding、AI 设置、Appearance、会话菜单、云端 Agent 容量弹窗、launch modals、额度/方案弹窗、Agent tips、conversation details、CLI 权限提示、Warp on Web home、Agent 状态标签、环境 fallback、rewind、auth-secret 和环境删除确认框仍需要在可触发对应状态的交互式桌面会话中复验。

## 仍未完整覆盖的范围

当前版本仍有以下限制：

- 没有运行时语言切换开关。汉化是源码级替换，构建出的应用默认显示简体中文。
- 登录、账号、云端额度、团队计费等路径需要真实账号和服务状态，部分仍是人工 release gate。
- `modals` 预设覆盖率偏低；Round 4 审计后确认它仍主要由 Agent/terminal 内部模板、终端协议、诊断和低频路径主导。
- 一些英文词保留原文，例如 `Warp`、`Agent`、`Notebook`、`MCP`、`GitHub`、`CLI` 等产品或技术名词。
- 部分命令语法保持英文，例如 `history:`、`files:`、`workflows:`，这是为了不破坏用户输入和过滤器解析逻辑。
- 部分动态或搜索相关字符串继续保留，例如 `${price}/month`、`2x`、`5x`、主题名、设置搜索关键词，以及会影响搜索 tag 的 Appearance 英文关键词。
- 仓库中的内部日志、测试用例、序列化字段、遥测事件名通常不作为 UI 汉化目标。

## 汉化实现方式

Warp 当前大量 UI 文案仍是 Rust 源码中的内联字符串。为了降低维护成本，本项目没有直接手工散改所有源码，而是使用“翻译清单 + 应用脚本”的方式。

核心文件：

| 文件 | 用途 |
| --- | --- |
| [`resources/localization/zh-Hans-overrides.toml`](resources/localization/zh-Hans-overrides.toml) | 翻译清单，每条记录指定文件、源字符串和目标中文 |
| [`script/zh_apply_localization.py`](script/zh_apply_localization.py) | 将清单中的翻译应用到 Rust 字符串字面量 |
| [`script/zh_localization_inventory.py`](script/zh_localization_inventory.py) | 扫描可能仍需汉化的候选字符串，并生成覆盖率 |
| [`docs/zh-Hans-localization.md`](docs/zh-Hans-localization.md) | 详细维护记录、验证命令、已知失败和 release gate |

翻译应用脚本具备幂等性：

- 如果源码中仍是英文源字符串，脚本会替换成中文。
- 如果源码中已经是中文目标字符串，脚本会视为已应用。
- 如果源字符串和目标字符串都找不到，脚本会报错，提示上游源码发生漂移。

这种方式适合长期维护本地 fork：同步上游后先跑 dry-run，就能知道哪些翻译需要更新。

## 快速开始

### 克隆仓库

本仓库包含 Git LFS 文件。首次克隆后建议确认 LFS 对象已拉取：

```bash
git clone https://github.com/Drew1811266/Warp-CN.git
cd Warp-CN
git lfs install
git lfs pull
```

如果已经克隆但构建时发现模型或二进制资源缺失，可以重新拉取：

```bash
git lfs fetch --all
git lfs checkout
```

### 应用或校验汉化

通常仓库中的源码已经处于汉化后的状态。同步上游或修改翻译前，可以先做 dry-run：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
```

期望输出类似：

```text
entries: 2556
files: 186
already_applied: 2541
would_change: 0
missing: 0
```

如果需要重新应用翻译：

```bash
python3 script/zh_apply_localization.py
cargo fmt
```

### 构建并运行

Warp 的官方本地构建入口仍然适用：

```bash
./script/bootstrap --skip-common-skills
./script/run
```

用于非交互式构建 bundle 的命令：

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

成功后会生成：

```text
target/debug/bundle/osx/WarpOss.app
```

可以直接启动：

```bash
open -n target/debug/bundle/osx/WarpOss.app
```

> [!NOTE]
> 当前 app crate 的 package 名称是 `warp`，不是 `app`。因此请使用 `cargo check -p warp`。旧计划中的 `cargo check -p app` 会失败。

## 本地验证清单

推荐在发布或同步上游后运行：

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
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

人工冒烟建议覆盖：

- 首次启动 Agent 路径。
- 首次启动 terminal-only 路径。
- 登录、浏览器授权、token fallback、隐私设置。
- 工作区菜单、左右面板、垂直标签页。
- 命令面板、命令搜索、斜杠命令。
- 设置页：Account、Appearance、Features、Privacy、AI、Code、MCP、Billing、Environments。
- 常见 toast、 destructive dialog、主题弹窗、标签页配置弹窗、终端共享弹窗。

## 如何继续汉化

### 1. 找出候选英文字符串

按区域生成 inventory：

```bash
python3 script/zh_localization_inventory.py --preset onboarding > /tmp/zh-onboarding.md
python3 script/zh_localization_inventory.py --preset workspace > /tmp/zh-workspace.md
python3 script/zh_localization_inventory.py --preset search > /tmp/zh-search.md
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
python3 script/zh_localization_inventory.py --preset modals > /tmp/zh-modals.md
```

Round 4 之后也可以先看候选热点或只看候选行：

```bash
python3 script/zh_localization_inventory.py --preset workspace --status candidate
python3 script/zh_localization_inventory.py --preset settings --status covered-target
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

只优先处理 `candidate` 行。`covered-source` 和 `covered-target` 表示清单中已有对应记录。

### 2. 添加翻译条目

在 `resources/localization/zh-Hans-overrides.toml` 中增加条目：

```toml
[[replace]]
path = "app/src/example.rs"
source = "English text"
target = "中文文本"
```

注意：

- `path` 必须是仓库根目录下的相对路径。
- `source` 必须精确匹配 Rust 双引号字符串字面量。
- 不要翻译内部协议字段、遥测事件名、配置 key、命令过滤语法，除非确认它们是 UI 文案。

### 3. 应用并验证

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
git diff --check
cargo check -p warp
```

如果改动在搜索、onboarding、settings 等具体模块，还应运行对应测试或至少运行相关 package 的 `cargo check`。

## 同步上游流程

本项目保留上游远程：

```bash
origin  https://github.com/warpdotdev/warp.git
github  https://github.com/Drew1811266/Warp-CN.git
```

推荐同步流程：

```bash
git switch drew/zh-Hans-localization
git fetch origin
git merge origin/master
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
cargo check -p warp
```

如果上游变更导致 dry-run 出现 `missing`，说明某些英文源字符串已经被上游修改或移动。处理方式：

1. 打开报错指向的源码文件。
2. 找到新的英文文案或新的文件路径。
3. 更新 `zh-Hans-overrides.toml` 中对应 `source` 或 `path`。
4. 重新运行 dry-run。

## 翻译风格约定

为了保持界面一致，本项目采用以下约定：

- 面向用户的提示使用自然、简洁的中文。
- 产品名和专有名词尽量保留：`Warp`、`Warp Drive`、`Agent`、`Notebook`、`MCP`、`CLI`。
- 操作按钮尽量使用短词：`继续`、`取消`、`保存`、`共享`、`删除`。
- 命令、快捷键、路径、环境变量、配置文件名保留原样。
- 句末标点尽量与上下文一致，长说明使用中文全角标点。
- 不为了覆盖率翻译内部实现字符串。

## 里程碑回顾

第一阶段 M0-M8 已完成：

| 里程碑 | 内容 |
| --- | --- |
| M0 | 建立汉化基线、文档和验证口径 |
| M1 | 加固翻译应用脚本 |
| M2 | 增加 inventory 和覆盖率工具 |
| M3 | 汉化 onboarding、认证、工作区和搜索入口 |
| M4 | 扩展设置核心页 |
| M5 | 扩展高级设置页 |
| M6 | 扩展 modal、toast、Agent 相关界面 |
| M7 | 扩展主题、标签页配置、Drive、共享会话、slash commands |
| M8 | 完成 release checklist、bundle 验证、GUI 冒烟和命令面板筛选标签修复 |

第二阶段第一轮已完成：

| 任务 | 内容 |
| --- | --- |
| P2-M0 | 编写第二阶段任务规划和详细实施计划 |
| P2-M1 | 降噪 inventory 统计口径，过滤 telemetry、快捷键、搜索 tag、占位符和内部 id |
| P2-M2 | 汉化 HOA onboarding、垂直标签页、Agent inbox 和 tab config 引导 |
| P2-M3 | 汉化 AI 设置深层路径、BYO API keys 和 AWS Bedrock 凭据设置 |
| P2-M4 | 审查 Appearance 候选；剩余项主要是搜索 tag、主题名和占位符，暂不替换 |
| P2-M5 | 汉化终端 rewind 搜索提示和 auth-secret 删除确认框 |
| P2-M6 | 完成命令行 release audit，GUI 自动 smoke 记录为 manual gate |

第二阶段 Round 2 已完成：

| 任务 | 内容 |
| --- | --- |
| Round 2 计划 | `05b719f4 docs: plan phase 2 round 2 zh-Hans localization` |
| Appearance 命令动作 | `81672827 feat: localize appearance command actions` |
| 会话列表操作 | `25d71e8c feat: localize conversation actions` |
| 云端 Agent 容量弹窗 | `4c31e506 feat: localize cloud agent capacity modal` |
| AWS 凭据与环境删除确认 | `43613337 feat: localize credential and environment dialogs` |

第二阶段 Round 3 已完成：

| 任务 | 内容 |
| --- | --- |
| Round 3 计划 | `9fa400ff docs: plan phase 2 round 3 zh-Hans localization` |
| Launch modals | `524db95b feat: localize launch modals` |
| 额度和方案弹窗 | `9511f730 feat: localize credit and plan modals` |
| Agent tips | `d3e7a2c6 feat: localize agent tips` |
| Conversation details panel | `c551a024 feat: localize conversation details panel` |
| CLI 和确认提示 | `b046da1f feat: localize cli and confirmation prompts` |

详细执行记录见 [`docs/zh-Hans-localization.md`](docs/zh-Hans-localization.md) 和 [`docs/zh-Hans-localization-phase2.md`](docs/zh-Hans-localization-phase2.md)。

## 常见问题

### 这是完整汉化版吗？

不是。它是高可见路径优先的简体中文本地化分支。当前已经能覆盖首次启动、工作区、搜索、设置、常见弹窗和部分 Agent 工作流，但仍存在低频英文路径。

### 为什么不是运行时语言包？

因为上游 Warp 当前没有完整的一方应用语言设置或成熟 UI localization framework。本项目采用源码字符串替换作为本地 fork 的可维护方案。

### 为什么有些英文保留？

有些英文是产品名、命令语法、配置 key、协议字段或内部标识符。翻译这些字符串可能破坏功能或造成使用混乱。

### 可以直接安装使用吗？

本仓库目前主要提供源码和本地构建流程。构建成功后可以运行 `target/debug/bundle/osx/WarpOss.app`。如果后续发布签名好的安装包，应在 release 页面另行说明。

### 为什么 `./script/run --dont-open` 需要设置 `TERM=xterm-256color`？

当前环境下，不设置该变量时 `cargo-bundle` 可能在输出彩色状态时触发 `ColorOutOfRange` panic。使用下面命令可以规避：

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

## 上游项目

Warp 是一个从终端发展而来的 agentic development environment。你可以在这些链接了解官方项目：

- 官方网站：[warp.dev](https://www.warp.dev)
- 上游仓库：[warpdotdev/warp](https://github.com/warpdotdev/warp)
- 官方文档：[docs.warp.dev](https://docs.warp.dev)

## 许可证

本仓库基于 Warp 开源客户端。

- `warpui_core` 和 `warpui` crates 使用 [`LICENSE-MIT`](LICENSE-MIT)。
- 其余代码使用 [`LICENSE-AGPL`](LICENSE-AGPL)。

本地化翻译和维护脚本随本 fork 一并发布，但不改变上游项目原有许可证要求。使用、分发或二次修改前，请阅读仓库中的许可证文件。
