# Warp CN 第二阶段汉化开发任务规划

## 1. 阶段定位

第一阶段已经完成高可见路径汉化，当前版本不再是“初始尝试”。第二阶段的目标是把项目从“可用的高可见汉化版”推进到“更接近可发布、可维护、可持续同步上游的中文本地化版本”。

第二阶段不追求一次性全仓翻译。原因是 Warp 仓库中存在大量非 UI 字符串：

- 日志、遥测、调试命令、测试辅助文本。
- 内部协议字段、settings key、command id、binding id。
- 用户输入语法、过滤器 token、文件路径、URL、模型名。
- 示例代码、终端输出、错误栈和低频开发者诊断文本。

这些字符串进入覆盖率分母后会拉低 `modals` 和 `release` 覆盖率，但它们不等同于真实用户界面未汉化。因此第二阶段采用“真实用户路径优先 + 工具降噪 + 可验证交付”的策略。

## 2. 当前数据基线

最近一次统计时间：2026-05-29。

| 预设 | 已覆盖 | 候选 | 覆盖率 | 第二阶段解读 |
| --- | ---: | ---: | ---: | --- |
| `onboarding` | 266 | 92 | 74.3% | 主流程已可用，剩余主要是 telemetry、示例输入、主题名和少量 callout 文案 |
| `workspace` | 451 | 529 | 46.0% | 混有大量 debug/log/drag 内部文本，真实用户路径集中在 HOA onboarding、tab config、user menu、工具面板 |
| `search` | 267 | 63 | 80.9% | 已较高，剩余多为内部 id、错误诊断、命令语法和少量示例 |
| `settings` | 1126 | 946 | 54.3% | 需要继续补 AI、BYO API keys、AWS Bedrock、Appearance、Billing/MCP 深层路径 |
| `modals` | 560 | 6278 | 8.2% | 分母包含大量 AI/terminal/cloud 内部错误和诊断，必须先降噪再分批处理 |
| `release` | 2548 | 7882 | 24.4% | 聚合预设，只能作为趋势指标，不能直接代表用户可见汉化比例 |

## 3. 第二阶段目标

第二阶段完成后，应满足以下标准：

1. README 和维护文档清楚说明项目处于“第二阶段深度覆盖与发布质量打磨”。
2. inventory 脚本能更好地区分用户可见文案和内部噪声。
3. 工作区新功能 onboarding、tab config 引导、Agent inbox 介绍等真实用户路径完成汉化。
4. 设置页深层路径继续补齐，尤其是 AI、API keys、AWS Bedrock、Appearance 中用户会看到的标题、按钮和说明。
5. 常见弹窗、toast、错误提示进入第二轮清理，优先处理确认框、账号/云端/权限相关提示。
6. 建立第二阶段 GUI 冒烟矩阵，后续每轮能按页面和路径验证，而不是只依赖覆盖率数字。
7. 每个里程碑都必须有明确的验收命令和人工审查结论，通过后才进入下一个里程碑。

## 4. 非目标

第二阶段明确不做：

- 不引入运行时语言切换。
- 不重构 Warp 的 UI 本地化架构。
- 不翻译命令过滤语法，例如 `history:`、`files:`、`launch_configs:`。
- 不翻译 telemetry event、settings key、搜索索引内部 tag、debug 菜单内部 id。
- 不追求 `release` 覆盖率在第二阶段达到很高百分比。
- 不为了覆盖率翻译日志、错误栈、测试文本或开发者诊断字符串。

## 5. 术语策略

第二阶段需要进一步固定术语，避免不同页面出现同义不同译。

| English | zh-Hans | 备注 |
| --- | --- | --- |
| Agent | Agent | 产品核心词，保留英文 |
| Warp Agent | Warp Agent | 保留品牌词 |
| Agent inbox | Agent 收件箱 | 用户可见功能名 |
| Tab config | 标签页配置 | 已在第一阶段使用 |
| Vertical tabs | 垂直标签页 | 已在 UI 中使用 |
| Launch configuration | 启动配置 | 命令面板筛选标签已使用 |
| Workflow | 工作流 | Drive/command search 统一 |
| Notebook | Notebook | 产品对象名，保留英文更清晰 |
| Prompt | 提示词 | AI 输入内容 |
| Environment Variables | 环境变量 | 设置和 Drive 对象 |
| API keys | API keys | 技术名词保留 key |
| AWS Bedrock credentials | AWS Bedrock 凭据 | 品牌保留，credentials 译为凭据 |
| Build plan | Build 方案 | Warp 计划名保留 Build |
| Billing and usage | 账单与用量 | 已使用 |
| destructive dialog | 破坏性确认框 | 文档术语，不一定出现在 UI |

