# zh-Hans Release Candidate 2026-06-01 RC9

RC9 is the Phase 26-32 post-RC8 localization record for Warp CN.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC9 includes:

- Public-RC fixture and account readiness planning.
- Terminal backlog source pass 3.
- AI/Agent backlog source pass 2.
- Settings AI page and secondary modals cleanup.
- Low-load GUI fixture evidence for local onboarding, logged-out privacy, workspace, and Settings anchors.
- Isolated test-account public-RC audit.
- Final manifest, export, Python, formatting, diff, and low-concurrency Rust compile gates.

RC9 does not claim first-party runtime i18n support, complete whole-repository localization, or public-RC GUI readiness.

## Manifest And Coverage

```text
python3 script/zh_apply_localization.py --metadata-summary --json
entries: 6294
key: 150 (2.4%)
context: 6294 (100.0%)
status: 6294 (100.0%)
preserve_terms: 18 (0.3%)
notes: 0
expected_count: 150 (2.4%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 6294
files: 301
already_applied: 4760
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 817 covered, 49 candidates, 94.3%
search: 269 covered, 0 candidates, 100.0%
settings: 1953 covered, 74 candidates, 96.3%
modals: 3682 covered, 1914 candidates, 65.8%
release: 6897 covered, 2037 candidates, 77.2%
```

Phase-specific coverage:

```text
AI / Agent: 1904 covered, 780 candidates, 70.9%
Terminal: 1231 covered, 1134 candidates, 52.1%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc9.json: 2028430 bytes
/tmp/warp-cn-zh-Hans-locale-rc9.pretty.json: 2381488 bytes
/tmp/warp-cn-zh-Hans-locale-rc9.yaml: 1726169 bytes
```

## Command-Line Gate

Passed or completed cleanly:

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
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc9.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc9.json > /tmp/warp-cn-zh-Hans-locale-rc9.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc9.yaml
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
- The full manifest dry-run was executed through a throttled wrapper to reduce heat. The Python summary was clean with `would_change: 0` and `missing: 0`; the wrapper exited nonzero after the summary because of STOP/CONT signal handling, not because of localization drift.

## GUI Evidence

RC9 adds Phase 30 current-cycle local fixture screenshots:

- `docs/gui-smoke-artifacts/phase30/p30-onboarding-welcome-local-fixture-window.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-agent-choice.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-customize.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-agent-settings-residue.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-third-party-agent.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-theme-choice.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-ai-enable-skip-login.png`
- `docs/gui-smoke-artifacts/phase30/p30-disable-ai-confirmation.png`
- `docs/gui-smoke-artifacts/phase30/p30-main-window-local-fixture.png`
- `docs/gui-smoke-artifacts/phase30/p30-settings-account-local-fixture.png`
- `docs/gui-smoke-artifacts/phase30/p30-settings-agent-local-fixture.png`
- `docs/gui-smoke-artifacts/phase30/p30-settings-privacy-local-fixture.png`

Phase 30 evidence supports local fixture review for:

- `GUI-ONB-01`: fresh onboarding Agent path, with embedded image English residue and one reused-bundle pre-Phase-28 model label residue.
- `GUI-AUTH-03`: privacy settings and disable-AI confirmation.
- `GUI-WS-01`: main window, left panel, search, and Settings navigation.
- `GUI-SET-03`: logged-out Settings > Agent shell only.

No account, billing quota, cloud environment, secret, production object, or team ownership state was touched.

## Release Decision

RC9 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Locale exports are generated and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage improved from RC8 `66.9%` to RC9 `77.2%`.
- Phase 30 provides current-cycle fixture evidence for local onboarding, logged-out privacy, workspace, and Settings anchors.

RC9 is not `ready-for-public-rc` because public-RC criteria still require current-cycle isolated-account/state evidence for these rows:

- `GUI-AUTH-01`: browser login and auth callback.
- `GUI-SET-03`: real-account AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-06`: disposable environment deletion confirmation.
- `GUI-WS-04`: disposable managed auth secret deletion confirmation.
- `GUI-WS-06`: disposable custom endpoint removal confirmation without fixture env.
- `GUI-WS-07`: disposable team ownership transfer confirmation.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`: safe billing/quota/cloud backend states.

## Next Gate

Before public RC:

1. Provide a disposable test account/team and backend fixture states from `docs/zh-Hans-public-rc-gate-runbook.md`.
2. Rebuild the bundle from current RC9 source and rerun Phase 30-style screenshots so reused-bundle residue is removed.
3. Capture cropped/redacted screenshots for the account/state rows.
4. Keep fixture evidence separate from true account-verified evidence.
5. Re-run the command-line gate and reconsider `ready-for-public-rc`.
