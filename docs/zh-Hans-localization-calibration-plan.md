# Warp CN zh-Hans 汉化校准方案

Last updated: 2026-06-05

本文件是一套可执行的 Warp CN 汉化校准方案。目标是让 Codex 按人工审校方式逐模块、逐条排查汉化质量，明确哪些问题属于文案问题、功能风险、乱码或渲染风险、性能风险，以及哪些 public-RC 结论必须等真实 GUI 和安全证据后才能升级。

本文是校准方案和执行规范，不是 public-RC 通过证明。任何发布结论仍必须以当轮执行记录、低负载验证输出、GUI 证据、public-RC blocker registry 和脱敏证据 lint 为准。

## 1. 当前项目分析

### 1.1 仓库汉化模型

Warp CN 当前采用源码级汉化覆盖模型：

1. 上游英文源码仍是语义基准。
2. `resources/localization/zh-Hans-overrides.toml` 是汉化主源。
3. `script/zh_apply_localization.py` 将 manifest 应用到 Rust 源码。
4. 已应用的中文源码应视为可再生输出，不能替代 manifest。
5. 持久可信资产是 manifest、glossary、ignore rules、audit ledger、public-RC evidence ledger、验证脚本和阶段记录。

因此，任何校准都必须先审 manifest 行，再审源码上下文，最后用 GUI 或测试证据证明真实产品行为。

### 1.2 当前可量化基线

| 项目 | 当前值 |
| --- | ---: |
| Manifest entries | 7,943 |
| Covered source files | 552 |
| Already applied entries | 5,690 |
| Dry-run would_change | 0 |
| Dry-run missing | 0 |
| Release inventory covered | 8,574 |
| Release inventory candidates | 2 |
| Release inventory coverage | 100.0% |
| Public-RC blockers | 11 |

当前校准结论应从这个边界开始：

- 低负载源码级汉化状态已经具备可审计基础。
- 现有 full audit 对 7,943 条产生了逐条 ledger，当前没有 `needs-copy-review` 或 `needs-functional-review` 行。
- 仍有 1,030 条 `blocked-public-rc` 行需要真实产品状态、隔离账号、后端 fixture 或一次性对象证据。
- public-RC blocker registry 仍有 11 行阻塞，不能因为源码级校准通过而宣称 public-RC ready。

### 1.3 主要模块分布

全量 audit ledger 显示当前汉化条目集中在以下区域：

| 模块前缀 | 条目数 | 校准含义 |
| --- | ---: | --- |
| `app/src/ai` | 2,375 | Agent、AI provider、BYOK、自定义推理、模型状态，是高风险主战场。 |
| `app/src/terminal` | 1,978 | 终端标签、命令、提示、shell 示例，必须保护命令和 flag。 |
| `app/src/settings_view` | 1,873 | 设置页、账单、团队、AI、环境，GUI 和账号状态依赖强。 |
| `app/src/workspace` | 706 | 工作区、标签页、会话、通知、共享动作，需要 GUI 冒烟。 |
| `app/src/drive` | 225 | Warp Drive、保存、同步、共享，需区分本地和云端状态。 |
| `app/src/search` | 204 | 命令面板和搜索，需保护搜索行为、action id 和关键词策略。 |
| `crates/onboarding/src` | 159 | 首次启动路径、登录/跳过登录、权限文案，需新 profile GUI 证据。 |
| `app/src/auth` | 136 | 登录、token、回调、账号状态，高安全风险。 |

### 1.4 主要风险分布

当前 full audit 的风险标签用于排序，不等同于最终缺陷：

| 风险标签 | 条目数 | 校准重点 |
| --- | ---: | --- |
| `terminal-command` | 3,187 | 命令、flag、路径、shell 片段不能被误翻译。 |
| `english-preserved` | 2,226 | 判断英文保留是否是产品名、内部标识，还是遗漏汉化。 |
| `dynamic-placeholder` | 1,662 | `{}`、变量、URL、markdown、slash command 必须完全保留。 |
| `team-workspace` | 1,179 | 团队、成员、权限、所有权操作需要账号/对象证据。 |
| `environment-endpoint` | 787 | endpoint、环境、provider、AWS Bedrock 不能影响配置行为。 |
| `billing-quota` | 482 | 账单、额度、迁移、订阅文案不能误导成本和权益。 |
| `api-key-secret` | 459 | API key、secret、token 文案必须脱敏且保护真实凭据。 |
| `error-state` | 353 | 错误文案要清楚，但不能破坏诊断和支持信息。 |
| `destructive-action` | 221 | 删除、移除、禁用、转让必须区分动作后果。 |
| `auth-login` | 119 | 登录、OAuth、token 回调必须用隔离账号验证。 |

