# Warp CN Phase 4 发布质量与高价值残留收敛

## 1. 阶段定位

Phase 3 已经把本项目从“源码级替换脚本”升级成可审计的汉化 overlay 工程：manifest v2 元数据、inventory ignore 外置、术语表校验、GUI 冒烟矩阵、stable-first 上游同步流程和 JSON/YAML locale 导出雏形都已建立。

Phase 4 的目标是把这些资产用于下一轮实际交付：优先收敛高价值用户可见残留、补强 GUI 复验、提高 manifest 可迁移性，并形成一次可发布的中文构建流程。

核心判断：

- 继续保持“官方源码 + 汉化 overlay”的项目定位。
- 不追求整仓覆盖率，而是按真实用户路径收敛残留英文。
- 对 `modals` 预设要先分类、再翻译或忽略；不能把终端协议、Agent transcript、诊断模板和日志当作普通 UI 文案批量处理。
- Phase 4 结束时应能给出一次可复现的 release candidate 记录，而不仅是更多 manifest 条目。

## 2. 当前基线

基线日期：2026-05-30。

```text
entries: 2556
files: 186
already_applied: 2541
would_change: 0
missing: 0
```

Release coverage 快照：

```text
preset: release
covered: 2802
candidates: 6678
coverage: 29.6%
```

当前候选热点：

| 预设 | 热点路径 | 当前判断 |
| --- | --- | --- |
| `workspace` | `app/src/workspace/view.rs`, `app/src/workspace/mod.rs`, `app/src/workspace/tab_settings.rs` | 仍可能有工作区菜单、tab、toast、拖拽、右侧栏等可见残留，适合作为下一轮真实 UI 审查入口。 |
| `settings` | `app/src/settings_view/features_page.rs`, `app/src/settings_view/mod.rs`, `app/src/settings_view/teams_page.rs`, `app/src/settings_view/appearance_page.rs` | 混有设置搜索词、feature metadata、团队管理深层路径和真实表单文案，需要按页面逐项判定。 |
| `modals` | `app/src/terminal/view.rs`, `app/src/terminal/view/action.rs`, `app/src/terminal/input.rs`, `app/src/ai/agent/mod.rs`, `app/src/ai/agent_sdk/driver.rs` | 大量候选不是普通 UI 文案。Phase 4 应优先建立分类和忽略依据，再处理高频弹窗/确认/错误。 |

## 3. 非目标

Phase 4 不做：

- 不实现运行时语言切换。
- 不重构 Warp UI i18n runtime。
- 不把中文源码 fork 当作唯一主线。
- 不为了覆盖率翻译命令语法、终端协议、telemetry、内部 ID、日志、测试字符串或 settings/search token。
- 不追随 dev/nightly 每日发布；发布仍跟 stable tag、release branch 或明确记录的上游 commit。
- 不一次性给全部旧 manifest 条目补齐 key/context；只先处理高风险、高频和未来迁移价值高的条目。

## 4. Phase 4 里程碑

### P4-M0：Phase 4 入口和执行队列

交付：

- 新增 `docs/zh-Hans-localization-phase4.md`。
- README 和维护文档指向 Phase 4。
- 明确下一轮执行顺序、验收命令和不做事项。

验收：

```bash
git diff --check
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
```

### P4-M1：Manifest v2 元数据高价值补齐

交付：

- 给下一轮会频繁维护的条目补充 `key`、`context`、`status`、`expected_count` 和必要的 `preserve_terms`。
- 第一批优先覆盖 workspace、settings、GUI 矩阵中 manual gate 相关条目。
- 增加或完善元数据统计脚本入口，至少能报告 `key` 覆盖率、`context` 覆盖率和 `expected_count` 覆盖率。

验收：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/test_zh_apply_localization.py
python3 script/test_zh_export_locale.py
git diff --check
```

### P4-M2：Workspace 残留审查与小批量汉化

交付：

- 审查 `workspace` top paths 中的 `candidate` 行。
- 对真实用户可见的菜单、toast、tab、面板、拖拽和崩溃恢复文案添加 manifest 条目。
- 对非 UI 或不应翻译项补充 ignore 规则或 notes，必须记录理由。

优先路径：

- `app/src/workspace/view.rs`
- `app/src/workspace/mod.rs`
- `app/src/workspace/tab_settings.rs`
- `app/src/workspace/cross_window_tab_drag.rs`
- `app/src/workspace/view/right_panel.rs`
- `app/src/workspace/view/global_search/view.rs`

验收：

```bash
python3 script/zh_localization_inventory.py --preset workspace --status candidate
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
cargo fmt --check
git diff --check
cargo check -p warp
```

### P4-M3：Settings 残留审查与术语收敛

交付：

- 审查 `settings` top paths 中的真实表单、说明、按钮、错误和团队管理文案。
- 保留搜索关键词、feature metadata、配置 key 和动态 token。
- 将高频设置术语补进 glossary，例如确认是否统一 `Teams`、`Members`、`Features`、`Privacy`、`Usage` 等译法。

优先路径：

- `app/src/settings_view/features_page.rs`
- `app/src/settings_view/mod.rs`
- `app/src/settings_view/teams_page.rs`
- `app/src/settings_view/appearance_page.rs`
- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/custom_inference_modal.rs`

验收：

