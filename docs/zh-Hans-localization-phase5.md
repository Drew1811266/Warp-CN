# Warp CN Phase 5 发布硬化与可复验交付

## 1. 阶段定位

Phase 4 已经形成一次可复现的 release candidate：manifest、glossary、locale export、cargo gate、bundle gate、GUI 矩阵和上游同步演练都已落档。Phase 5 不再以“增加覆盖率”为主目标，而是把中文构建推进到更接近公开交付的状态。

Phase 5 的核心目标：

- 重新刷新上游 stable 基线，消除 Phase 4 中 `git fetch origin --tags` 网络失败带来的不确定性。
- 建立更稳定的 GUI 复验 profile 和截图/记录流程，减少“能启动但不能验收”的灰区。
- 用安全测试对象收敛 destructive confirmation manual gates。
- 继续按分类结果做 terminal/Agent 用户可见小切片，不批量翻译协议、transcript、日志和 token。
- 提高 manifest 可迁移性，让新增高价值条目更接近未来官方 locale 资产。

## 2. 当前基线

基线日期：2026-05-30。

```text
entries: 2619
files: 190
already_applied: 2604
would_change: 0
missing: 0
```

Release coverage 快照：

```text
preset: release
covered: 2845
candidates: 6453
coverage: 30.6%
```

Phase 4 release candidate：

- 记录：`docs/zh-Hans-release-candidate-2026-05-30.md`
- bundle：`target/debug/bundle/osx/WarpOss.app`
- selected stable base：`v0.2026.05.27.09.22.stable_00`
- stable sync caveat：Phase 4 的 `git fetch origin --tags` 因 GitHub 网络错误失败，公开发布前必须重试。

## 3. 非目标

Phase 5 不做：

- 不实现运行时语言切换或完整 i18n runtime。
- 不把中文源码 fork 当作唯一主线。
- 不追 dev/nightly 每日发布。
- 不翻译命令语法、终端协议、settings/search token、feature flag、telemetry、日志、测试 fixtures。
- 不用真实主账号测试删除、转让、计费等高风险路径；这些必须使用隔离测试对象或继续保留 manual gate。
- 不把 bundle 成功、进程启动或截图存在误写为 GUI verified。

## 4. Phase 5 里程碑

### P5-M0：Phase 5 入口和基线复核

交付：

- 新增 `docs/zh-Hans-localization-phase5.md`。
- README 和维护文档指向 Phase 5。
- 复核 Phase 4 RC 记录、GUI 矩阵和上游同步记录是否互相一致。

验收：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

### P5-M1：刷新上游 stable 基线

交付：

- 重试 `git fetch origin --tags`，确认是否存在比 `v0.2026.05.27.09.22.stable_00` 更新的 stable tag。
- 若有新 stable，选择明确 `UPSTREAM_BASE` 并做 dry-run 漂移检查。
- 若 fetch 仍失败，记录网络失败和本地 refs 状态，不继续声称可公开发布。

验收：

```bash
git remote -v
git fetch origin --tags
git tag --sort=-v:refname | rg 'stable' | head
git rev-parse "$UPSTREAM_BASE^{commit}"
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
```

如果发生上游漂移：

- `missing` 必须回到 `0`。
- `would_change` 必须在应用 overlay 后回到 `0`。
- drift 修复原因必须记录到维护文档或 RC2 记录。

### P5-M2：建立 GUI 复验 profile 和证据流程

交付：

- 定义 GUI smoke 的本地测试 profile 使用方式，避免污染真实用户状态。
- 记录 macOS 权限弹窗处理策略，例如 `WarpOss` 访问其他 App 数据的提示默认不授权，除非某个测试明确需要。
- 为 GUI 矩阵增加“证据路径”字段或统一记录段落，记录截图路径、Computer Use 读取结果和无法触发原因。

