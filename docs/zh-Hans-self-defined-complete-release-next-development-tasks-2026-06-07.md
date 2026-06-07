# Warp CN 0.19 自定义汉化完成版后续开发任务 - 2026-06-07

## 策略更新

用户已取消“开发时尽量让电脑保持低负载”的限制。后续开发不再把
`script/zh_low_load_gate.py` 作为 `cargo check`、本地启动、bundle 或 GUI smoke 的前置
条件。

本项目当前目标仍然是本仓库自行定义的 `Warp CN 0.19 自定义汉化完成版`，不是 Warp
官方中文版本，也不等待 Warp 官方对后端 fixture、账号状态或发行物背书。

## 当前基线

```text
self-defined target: 0.19
source overlay: clean
dry_run: would_change 0, missing 0
release inventory: 100.0%
public-RC blockers: preserved for future higher-assurance route
GUI smoke: pending current-cycle evidence
onboarding static PNG: pending-replacement or known limitation
cargo_check: pending direct run
bundle_or_launch: pending direct run
publication: not approved
```

## R1 直接重型验证

目标：取消 low-load 前置条件后，直接跑发行前必要命令，并把结果写入新的预检记录。

建议输出文件：

- `docs/zh-Hans-packaging-preflight-2026-06-07.md`
- `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`

执行命令：

```bash
python3 script/privacy_guard.py --all-tracked
git diff --check
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

完成信号：

- `privacy_guard` 通过。
- `git diff --check` 通过。
- `cargo check` 通过，或失败输出被归档并拆成修复任务。
- 本地启动命令通过，或失败输出被归档并拆成修复任务。

## R2 当前周期 GUI Smoke

目标：补齐 0.19 自定义完成版需要的高频界面验证，不覆盖官方后端路径。

待更新文件：

- `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`
- `docs/zh-Hans-gui-smoke-matrix.md`

验证范围：

| ID | 区域 | 完成要求 |
| --- | --- | --- |
| GUI-SD-01 | App launch | 当前周期启动界面中文可读，未发现明显布局破损 |
| GUI-SD-03 | Workspace shell | shell、tab、基础命令输出周边中文可读 |
| GUI-SD-04 | Command palette | 命令面板搜索、空状态或结果行中文可读 |
| GUI-SD-05 | Settings core pages | 核心设置页中文可读，无明显截断 |
| GUI-SD-06 | AI settings entry | AI 设置入口中文可读，真实凭据路径不输入敏感信息 |
| GUI-SD-07 | Dangerous confirmation cancel path | 只验证取消路径和文案可读性，不执行真实删除或转让 |

完成信号：

- Artifact index 中每个已验证行有 `pass`、`known-limitation` 或 `blocked-with-reason`。
- 不提交原始私有截图、回调 URL、账号标识、billing ID、endpoint URL、cookie、token 或
  magic link。

## R3 Onboarding 静态资产处置

目标：处理 onboarding PNG 中的英文残留，使 0.19 发行说明不会把未替换图片误报为已完成。

待更新文件：

- `docs/zh-Hans-onboarding-visual-regeneration-plan.md`
- `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`
- `docs/zh-Hans-release-notes-0.19-draft.md`

允许结果：

- 重新生成或替换 onboarding 图片。
- 裁剪规避英文残留，但必须保留界面语义。
- 明确列为 `known limitation`，并在 release notes 中说明不影响源码级汉化完成。

完成信号：

- GUI-SD-02 状态不再是裸 `pending`。
- release notes 对静态资产边界有明确说明。

## R4 Release Notes 与 Checklist 冻结

目标：把 0.19 的“可发布但非官方”口径冻结到发行文档。

待更新文件：

- `docs/zh-Hans-release-notes-0.19-draft.md`
- `docs/zh-Hans-self-defined-complete-release-checklist-0.19.md`
- `README.md`

完成信号：

- Release notes 明确写明不是 Warp 官方中文版本。
- Checklist 中所有已完成项有命令或文档证据支撑。
- 未验证的官方后端、billing、Cloud、team、secret、endpoint 路径列入 known limitations。
- Publication gates 保持未勾选，直到用户明确批准 tag、push 和 GitHub release。

## R5 Git Hygiene 与发行冻结

目标：在发布前把工作树状态、文档范围和风险边界整理清楚。

建议命令：

```bash
git status --short
git diff --check
python3 script/privacy_guard.py --all-tracked
```

完成信号：

- 文档变更、脚本变更、生成产物和证据产物被分组说明。
- 不相关的既有改动不被回滚。
- 没有用户批准前，不执行 `git tag`、`git push` 或 GitHub release 创建。

## R6 后续更高保证路线

这条路线不阻塞 0.19 自定义汉化完成版，只用于未来想重新推进 public-RC 或官方后端证据
完整版时继续使用。

保留范围：

- backend fixture approval。
- isolated account 审批和验证。
- disposable object 审批和验证。
- public-RC evidence ledger 的脱敏证据闭环。

0.19 自定义完成版不得为了清空 public-RC blocker，把缺证据行写成 `provided`。

## 下一步执行入口

- `docs/superpowers/plans/2026-06-07-zh-Hans-self-defined-complete-release-followup.md`
