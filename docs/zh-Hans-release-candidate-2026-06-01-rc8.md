# zh-Hans Release Candidate 2026-06-01 RC8

RC8 is the Phase 19-25 post-RC7 localization record for Warp CN.

Decision: `ready-for-local-use-source-level`

Public RC decision: not ready.

## Scope

RC8 includes:

- Low-load GUI evidence recovery for base/settings anchors.
- Safe public-RC account/state runbook.
- Terminal backlog classification pass 2.
- Settings and Workspace second pass.
- AI SDK, execution profile editor, environment, secret, integration output, and requested command pass.
- Manifest metadata migration to full `context/status` coverage.
- Command-line, export, Python test, formatting, diff, and low-concurrency Rust compile gates.

RC8 does not claim first-party runtime i18n support, complete whole-repository localization, or public-RC GUI readiness.

## Manifest And Coverage

```text
python3 script/zh_apply_localization.py --metadata-summary --json
entries: 5487
key: 150 (2.7%)
context: 5487 (100.0%)
status: 5487 (100.0%)
preserve_terms: 18 (0.3%)
notes: 0 (0.0%)
expected_count: 150 (2.7%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 5487
files: 273
already_applied: 4318
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 817 covered, 49 candidates, 94.3%
search: 269 covered, 0 candidates, 100.0%
settings: 1771 covered, 254 candidates, 87.5%
modals: 2922 covered, 2637 candidates, 52.6%
release: 5955 covered, 2940 candidates, 66.9%
```

Phase-specific coverage:

```text
AI / Agent: 1502 covered, 1182 candidates, 56.0%
Terminal: 873 covered, 1455 candidates, 37.5%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale.json: 1749159 bytes
/tmp/warp-cn-zh-Hans-locale.pretty.json: 2061214 bytes
/tmp/warp-cn-zh-Hans-locale.yaml: 1485634 bytes
```

## Command-Line Gate

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
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale.json > /tmp/warp-cn-zh-Hans-locale.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale.yaml
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
cargo check -j 2 -p warp
```

Python tests:

```text
19 tests passed
```

Rust compile gate:

```text
cargo check -j 2 -p warp
Finished dev profile successfully
```

Known command-line warnings:

- `cargo check -j 2 -p warp` reports existing unused-variable warnings in `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` and `app/src/terminal/input/slash_commands/mod.rs`.

## GUI Evidence

RC8 preserves the Phase 19 current-cycle screenshots:

- `docs/gui-smoke-artifacts/phase19/p19-settings-agent-readable.png`
- `docs/gui-smoke-artifacts/phase19/p19-command-palette-readable.png`
- `docs/gui-smoke-artifacts/phase19/p19-warp-drive-english-residue.png`

Phase 19 re-verified current-cycle anchors for the base workspace and settings shell, and fixed the logged-out Warp Drive source residues found during that pass.

No account, Billing, Cloud, destructive confirmation, or Agent lifecycle row is promoted to public-RC verified in RC8. Phase 21-23 were source-only passes and did not capture new GUI state evidence.

## Release Decision

RC8 is `ready-for-local-use-source-level`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Locale exports are generated and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage improved from RC7 `53.4%` to RC8 `66.9%`.

RC8 is not `ready-for-public-rc` because public-RC criteria still require current-cycle GUI evidence for account/state paths. The following remain manual, fixture, or isolated-test-account gates:

- Fresh Agent onboarding.
- Browser login and token fallback.
- AI settings deep paths, BYO API keys, and real-account custom endpoint path.
- Environment deletion and auth-secret deletion confirmations.
- Agent lifecycle status and error states.
- Billing, cloud capacity, credits, and plan modals.

## Next Gate

Before public RC:

1. Use `docs/zh-Hans-public-rc-gate-runbook.md`.
2. Use only isolated disposable profiles and test accounts.
3. Do not use the user's main account, real billing quota, production cloud environment, real secrets, or team ownership state.
4. Capture cropped/redacted screenshots for the remaining manual GUI rows.
5. Promote fixture evidence separately from true account-verified evidence.
6. Re-run the command-line gate and reconsider `ready-for-public-rc`.