### 1.5 当前 public-RC 阻塞

`resources/localization/zh-Hans-public-rc-blockers.toml` 当前跟踪 11 个 public-RC 必需 blocker：

| 类别 | 数量 | 行 |
| --- | ---: | --- |
| `isolated_account` | 3 | `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06` |
| `backend_fixture` | 5 | `GUI-SET-04`, `GUI-SET-05`, `GUI-BILL-01`, `GUI-BILL-02`, `GUI-CLOUD-01` |
| `disposable_object` | 3 | `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07` |

这些行只能在三类证据一致时升级：

1. blocker registry 的状态已更新。
2. 人工阶段记录说明证据如何清除 blocker。
3. 脱敏 GUI、后端、账号或 cleanup artifact 存在并通过 lint。

## 2. 校准目标

本方案要覆盖五类问题：

1. 汉化内容是否有错：语义、上下文、动作后果、产品语气、术语一致性。
2. 是否过于机翻：逐词直译、中文不自然、术语漂移、按钮过长、用户行动不清晰。
3. 是否导致功能 bug：placeholder、命令、协议、存储 key、搜索、action id、测试 fixture、日志诊断被误翻译。
4. 是否乱码或渲染异常：UTF-8、TOML 解析、字体 fallback、CJK 宽度、截断、重叠、不可读字符。
5. 是否影响性能：运行时文本渲染、布局重排、字体 fallback、校准脚本耗时、构建和 GUI 启动热负载。

非目标：

- 不用主账号补 public-RC 证据。
- 不购买额度、不绑定支付方式、不消耗真实云资源。
- 不用 fixture 证据冒充真实 public-RC 证据。
- 不把低负载脚本通过误报成 GUI 或 release readiness。

## 3. Codex 模拟人工审校定义

这里的“模拟人工”不是抽样阅读，也不是只跑脚本。Codex 必须按以下方式审：

1. 每个 manifest entry 都要进入 ledger。
2. 每条 entry 至少检查 source、target、path、context、source-state、token preservation、glossary、copy quality、functional risk。
3. 高风险行必须关联模块、风险标签和所需 GUI 或 public-RC row。
4. 每个模块必须有模块级结论，说明哪些只通过源码审查，哪些需要 GUI，哪些需要隔离账号或 fixture。
5. 每个周期必须留下机器可复核产物，而不是只写一句“看起来没问题”。

推荐每轮输出：

```text
docs/zh-Hans-calibration-cycles/YYYY-MM-DD/
  summary.md
  module-matrix.md
  entries.json
  entries.tsv
  copy-review-findings.md
  functional-risk-findings.md
  mojibake-and-layout-findings.md
  performance-probe.md
  public-rc-blocker-status.md
```

## 4. 逐条审校流程

对每个 `[[replace]]` 行执行以下检查。

### 4.1 Entry 定位

记录：

- `entry_index`
- `manifest_line`
- `key`
- `path`
- `source`
- `target`
- `context`
- `status`
- `expected_count`
- 所属模块
- 风险标签

通过源码定位判断：

- `target-present`：中文已应用。
- `target-and-source-present`：同文件仍存在英文源，需判断是否多处上下文。
- `source-present-not-applied`：manifest 未应用或 expected_count 不匹配。
- `missing-in-current-source`：上游漂移、文件移动或 manifest 过期。
- `file-missing`：路径失效。

`missing-in-current-source` 不一定是文案错误，但必须进入 source-state review，不能静默接受。

### 4.2 文案正确性检查

逐条判断：