## 6. 里程碑拆分

### P2-M0：第二阶段文档与任务边界

目标：

- 写清楚第二阶段为何不是“初期继续汉化”，而是“深度覆盖与发布质量打磨”。
- 明确用户可见路径、工具降噪和发布验证的优先级。

交付：

- `docs/zh-Hans-localization-phase2.md`
- `docs/superpowers/plans/2026-05-29-zh-Hans-phase2-implementation.md`

验收：

- 文档解释清楚当前覆盖率低的原因。
- 每个后续里程碑都有输入、输出和验证方式。

### P2-M1：inventory 降噪和审计口径升级

目标：

- 减少 telemetry、debug、keybinding、纯占位符、内部 id、搜索 tag 对候选池的污染。
- 让覆盖率更接近真实 UI 状态。

候选改动：

- `script/zh_localization_inventory.py`
- `docs/zh-Hans-localization.md`

预期效果：

- `onboarding` 候选中 telemetry 噪声明显减少。
- `workspace` 候选中 tab drag/debug/log 噪声明显减少。
- `settings` 候选中纯搜索 tag、纯示例 token、纯占位符不再误导优先级。

验收：

- `python3 script/zh_localization_inventory.py --preset release --coverage` 可运行。
- 输出数字变化有解释记录。
- 不隐藏明确用户可见的按钮、标题、说明、toast、dialog 文案。

执行记录：

| 预设 | 降噪前候选 | 降噪后候选 | 降噪后覆盖率 |
| --- | ---: | ---: | ---: |
| `onboarding` | 92 | 55 | 82.9% |
| `workspace` | 529 | 519 | 46.5% |
| `settings` | 946 | 903 | 55.5% |
| `release` | 7882 | 7374 | 25.7% |

这次降噪主要移除了 telemetry 文件、快捷键、过滤 token、纯占位符、内部 id 和 settings search tag。`workspace` 候选下降不大，说明其剩余候选仍需要按 HOA onboarding、工具面板和真实用户路径继续处理。

### P2-M2：工作区新功能引导与 HOA onboarding

目标：

- 补齐工作区内用户会实际看到的新功能介绍路径。
- 优先处理 `app/src/workspace/hoa_onboarding/**`。

重点文件：

- `app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs`
- `app/src/workspace/hoa_onboarding/tab_config_step.rs`
- `app/src/workspace/hoa_onboarding/welcome_banner.rs`

重点文案：

- `See what's new`
- `Finish`
- `Switch back to horizontal tabs`
- `Introducing vertical tabs - the new default`
- `Meet your new agent inbox`
- `Create your first tab config`
- `Vertical tabs`
- `Tab configs`
- `Agent inbox`
- `Native code review`
- `Introducing universal agent support: level up any coding agent with Warp`

验收：

- `workspace` 覆盖率提升或候选数量下降。
- `cargo check -p warp` 通过。
- GUI 或代码审查确认 HOA onboarding 文案没有明显英文残留。

### P2-M3：AI 设置深层路径、BYO API keys、AWS Bedrock

目标：

- 补齐 AI 设置页中用户可见的二级路径。
- 重点处理 API keys、Build plan 升级提示、AWS Bedrock 凭据设置。

重点文件：

- `app/src/settings_view/ai_page.rs`

重点文案：

- `Upgrade to the Build plan`
- `Create an account`
- `Ask your team's admin to upgrade to the Build plan to use your own API keys.`
- `Use AWS Bedrock credentials`
- `Login Command`
- `AWS Profile`
- `Automatically run login command`
- `When enabled, the login command will run automatically when AWS Bedrock credentials expire.`
- `Refresh`

验收：

- `settings` 覆盖率提升或候选数量下降。
- `cargo check -p warp` 通过。
- API key 示例值如 `sk-...` 不被翻译。
- AWS 命令如 `aws login` 不被翻译。

### P2-M4：Appearance/设置页剩余高可见控件清理

目标：

