# zh-Hans 私有审批路由状态

日期：2026-06-03

## 范围

本文只记录 `Task 2 / Lane 1` 的公开路由状态和后续私有审批动作。它不包含原始
fixture 数据、账号标识、backend object 细节、candidate evidence、support 邮件正
文、私有 thread 内容、截图、录屏或完整日志。

## 公开路由记录

- GitHub issue：<https://github.com/warpdotdev/warp/issues/12129>
- 当前状态：`OPEN`
- 路由结论：该 issue 已确认为私有 zh-Hans RC release-evidence /
  fixture-owner approval 路由请求，不是公开 Warp client bug。
- 最新公开建议：继续避免在 GitHub 公开 issue 中发布 raw fixture data、account
  identifiers、backend object details 或 evidence；改走 private support 或内部
  owner channel。

## 推荐私有渠道

| 场景 | 推荐渠道 | 用途 |
| --- | --- | --- |
| backend routing、subscriber technical、credits 支持 | `support@warp.dev` | backend fixture owner approval 的首选入口 |
| billing/accounting decision | `billing@warp.dev` | 仅在 support 要求转 billing 或确需账务决策时使用 |
| Enterprise 或内部 test-team 流程 | Enterprise/account-manager Slack | 仅在该 RC 流程绑定企业或内部测试团队时使用 |

## 当前审批状态

- 私有请求草稿：已在 Git 外生成，路径为
  `/tmp/warp-cn-backend-fixture-private-support-request.md`。
- 私有发送状态：已通过 macOS Mail app 发往 `support@warp.dev`。
- 发送复查：2026-06-03 18:24 CST，Mail Outbox 复查为 `0`。
- 背景说明 follow-up：已通过 macOS Mail app 发往 `support@warp.dev`，主题为
  `Context for Warp CN zh-Hans localization fork request`。
- follow-up 发送复查：2026-06-03 18:44 CST，Mail Outbox 复查为 `0`。
- support 自动回执：已收到两封 `Warp Support` 自动回执，时间分别为
  2026-06-03 18:24 CST 和 2026-06-03 18:44 CST。
- 回执性质：headers 标记为 Front 自动回复；未包含 fixture owner approval、
  reviewed evidence acceptance、cleanup proof 或人工 owner route。
- Gmail follow-up：2026-06-05 10:27 CST，经用户确认后，已使用 GitHub-linked
  Gmail account 重新发往 `support@warp.dev`，主题为
  `Warp CN zh-Hans localization fork context and private approval route`。
- Gmail 发送复查：Gmail UI 返回 `邮件已发送`；尚未收到新的 support case、人工回
  复或 owner route。
- support case：尚未收到。
- 私有 thread：尚未收到。
- `approval_channel`：`support@warp.dev`
- `approval_reference`：`pending-support-case-or-owner-approval`
- `owner_approval`：未收到。
- `approved_rows`：未批准；待审批 row scope 为 `GUI-BILL-01`, `GUI-BILL-02`,
  `GUI-CLOUD-01`, `GUI-SET-04`, `GUI-SET-05`。
- `raw_evidence_review_required`：`true`
- `redacted_artifact_review_required`：`true`
- `cleanup_proof_required`：`true`

## 下一步

1. 等待 `support@warp.dev` 返回 support case、路由建议或 owner channel。
2. 如果 support 指示需要账务判断，仅转发最小必要上下文到 `billing@warp.dev`。
3. 如果 support 指示需要内部 owner channel，只迁移最小必要上下文，不迁移原始
   evidence。
4. 收到明确 owner approval 后，只在 repo-facing 文档中记录脱敏摘要：
   `approval_channel`、`approval_reference`、`approved_rows`、
   `raw_evidence_review_required`、`redacted_artifact_review_required` 和
   `cleanup_proof_required`。
5. 不提交 support 邮件全文、私有 thread 内容、账号标识、fixture ID、backend
   object ID、raw evidence 或 candidate evidence。

## 安全边界

- public GitHub issue #12129 只作为 routing record。
- support case ID、thread URL 或 Slack permalink 必须脱敏后再写入 Git。
- support case 本身不能替代 owner approval 或 reviewer acceptance。
- 未收到私有 owner approval 前，不创建 backend fixture candidate 文件，不更新
  evidence ledger，不修改 blocker ledger。
