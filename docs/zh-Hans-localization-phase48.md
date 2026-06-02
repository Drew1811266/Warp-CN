# zh-Hans Localization Phase 48

Date: 2026-06-02 Asia/Shanghai

## Goal

Produce RC11 after source, fixture-GUI, static visual-asset, and public-RC external-state reviews.

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
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc11.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc11.json > /tmp/warp-cn-zh-Hans-locale-rc11.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc11.yaml
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
CARGO_BUILD_JOBS=2 cargo check -j 2 -p warp
```

Final dry-run:

```text
entries: 7088
files: 367
already_applied: 5124
would_change: 0
missing: 0
```

## Metrics

Manifest metadata:

```text
entries: 7088
context: 7088 (100.0%)
status: 7088 (100.0%)
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 4423 covered, 1187 candidates, 78.8%
release: 7757 covered, 1191 candidates, 86.7%
terminal: 1653 covered, 718 candidates, 69.7%
AI / Agent: 2223 covered, 469 candidates, 82.6%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc11.json: 2291118 bytes
/tmp/warp-cn-zh-Hans-locale-rc11.pretty.json: 2681668 bytes
/tmp/warp-cn-zh-Hans-locale-rc11.yaml: 1950745 bytes
```

## Release Candidate

Created:

- `docs/zh-Hans-release-candidate-2026-06-02-rc11.md`

Decision:

```text
ready-for-local-use-with-fixture-evidence
```

Public RC remains not ready because Phase 46 could not run account/backend-state rows without disposable test prerequisites, and Phase 45 deferred onboarding visual residue to design regeneration.

## Low-Load Review

The final gate used:

- Sequential Python checks.
- `nice -n 10` for longer Python and Rust commands.
- `CARGO_BUILD_JOBS=2` and `cargo check -j 2 -p warp`.
- No concurrent Rust/Python full scans.
- No GUI launch.
- No account/backend/destructive-object interaction.

## Qualification

Phase 48 is accepted as `qualified-rc11-gate`.

The phase is qualified because the final dry-run is clean, JSON/YAML exports complete, JSON parses, Python tests pass, formatting and diff checks pass, low-concurrency `cargo check -j 2 -p warp` passes, and the RC11 decision clearly separates source coverage, fixture GUI evidence, visual-residue policy, and public-RC external-state blockers.
