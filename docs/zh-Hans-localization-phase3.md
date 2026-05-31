# Warp CN Phase 3 汉化资产化与发布流程固化

## 1. 阶段定位

Phase 2 已经把本项目从首轮高可见汉化推进到可发布审计状态。当前 `zh-Hans-overrides.toml` 有 2556 条翻译、覆盖 186 个源码文件，`dry-run` 已能稳定报告上游字符串漂移。

Phase 3 的目标不是继续盲目提高覆盖率，而是把当前源码级汉化流程升级为长期可维护、可审计、可迁移的汉化 overlay 工程。

核心判断：

- 中文源码是应用 manifest 后的工作树状态。
- 真正的长期资产是 manifest、术语表、忽略规则、验证矩阵、同步流程和 GUI 复验记录。
- 在 Warp 官方 i18n 机制成熟前，本项目继续维护社区中文构建版；一旦官方 locale 机制可用，Phase 3 产物应能迁移为官方 `zh-CN` locale。

## 2. 当前基线

基线日期：2026-05-30。

```text
entries: 2556
files: 186
already_applied: 2541
would_change: 0
missing: 0
```

主要剩余候选热点：

| 预设 | 热点路径 | 解读 |
| --- | --- | --- |
| `workspace` | `app/src/workspace/view.rs`, `app/src/workspace/mod.rs`, `app/src/workspace/tab_settings.rs` | 仍混有菜单、toast、worktree 诊断和内部命令文本，需要继续按真实 UI 审核。 |
| `settings` | `app/src/settings_view/features_page.rs`, `app/src/settings_view/mod.rs`, `app/src/settings_view/teams_page.rs` | 候选包含搜索词、feature metadata 和团队管理深层路径，不能批量翻译。 |
| `modals` | `app/src/terminal/view.rs`, `app/src/terminal/view/action.rs`, `app/src/terminal/input.rs`, `app/src/ai/agent/mod.rs` | 终端、Agent transcript 和低层错误占大头，应继续分类处理。 |

## 3. 非目标

Phase 3 不做：

- 不引入运行时语言切换。
- 不重构 Warp UI i18n runtime。
- 不为了覆盖率翻译终端协议、telemetry、settings key、搜索 tag、命令 token、测试文本或内部日志。
- 不追随上游 dev/nightly 做用户发布；用户发布只跟 stable 或明确选定的上游基线。
- 不一次性给 2556 条 manifest 全部补齐元数据；先建立 schema 和样例，再按高价值路径渐进迁移。

## 4. Manifest v2 方向

现有条目继续兼容：

```toml
[[replace]]
path = "app/src/example.rs"
source = "Open"
target = "打开"
```

新条目可以逐步增加元数据：

```toml
[[replace]]
key = "settings.ai.bedrock.login_command"
path = "app/src/settings_view/ai_page.rs"
source = "Login Command"
target = "登录命令"
context = "AI settings AWS Bedrock credentials form label"
status = "active"
preserve_terms = ["AWS Bedrock", "Warp"]
notes = "Provider and product names stay in English."
expected_count = 1
```

字段含义：

| 字段 | 类型 | 要求 |
| --- | --- | --- |
| `path` | string | 必填，仓库根目录相对路径。 |
| `source` | string | 必填，上游英文 Rust 字符串字面量。 |
| `target` | string | 必填，简体中文目标文案。 |
| `key` | string | 可选但推荐，未来 locale 迁移用稳定 ID。 |
| `context` | string | 可选，说明 UI 位置或触发场景。 |
| `status` | string | 可选，允许 `active`、`needs-review`、`deprecated`、`blocked`。 |
| `preserve_terms` | array[string] | 可选，必须保留英文的产品名、命令或品牌词。 |
| `notes` | string | 可选，记录漂移、占位符、视觉或验证风险。 |
| `expected_count` | integer | 可选，要求该 source 在目标文件中出现的次数。 |

