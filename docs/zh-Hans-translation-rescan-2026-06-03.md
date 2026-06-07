# Warp CN Translation Rescan

Date: 2026-06-03

## 结论

translation overlay clean，正式 release 仍然被 public-RC 证据阻塞。

## 轻量级命令结果

以下是本次 rescan 的精确轻量级结果：

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --metadata-summary
entries: 7943
key: 150 (1.9%)
context: 7943 (100.0%)
status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
notes: 0 (0.0%)
expected_count: 195 (2.5%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0

python3 script/zh_localization_inventory.py --preset release --coverage
preset: release
covered: 8574
candidates: 2
coverage: 100.0%

python3 script/zh_public_rc_status.py
zh-Hans public-RC blocker status
total: 11
public_rc_required: 11
statuses:
  blocked-no-backend-fixture: 5
  blocked-no-disposable-object: 3
  blocked-no-isolated-account: 3
categories:
  backend_fixture: 5
  disposable_object: 3
  isolated_account: 3

python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
zh-Hans public-RC evidence lint
total_required: 11
ready_rows: 0
missing_rows: 0
errors: 11
decision: fail
```

## Strict Artifact Lint

`python3 script/zh_public_rc_evidence_lint.py --strict-artifacts` 的实际输出包含 `missing_rows: 0`，但脚本同时报告了 11 条 `missing evidence` errors；按 release 规划语义，这表示还有 11 条 evidence row 仍未提供，因此 strict-artifact lint 依然应视为失败：

```text
error: GUI-AUTH-01: missing evidence
error: GUI-SET-03: missing evidence
error: GUI-SET-04: missing evidence
error: GUI-SET-05: missing evidence
error: GUI-SET-06: missing evidence
error: GUI-WS-04: missing evidence
error: GUI-WS-06: missing evidence
error: GUI-WS-07: missing evidence
error: GUI-BILL-01: missing evidence
error: GUI-BILL-02: missing evidence
error: GUI-CLOUD-01: missing evidence
```

## 结论

- translation overlay clean。
- manifest、glossary、metadata、dry-run 和 release coverage 都维持在当前可接受基线。
- formal release 仍然被 11 条 public-RC evidence 阻塞，不能推进到 publication。
