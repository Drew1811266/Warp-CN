# zh-Hans Release Candidate 2026-05-31 RC3

RC3 is the Phase 6 release-readiness record for Warp CN.

Decision: `ready-for-local-use`

Public RC decision: not ready.

## Scope

RC3 includes:

- Phase 6 upstream stable ref refresh.
- Phase 6 GUI automation/profile evidence.
- Concrete destructive-confirmation blockers for endpoint, environment, and auth-secret deletion.
- Fixture ownership categories for account, Billing, Cloud, Agent, onboarding, and web gates.
- One targeted user-visible slice: `terminal.view.notifications`.
- Machine-readable metadata summary output: `python3 script/zh_apply_localization.py --metadata-summary --json`.

RC3 does not claim first-party runtime i18n support, complete UI coverage, public-RC readiness, verified destructive confirmation GUI evidence, or verified account/Billing/Cloud/Agent lifecycle states.

## Upstream Base

- Branch: `drew/zh-Hans-localization`
- Local HEAD during RC3 gate: `305b2821f493eb2d0526a13669bbdf0fe8f74d51`
- Worktree state: dirty, containing Phase 3 through Phase 6 localization work.
- `git fetch origin --tags`: passed on 2026-05-31.
- Latest fetched stable tag: `v0.2026.05.27.09.22.stable_00`
- Latest fetched stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Latest fetched stable subject: `Enable async find on dogfood, add toggle for Preview/Stable (#11555)`
- Current `origin/master`: `74d256646c24f5ac8cc93af1792e57e35062cc44`
- Current `origin/master` subject: `[4/5] Use remote-aware skill locations in UI consumers (#11581)`
- Ahead/behind against selected stable tag: `0 88` from `git rev-list --left-right --count "$UPSTREAM_BASE...HEAD"`

Stable freshness blocker is cleared for RC3 because upstream refs were freshly fetched. No newer stable tag appeared.

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

Metadata JSON was also generated:

```json
{
  "entries": 2661,
  "key": {"count": 149, "percent": 5.6},
  "context": {"count": 149, "percent": 5.6},
  "status": {"count": 149, "percent": 5.6},
  "preserve_terms": {"count": 18, "percent": 0.7},
  "notes": {"count": 0, "percent": 0.0},
  "expected_count": {"count": 149, "percent": 5.6}
}
```

Locale exports:

- `/tmp/zh-CN.json`: 697971 bytes; `python3 -m json.tool /tmp/zh-CN.json` passed.
- `/tmp/zh-CN.yaml`: 570094 bytes.
- `/tmp/zh-metadata-summary.json`: 368 bytes.

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
python3 -m json.tool /tmp/zh-CN.json > /tmp/zh-CN.pretty.json
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
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

## GUI Gate

P6-M2 status: `automation-blocked`.

Evidence:

- Bundle gate passed and `open -n target/debug/bundle/osx/WarpOss.app` returned successfully.
- `pgrep -afil 'warp-oss|terminal-server'` found `warp-oss` and `terminal-server`.
- Computer Use timed out for both `WarpOss` and `dev.warp.WarpOss`.
- macOS screenshot showed: `你不能打开应用程序 “WarpOss”，因为它没有响应。`
- Screenshot: `docs/gui-smoke-artifacts/phase6/p6-m2-warp-oss-not-responding-2026-05-31.png`

No business GUI row was promoted to `verified` from process evidence.

Destructive confirmation status:

- `GUI-WS-06`: custom endpoint deletion has translated source anchors, but no disposable `zh-smoke-delete-endpoint` object and current GUI is `automation-blocked`.
- `GUI-SET-06`: environment deletion has translated source anchors, but no isolated cloud environment object and current GUI is `automation-blocked`.
- `GUI-WS-04`: auth-secret deletion has translated source anchors, but no isolated managed auth secret and current GUI is `automation-blocked`.

No real endpoint, cloud environment, or secret was deleted.

## Release Decision

RC3 is `ready-for-local-use`.

Reasoning:

- Upstream stable freshness is now satisfied for the selected stable base.
- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Locale exports and command-line tests pass.
- Bundle gate passes and produces `target/debug/bundle/osx/WarpOss.app`.
- GUI automation is still blocked by the local app/window state.
- At least one destructive confirmation does not yet have real GUI evidence.
- Account, Billing, Cloud, and Agent gates have concrete fixture categories, but the actual GUI/state evidence is still pending.

RC3 is not `ready-for-public-rc` because the public-RC criteria require real GUI evidence for base workspace, settings shell, command palette, vertical tab menu, and at least one destructive confirmation. Phase 6 preserved older verified GUI rows, but the current RC3 run cannot reproduce interactive GUI evidence and cannot verify destructive confirmation.

## Next Gate

Before public RC:

1. Recover an interactive `WarpOss` profile/window state or create an isolated GUI profile that launches reliably.
2. Create a disposable local custom endpoint named `zh-smoke-delete-endpoint`.
3. Re-run `GUI-WS-06` and capture real Computer Use or screenshot evidence for `移除端点？`, `确定要移除此端点吗？`, `取消`, and `移除端点`.
4. Re-run base workspace/settings/command-palette smoke in the same RC cycle.
5. Only then reconsider `ready-for-public-rc`.