## 5. 里程碑

### P3-M0：阶段文档与维护入口

交付：

- `docs/zh-Hans-localization-phase3.md`
- 更新 `docs/zh-Hans-localization.md`
- 视需要更新 `README.md`

验收：

- 文档明确 Phase 3 是资产化和发布流程固化，不是继续追覆盖率。
- 维护流程包含 manifest schema 校验命令。

### P3-M1：Manifest v2 兼容与校验

交付：

- `script/zh_apply_localization.py` 支持 v2 元数据字段。
- 新增 `--validate-manifest`。
- 新增脚本单测覆盖元数据读取、重复 key、非法 status 和 v1 兼容性。

验收：

```bash
python3 script/test_zh_apply_localization.py
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 -m py_compile script/zh_apply_localization.py script/test_zh_apply_localization.py
```

### P3-M2：Inventory ignore 规则外置

交付：

- 新建 `resources/localization/zh-Hans-inventory-ignore.toml`。
- 将当前脚本内的精确路径、路径片段、line pattern、literal pattern 逐步外置。
- 新增文档规则：新增排除项前必须先审查候选内容并记录原因。
- `script/zh_localization_inventory.py` 默认读取该配置，也支持 `--ignore-config` 指向临时配置。

验收：

```bash
python3 script/test_zh_localization_inventory.py
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
python3 -m py_compile script/zh_localization_inventory.py script/test_zh_localization_inventory.py
```

### P3-M3：术语表机器化

交付：

- 新建 `resources/localization/zh-Hans-glossary.toml`。
- 固化产品名、保留词、固定译法和禁止译法。
- 新增 glossary 校验，避免同义不同译或误译保留词。
- 第一版规则保持保守，不强制历史条目中的 `Notebook`、`API keys` 等既有译法立即统一。

验收：

```bash
python3 script/test_zh_apply_localization.py
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 -m py_compile script/zh_apply_localization.py script/test_zh_apply_localization.py
```

### P3-M4：GUI 冒烟矩阵结构化

交付：

- 新建 `docs/zh-Hans-gui-smoke-matrix.md`。
- 将已有 manual gate 拆成路径、触发条件、账号需求、期望中文、最近验证日期和当前状态。
- 将 README 和维护文档指向该矩阵，后续 release smoke 只在矩阵中更新状态。

验收：

- 每个 manual gate 都能说明为什么不能自动验证。
- 不把进程启动等同于视觉验收。
- `git diff --check` 通过。

### P3-M5：上游 stable 适配流程

交付：

- 新建 `docs/zh-Hans-upstream-sync.md`。
- 固定 stable-first 发布策略和上游同步检查顺序。
- README 和维护文档指向该流程，避免继续使用只写 `origin/master` 的简略同步步骤。

验收：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

### P3-M6：Locale 导出雏形

交付：

- 新增 `script/zh_export_locale.py`。
- 从 manifest 导出 JSON 或 YAML，用于未来迁移到官方 locale 格式。
- 新增导出脚本单测，覆盖内部字段剥离、UTF-8 JSON 和人工可读 YAML。

验收：

```bash
python3 script/test_zh_export_locale.py
python3 -m py_compile script/zh_export_locale.py script/test_zh_export_locale.py
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
python3 - <<'PY'
import json
from pathlib import Path
json.loads(Path("/tmp/zh-CN.json").read_text(encoding="utf-8"))
PY
```

## 6. 执行规则

1. 每个切片先验证 manifest，再应用翻译或更新工具。
2. 新增元数据不得改变现有替换行为。
3. 新增 ignore 规则必须有可审计理由，不能为了提高覆盖率隐藏真实 UI。
4. GUI 路径无法触发时记录为 manual gate，不声称已完成视觉验收。
5. 每次上游同步都记录 upstream commit/tag、dry-run 结果、coverage 快照和 GUI gate 状态。