| 检查项 | 通过条件 |
| --- | --- |
| 语义 | target 保留 source 的产品意图和动作后果。 |
| 上下文 | 附近源码能证明它是用户可见文案或安全可翻译文案。 |
| 语气 | 符合终端和生产力工具语气，短、清楚、直接。 |
| 术语 | 符合 `zh-Hans-glossary.toml`，保留 Warp、Warp Drive、Agent、MCP、CLI、GitHub、AWS Bedrock 等产品词。 |
| 禁用词 | 不出现 forbidden target，例如当前项目禁用 `智能体`。 |
| 动作一致 | delete/remove/disable/deactivate/transfer/revoke 不混用成模糊动作。 |
| 用户结果 | 对账单、删除、登录、权限、团队所有权等动作说明后果。 |

### 4.3 机翻感检查

每条可疑文案按 0 到 2 分评分，任一项为 0 必须进入 copy review：

| 维度 | 2 分 | 1 分 | 0 分 |
| --- | --- | --- | --- |
| 语义自然 | 中文像产品文案 | 可理解但生硬 | 直译导致误解 |
| 产品语气 | 精炼、动作明确 | 偏长或普通 | 像机器直译或说明书腔 |
| 术语一致 | 与 glossary 和历史文档一致 | 轻微漂移 | 同一概念多种译法 |
| UI 适配 | 适合按钮、菜单、toast | 可能偏长 | 明显会挤压或换行失控 |
| 风险上下文 | 对高风险动作足够明确 | 需要 GUI 辅助 | 可能误导用户执行危险动作 |

常见机翻红旗：

- 英语词序硬搬进中文，例如形容词堆叠、名词堆叠、缺少动词。
- 把产品词误翻，例如 Agent、Warp Drive、MCP、CLI。
- 把可执行 token 翻译成中文，例如 `--flag`、`/command`、provider id、model id。
- 把内部 diagnostics 当用户文案翻译。
- 在按钮上使用长句或解释性话术。
- 同一动作在同一流程里一会儿叫“删除”、一会儿叫“移除”、一会儿叫“禁用”，但源码动作并不相同。
- 保留英文但没有产品、命令、内部标识或 UI 证据支撑。
- 句子能懂，但用户不知道下一步会发生什么。

可接受的英文保留：

- 产品名和品牌名。
- provider、model、protocol、schema、config key、CLI token。
- 用户需要复制的命令、路径、环境变量、flag。
- 搜索或 action id 在当前产品设计中必须保留英文时。

### 4.4 功能安全检查

每条 entry 都要确认 target 没有破坏：

- `{}`、`{name}`、`{max_rows}` 等 Rust 或 UI placeholder。
- `%s`、`${VAR}`、`$ENV`、URL、markdown link。
- backtick 内代码、shell 命令、long flag、slash command。
- JSON、YAML、GraphQL、HTTP header、serde field。
- storage key、feature flag、telemetry event。
- action id、command id、search tags、search keywords。
- provider name、model id、endpoint name、API key label。
- test fixture、snapshot、parser input、diagnostic log。

默认规则：

- 行为、存储、协议、telemetry、diagnostic 字符串默认 preserve。
- 混合说明和 token 的字符串做 partial translate。
- 确认是被动 UI 文案时才完整 translate。
- 不确定时标记 `needs-owner-review` 或 `needs-functional-review`，不能靠猜。

### 4.5 乱码和格式检查

每条 entry 至少检查：

- TOML 能解析。
- target 是 UTF-8。
- 不包含替换字符 `�`。
- 不包含典型 mojibake 片段，例如 `Ã`, `Â`, `â€™`, `ä¸`。
- 中文标点符合 UI 语境。
- 中英文间空格不破坏 token，例如 `API 密钥`、`AWS Bedrock 配置文件`。
- 多行、换行、制表符、转义字符与源码预期一致。
- UI 紧凑区不因为全角字符、长句或换行导致遮挡。

## 5. 逐模块校准路线

### 5.1 AI 和 Agent

路径：

