# zh-Hans Release Candidate 2026-05-31 RC4

RC4 is the Phase 7 GUI evidence recovery record for Warp CN.

Decision: `ready-for-local-use`

Public RC decision: not ready.

## Scope

RC4 includes:

- Phase 7 debug profile and path-isolation audit for `WARP_DATA_PROFILE=zh-rc4`.
- Current-cycle interactive GUI launch evidence for `WarpOss.app`.
- Current-cycle base GUI smoke for workspace, menu, command palette, settings shell, tab context menu, and new terminal entry.
- A real attempt to reach the lowest-risk destructive confirmation path, `GUI-WS-06` custom endpoint deletion.
- Full command-line, test, and bundle release gate rerun after GUI evidence recovery.

RC4 does not claim first-party runtime i18n support, complete UI coverage, public-RC readiness, verified custom endpoint deletion, or verified account/Billing/Cloud/Agent lifecycle states.

## Upstream Base

- Branch: `drew/zh-Hans-localization`
- Local HEAD during RC4 gate: `305b2821f493eb2d0526a13669bbdf0fe8f74d51`
- Worktree state: dirty, containing Phase 3 through Phase 7 localization work.
- Selected stable tag: `v0.2026.05.27.09.22.stable_00`
- Selected stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Ahead/behind against selected stable tag: `0 88` from `git rev-list --left-right --count v0.2026.05.27.09.22.stable_00...HEAD`

RC4 inherits the RC3 upstream freshness result: `git fetch origin --tags` passed on 2026-05-31 and no newer stable tag appeared at that time.

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

Metadata JSON was generated and parsed successfully:

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

## GUI Gate

P7-M2 launch status: `interactive-profile-ready`.

Evidence:

- `launchctl setenv WARP_DATA_PROFILE zh-rc4` plus `open -n target/debug/bundle/osx/WarpOss.app` launched the GUI process with the debug profile.
- `ps eww -p 80871` confirmed `WARP_DATA_PROFILE=zh-rc4` in the `warp-oss` GUI process.
- `docs/gui-smoke-artifacts/phase7/p7-m2-launch.png` captured the macOS permission prompt.
- `docs/gui-smoke-artifacts/phase7/p7-m2-after-permission-deny.png` captured the visible welcome screen after denying the prompt.
- `docs/gui-smoke-artifacts/phase7/p7-m2-warp-oss.log.txt` captured 111 lines of app log output.
- Computer Use read menu labels from `WarpOss`.

Current-cycle base GUI smoke passed in P7-M4:

- Workspace evidence: `docs/gui-smoke-artifacts/phase7/p7-m4-workspace.png`.
- Command palette evidence: `docs/gui-smoke-artifacts/phase7/p7-m4-command-palette.png`.
- Settings shell evidence: `docs/gui-smoke-artifacts/phase7/p7-m4-settings-shell.png`.
- Tab context menu evidence: `docs/gui-smoke-artifacts/phase7/p7-m4-tab-context-menu.png`.
- New terminal entry evidence: `docs/gui-smoke-artifacts/phase7/p7-m4-new-session-menu.png`.
- File menu evidence: `docs/gui-smoke-artifacts/phase7/p7-m4-file-menu.png`.

Verified anchors include `文件`, `编辑`, `视图`, `标签页`, `块`, `AI`, `Drive`, `窗口`, `帮助`, `搜索命令`, `文件`, `操作`, `会话`, `启动配置`, `账户`, `Agent`, `代码`, `云平台`, `团队`, `外观`, `功能`, `键盘快捷键`, `Warp Drive`, `隐私`, `关于`, `共享会话`, `复制标签页标题`, `重命名标签页`, `关闭标签页`, `关闭其他标签页`, `关闭右侧标签页`, and `另存为新配置`.

## Destructive Confirmation Gate

`GUI-WS-06` remains unverified.

P7-M1/P7-M3 proved the custom endpoint state is safe to test only when the GUI process has `WARP_DATA_PROFILE=zh-rc4`, because the endpoint API keys are stored in secure storage under a profiled `ChannelState::data_domain()`.

P7-M5 then attempted to reach Settings > AI > custom inference, but the `zh-rc4` profile was logged out after terminal-only onboarding. Source review confirmed `UserWorkspaces::is_custom_inference_enabled()` returns false for anonymous or logged-out users before checking plan/workspace state. As a result, the `自定义推理` UI was not shown and `zh-smoke-delete-endpoint` could not be created.

Evidence:

- `docs/gui-smoke-artifacts/phase7/p7-m5-custom-inference-blocked-logged-out.png`

No real endpoint was touched. No disposable endpoint was created or deleted.

## Release Decision

RC4 is `ready-for-local-use`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Locale exports and command-line tests pass.
- Bundle gate passes and produces `target/debug/bundle/osx/WarpOss.app`.
- Current-cycle base GUI smoke is recovered and verified with screenshots.
- The custom endpoint destructive confirmation path is blocked by logged-out product state, not by launch automation.
- The minimum public-RC destructive confirmation evidence is still missing.

RC4 is not `ready-for-public-rc` because public-RC criteria require at least one destructive confirmation verified in the real GUI with an isolated disposable object. Phase 7 recovered the GUI base evidence, but it did not create or delete `zh-smoke-delete-endpoint`.

## Next Gate

Before public RC:

1. Provide an isolated test account or fixture where custom inference is enabled without touching the main account.
2. Create a disposable local custom endpoint named `zh-smoke-delete-endpoint`.
3. Capture the remove confirmation showing `移除端点？`, `确定要移除此端点吗？`, `取消`, and `移除端点`.
4. Click `取消` first and confirm the endpoint remains.
5. Reopen the dialog, remove the disposable endpoint, and record that no real endpoint was deleted.
6. Re-run the RC gate and only then reconsider `ready-for-public-rc`.
