# zh-Hans Localization Phase 54

Date: 2026-06-02 Asia/Shanghai

## Goal

Produce RC12 after the post-RC11 queue, terminal visible-UI pass, terminal executor/protocol pass, AI/Agent backlog pass, and visual/public-RC blocker refresh.

## Final Gate

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
rg -n 'target = ".*(智能体|智能代理|智能助手|智能助理|命令调色板|端点点|帐号)' resources/localization/zh-Hans-overrides.toml
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary --json
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py --preset onboarding --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset workspace --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset search --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset settings --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset modals --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/ai --coverage
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc12.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc12.json > /tmp/warp-cn-zh-Hans-locale-rc12.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc12.yaml
nice -n 10 python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt --check
git diff --check
CARGO_BUILD_JOBS=2 nice -n 10 cargo check -j 2 -p warp
```

Final dry-run:

```text
entries: 7372
files: 399
already_applied: 5261
would_change: 0
missing: 0
```

The forbidden/awkward target-term search returned no matches.

## Metrics

Manifest metadata:

```text
entries: 7372
key: 150 (2.0%)
context: 7372 (100.0%)
status: 7372 (100.0%)
preserve_terms: 18 (0.2%)
notes: 0
expected_count: 171 (2.3%)
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 4736 covered, 879 candidates, 84.3%
release: 8070 covered, 883 candidates, 90.1%
terminal: 1850 covered, 524 candidates, 77.9%
AI / Agent: 2339 covered, 355 candidates, 86.8%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc12.json: 2381963 bytes
/tmp/warp-cn-zh-Hans-locale-rc12.pretty.json: 2786034 bytes
/tmp/warp-cn-zh-Hans-locale-rc12.yaml: 2027958 bytes
```

## Release Candidate

Created:

- `docs/zh-Hans-release-candidate-2026-06-02-rc12.md`

Decision:

```text
ready-for-local-use-with-fixture-evidence
```

Public RC remains not ready because isolated account/backend-state evidence is still unavailable and the onboarding PNG residue still needs regenerated Chinese-localized preview art or explicit design approval.

## Low-Load Review

The final gate used:

- Sequential Python checks.
- `nice -n 10` for longer Python, formatting, and Rust commands.
- `CARGO_BUILD_JOBS=2` and `cargo check -j 2 -p warp`.
- No concurrent Rust/Python full scans.
- No GUI launch.
- No account/backend/destructive-object interaction.

`cargo check -j 2 -p warp` passed with existing unused-variable warnings in `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` and `app/src/terminal/input/slash_commands/mod.rs`.

## Qualification

Phase 54 is accepted as `qualified-rc12-gate`.

The phase is qualified because the manifest and glossary gates pass, the final dry-run is clean, JSON/YAML exports complete, JSON parses, Python tests pass, formatting and diff checks pass, low-concurrency `cargo check -j 2 -p warp` passes, and the RC12 decision keeps source localization progress separate from visual-asset and public-RC external-state blockers.
