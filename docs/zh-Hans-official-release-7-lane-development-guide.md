# Warp CN 正式汉化发行版 7-Lane 开发文档

日期：2026-06-03

## 目的

这份文档把正式汉化发行版的后续工作拆成 7 条可执行 lane。它面向
`Subagent-Driven` 或人工分工执行，目标是把当前状态从
`ready-for-local-use-with-fixture-evidence` 推进到可发布的正式汉化发行版。

当前公开 GitHub issue
[warpdotdev/warp#12129](https://github.com/warpdotdev/warp/issues/12129)
已经被确认为“私有 release-evidence / fixture-owner approval 路由请求”，不是
公开 Warp client bug。后续 fixture approval、reviewed redacted evidence 和
cleanup proof 必须走私有支持或内部 owner 渠道，不能继续在公开 GitHub issue
中贴原始证据。

## 当前基线

| 项目 | 当前值 |
| --- | --- |
| 版本线 | `0.18 -> 0.19 draft` |
| 最近 RC | `2026-06-03 RC38` |
| 当前结论 | `ready-for-local-use-with-fixture-evidence` |
| Manifest 条目 | 7,943 |
| 覆盖文件 | 552 |
| 已应用条目 | 5,690 |
| 待应用变更 | 0 |
| 丢失或漂移条目 | 0 |
| Release inventory | 8,574 covered / 2 candidates / 100.0% |
| Public-RC blocker | 11 |
| Ready evidence rows | 0 |
| Strict artifact lint | 预期失败，直到 11 条 evidence row 全部提供 |

当前主要问题不是大规模翻译缺失，而是正式发行所需的私有审批、证据、GUI、
打包和发布闭环尚未完成。

## 总体完成标准

正式汉化发行版只能在以下条件同时成立后推进：

1. `python3 script/zh_apply_localization.py --dry-run --summary` 保持
   `would_change: 0` 和 `missing: 0`。
2. `python3 script/zh_localization_inventory.py --preset release --coverage`
   保持 release coverage 100.0%。
3. 11 条 public-RC blocker 全部有 reviewed redacted artifact 和 evidence
   ledger 记录。
4. `python3 script/zh_public_rc_evidence_lint.py --strict-artifacts` 通过。
5. GUI smoke、静态资产、bundle、低负载 gate、privacy guard 和 diff check 通过。
6. 发布说明、README、RC 记录、版本号和 Git tag 策略一致。
7. 用户明确批准 tag、push 和 GitHub release。

## Lane 总览

| Lane | 目标 | 当前状态 | 完成信号 |
| --- | --- | --- | --- |
| 1. 私有审批路由 | 把公开 GitHub 路由记录转成可执行的私有审批请求 | GitHub 已确认应转私有渠道 | support/internal thread ID 和 owner approval 格式存在 |
| 2. 证据与脱敏 | 建立 reviewed redacted candidate 到 artifact 的闭环 | 模板和 preflight 已有，真实证据未提供 | 11 条 candidate 均通过 human review 和 preflight |
| 3. 阻塞行关闭 | 逐行关闭 backend/isolated/disposable blockers | 11 条 blocked | strict artifact lint 通过 |
| 4. 隔离账号和一次性对象准备 | 准备不污染真实账号和真实对象的测试环境 | 文档已有，批准未完成 | isolated account 和 disposable object approval packet 完整 |
| 5. 翻译完整性与质量 | 证明源码级汉化仍干净且术语一致 | 当前 clean | manifest/glossary/dry-run/inventory/status 全部通过 |
| 6. 打包与发布工程 | 生成可验证、可回滚的发行候选 | heavy gate 未跑 | bundle、GUI launch、privacy 和 diff gate 通过 |
| 7. 发布说明与验收 | 固化用户可读 release material 和 go/no-go | 0.19 draft-only | final release notes、checklist、tag approval ready |

## Lane 1：私有审批路由

### 目标

把公开 GitHub issue 的结论转化为私有、可跟踪、可审计的审批路线。这个 lane 不
收集证据、不清 blocker，只解决“谁批准、在哪里批准、批准文本是什么格式”。

### 输入

- GitHub 路由记录：
  [warpdotdev/warp#12129](https://github.com/warpdotdev/warp/issues/12129)。
- 本地 backend fixture intake bundle：
  `/tmp/warp-cn-backend-fixture-intake/`。
- 本地 isolated account intake bundle：
  `/tmp/warp-cn-isolated-account-intake/`。
- 本地 disposable object intake bundle：
  `/tmp/warp-cn-disposable-object-intake/`。

### 私有渠道选择

| 情况 | 渠道 |
| --- | --- |
| backend routing、subscriber technical、credits 相关支持 | `support@warp.dev` |
| billing/accounting decision | `billing@warp.dev` |
| Enterprise 或内部 test-team 流程 | Enterprise/account-manager Slack |
| 公开状态留痕 | GitHub issue #12129 只保留 routing record |

### 执行步骤

1. 从 `/tmp/warp-cn-backend-fixture-intake/owner-approval-request.md` 提取
   私有审批请求正文。
2. 在正文顶部补充 GitHub 路由结论：

```text
Public GitHub issue #12129 confirmed this is not a public Warp client bug and
should be routed through private support/internal owner channels. No raw fixture
data, account identifiers, backend object details, or evidence should be shared
in GitHub.
```

3. 通过 `support@warp.dev` 发起 backend routing 请求；如果被要求转 billing，
   再向 `billing@warp.dev` 发送最小必要上下文。
4. 记录返回的 case ID、thread URL 或 Slack permalink，但不要把私有 thread
   内容、账号标识、fixture ID 或原始证据提交到 Git。
5. 得到 owner approval 后，只允许把审批摘要写入 repo-facing 文档：

```text
approval_channel: private-support-or-internal-owner
approval_reference: <case-id-or-redacted-thread-reference>
approved_rows: GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01, GUI-SET-04, GUI-SET-05
raw_evidence_review_required: true
redacted_artifact_review_required: true
cleanup_proof_required: true
```

### 产物

- 私有：support case、Slack thread、owner approval。
- Git 外：reviewed raw evidence、candidate evidence 文本。
- Git 内：只允许写入脱敏 approval summary 和后续 evidence metadata。

### 验收

Lane 1 完成必须同时满足：

- 明确 owner 或 support route。
- 明确 approval reference。
- 明确哪些 row 被批准。
- 明确 raw evidence reviewer 和 redaction reviewer。
- 明确 cleanup proof 要求。

### No-Go

- 不在 GitHub 公开 issue 里贴 raw fixture、账号、backend object、candidate
  artifact、截图或录屏。
- 不把私有 support 邮件全文提交到 Git。
- 不把 support case 误当成 evidence approval；必须有 owner approval 或
  reviewer acceptance。

## Lane 2：证据与脱敏

### 目标

建立从 raw evidence 到 reviewed redacted artifact 的可重复流程。这个 lane 的
完成标准不是“截图拍到了”，而是“候选文本通过工具预检、人审、隐私规则和 ledger
一致性检查”。

### 输入

- 已批准的 fixture/account/object。
- Git 外 raw evidence。
- Git 外 candidate 文件。
- `script/zh_public_rc_evidence_candidate.py`。
- `script/zh_public_rc_evidence_lint.py`。
- `docs/zh-Hans-evidence-policy.md`。

### Git 外 candidate 文件路径

| Row | Git 外 candidate |
| --- | --- |
| `GUI-AUTH-01` | `/tmp/gui-auth-01-candidate.txt` |
| `GUI-SET-03` | `/tmp/gui-set-03-candidate.txt` |
| `GUI-WS-06` | `/tmp/gui-ws-06-candidate.txt` |
| `GUI-SET-06` | `/tmp/gui-set-06-candidate.txt` |
| `GUI-WS-04` | `/tmp/gui-ws-04-candidate.txt` |
| `GUI-WS-07` | `/tmp/gui-ws-07-candidate.txt` |
| `GUI-BILL-01` | `/tmp/gui-bill-01-candidate.txt` |
| `GUI-BILL-02` | `/tmp/gui-bill-02-candidate.txt` |
| `GUI-CLOUD-01` | `/tmp/gui-cloud-01-candidate.txt` |
| `GUI-SET-04` | `/tmp/gui-set-04-candidate.txt` |
| `GUI-SET-05` | `/tmp/gui-set-05-candidate.txt` |

### 允许入库的 redacted artifact 路径

只在 human review 和 candidate preflight 均通过后，才能创建：

| Row | Git 内 redacted artifact |
| --- | --- |
| `GUI-AUTH-01` | `artifacts/redacted/gui-auth-01.txt` |
| `GUI-SET-03` | `artifacts/redacted/gui-set-03.txt` |
| `GUI-WS-06` | `artifacts/redacted/gui-ws-06.txt` |
| `GUI-SET-06` | `artifacts/redacted/gui-set-06.txt` |
| `GUI-WS-04` | `artifacts/redacted/gui-ws-04.txt` |
| `GUI-WS-07` | `artifacts/redacted/gui-ws-07.txt` |
| `GUI-BILL-01` | `artifacts/redacted/gui-bill-01.txt` |
| `GUI-BILL-02` | `artifacts/redacted/gui-bill-02.txt` |
| `GUI-CLOUD-01` | `artifacts/redacted/gui-cloud-01.txt` |
| `GUI-SET-04` | `artifacts/redacted/gui-set-04.txt` |
| `GUI-SET-05` | `artifacts/redacted/gui-set-05.txt` |

### Candidate preflight 命令

逐行运行，不要批量跳过失败行：

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-AUTH-01 --artifact /tmp/gui-auth-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-03 --artifact /tmp/gui-set-03-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-06 --artifact /tmp/gui-ws-06-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-06 --artifact /tmp/gui-set-06-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-04 --artifact /tmp/gui-ws-04-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-07 --artifact /tmp/gui-ws-07-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-01 --artifact /tmp/gui-bill-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-02 --artifact /tmp/gui-bill-02-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-CLOUD-01 --artifact /tmp/gui-cloud-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-04 --artifact /tmp/gui-set-04-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /tmp/gui-set-05-candidate.txt --markdown
```

每条都必须返回可进入 human review 的状态。若返回 rejected，停止该 row，不得
手动绕过。

### 必须脱敏的内容

- 账号邮箱、用户名、account ID、team ID、billing ID。
- callback URL、magic link、cookie、token、API key、endpoint URL。
- AWS、Bedrock、provider credential、secret value。
- 私有 object ID、fixture ID、workspace ID、cloud quota 细节。
- 原始截图、录屏、完整日志、support 邮件全文。

### 验收

Lane 2 完成必须满足：

- 11 条 Git 外 candidate 均存在。
- 11 条 candidate 均通过 preflight。
- redaction reviewer 明确接受。
- cleanup proof 格式明确。
- 还未写入 ledger 前，strict artifact lint 允许继续失败；写入后必须通过。

## Lane 3：阻塞行关闭

### 目标

把 11 条 public-RC blocker 从 blocked 状态推进到 evidence provided。这个 lane 是
release 的核心 gate。

### Row 分组

| Category | Rows | 数量 |
| --- | --- | ---: |
| `backend_fixture` | `GUI-BILL-01`, `GUI-BILL-02`, `GUI-CLOUD-01`, `GUI-SET-04`, `GUI-SET-05` | 5 |
| `isolated_account` | `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06` | 3 |
| `disposable_object` | `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07` | 3 |

### 执行顺序

1. 先关闭 `backend_fixture`，因为它数量最多，且依赖 private owner routing。
2. 再关闭 `isolated_account`，必须使用隔离测试账号。
3. 最后关闭 `disposable_object`，必须先验证取消路径，再执行删除或转让。
4. 每关闭一个 category，运行 category report 和 strict lint。

### Queue 和 missing-action 命令

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
```

### Evidence ledger 更新边界

只在以下条件同时满足时，才允许修改：

- `resources/localization/zh-Hans-public-rc-evidence.toml`
- `resources/localization/zh-Hans-public-rc-blockers.toml`

条件：

1. owner approval 或 explicit object/account approval 存在。
2. Git 外 raw evidence 已由 reviewer 审阅。
3. Git 外 candidate 已通过 preflight。
4. redacted artifact 已创建在 `artifacts/redacted/`。
5. cleanup proof 已脱敏。
6. `python3 script/privacy_guard.py --all-tracked` 通过。

### 验收命令

```bash
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py --json
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
python3 script/privacy_guard.py --all-tracked
git diff --check
```

Lane 3 完成时，`strict-artifacts` 必须退出 0，且 11 条 row 不再报告
`missing evidence`。

## Lane 4：隔离账号和一次性对象准备

### 目标

在不依赖官方 backend fixture 批准的情况下，先准备能安全执行的账号和对象路线。
这个 lane 只准备环境与审批，不擅自执行真实删除、转让或登录证据采集。

### Isolated account 要求

Rows:

- `GUI-AUTH-01`
- `GUI-SET-03`
- `GUI-WS-06`

Approval packet 必须包含：

```text
isolated account is not the user's main account
login flow is approved for public-RC evidence capture
Settings > AI visibility is approved
custom inference endpoint test object is named zh-smoke-delete-endpoint
logout or profile cleanup proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

### Disposable object 要求

Rows:

- `GUI-SET-06`
- `GUI-WS-04`
- `GUI-WS-07`

Allowlisted objects:

```text
zh-smoke-delete-environment
zh-smoke-delete-secret
zh-smoke-public-rc-team
```

Approval packet 必须包含：

```text
object exists and is disposable
object name exactly matches the allowlist
cancel-first path is approved
delete or transfer path is explicitly approved
cleanup absence or restoration proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

### 执行文档

- `docs/zh-Hans-public-rc-isolated-account-execution.md`
- `docs/zh-Hans-public-rc-disposable-object-execution.md`
- `docs/zh-Hans-public-rc-independent-lanes-execution.md`

### 验收

Lane 4 完成时必须存在：

- isolated account approval。
- disposable object approval。
- account logout/profile cleanup proof 格式。
- object delete/transfer cleanup proof 格式。
- allowlist 和 no-go 规则确认。
- post-approval evidence execution handoff 已明确。

## Lane 5：翻译完整性与质量

### 目标

证明当前发行候选不是“证据齐了但翻译漂了”。每次进入正式发行冻结前都要跑完整轻量级复扫。

### 必跑命令

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_public_rc_evidence_candidate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py
```

### 当前预期

在 11 条 evidence 未关闭前：

```text
manifest validation passed
glossary check passed
would_change: 0
missing: 0
release coverage: 100.0%
public-RC blockers: 11
strict artifact lint: fail
```

在 Lane 3 完成后：

```text
manifest validation passed
glossary check passed
would_change: 0
missing: 0
release coverage: 100.0%
public-RC blockers: 0 or all provided
strict artifact lint: pass
```

### 质量复核重点

- 不翻译命令、协议字段、配置 key、测试 fixture、telemetry event。
- 保留 `Agent` 等产品/功能术语，除非有统一迁移决策。
- 对 Settings、Billing、Cloud、Workspace、Danger confirmation 做人工中文语义复核。
- 检查中文长度是否可能挤压按钮、弹窗标题、菜单项。

### 验收

- 轻量级命令全部通过，或只剩 evidence 未提供导致的预期 strict lint failure。
- 若新增翻译条目，必须更新 `resources/localization/zh-Hans-overrides.toml` 并通过
  glossary、dry-run、inventory。
- `git diff --check` 通过。

## Lane 6：打包与发布工程

### 目标

生成可验证、可安装、可回滚的正式发行候选。这个 lane 不负责发布，只负责把
release artifact 做到可交付。

### 前置条件

- Lane 3 完成，strict artifact lint 通过。
- Lane 5 当前周期复扫通过。
- 用户明确批准运行重型 gate。
- 低负载 gate 允许继续。

### 低负载 gate

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

只有输出 `decision: run-heavy-gate` 时继续。

### Heavy gate

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
python3 script/privacy_guard.py --all-tracked
git diff --check
```

### GUI 和 bundle 验收

必须记录：

- `target/debug/bundle/osx/WarpOss.app` 的当前周期生成时间。
- GUI launch 是否成功。
- 是否有当前周期 GUI smoke matrix 证据。
- onboarding 静态 PNG 英文残留是否重生成或获得设计批准。
- 安装、启动、退出、重开是否无阻塞错误。

### 不在本 lane 执行的动作

- 不创建 tag。
- 不 push。
- 不创建 GitHub release。
- 不宣称 Warp 官方发行版。

## Lane 7：发布说明与验收

### 目标

把证据、质量、打包结果和用户可读说明汇总成最终 go/no-go 决策材料。

### 文档产物

正式发布前应准备：

- `docs/zh-Hans-release-notes-0.19.md`
- `docs/zh-Hans-official-release-checklist-0.19.md`
- `docs/zh-Hans-release-candidate-2026-06-03-formal.md`
- README 当前状态更新。
- `docs/zh-Hans-localization.md` 阶段索引更新。

当前已有草稿：

- `docs/zh-Hans-release-notes-0.19-draft.md`
- `docs/zh-Hans-packaging-preflight-2026-06-03.md`
- `docs/zh-Hans-translation-rescan-2026-06-03.md`

### 发布说明必须包含

```text
scope: Simplified Chinese localization fork
not official Warp release: true
source overlay status: clean
public-RC evidence status: complete
backend fixture approval: private route, redacted reference only
GUI smoke status: complete
packaging status: complete
known limitations: upstream official i18n still pending
support boundary: Warp official services remain upstream-controlled
```

### Final go/no-go checklist

```text
manifest validation: pass
glossary check: pass
dry-run would_change: 0
dry-run missing: 0
release inventory: 100.0%
public-RC evidence strict lint: pass
privacy guard: pass
unit tests: pass
low-load gate: pass
cargo check: pass
bundle build: pass
GUI launch: pass
release notes: final
README status: final
tag approval: explicit user approval
push approval: explicit user approval
GitHub release approval: explicit user approval
```

### 发布命令边界

以下命令只能在用户明确批准后执行：

```bash
git tag 0.19
git push github main
git push github 0.19
gh release create 0.19
```

如果发布版本号从 `0.19` 改为其他值，必须先同步 README、release notes、RC 记录和
tag 名称。

## 推荐执行顺序

1. Lane 1：发起私有审批路由，拿到 support/internal reference。
2. Lane 4：并行准备 isolated account 和 disposable object approval packet。
3. Lane 2：在审批返回后生成 Git 外 candidate，并逐行 preflight。
4. Lane 3：写入 reviewed redacted artifact 和 evidence ledger，关闭 11 条 blocker。
5. Lane 5：跑当前周期翻译完整性复扫。
6. Lane 6：在低负载和用户批准下跑 heavy gate、bundle、GUI。
7. Lane 7：冻结发布说明、验收清单、版本号，等待 tag/push/release 明确批准。

## Subagent-Driven 分派建议

| Subagent | Scope | 不允许做的事 |
| --- | --- | --- |
| Lane 1 worker | support/internal routing packet 和 approval reference 记录 | 不发送原始证据到公开 GitHub |
| Lane 2 worker | candidate schema、preflight、redaction checklist | 不创建未审阅 artifact |
| Lane 3 worker | evidence ledger 和 blocker closure | 不把未审阅 row 标为 provided |
| Lane 4 worker | isolated/disposable approval packets | 不用主账号，不删真实对象 |
| Lane 5 worker | manifest/glossary/inventory/unit tests | 不改 release 状态 |
| Lane 6 worker | heavy gate、bundle、GUI launch 记录 | 不 tag、不 push |
| Lane 7 worker | release notes、checklist、README 状态 | 不创建 GitHub release |

## 全局 No-Go

- 不使用个人主账号。
- 不使用真实 AWS、Bedrock、API key、token、cookie、magic link 或付款方式。
- 不创建、删除、转让或重置真实对象。
- 不把原始截图、录屏、回调 URL、账号标识、endpoint URL、billing ID、team ID、
  fixture ID 或 private object name 提交到 Git。
- 不在没有 reviewed redaction 和 cleanup proof 的情况下把 evidence row 标为
  `provided`。
- 不在没有用户明确批准时创建 tag、push 或 GitHub release。
