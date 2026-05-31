# zh-Hans Release Candidate 2026-05-31 RC5

RC5 is the Phase 8 public-RC evidence-path record for Warp CN.

Decision: `ready-for-local-use`

Public RC decision: not ready.

## Scope

RC5 includes:

- Phase 8 entry baseline.
- Fresh upstream refs recheck.
- Evidence-path selection for `GUI-WS-06` custom endpoint deletion.
- Full command-line, test, and bundle release gate rerun.

RC5 does not claim first-party runtime i18n support, complete UI coverage, public-RC readiness, verified custom endpoint deletion, verified logged-in custom inference UI, or verified account/Billing/Cloud/Agent lifecycle states.

## Upstream Base

- Branch: `drew/zh-Hans-localization`
- Local HEAD during RC5 gate: `305b2821f493eb2d0526a13669bbdf0fe8f74d51`
- Worktree state: dirty, containing Phase 3 through Phase 8 localization work.
- `git fetch origin --tags`: passed on 2026-05-31.
- Selected stable tag: `v0.2026.05.27.09.22.stable_00`
- Selected stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Selected stable subject: `Enable async find on dogfood, add toggle for Preview/Stable (#11555)`
- Current `origin/master`: `5767910b5e41bda196baaea041862e9505e46e20`
- Current `origin/master` subject: `Add ./script/format for customized cargo fmt invocation. (#11747)`
- Ahead/behind against selected stable tag: `0 88` from `git rev-list --left-right --count "$UPSTREAM_BASE...HEAD"`

Stable freshness is satisfied for RC5 because upstream refs were freshly fetched and no newer stable tag appeared.

## Manifest And Coverage

```text
manifest validation passed
glossary check passed

entries: 2661
key: 149 (5.6%)
context: 149 (5.6%)
status: 149 (5.6%)
preserve_terms: 18 (0.7%)
notes: 0 (0.0%)
expected_count: 149 (5.6%)

entries: 2661
files: 197
already_applied: 2646
would_change: 0
missing: 0

preset: release
covered: 2889
candidates: 6409
coverage: 31.1%
```

Locale exports:

- `/tmp/zh-CN.json`: 697971 bytes; `python3 -m json.tool /tmp/zh-CN.json` passed.
- `/tmp/zh-CN.yaml`: 570094 bytes.

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
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
python3 -m json.tool /tmp/zh-CN.json
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 script/test_zh_apply_localization.py
python3 script/test_zh_localization_inventory.py
python3 script/test_zh_export_locale.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Python tests:

```text
script/test_zh_apply_localization.py: 11 passed
script/test_zh_localization_inventory.py: 3 passed
script/test_zh_export_locale.py: 4 passed
```

Rust tests:

```text
cargo test -p warp_search_core: 13 unit tests passed; 1 doctest passed
cargo test -p warp command_palette: 15 passed; 0 failed; 4698 filtered out
```

Known command-line warnings:

- `cargo check`, `cargo test -p warp command_palette`, and bundle build report existing unused-variable warnings in `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` and `app/src/terminal/input/slash_commands/mod.rs`.
- `./script/run --dont-open` cannot access the private `ssh://git@github.com/warpdotdev/warp-channel-config.git` channel config and skips it.
- The oss channel has no `.icon` bundle at `app/channels/oss/icon/AppIcon.icon`, so adaptive icon compilation is skipped.

Bundle:

```text
target/debug/bundle/osx/WarpOss.app
```

## GUI Evidence Path

P8 evidence path:

```text
no-test-account
```

No isolated test account or fixture credentials were available in the current execution context. The executor did not guess credentials and did not use the user's main account.

Because the public-RC path requires real logged-in product state where `自定义推理` is visible, the following Phase 8 GUI stages were deferred:

- P8-M3: no logged-in `zh-rc5` profile was launched.
- P8-M4: no logged-in current-cycle base GUI evidence was collected.
- P8-M5: no `zh-smoke-delete-endpoint` was created.
- P8-M6: no remove endpoint confirmation was opened, cancelled, or confirmed.

No endpoint was created or deleted.

## Release Decision

RC5 is `ready-for-local-use`.

Reasoning:

- Upstream stable freshness is satisfied for the selected stable base.
- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Locale exports and command-line tests pass.
- Bundle gate passes and produces `target/debug/bundle/osx/WarpOss.app`.
- Phase 7 current-cycle base GUI evidence remains useful for local-use context.
- Phase 8 does not have isolated test-account evidence for custom inference or endpoint deletion.

RC5 is not `ready-for-public-rc` because public-RC criteria require `GUI-WS-06` to be verified in the real GUI with an isolated disposable endpoint. The current run selected `no-test-account`, so that evidence cannot be produced safely.

## Next Gate

Before public RC:

1. Provide an isolated test account where Settings > AI shows `自定义推理`.
2. Launch `WarpOss.app` with `WARP_DATA_PROFILE=zh-rc5` or a later fresh debug profile.
3. Create only `zh-smoke-delete-endpoint` with fake endpoint values.
4. Open the remove confirmation and capture `移除端点？`, `确定要移除此端点吗？`, `取消`, and `移除端点`.
5. Click `取消` first and prove the endpoint remains.
6. Reopen the dialog and remove only the disposable endpoint.
7. Re-run the RC gate and reconsider `ready-for-public-rc`.

Optional non-public fallback:

- Add a debug-only custom inference fixture to render the custom endpoint list and remove-confirmation dialog without real account state. This can validate localization rendering, but it cannot by itself satisfy public-RC evidence requirements.