- `app/src/ai`
- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/custom_inference_modal.rs`

重点：

- Agent 作为产品词保留，不改成 forbidden term。
- provider、model、endpoint、API key、BYOK、fallback、credit 语义准确。
- 任务状态如 queued、running、failed、blocked、cancelled 清楚。
- Driver output 中 code、命令、sentinel、模型输出状态不能破坏解析。
- 自定义推理 add/edit/remove 必须区分源码审查、fixture 证据和真实隔离账号证据。

退出条件：

- source-level audit 无 copy/functional actionable row。
- AI settings 和 custom inference 相关 public-RC rows 保持 blocked，直到隔离账号或 fixture 证据满足对应等级。
- GUI 证据能证明控件文案、错误状态和按钮长度。

### 5.2 Terminal 和命令

路径：

- `app/src/terminal`
- slash command 相关路径
- terminal input 和 view

重点：

- shell 命令、flags、路径、环境变量、slash command 名称不翻译。
- 可复制命令中的参数顺序和标点不变化。
- 提示文案可以翻译，但不能改变命令含义。
- `copy on select`、keyboard shortcut、terminal selection 等术语需要项目内一致。
- CJK 宽度、光标位置、选择文本、terminal copy 行为需要 GUI 或 targeted test。

退出条件：

- token preservation clean。
- command/search 相关测试通过。
- 终端 GUI 冒烟看见中文标签且命令输入不受影响。

### 5.3 Settings

路径：

- `app/src/settings_view`

重点：

- 设置页导航、tab、toggle、checkbox、帮助文字短且一致。
- Appearance、AI、Billing、Teams、Environment、Privacy、Code 等分区术语稳定。
- 短按钮不写解释性长句。
- destructive、billing、auth、cloud、team、secret 操作进入高风险证据路径。

退出条件：

- low-load validation clean。
- Settings shell GUI 行可读。
- public-RC blocker 行不被源码审查单独升级。

### 5.4 Workspace、Tabs、Warp Drive

路径：

- `app/src/workspace`
- `app/src/drive`
- tab configs

重点：

- 保存、共享、同步、导入、导出、复制链接、分支、工作目录等动作准确。
- Warp Drive 作为产品词保留。
- 团队、权限、共享、所有权相关文案需要账号或对象证据。
- 空状态和 toast 不应显得机翻。

退出条件：

- GUI 冒烟覆盖菜单、tab context menu、workspace top-level search、Drive entry。
- 涉及 cloud/team/share 的行按 blocker 或 evidence matrix 分级。

### 5.5 Search 和命令面板

路径：

- command palette
- search entry points
- action registry

重点：

- visible label 可以汉化。
- search tags、search keywords、action id 必须按产品策略处理。
- 快捷键符号、prefix、filter chips 不破坏检索。
- 英文保留必须能解释为搜索行为或产品词，而不是遗漏。

退出条件：

- source review 和 low-load gate clean。
- command palette GUI 证据覆盖中文 label 和搜索行为。

### 5.6 Onboarding、Auth、Account

路径：

- onboarding slides
- `app/src/auth`
- login modal 和 token fallback

重点：

- 登录、跳过登录、禁用 AI、禁用 Warp Drive、token paste、callback 文案明确。
- 不能使用主账号收集 public-RC 证据。
- OAuth、token、magic link、cookie、账号 id 不能进入仓库。
- 登录失败和安全提示不能误导用户暴露凭据。

退出条件：

- 非破坏 onboarding GUI 可用新 profile 验证。
- auth/account public-RC 行必须等隔离账号。

### 5.7 Billing、Teams、Cloud、Destructive

路径：

- billing and usage
- teams page
- environment page
- cloud/capacity dialogs
- secret、endpoint、ownership transfer confirmations

重点：

- 不误导费用、额度、订阅、迁移、团队席位。
- 删除、移除、转让、撤销、禁用动作必须准确区分。
- 每个 destructive path 先验证 cancel，再只允许精确命名的一次性对象。
- 不购买、不绑定支付、不消耗真实额度、不删除真实对象。

退出条件：

- source-level 文案可通过。
- public-RC 只能在 blocker registry、human record、redacted artifact 三者一致时升级。

### 5.8 Logs、Telemetry、Protocol、Tests

路径：

- `TelemetryEvent`
- `log::`、`tracing::`、`panic!`、`anyhow!`
- serde/schema/test fixture/parser fixture

重点：

- 默认不翻译。
- 如果确实用户可见，必须写明 source context。
- 内部字符串进入 ignore rule 时要有注释说明。

退出条件：

- inventory ignore 精确，不隐藏真实 UI 文案。
- tests 和 fixtures 不因无产品价值的翻译而漂移。

## 6. 低负载验证套件

每轮校准先运行轻量验证：

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable
python3 -m json.tool docs/zh-Hans-full-translation-audit-0.18/entries.json > /tmp/warp-cn-full-audit-entries.pretty.json
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py --json > /tmp/warp-cn-public-rc-evidence-report.json
python3 script/zh_public_rc_evidence_queue.py --json > /tmp/warp-cn-public-rc-evidence-queue.json
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/zh_public_rc_status.py script/zh_public_rc_evidence_lint.py script/zh_public_rc_evidence_report.py script/zh_public_rc_evidence_queue.py script/zh_public_rc_evidence_candidate.py script/privacy_guard.py script/zh_full_translation_audit.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py script/test_zh_public_rc_evidence_candidate.py
cargo fmt --check
git diff --check
```

