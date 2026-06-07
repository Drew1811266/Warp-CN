# Warp CN 正式汉化发行版开发计划

日期：2026-06-03

## 目标定义

本计划的目标是把 Warp CN 从 `ready-for-local-use-with-fixture-evidence`
推进到可公开发布的正式汉化发行版。

这里的“正式汉化发行版”指 Warp CN fork 的可审查中文发行版，不代表 Warp
官方中文版本，也不改变 Warp 官方账号体系、云服务、协议、商标和许可证边界。

## 当前基线

| 项目 | 当前状态 |
| --- | --- |
| 项目版本 | `0.18` |
| 最近 RC 记录 | `2026-06-03 RC38` |
| 当前结论 | `ready-for-local-use-with-fixture-evidence` |
| Manifest 条目 | 7,943 |
| 覆盖文件 | 552 |
| 已应用条目 | 5,690 |
| 待应用变更 | 0 |
| 丢失或漂移条目 | 0 |
| Release inventory | 8,574 covered / 2 candidates / 100.0% |
| Public-RC blocker | 11 |
| Ready evidence rows | 0 |

当前阶段的主要问题已经不是大规模源码文案未翻译，而是正式发行前的外部状态、
GUI、证据、资产、构建和发布闭环尚未完成。

## 正式发行准入标准

正式发行必须同时满足以下条件：

1. 源码级汉化 overlay 仍然干净：`would_change: 0`，`missing: 0`。
2. `resources/localization/zh-Hans-overrides.toml` 通过 manifest、glossary、
   metadata 和 full-audit 检查。
3. 11 个 public-RC blocker 全部有已审查、已脱敏、可提交的证据元数据。
4. `python3 script/zh_public_rc_evidence_lint.py --strict-artifacts` 通过。
5. 当前周期 GUI smoke 证据存在，且覆盖登录、设置、工作区、常见弹窗、危险确认
   和外部状态路径。
6. onboarding 静态 PNG 的英文残留完成重新生成或获得明确设计批准。
7. 低负载 gate 允许后，重型 gate 通过：Rust check、bundle 生成、基础 GUI
   启动、隐私检查、格式检查和 diff 检查。
8. 上游 stable 同步状态有明确 commit/tree 证据，不混用 ancestry、tree parity
   和 tag retarget 结论。
9. README、开发手册、发行说明、证据记录和版本标签保持一致。
10. 用户明确批准发布、打 tag、推送或创建 release。

## 工作流总览

| 工作流 | 目标 | 当前状态 | 完成信号 |
| --- | --- | --- | --- |
| Evidence Governance | 固化证据规则和安全边界 | 工具已具备，证据仍缺失 | strict artifact lint 通过 |
| Backend Fixture Lane | 验证计费、Cloud、Bedrock 等后端状态路径 | 5 行 blocked | 5 行 evidence ready |
| Isolated Account Lane | 验证登录、账号态、AI 设置、自定义推理 | 3 行 blocked | 3 行 evidence ready |
| Disposable Object Lane | 验证环境、secret、team 等危险对象路径 | 3 行 blocked | 3 行 evidence ready |
| GUI Smoke Lane | 补齐当前周期 GUI 启动和主要界面证据 | RC38 未运行 GUI launch | 当前周期 GUI matrix 通过 |
| Visual Asset Lane | 处理 onboarding PNG 英文残留 | 未完成 | PNG 已重生成或设计批准 |
| Upstream Freshness Lane | 确认与上游 stable 的关系 | tree 等价记录存在 | 发行文档使用精确 commit/tree 语言 |
| Packaging Lane | 构建可交付 bundle | RC38 有本地 bundle 记录 | 发行候选 bundle 通过重型 gate |
| Publication Lane | 发布正式汉化版本 | 未批准 | tag、release note、远端状态一致 |

## Public-RC Blocker 分解

### Backend Fixture Lane

行：

- `GUI-BILL-01`：out-of-credits 或 billing modal。
- `GUI-BILL-02`：Build plan migration modal。
- `GUI-CLOUD-01`：Cloud capacity 或 quota modal。
- `GUI-SET-04`：AWS Bedrock settings。
- `GUI-SET-05`：invalid Bedrock credential error。

执行边界：

- 只使用 fixture owner 批准的安全后端状态。
- 不购买 credits，不绑定付款方式，不消耗真实 quota。
- 不输入真实 AWS、Bedrock、API key 或 provider credentials。

完成标准：

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

其中 strict lint 必须不再因 backend fixture 行失败。

### Isolated Account Lane

行：

- `GUI-AUTH-01`：browser login callback 和返回账号态。
- `GUI-SET-03`：Settings > AI 和 custom inference 可见状态。
- `GUI-WS-06`：custom inference endpoint removal。

执行边界：

- 必须使用隔离测试账号。
- 不使用个人主账号。
- 不提交账号标识、cookie、token、magic link、callback URL 或 endpoint URL。
- 不创建或删除非 allowlisted endpoint。

完成标准：

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

其中 strict lint 必须不再因 isolated account 行失败。

### Disposable Object Lane

行：

- `GUI-SET-06`：删除 `zh-smoke-delete-environment`。
- `GUI-WS-04`：删除 `zh-smoke-delete-secret`。
- `GUI-WS-07`：转让或清理 `zh-smoke-public-rc-team`。

