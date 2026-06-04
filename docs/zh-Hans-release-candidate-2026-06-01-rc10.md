# zh-Hans Release Candidate 2026-06-01 RC10

RC10 is the Phase 33-40 post-RC9 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC10 includes:

- Post-RC9 queue hygiene and classification.
- Terminal backlog source pass 4.
- AI/Agent backlog source pass 3.
- Settings, workspace, and modal polish.
- GUI fixture and visual residue preparation.
- Current-source bundle GUI smoke with local logged-out/onboarding evidence.
- Isolated account/backend-state public-RC blocker audit.
- Final manifest, export, Python, formatting, diff, and low-concurrency Rust compile gates.

RC10 does not claim first-party runtime i18n support, complete whole-repository localization, or public-RC GUI readiness.

## Manifest And Coverage

```text
python3 script/zh_apply_localization.py --metadata-summary --json
entries: 6786
key: 150 (2.2%)
context: 6786 (100.0%)
status: 6786 (100.0%)
preserve_terms: 18 (0.3%)
notes: 0
expected_count: 150 (2.2%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 6786
files: 342
already_applied: 4973
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 4093 covered, 1510 candidates, 73.1%
release: 7427 covered, 1514 candidates, 83.1%
```

Phase-specific coverage:

```text
Terminal: 1448 covered, 918 candidates, 61.2%
AI / Agent: 2098 covered, 592 candidates, 78.0%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc10.json: 2192949 bytes
/tmp/warp-cn-zh-Hans-locale-rc10.pretty.json: 2568910 bytes
/tmp/warp-cn-zh-Hans-locale-rc10.yaml: 1867072 bytes
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
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc10.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc10.json > /tmp/warp-cn-zh-Hans-locale-rc10.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc10.yaml
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
- The final manifest dry-run was executed through a throttled Python wrapper to reduce sustained CPU load. The direct Python command itself exited successfully and reported `would_change: 0`, `missing: 0`.

## GUI Evidence

RC10 adds Phase 38 current-source local GUI screenshots:

- `docs/gui-smoke-artifacts/phase38/p38-onboarding-welcome-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-agent-choice-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-customize-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-agent-settings-runtime-residue.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-third-party-agent-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-theme-choice-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-ai-enable-skip-login-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-disable-ai-confirmation-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-main-window-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-settings-account-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-settings-agent-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-settings-privacy-current-source.png`

Phase 38 evidence supports current-source local review for:

- `GUI-BASE-01`: macOS menu bar anchors.
- `GUI-BASE-04`: terminal-only/no-AI main window.
- `GUI-ONB-01`: fresh onboarding Agent path.
- `GUI-AUTH-03`: disable-AI and skip-login local path.
- `GUI-SET-01`: Settings shell, Account, Warp Agent, and Privacy anchors.

No account, billing quota, cloud environment, secret, production object, or team ownership state was touched.

## Residue And Fixes

Static onboarding preview PNGs still contain embedded English UI and remain `visual-residue`; they are bitmap assets, not manifest drift.

The current-source smoke initially showed server/cache-provided `auto (cost-efficient)` model metadata. Phase 38 added a narrow exact-match runtime display-name mapping for built-in `auto` model labels without changing model IDs or arbitrary third-party model names. The focused unit test passed:

```text
cargo test -j 2 -p warp llm_info_localizes_builtin_auto_display_names_from_wire_metadata
```

## Release Decision

RC10 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Locale exports are generated and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage improved from RC9 `77.2%` to RC10 `83.1%`.
- Current-source GUI evidence replaces the Phase 30 reused-bundle evidence for key local onboarding, logged-out privacy, main-window, and Settings anchors.

RC10 is not `ready-for-public-rc` because public-RC criteria still require current-cycle isolated-account/state evidence for these rows:

- `GUI-AUTH-01`: browser login and auth callback.
- `GUI-SET-03`: real-account AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-06`: disposable environment deletion confirmation.
- `GUI-WS-04`: disposable managed auth secret deletion confirmation.
- `GUI-WS-06`: disposable custom endpoint removal confirmation without fixture env.
- `GUI-WS-07`: disposable team ownership transfer confirmation.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`: safe billing/quota/cloud backend states.
- `GUI-SET-04` and `GUI-SET-05`: disposable AWS/Bedrock profile or invalid credential fixture.

## Next Gate

Before public RC:

1. Provide a disposable test account/team and backend fixture states from `docs/zh-Hans-public-rc-gate-runbook.md`.
2. Capture cropped/redacted screenshots for the account/state rows.
3. Confirm cleanup for every disposable object.
4. Keep fixture evidence separate from true account-verified evidence.
5. Re-run the command-line gate and reconsider `ready-for-public-rc`.