验收：

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
git diff --check
```

人工验收：

- GUI 矩阵至少新增一条本轮截图/Computer Use 证据记录。
- 不把权限弹窗、进程启动或截图成功单独写成业务路径 verified。

### P5-M3：Destructive confirmation 安全对象复验

交付：

- 为可安全构造的对象建立测试路径：custom endpoint、environment、auth secret、可删会话。
- 优先复验低风险 destructive confirmation：remove endpoint、environment deletion、auth-secret deletion。
- 若无法安全构造对象，记录“缺少测试对象”的具体原因，而不是保留泛泛 manual gate。

验收：

```bash
python3 script/zh_apply_localization.py --dry-run --summary
git diff --check
```

GUI 矩阵要求：

- `GUI-SET-06`、`GUI-WS-04`、`GUI-WS-06` 至少推进一个到 `verified`，或为每个保留项写出缺失对象/账号/权限原因。
- 不测试 team ownership transfer，除非有隔离团队 owner 账号。

### P5-M4：账号、Billing、Cloud 和 Agent 状态门禁拆分

交付：

- 把登录、billing、cloud agent capacity、plan migration、Agent queued/running/failed 状态拆成独立触发条件。
- 明确哪些需要测试账号、哪些需要服务端状态、哪些可以用本地 mock/state 触发。
- 不急于翻译更多 billing/cloud 文案，先解决“怎么验”的问题。

验收：

- `docs/zh-Hans-gui-smoke-matrix.md` 中对应条目不再只写笼统 `manual-gate`，而是有具体触发条件和阻塞原因。
- 新增的触发说明不能依赖主账号或真实生产团队做破坏性操作。

### P5-M5：Terminal/Agent 用户可见小切片

交付：

- 基于 `docs/zh-Hans-modal-candidate-classification.md`，只处理真实用户可见的小切片。
- 优先候选：
  - `terminal.view.notifications`
  - `terminal.view.shell_init`
  - `terminal.view.oz_permissions`
  - `terminal.view.file_context_menu`
  - `agent.driver.user_errors`
- 每个新增 manifest 条目必须包含 `key`、`context`、`status`、`expected_count`。

验收：

```bash
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
cargo fmt --check
git diff --check
cargo check -p warp
```

### P5-M6：Manifest 迁移资产强化

交付：

- 提高高价值条目的 v2 元数据覆盖率，不追求全量机械补齐。
- 优先给 Phase 4/5 新增条目、GUI manual gate 条目、destructive confirmation 条目补齐 metadata。
- 评估是否需要增加机器可读统计输出，例如 `--metadata-summary --json`，供后续 release notes 或 CI 使用。

验收：

```bash
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
python3 script/test_zh_apply_localization.py
python3 script/test_zh_export_locale.py
git diff --check
```

建议目标：

- `key/context/status/expected_count` 覆盖率从 Phase 4 的 `3.0%` 提升到至少 `5%`。
- 不为低价值历史条目机械补 metadata。

### P5-M7：RC2 打包、发布说明和安装边界

交付：

- 形成 `zh-Hans` RC2 记录。
- 明确是否可以公开发布；如果不能，写明阻塞项。
- 补充用户安装/运行说明、已知限制、manual gates、非官方声明。

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

### P5-M8：发布决策

交付：

- 给出明确发布判断：`ready-for-local-use`、`ready-for-public-rc` 或 `blocked`。
- 如果 `ready-for-public-rc`，准备 release notes 草案。
- 如果 `blocked`，列出阻塞项、负责人、下一步验证命令。

发布前必须满足：

- 上游 stable refs 已刷新，或公开说明当前基于本地已知 stable。
- `missing: 0`。
- RC2 命令行 gate 通过。
- GUI 矩阵中基础工作区、设置 shell、命令面板、至少一个 destructive confirmation 有真实证据。
- 仍保留的 account/billing/cloud/Agent gates 都有明确触发条件和阻塞原因。

## 5. 推荐执行顺序

1. P5-M0：先建立阶段入口。
2. P5-M1：优先刷新上游，避免在旧 stable 上继续堆工作。
3. P5-M2：建立 GUI 证据流程，否则 manual gate 仍会反复卡住。
4. P5-M3：用安全对象关闭至少一个 destructive confirmation。
5. P5-M4：把账号/服务端状态拆清楚。
6. P5-M5：做 terminal/Agent 小切片。
7. P5-M6：补 metadata 和 locale 迁移资产。
8. P5-M7：形成 RC2。
9. P5-M8：做发布判断。

## 6. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 上游 fetch 继续失败 | 不发布“最新 stable”声明；使用本地 stable 只做演练，记录网络失败。 |
| GUI profile 污染真实用户状态 | 使用隔离测试对象和明确的本地 profile 记录；不操作主账号高风险资源。 |
| 为关闭 manual gate 而误做破坏性操作 | 只测试可恢复或隔离对象；team ownership transfer 默认不测试。 |
| terminal/Agent 候选被批量误翻 | 只按 P4-M4 分类小切片处理；协议、transcript、日志默认保留。 |
| metadata 工作变成机械劳动 | 只补 release/gate/新增高价值条目，设置覆盖率目标而非全量目标。 |

## 7. Phase 5 完成定义

Phase 5 可以视为完成，当且仅当：

- README 和维护文档指向 Phase 5 当前状态。
- 上游 stable 刷新结果明确记录。
- GUI 矩阵新增真实证据，并至少推进一个 destructive confirmation 或写明具体阻塞。
- terminal/Agent 至少完成一个用户可见小切片，或明确说明为什么本轮不应翻译。
- v2 metadata 覆盖率提升到计划目标或有合理记录。
- RC2 gate 通过，且发布判断为 `ready-for-local-use`、`ready-for-public-rc` 或 `blocked` 中的一个。