- 处理 Appearance 里用户可见且未覆盖的控件标题和说明。
- 保留主题名、数值占位符和内部搜索 tag。

重点文件：

- `app/src/settings_view/appearance_page.rs`
- 必要时补充 `app/src/settings_view/about_page.rs`

重点原则：

- `compact mode`、`cursor blink`、`block dividers` 等如果是设置搜索 tag 或内部匹配词，不直接翻译。
- 真正显示在 UI 的 label/description 才进入 manifest。
- `Aurora`、`Classic 1`、`Glow` 等主题名保持原文。

验收：

- `settings` inventory 中高可见 Appearance 英文减少。
- `cargo check -p warp` 通过。
- 不破坏设置搜索匹配。

### P2-M5：账号、云端、权限、toast 和常见确认框第二轮清理

目标：

- 处理用户遇到故障或权限操作时会看到的英文。
- 优先处理账号、云同步、CLI 安装、共享、删除、权限相关提示。

候选区域：

- `app/src/auth/**`
- `app/src/workspace/cli_install.rs`
- `app/src/workspace/close_session_confirmation_dialog.rs`
- `app/src/workspace/rewind_confirmation_dialog.rs`
- `app/src/drive/**`
- `app/src/terminal/**` 中明确用户可见的 modal/toast

验收：

- `onboarding`、`workspace`、`modals` 的真实用户可见候选减少。
- `cargo check -p warp` 通过。
- 对登录/account 路径未能自动验证的项目写入 manual smoke gate。

### P2-M6：第二阶段发布审计与 GUI 冒烟矩阵

目标：

- 更新 release checklist。
- 固化第二阶段覆盖率快照。
- 记录可自动验证和必须人工验证的边界。

交付：

- 更新 `docs/zh-Hans-localization.md`
- 如有必要更新 `README.md`

验收命令：

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

GUI 冒烟：

- 启动 `target/debug/bundle/osx/WarpOss.app`。
- 检查工作区中文入口。
- 打开命令面板。
- 打开设置页的 Appearance、AI、MCP/API keys/AWS Bedrock 相关区域。
- 检查 HOA onboarding 或对应新功能入口，如无法触发则记录为人工 gate。

## 7. 风险与缓解

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 覆盖率误导优先级 | 时间浪费在内部字符串上 | P2-M1 先降噪，再按真实路径翻译 |
| 翻译破坏命令语法 | 搜索/filter/input 行为异常 | 保留过滤 token、命令、key、URL、路径 |
| 设置页搜索 tag 被替换 | 搜索体验退化 | 搜索 tag 默认保留英文，必要时追加中文而不是替换 |
| 模态框范围太大 | 单批 diff 不可审查 | P2-M5 只处理账号、云端、权限、常见确认框 |
| GUI 路径需要账号 | 自动化无法覆盖 | 文档中记录 manual gate，不声称已完全验证 |

## 8. 合理性复盘

### 8.1 是否解决用户提出的问题？

是。用户关心 README 中低覆盖率是否意味着还处于初期。该规划明确回答：当前是第一阶段可用版，第二阶段聚焦深度覆盖和发布质量，不是从零开始。

### 8.2 是否避免盲目追覆盖率？

是。规划把 P2-M1 设为工具降噪，先改善统计口径，再处理用户路径。`modals` 和 `release` 覆盖率不会作为唯一目标。

### 8.3 是否每个里程碑都可验收？

是。每个里程碑都有文件范围、目标、验收命令或人工 gate。P2-M6 还提供完整 release checklist。

### 8.4 是否存在过大任务？

P2-M5 风险最大，因为 `modals` 范围极宽。规划已经将其收窄为账号、云端、权限、常见确认框，不覆盖所有 `terminal`/`ai` 深层路径。

### 8.5 是否适合 Codex goal 连续执行？

适合。P2-M0 到 P2-M6 是顺序依赖：先文档，再工具降噪，再按路径扩展翻译，最后发布审计。每个里程碑完成后可以用覆盖率、dry-run、compile/test 和 GUI 检查判断是否进入下一步。

## 9. 结论

第二阶段规划合理，可以进入详细实施计划编写。

执行时应坚持三条规则：

1. 每个里程碑必须先验证再宣布完成。
2. 不翻译会影响功能的内部 token 或配置 key。
3. 如果发现某个路径无法自动验证，必须记录为 manual gate，而不是假定已覆盖。