解释规则：

- `--fail-on-actionable` 失败时，不进入 release handoff。
- `strict-artifacts` 失败不一定是校准失败，当前 11 个 public-RC 证据缺失时期望失败。
- low-load 通过只代表源码级和脚本级干净，不代表 GUI ready。

## 7. 重负载和 GUI gate

任何 Rust 编译、bundle build、GUI launch 之前都必须跑热负载 gate：

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

只有输出 `decision: run-heavy-gate` 才能继续：

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

如果输出 `decision: defer-heavy-gate`：

- 记录原始原因。
- 本轮不重复尝试重负载命令。
- 不把 heavy gate 未跑描述成失败，也不描述成通过。

GUI 校准证据优先级：

1. Computer Use 或 accessibility tree 中的文字锚点。
2. 裁剪且脱敏的截图。
3. 进程、bundle、日志证据仅证明启动，不证明 UI 文案通过。

## 8. 乱码和渲染校准

### 8.1 静态乱码扫描

推荐新增或执行等价扫描：

```bash
iconv -f UTF-8 -t UTF-8 resources/localization/zh-Hans-overrides.toml > /dev/null
rg -n '�|Ã|Â|â€™|â€œ|â€|ä¸|å[\\x80-\\xBF]' resources/localization app crates docs
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 -m json.tool /tmp/zh-CN.json > /tmp/zh-CN.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
```

需要人工确认的情况：

- 文件中存在历史英文、URL 或 provider id，不应被误报为遗漏汉化。
- 文档中引用旧截图路径或旧阶段记录，不应当作为产品 UI 乱码。
- escape 表示法和实际显示字符必须根据源码解析方式判断。

### 8.2 GUI 渲染检查

对每个 GUI 模块记录：

- 主要中文锚点是否可读。
- 是否出现方框、问号、替换字符。
- 文案是否截断。
- 按钮是否因为中文过长撑破布局。
- modal 标题、正文、主按钮、取消按钮是否互相遮挡。
- terminal 中 CJK 宽度、选择、复制、光标移动是否异常。

建议每个模块最少保留一条 accessibility anchor，截图只作辅助。

## 9. 性能影响校准

### 9.1 预期性能模型

当前源码级 overlay 本身不引入运行时 i18n lookup，所以一般不会因为字符串查找增加 runtime overhead。真正需要校准的是：

- 中文字符串长度导致布局测量、换行、reflow 增加。
- CJK glyph 和 font fallback 导致首次渲染或 terminal rendering 更重。
- 终端、搜索、命令面板中字符串宽度变化影响绘制和检索。
- 过长 target 增加 UI 截断、tooltip、accessibility text 负担。
- 校准脚本本身耗时增加，影响开发循环，不等同于用户 runtime 性能。

### 9.2 脚本性能探针

每轮可记录：

```bash
/usr/bin/time -l python3 script/zh_apply_localization.py --dry-run --summary
/usr/bin/time -l python3 script/zh_full_translation_audit.py --fail-on-actionable
/usr/bin/time -l python3 script/zh_localization_inventory.py --preset release --coverage
```

