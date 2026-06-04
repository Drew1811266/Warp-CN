# zh-Hans Release Candidate 2026-05-31 RC6

RC6 is the Phase 9 custom inference evidence enablement record for Warp CN.

Decision: `ready-for-local-use`

Public RC decision: not ready.

## Scope

RC6 includes:

- Phase 9 entry baseline and RC5 blocker carry-forward.
- Isolated custom inference test-account runbook.
- Debug-only `WARP_CN_CUSTOM_INFERENCE_SMOKE=1` custom inference fixture.
- Fixture GUI evidence for custom endpoint list, edit, cancel-delete, and final remove.
- Full command-line, focused test, and bundle gate rerun.

RC6 does not claim first-party runtime i18n support, complete UI coverage, public-RC readiness, verified real-account custom inference, or verified account/Billing/Cloud/Agent lifecycle states.

## Upstream Base

- Branch: `drew/zh-Hans-localization`
- Local HEAD during RC6 gate: `305b2821`
- Worktree state: dirty, containing Phase 3 through Phase 9 localization work.
- RC6 reuses the RC5 selected stable base: `v0.2026.05.27.09.22.stable_00`.
- Selected stable commit from RC5: `2566f54af7c3e71facfe1865f2c492549b14248a`.

## Manifest And Coverage

```text
manifest validation passed
glossary check passed

entries: 2662
key: 150 (5.6%)
context: 150 (5.6%)
status: 150 (5.6%)
preserve_terms: 18 (0.7%)
notes: 0 (0.0%)
expected_count: 150 (5.6%)

entries: 2662
files: 197
already_applied: 2647
would_change: 0
missing: 0

preset: release
covered: 2890
candidates: 6408
coverage: 31.1%
```

Locale exports:

- `/tmp/zh-CN.json`: 698283 bytes; `python3 -m json.tool /tmp/zh-CN.json` passed.
- `/tmp/zh-CN.pretty.json`: 863568 bytes.
- `/tmp/zh-CN.yaml`: 570358 bytes.

## Command-Line Gate

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 -m json.tool /tmp/zh-CN.json > /tmp/zh-CN.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_export_locale.py script/test_zh_localization_inventory.py
cargo fmt --check
git diff --check
cargo test -p ai custom_inference_smoke
cargo test -p warp custom_inference_smoke_override
cargo test -p warp endpoint_form_valid_accepts_complete_valid_form
cargo test -p warp_search_core
cargo test -p warp command_palette
cargo check -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Python tests:

```text
18 tests passed
```

Rust tests:

```text
cargo test -p ai custom_inference_smoke: 3 passed
cargo test -p warp custom_inference_smoke_override: 1 passed
cargo test -p warp endpoint_form_valid_accepts_complete_valid_form: 1 passed
cargo test -p warp_search_core: 13 unit tests passed; 1 doctest passed
cargo test -p warp command_palette: 15 passed; 0 failed; 4699 filtered out
```

Known command-line warnings:

- `cargo check`, focused `cargo test -p warp ...`, and bundle build report existing unused-variable warnings in `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` and `app/src/terminal/input/slash_commands/mod.rs`.
- `./script/run --dont-open` cannot access the private `ssh://git@github.com/warpdotdev/warp-channel-config.git` channel config and skips it.
- The oss channel has no `.icon` bundle at `app/channels/oss/icon/AppIcon.icon`, so adaptive icon compilation is skipped.

Bundle:

```text
target/debug/bundle/osx/WarpOss.app
```

## GUI Evidence

Fixture evidence path:

```text
fixture-verified
```

P9-M4 launched `WarpOss.app` with `WARP_DATA_PROFILE=zh-rc6` and `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`. The debug fixture seeded one in-memory endpoint:

```text
Name: zh-smoke-delete-endpoint
URL: https://example.com
API key: sk-zh-smoke-dummy-key
Model: zh-smoke-model
Alias: zh-smoke
```

Evidence captured:

