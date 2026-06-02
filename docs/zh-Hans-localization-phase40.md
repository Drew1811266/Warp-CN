# zh-Hans Localization Phase 40

Date: 2026-06-02 Asia/Shanghai

## Goal

Produce RC10 after source backlog reduction, current-source fixture GUI evidence, and the isolated account/backend-state blocker audit.

## Final Gate

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_localization_inventory.py app/src/terminal --coverage
python3 script/zh_localization_inventory.py app/src/ai --coverage
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc10.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc10.json > /tmp/warp-cn-zh-Hans-locale-rc10.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc10.yaml
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
cargo check -j 2 -p warp
```

The final dry-run was executed with a low-duty-cycle Python wrapper to reduce sustained CPU load. It returned successfully:

```text
entries: 6786
files: 342
already_applied: 4973
would_change: 0
missing: 0
```

## Metrics

Manifest metadata:

```text
entries: 6786
context: 6786 (100.0%)
status: 6786 (100.0%)
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 4093 covered, 1510 candidates, 73.1%
release: 7427 covered, 1514 candidates, 83.1%
terminal: 1448 covered, 918 candidates, 61.2%
AI / Agent: 2098 covered, 592 candidates, 78.0%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc10.json: 2192949 bytes
/tmp/warp-cn-zh-Hans-locale-rc10.pretty.json: 2568910 bytes
/tmp/warp-cn-zh-Hans-locale-rc10.yaml: 1867072 bytes
```

## Release Candidate

Created:

- `docs/zh-Hans-release-candidate-2026-06-01-rc10.md`

Decision:

```text
ready-for-local-use-with-fixture-evidence
```

Public RC remains not ready because Phase 39 could not run account/backend-state rows without disposable test prerequisites.

## Low-Load Review

The final gate used:

- Sequential Python checks.
- `nice -n 10` or `nice -n 15` for longer commands.
- A throttled dry-run wrapper.
- `CARGO_BUILD_JOBS=2` and `cargo check -j 2 -p warp`.
- No concurrent Rust/Python full scans or GUI smoke.
- No lingering `warp-oss`, `terminal-server`, `cargo`, `rustc`, or localization Python processes after the gate.

## Qualification

Phase 40 is accepted as `qualified-rc10-gate`.

The phase is qualified because the final dry-run is clean, JSON/YAML exports complete, JSON parses, Python tests pass, formatting and diff checks pass, low-concurrency `cargo check -j 2 -p warp` passes, and the RC10 decision preserves the public-RC blocker until true isolated account/backend evidence exists.