触发调查条件：

- 同一机器、相近负载下脚本耗时相比上轮增加超过 20%。
- full audit 内存异常增长。
- manifest entry 增长后 audit 输出出现明显 I/O 瓶颈。

### 9.3 App 性能探针

只在 heavy gate 允许后执行：

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
pgrep -afil 'WarpOss|warp-oss|terminal-server'
/usr/bin/log show --last 10m --predicate 'process == "warp-oss"' --style compact
```

记录：

- 启动是否成功。
- 菜单和主窗口是否可交互。
- 是否出现 thermal 或 performance warning。
- 是否有明显 UI 卡顿、长时间空白、字体 fallback 抖动。
- CPU 和内存是否显著高于上一轮同类 debug build。

判断规则：

- 没有运行 heavy gate 时，只能写“性能未做 GUI/runtime 结论”。
- 看到脚本耗时变化，只能说明开发验证成本变化，不直接说明用户 app 性能。
- 看到字体、截断、重排问题时，优先归入渲染/UI 适配，不先归入性能 bug。

## 10. Public-RC 证据策略

public-RC 校准要遵守：

- 只使用隔离测试账号，不使用用户主账号。
- 只使用安全 backend fixture，不输入真实 AWS、API key、token、cookie。
- 只操作精确命名的一次性对象。
- destructive path 必须先证明 cancel 路径，再按明确批准处理对象。
- 所有 artifact 必须裁剪、脱敏、lint。

每个 blocker 行的升级记录必须包含：

```text
row_id:
old_status:
new_status:
evidence_type:
evidence_paths:
accessibility_anchors:
cleanup_proof:
redaction_summary:
operator:
date:
why_safe:
```

`script/zh_public_rc_evidence_lint.py --strict-artifacts` 通过前，不得宣称 public-RC ready。

## 11. 审校决策分类

逐条 entry 使用以下决策：

| 决策 | 含义 | 后续动作 |
| --- | --- | --- |
| `accepted-source` | 源码上下文、术语、token、功能风险均通过。 | 可进入模块汇总。 |
| `accepted-with-note` | 文案可接受，但有 GUI、长度、高风险或证据备注。 | 保留 note，等待对应证据。 |
| `needs-copy-fix` | 语义、术语、机翻感或动作后果有问题。 | 修改 manifest target，重新 apply 和 audit。 |
| `needs-functional-review` | 可能影响解析、placeholder、搜索、存储或协议。 | 找 owner 或加 targeted test。 |
| `blocked-public-rc` | 源码可接受，但缺真实产品状态证据。 | 保持 blocker，不升级。 |
| `ignored-internal` | 已确认是内部字符串或不可翻译项。 | 写入 ignore rule 或记录理由。 |

模块级结论使用：

- `reviewed-low-load`
- `needs-gui`
- `needs-account-state`
- `fixture-only`
- `public-rc-blocked`
- `public-rc-ready`

## 12. 执行周期模板

每轮校准文档建议使用：

```markdown
# zh-Hans Calibration Cycle YYYY-MM-DD

## Snapshot

- Branch:
- Worktree state:
- Version:
- Manifest entries:
- Source files:
- Public-RC blockers:
- Heavy gate decision:

## Commands Run

| Command | Result | Notes |
| --- | --- | --- |

## Module Results

| Module | Entries reviewed | Copy result | Functional result | GUI result | Public-RC result |
| --- | ---: | --- | --- | --- | --- |

## Findings

| ID | Severity | Entry | Module | Finding | Required action |
| --- | --- | --- | --- | --- | --- |

## Deferred Items

| Item | Reason | Required prerequisite |
| --- | --- | --- |

## Final Decision