执行边界：

- 先验证取消路径。
- 删除或转让前必须获得明确批准。
- 只能操作 registry 中 allowlisted 的一次性对象名。
- 不触碰真实 team、secret、environment 或 endpoint。

完成标准：

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

其中 strict lint 必须不再因 disposable object 行失败。

## 发行阶段路线图

### 阶段 R1：正式发行计划冻结

目标：

- 固化本计划。
- 将本计划加入 README 维护文档索引。
- 记录当前基线、准入标准、工作流和 no-go 规则。

完成信号：

- `docs/zh-Hans-official-release-development-plan.md` 存在。
- `docs/superpowers/plans/2026-06-03-zh-Hans-official-release-plan.md` 存在。
- 低负载文档 gate 通过。

### 阶段 R2：证据准备与 lane 分派

目标：

- 为 backend fixture、isolated account、disposable object 三条 lane 生成
  当前 queue 和 missing-action packet。
- 明确每条 lane 的批准人、输入产物、脱敏规则和 cleanup proof 形式。
- 不在此阶段创建真实证据或清 blocker。

建议产物：

- `docs/zh-Hans-public-rc-backend-fixture-execution.md`
- `docs/zh-Hans-public-rc-isolated-account-execution.md`
- `docs/zh-Hans-public-rc-disposable-object-execution.md`

完成信号：

- 每条 lane 有独立执行文档。
- 每条 lane 能用 `script/zh_public_rc_evidence_candidate.py` 预检候选证据。

### 阶段 R3：backend fixture 证据闭环

目标：

- 优先处理中等风险但数量最多的 backend fixture 行。
- 收集 5 行已审查脱敏证据。
- 更新 evidence ledger。

完成信号：

- backend fixture 5 行从 `missing` 变为 ready。
- strict artifact lint 仍可能因其他 lane 失败，但不再因 backend fixture 失败。

### 阶段 R4：isolated account 证据闭环

目标：

- 使用隔离账号验证登录、账号态、AI 设置和自定义推理相关路径。
- 收集 3 行已审查脱敏证据。
- 确认 logout 或 profile cleanup proof。

完成信号：

- isolated account 3 行从 `missing` 变为 ready。
- 不提交任何真实账号或认证材料。

### 阶段 R5：disposable object 证据闭环

目标：

- 使用一次性对象验证危险确认、取消路径和 cleanup proof。
- 收集 3 行已审查脱敏证据。

完成信号：

- disposable object 3 行从 `missing` 变为 ready。
- strict artifact lint 通过或只剩非 blocker 型文档问题。

### 阶段 R6：GUI、资产和重型 gate

目标：

- 在低负载 gate 允许时重跑 bundle、GUI launch 和 current-cycle smoke。
- 处理 onboarding PNG 英文残留。
- 生成正式发行候选的 current-cycle 证据。

执行 gate：

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

完成信号：

- `target/debug/bundle/osx/WarpOss.app` 是当前周期产物。
- GUI launch 和 smoke matrix 有当前周期证据。
- PNG 残留得到处理或批准。

### 阶段 R7：正式发行冻结

目标：

- 生成正式发行记录。
- 更新 README、开发手册、发行说明、证据 ledger 和版本号。
- 准备 tag 和远端发布操作。

建议产物：

- `docs/zh-Hans-release-candidate-2026-06-03-formal.md`
- `docs/zh-Hans-official-release-checklist-0.19.md`
- `docs/zh-Hans-release-notes-0.19.md`

完成信号：

- 所有低负载 gate、重型 gate、strict evidence lint 和 privacy guard 通过。
- 用户明确批准 tag、push、release。
- 远端 tag、release notes 和 README 版本一致。

## No-Go 规则

以下事项不能作为自动化步骤执行，必须先获得明确批准：

- 使用个人主账号登录。
- 修改真实 billing、Cloud、team、secret、environment 或 endpoint。
- 输入真实 AWS、Bedrock、API key、token、cookie 或 magic link。
- 删除、转让或重置任何非 allowlisted 对象。
- 提交原始截图、录屏、账号标识、callback URL 或私有 endpoint。
- 发布 tag、push 到远端、创建 GitHub release。
- 声称本 fork 是 Warp 官方中文版本。

## 每轮执行前的低负载检查

```bash
git status --short --branch
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py --json
python3 script/zh_public_rc_evidence_queue.py --json
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py script/test_zh_public_rc_evidence_candidate.py
cargo fmt --check
git diff --check
```

## 当前优先级

1. 冻结正式发行计划文档和执行计划。
2. 生成三条 public-RC evidence lane 的执行文档。
3. 先推进 backend fixture lane，因为它有 5 行 blocker，风险低于账号和删除类路径。
4. 再推进 isolated account lane，确保完全隔离账号和清理证明。
5. 最后推进 disposable object lane，因为它涉及删除、转让和 cleanup proof。
6. 证据全部 ready 后，再跑 GUI、PNG、重型 gate 和正式发行冻结。

## 后续开发任务文档

- `docs/zh-Hans-official-release-next-development-tasks.md`：R3-R7 后续任务队列、输入输出和阻塞条件。
- `docs/superpowers/plans/2026-06-03-zh-Hans-backend-fixture-evidence-closure-plan.md`：R3 backend fixture evidence closure 的可执行计划。
