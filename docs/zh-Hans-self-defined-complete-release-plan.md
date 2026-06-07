# Warp CN 自定义汉化完成版开发计划

日期：2026-06-06

策略更新：2026-06-07 用户已取消“开发时尽量让电脑保持低负载”的限制。后续
`cargo check`、本地启动、bundle 和 GUI smoke 不再等待 low-load gate；执行时直接记录
命令、耗时、结果和失败项。

## 目标定义

本计划把 Warp CN 的近期目标重新定义为“自定义汉化完成版”。它是本仓库自行维护、
自行验收、可本地构建、可公开说明边界的简体中文汉化版本。

它不是 Warp 官方中文版本，不代表 Warp 官方发布，也不要求 Warp 官方对中文文案、
后端 fixture、账号状态或发行物背书。所有对外表述都必须保留非官方 fork 边界。

## 当前基线

当前代码和文档仍保留 public-RC 证据体系。该体系继续用于更高等级的官方后端状态
证据追踪，但不再作为“自定义汉化完成版”的硬性完成条件。

```text
version baseline: 0.18 / RC38
self-defined target: 0.19
source overlay: clean
manifest entries: 7943
covered files: 552
already_applied: 5690
would_change: 0
missing: 0
release inventory: 8574 covered, 2 intentional candidates, 100.0%
public-RC blockers: 11
self-defined release blocker reinterpretation: scoped-risk, not hard stop
```

## 完成版验收标准

0.19 自定义汉化完成版必须满足以下条件：

1. 源码级汉化 overlay 仍然干净：`would_change: 0`，`missing: 0`。
2. manifest、glossary、metadata、inventory、full audit 和相关单元测试通过。
3. 高频用户路径完成当前周期 GUI smoke：启动、首次界面、工作区、命令面板、设置页、
   常见弹窗、基础 AI 设置入口。
4. 不依赖官方后端状态的危险确认路径至少完成取消路径验证，真实删除、转让、计费和
   云容量变更不作为完成版必需项。
5. onboarding 静态 PNG 英文残留完成重新生成、替换、裁剪规避或明确列为发行已知限制。
6. 重型验证直接执行并记录结果：`cargo check -p warp`、bundle 或本地启动验证通过；
   如失败则记录完整输出和后续修复项。
7. 隐私检查、`git diff --check` 和发行文档一致性检查通过。
8. README、发行说明和 GitHub release 文案明确写明：这是非官方 Warp CN 汉化 fork。
9. 官方后端、账号、billing、Cloud、team、secret、endpoint 路径的未验证范围被记录为
   `known limitations`，不能伪装成已完整验证。
10. tag、push、GitHub release 必须等用户明确批准后执行。

## Public-RC Blocker 重新解释

原 public-RC blocker registry 不删除、不降级、不伪造通过。它仍然表示如果将来要做
“更高等级 public-RC / 官方后端证据完整版”，还需要完整证据闭环。

对 0.19 自定义汉化完成版，11 条 blocker 改为以下处理方式：

| 类别 | 数量 | 0.19 完成版处理 |
| --- | ---: | --- |
| `backend_fixture` | 5 | 记录为官方后端状态未验证范围；不等待 Warp 官方批准即可发布非官方完成版 |
| `isolated_account` | 3 | 优先使用隔离账号验证；如果无法安全验证，则列入 known limitations |
| `disposable_object` | 3 | 只验证取消路径和文案可读性；真实删除、转让必须另行批准 |

不得为了“清零”而把没有证据的行写成 `provided`。完成版口径是：核心汉化完成，官方后端
和高风险对象路径按范围声明处理。

## 后续开发 Lane

| Lane | 目标 | 是否依赖官方批准 | 完成信号 |
| --- | --- | --- | --- |
| L1 目标口径冻结 | 将 0.19 目标切换为自定义汉化完成版 | 否 | README 和 release notes 使用非官方完成版口径 |
| L2 翻译复扫 | 确认 overlay、术语表、inventory、full audit 干净 | 否 | 轻量校验和单元测试通过 |
| L3 GUI Smoke | 验证高频界面中文可读、布局稳定 | 否 | 当前周期 GUI artifact index 和 smoke matrix 更新 |
| L4 静态资产 | 处理 onboarding PNG 英文残留 | 否 | PNG 已替换或 known limitation 记录 |
| L5 范围声明 | 将官方后端/高风险对象路径写入 known limitations | 否 | release notes 有明确边界 |
| L6 打包检查 | 完成 Rust check、本地启动或 bundle | 否 | heavy gate 记录通过或失败项已归档 |
| L7 发行冻结 | 生成 0.19 checklist、release notes、tag/release 准备 | 否，发布动作需用户批准 | docs、tag、remote release 一致 |

## 执行顺序

1. 先冻结目标口径，避免继续把官方审批当作本项目完成条件。
2. 运行轻量翻译复扫，确认当前源码汉化仍可再生成且无漂移。
3. 直接执行 GUI smoke 和基础启动验证，记录耗时、命令输出和失败项。
4. 处理或记录 onboarding 静态 PNG 英文残留。
5. 写 0.19 自定义汉化完成版 release notes 和 known limitations。
6. 运行打包前检查和隐私检查。
7. 生成最终 release checklist，等待用户批准后再 tag、push、创建 GitHub release。

## No-Go

- 不声明 Warp 官方中文版本。
- 不使用个人主账号验证登录、删除、计费、Cloud、team、secret 或 endpoint。
- 不购买 credits，不绑定付款方式，不消耗真实 quota。
- 不输入真实 AWS、Bedrock、API key、cookie、token 或 magic link。
- 不把原始截图、录屏、回调 URL、账号标识、endpoint URL、billing ID 或 private object
  name 提交到 Git。
- 不把 public-RC evidence ledger 中缺证据的行标为 `provided`。
- 不在用户批准前创建 tag、push 或 GitHub release。

## 当前下一步

本计划的执行入口为：

- `docs/superpowers/plans/2026-06-06-zh-Hans-self-defined-complete-release.md`
- `docs/zh-Hans-self-defined-complete-release-next-development-tasks-2026-06-07.md`
- `docs/superpowers/plans/2026-06-07-zh-Hans-self-defined-complete-release-followup.md`
