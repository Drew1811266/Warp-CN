# Warp CN Packaging Preflight

Date: 2026-06-03

## 目标

这份文档记录 2026-06-03 的 packaging 预检状态，只覆盖低负载检查与后续重型 gate 的边界，不生成 bundle，也不启动 GUI。

## 已运行的低负载检查

以下命令已运行，并返回当前基线结果：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

当前低负载基线摘要：

```text
manifest validation passed
glossary check passed
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0
preset: release
covered: 8574
candidates: 2
coverage: 100.0%
total: 11
public_rc_required: 11
errors: 11
decision: fail
```

## Heavy Gate

heavy gate 未运行。

需要未来明确批准后再执行的重型 gate 命令：

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

## 本次产物边界

- 本次没有产生 bundle 证据。
- 本次没有产生 GUI 证据。
- 本次没有产生任何发布候选或 tag/release 相关产物。