- Local-use readiness:
- GUI readiness:
- Public-RC readiness:
- Performance conclusion:
```

## 13. 可执行分工

推荐把后续校准分成七条 lane：

| Lane | 目标 | 主要产物 |
| --- | --- | --- |
| Corpus lane | 确认 manifest、glossary、inventory、source-state 干净。 | entries ledger, drift report |
| Copy lane | 逐条反机翻和术语校准。 | copy findings, rewrite patch |
| Functional lane | 保护 token、parser、search、storage、protocol。 | functional findings, targeted tests |
| GUI lane | 模块化 accessibility 和截图证据。 | GUI anchors, redacted artifacts |
| Mojibake/layout lane | UTF-8、字体、CJK width、截断、重叠。 | rendering findings |
| Performance lane | 低负载、脚本耗时、heavy gate 后 runtime 探针。 | performance-probe.md |
| Public-RC lane | 11 个 blocker 的安全证据闭环。 | blocker status, evidence packets |

这些 lane 可以并行做文档和静态分析，但 heavy build、GUI、账号、backend fixture 相关任务必须串行且先过 gate。

## 14. 推荐后续增强

现有工具已经能做全量逐条模拟审计，但如果要让“机翻感、乱码、性能”更机器可复核，建议后续补强：

1. 在 `script/zh_full_translation_audit.py` 增加 `module`, `length_ratio`, `machine_copy_score`, `mojibake_status`, `ui_density_risk` 字段。
2. 新增 `script/zh_mojibake_scan.py`，集中扫描 UTF-8、mojibake、替换字符、异常转义。
3. 新增 `script/zh_module_calibration_report.py`，按模块聚合 copy、functional、GUI、public-RC 状态。
4. 新增 `script/zh_performance_probe.py`，统一记录低负载 gate、脚本耗时和 heavy gate 后 runtime 指标。
5. 将每轮校准输出固定到 `docs/zh-Hans-calibration-cycles/YYYY-MM-DD/`，避免阶段记录散落。
6. 为 command palette、terminal command、settings form、custom inference modal、billing/team destructive modal 增加 targeted tests 或 fixture tests。

## 15. 最终验收标准

### 15.1 本地工程使用可接受

必须全部满足：

- Manifest validation passed。
- Glossary check passed。
- Dry-run reports `would_change: 0`, `missing: 0`。
- Full audit has 0 actionable rows。
- Privacy guard passed。
- Python localization/public-RC tests passed。
- `cargo fmt --check` passed。
- `git diff --check` passed。
- Heavy gate 已执行并记录，或明确因 `defer-heavy-gate` 延后。
- 校准报告明确写出 GUI 和 public-RC 未完成项。

### 15.2 Public-RC 可接受

除本地工程使用标准外，还必须全部满足：

- Fresh current-source GUI smoke evidence exists。
- 11 个 public-RC blockers 全部清除。
- 每个 blocker 有脱敏证据、accessibility anchor、cleanup proof。
- `zh_public_rc_evidence_lint.py --strict-artifacts` passed。
- 静态图和视觉资产审查完成。
- 没有使用主账号、真实账单、真实 secret、真实 token、真实 endpoint 或真实团队所有权。
- 性能探针没有发现热负载、启动、渲染、字体 fallback 或 UI 卡顿问题。

### 15.3 不可接受结论

出现以下任一情况，必须拒绝 release 或 public-RC ready 结论：

- `needs-copy-review` 或 `needs-functional-review` 行未清。
- `dry-run` 有 missing 或 would_change。
- placeholder、URL、command、flag、env var 有 critical mismatch。
- 乱码扫描出现无法解释的 mojibake。
- GUI 证据只证明进程启动，没有证明中文 UI 可读。
- fixture-only 证据被当作真实 public-RC 证据。
- heavy gate defer 后仍执行重负载命令。
- 使用或泄露真实账号、token、API key、账单、团队、endpoint、secret。

## 16. 当前建议结论

基于 2026-06-05 的只读分析和轻量命令输出，本项目适合进入“系统化校准执行”阶段。当前最佳定位是：

```text
localization source-level calibration: ready to execute
current source-level audit posture: no actionable rows in existing 0.18 full audit
GUI readiness: incomplete
public-RC readiness: blocked by 11 evidence rows
performance conclusion: requires heat-gated runtime probes before any release claim
```

下一步应优先把本文转化为一次 dated calibration cycle：先复跑低负载套件，再按模块生成 copy、functional、mojibake/layout、performance 四类 finding ledger，最后只在 gate 允许时补 GUI 和 runtime 性能证据。
