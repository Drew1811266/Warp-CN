# Warp CN

Warp CN 是基于 [Warp](https://github.com/warpdotdev/warp) 开源客户端维护的简体中文本地化项目。它的目标是在 Warp 官方尚未提供完整应用语言切换和中文语言包之前，为中文用户提供一个可以本地构建、持续跟随上游的汉化版本。

> [!IMPORTANT]
> 本仓库不是 Warp 官方发行版，也不代表 Warp 官方中文版本。上游功能、账号体系、云服务、协议和许可证仍以 Warp 官方项目为准。

## 这个项目有什么用

- 让 Warp 开源客户端的高频可见界面显示简体中文。
- 用翻译清单维护汉化内容，减少直接散改源码带来的升级成本。
- 在同步上游版本后，通过脚本检查字符串漂移和翻译覆盖情况。
- 为未来迁移到官方 i18n / zh-CN locale 保留可复用的翻译资产。

当前汉化方式是源码级 overlay：翻译集中维护在 manifest 中，再由脚本应用到源码。中文源码应视为构建产物，真正需要长期维护的是翻译清单、术语表、忽略规则、审查记录和验证流程。

## 当前进度

当前版本：`0.13`

项目已经进入“可本地使用、继续审查打磨”的阶段：

- 已建立简体中文翻译清单、inventory 扫描、术语表校验和 locale 导出雏形。
- 已覆盖首次启动、工作区、搜索、设置、常见弹窗、toast、部分 Agent / Cloud / CLI 相关路径。
- 已完成多轮 release gate、bundle 构建验证和模块审查方案。
- 已新增隐私防护流程，阻止 GUI 截图、录屏、原始测试日志等敏感产物进入 Git 提交或推送。
- 当前仍不是完整公开 RC，真实账号、计费、云端状态、custom inference 删除确认等路径仍需要隔离账号继续验证。

更详细的进度记录在 `docs/` 中维护，README 只保留面向读者的摘要。

## 待完成内容

下一阶段重点：

- 继续逐条校准翻译准确性，优先审查高可见、高风险 UI 文案。
- 继续收敛 `workspace`、`settings`、`modals`、Agent 和 terminal 相关残留英文。
- 用隔离测试账号补齐登录、Billing、Cloud、自定义推理 endpoint 删除等 public-RC 证据。
- 将 manifest v2 元数据覆盖率继续提高，便于后续迁移到官方 locale 格式。
- 等待或推动 Warp 官方 i18n 框架成熟后，将当前清单迁移为官方 `zh-CN` 语言资源。

## 汉化实现方式

核心文件：

| 文件 | 用途 |
| --- | --- |
| `resources/localization/zh-Hans-overrides.toml` | 翻译清单，记录源文件、英文原文和中文译文 |
| `resources/localization/zh-Hans-inventory-ignore.toml` | inventory 忽略规则，排除非 UI 字符串 |
| `resources/localization/zh-Hans-glossary.toml` | 术语表规则，维护保留词、固定译法和禁用译法 |
| `script/zh_apply_localization.py` | 应用或校验翻译清单 |
| `script/zh_localization_inventory.py` | 扫描候选英文字符串和覆盖率 |
| `script/zh_export_locale.py` | 导出 JSON/YAML locale 雏形 |
| `script/privacy_guard.py` | 阻止截图、录屏、原始 GUI 证据等敏感产物进入 Git |

翻译应用脚本是幂等的：源码仍是英文时会替换为中文；源码已经是中文时会视为已应用；如果英文原文和中文目标都找不到，会提示上游字符串可能已经漂移。

## 快速开始

本仓库包含 Git LFS 文件：

```bash
git clone https://github.com/Drew1811266/Warp-CN.git
cd Warp-CN
git lfs install
git lfs pull
```

建议先启用本地隐私防护 hooks：

```bash
sh script/install_privacy_hooks.sh
```

校验汉化清单：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
```

重新应用翻译：

```bash
python3 script/zh_apply_localization.py
cargo fmt
```

构建并运行：

```bash
./script/bootstrap --skip-common-skills
./script/run
```

非交互式构建 bundle：

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

> [!NOTE]
> 当前 app crate 的 package 名称是 `warp`，因此请使用 `cargo check -p warp`。

## 常用验证

发布或同步上游前，至少运行：

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 -m unittest script.test_zh_apply_localization script.test_zh_localization_inventory script.test_zh_export_locale script.test_privacy_guard
cargo fmt --check
git diff --check
cargo check -p warp
```

如果改动涉及具体 UI 模块，还需要补充对应模块测试和人工 GUI 冒烟。

## 继续汉化

生成候选字符串清单：

```bash
python3 script/zh_localization_inventory.py --preset workspace --status candidate
python3 script/zh_localization_inventory.py --preset settings --status candidate
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

新增翻译条目时，优先使用 manifest v2 元数据：

```toml
[[replace]]
key = "workspace.example.open"
path = "app/src/example.rs"
source = "Open"
target = "打开"
context = "Example toolbar action"
status = "active"
preserve_terms = ["Warp"]
expected_count = 1
```

不要翻译命令语法、协议字段、配置 key、遥测事件名、测试字符串和内部日志，除非确认它们是用户可见 UI。

## 维护文档

- `docs/zh-Hans-localization.md`：主维护记录和总体流程。
- `docs/zh-Hans-upstream-sync.md`：同步上游 stable 的流程。
- `docs/zh-Hans-gui-smoke-matrix.md`：GUI 冒烟矩阵和 manual gate。
- `docs/zh-Hans-review-checklist.md`：模块审查和翻译质量检查清单。
- `docs/zh-Hans-full-translation-audit.md`：逐条翻译审查台账。
- `docs/zh-Hans-functional-risk-register.md`：高风险字符串处理规则。
- `docs/zh-Hans-evidence-policy.md`：GUI 证据和隐私产物处理规则。

## 常见问题

### 这是完整汉化版吗？

不是。它是高可见路径优先的简体中文本地化分支。当前已经覆盖大量常用界面，但仍会遇到低频英文路径。

### 为什么不是运行时语言包？

因为上游 Warp 当前还没有完整的一方应用语言设置或成熟 UI localization framework。本项目暂时采用源码级 overlay，后续目标是迁移为官方 locale。

### 为什么有些英文保留？

有些英文是产品名、命令语法、配置 key、协议字段或内部标识符。翻译这些字符串可能破坏功能或造成使用混乱。

## 上游项目

- 官方网站：[warp.dev](https://www.warp.dev)
- 上游仓库：[warpdotdev/warp](https://github.com/warpdotdev/warp)
- 官方文档：[docs.warp.dev](https://docs.warp.dev)

## 许可证

本仓库基于 Warp 开源客户端。

- `warpui_core` 和 `warpui` crates 使用 [`LICENSE-MIT`](LICENSE-MIT)。
- 其余代码使用 [`LICENSE-AGPL`](LICENSE-AGPL)。

本地化翻译和维护脚本随本 fork 一并发布，但不改变上游项目原有许可证要求。