- `docs/gui-smoke-artifacts/phase9/p9-m4-fixture-endpoint-seeded.png`
- `docs/gui-smoke-artifacts/phase9/p9-m4-fixture-edit-modal.png`
- `docs/gui-smoke-artifacts/phase9/p9-m4-fixture-remove-confirmation.png`
- `docs/gui-smoke-artifacts/phase9/p9-m4-fixture-after-cancel.png`
- `docs/gui-smoke-artifacts/phase9/p9-m4-fixture-after-remove.png`

Verified anchors:

- `自定义端点`
- `zh-smoke-delete-endpoint`
- `编辑自定义端点`
- `移除`
- `移除端点？`
- `确定要移除此端点吗？`
- `取消`
- `移除端点`
- `端点已移除`

The fixture found one localized copy leak: `app/src/settings_view/custom_inference_modal.rs` displayed `Remove` in the edit modal. RC6 adds `settings.custom_inference.remove_endpoint` to `resources/localization/zh-Hans-overrides.toml` and replaces the generated source text with `移除`. After the fix, `dry-run` remains clean with `missing: 0` and `would_change: 0`.

## Real Account Path

P9-M5 result:

```text
no-test-account
```

No isolated test account, credentials, magic link, or callback path was provided in this execution context. The executor did not use the user's main account.

A no-fixture `zh-rc6` launch proved the process had `WARP_DATA_PROFILE=zh-rc6` and no `WARP_CN_CUSTOM_INFERENCE_SMOKE`. Without the debug no-op storage fixture, macOS requested Keychain access for `dev.warp.WarpOss-zh-rc6` and App data access. Both prompts were denied.

Evidence captured:

- `docs/gui-smoke-artifacts/phase9/p9-m5-no-fixture-desktop.png`
- `docs/gui-smoke-artifacts/phase9/p9-m5-no-fixture-keychain-denied.png`
- `docs/gui-smoke-artifacts/phase9/p9-m5-no-fixture-after-deny.png`

No real endpoint was created or deleted.

## Cleanup Audit

P9-M7 cleanup passed:

- No `WarpOss.app`, `warp-oss`, or `terminal-server` process remained after cleanup.
- `launchctl getenv WARP_CN_CUSTOM_INFERENCE_SMOKE` printed no value.
- `launchctl getenv WARP_DATA_PROFILE` printed no value.
- `security find-generic-password -s dev.warp.WarpOss-zh-rc6 -a AiApiKeys` reported absent without printing secrets.
- Source audit confirmed the smoke path remains `cfg!(debug_assertions)` plus exact `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`.
- Final `git diff --check` passed.

## Release Decision

RC6 is `ready-for-local-use`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Locale exports and Python/Rust command-line tests pass.
- Bundle gate passes and produces `target/debug/bundle/osx/WarpOss.app`.
- The debug-only custom inference fixture proves localized rendering and automation for the endpoint list, edit modal, cancel-delete, and final remove path.
- The fixture also avoids Keychain/App Group prompt friction in debug smoke sessions without writing real secret state.
- The real-account path remains unavailable because no isolated logged-in custom inference account was provided.

RC6 is not `ready-for-public-rc` because public-RC criteria require `GUI-WS-06` to be verified in a real logged-in workspace without `WARP_CN_CUSTOM_INFERENCE_SMOKE`. Fixture evidence is explicitly non-public evidence.

## Next Gate

Before public RC:

1. Provide an isolated test account where Settings > AI shows `自定义推理`.
2. Launch `WarpOss.app` without `WARP_CN_CUSTOM_INFERENCE_SMOKE`.
3. Create only `zh-smoke-delete-endpoint` with non-secret disposable values.
4. Open the remove confirmation and capture `移除端点？`, `确定要移除此端点吗？`, `取消`, and `移除端点`.
5. Click `取消` first and prove the endpoint remains.
6. Reopen the dialog and remove only the disposable endpoint.
7. Re-run the RC gate and reconsider `ready-for-public-rc`.