```bash
python3 script/zh_localization_inventory.py --preset settings --status candidate
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
cargo fmt --check
git diff --check
cargo check -p warp
```

### P4-M4：Modals/Terminal/Agent 候选分类

交付：

- 对 `modals` 预设中最大的 terminal/Agent 路径做分类，不直接批量翻译。
- 建立候选分类：`user-visible-ui`、`terminal-protocol`、`agent-transcript`、`diagnostic-log`、`test-or-template`、`needs-runtime-trigger`。
- 将明显非 UI 的类别迁移到 ignore config，并写明原因。
- 将真实弹窗、确认框、用户可见错误和 release gate 相关文案拆成后续小批量翻译任务。
- 将第一轮分类结果记录到 `docs/zh-Hans-modal-candidate-classification.md`。

优先路径：

- `app/src/terminal/view.rs`
- `app/src/terminal/view/action.rs`
- `app/src/terminal/input.rs`
- `app/src/terminal/view/init.rs`
- `app/src/ai/agent/mod.rs`
- `app/src/ai/agent_sdk/driver.rs`
- `app/src/ai/agent_sdk/driver/output.rs`

验收：

```bash
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/test_zh_localization_inventory.py
python3 script/zh_apply_localization.py --dry-run --summary
git diff --check
```

### P4-M5：GUI 冒烟矩阵实测收敛

交付：

- 按 `docs/zh-Hans-gui-smoke-matrix.md` 选择可触发路径，把 `needs-trigger` 和 `automation-blocked` 尽量推进到 `verified` 或明确的 `manual-gate`。
- 至少复验工作区基础路径、命令面板、设置页核心路径和一个 destructive confirmation。
- 记录无法触发路径的账号/服务/状态依赖，不把 bundle 成功写成 GUI 验收成功。

验收：

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
git diff --check
```

人工记录必须更新：

- `docs/zh-Hans-gui-smoke-matrix.md`
- `docs/zh-Hans-localization.md` 的 release audit 区块

### P4-M6：Release candidate 打包与发布说明

交付：

- 形成一次 `zh-Hans` release candidate 记录。
- 记录 upstream base、manifest dry-run、coverage、glossary、locale export、cargo check/test、bundle gate、GUI matrix 状态。
- 增加用户安装/运行说明和已知限制，避免误导为官方发行版。

验收：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
cargo fmt --check
git diff --check
python3 script/test_zh_apply_localization.py
python3 script/test_zh_localization_inventory.py
python3 script/test_zh_export_locale.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

### P4-M7：上游 stable 同步演练

交付：

- 按 `docs/zh-Hans-upstream-sync.md` 选择一个明确 upstream base 做同步演练。
- 如果不实际合并，也要记录预检结果：当前 branch、上游候选、预计冲突面、dry-run 风险。
- 如果实际合并，必须先修复 manifest drift，再进入构建和 GUI gate。

验收：

```bash
git remote -v
git fetch origin --tags
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

## 5. 推荐执行顺序

优先级从高到低：

1. P4-M0：先落地本规划入口。
2. P4-M1：补齐高价值 manifest 元数据，让后续翻译和 locale 导出可审计。
3. P4-M2：处理 workspace 残留，因为它最接近用户日常使用。
4. P4-M3：处理 settings 残留，并同步强化 glossary。
5. P4-M4：分类 modals/terminal/Agent 候选，降低覆盖率噪声。
6. P4-M5：实测 GUI 矩阵，把可触发项从 manual/blocked 推进到 verified。
7. P4-M6：形成 release candidate。
8. P4-M7：做上游 stable 同步演练。

## 6. 验收原则

- 每个小批量翻译前先跑 manifest validation 和 dry-run。
- 每个新增 ignore 规则都要能解释“为什么不是用户可见 UI”。
- 每个 glossary 失败都要判断是误译、合理历史译法，还是规则过严。
- 每个 GUI gate 都必须区分 `verified`、`manual-gate`、`automation-blocked` 和 `needs-trigger`。
- 每次发布记录必须能复现：上游基线、命令输出、coverage、bundle 路径和 GUI 状态都要明确。

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 为提高覆盖率误翻译命令/协议/token | 先用 inventory 分类，再翻译；可疑项默认保留并记录原因。 |
| manifest 元数据补齐变成大规模机械劳动 | 只补高价值路径和新改条目；旧条目渐进迁移。 |
| settings 搜索词被误翻译导致搜索退化 | 搜索关键词和 tag 默认保留；只有确认是 UI label 时才进入 manifest。 |
| GUI 路径依赖账号或服务状态 | 在 smoke matrix 记录触发条件和 manual gate，不声称自动通过。 |
| 上游同步后字符串漂移扩大 | 先 dry-run，再修 manifest；不要在中文源码上手工追冲突。 |

## 8. Phase 4 完成定义

Phase 4 可以视为完成，当且仅当：

- README 和维护文档指向 Phase 4 当前状态。
- Workspace 和 Settings 至少各完成一轮候选审查并记录结果。
- Modals/Terminal/Agent 候选完成第一轮分类，ignore 规则有理由。
- GUI smoke matrix 至少新增一批真实 `verified` 记录，或明确记录无法触发原因。
- 一次 release candidate gate 通过并记录命令输出摘要。
- `zh_export_locale.py` 仍能导出 2556+ 条可解析 JSON，且新增 v2 元数据不破坏旧 manifest 条目。
