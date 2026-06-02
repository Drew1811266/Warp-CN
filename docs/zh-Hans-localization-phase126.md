# zh-Hans Localization Phase 126

Date: 2026-06-02

## Scope

Phase 126 froze the RC21 readiness decision after Phases 119 through 125. It ran
the final low-load validation bundle and did not launch GUI, build a bundle,
generate PNGs, log in, open browser auth, create backend fixtures, touch billing
or cloud state, create/delete managed secrets or endpoints, or mutate team
state.

## Final Validation Commands

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
result: manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
result: glossary check passed

nice -n 10 python3 script/zh_apply_localization.py --metadata-summary
entries: 7943
key: 150 (1.9%)
context: 7943 (100.0%)
status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
notes: 0 (0.0%)
expected_count: 195 (2.5%)

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0

nice -n 10 python3 script/zh_public_rc_status.py
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

## Export Gates

```text
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc21.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc21.json > /tmp/warp-cn-zh-Hans-locale-rc21.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc21.yaml
result: passed
```

Export sizes:

```text
/tmp/warp-cn-zh-Hans-locale-rc21.json: 2566862 bytes
/tmp/warp-cn-zh-Hans-locale-rc21.pretty.json: 3004049 bytes
/tmp/warp-cn-zh-Hans-locale-rc21.yaml: 2184303 bytes
```

## Python Gates

```text
nice -n 10 python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/zh_public_rc_status.py script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py
result: passed

nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py
result: 25 tests passed
```

## Rust Fixture Test

```text
CARGO_BUILD_JOBS=1 nice -n 15 cargo test -j 1 -p warp lifecycle_smoke_fixture -- --nocapture
result: 2 tests passed, 0 failed, 4715 filtered out
compile mode: single-job, nice priority
```

The command generated existing app crate warnings unrelated to the Phase 122
fixture slice.

## Format, Whitespace, And PNG Gates

```text
nice -n 10 cargo fmt --check
result: passed

git diff --check
result: passed

git status --short -- '*.png'
result: no output

git diff --name-only -- '*.png'
result: no output
```

## Heavy And GUI Gate Status

```text
Rust full compile: skipped-with-heat-safety
command not run: CARGO_BUILD_JOBS=1 nice -n 15 cargo check -j 1 -p warp

bundle build / GUI launch: skipped-with-heat-safety
PNG generation: not run, no approval
account/backend/billing/cloud/secret/endpoint/team operations: not run
```

## RC21 Record

```text
docs/zh-Hans-release-candidate-2026-06-02-rc21.md
```

## Decision

```text
RC21 decision: ready-for-local-use-with-fixture-evidence
public RC decision: not ready
```

## Qualification Review

```text
phase: 126
status: qualified-rc21-freeze
low-load final validation bundle: passed
targeted Rust fixture tests: passed
public-RC blocker script output included: yes
heavy full compile: skipped with heat-safety reason
bundle and GUI: skipped with heat-safety reason
PNG status: no changes
RC21 record exists: yes
overview updated: yes
public-RC blockers cleared: none
external operations run: none
```
