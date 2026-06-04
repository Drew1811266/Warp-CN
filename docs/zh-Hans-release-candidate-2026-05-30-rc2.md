# zh-Hans Release Candidate 2026-05-30 RC2

This record captures the Phase 5 release-hardening gate for the Warp CN source-level localization overlay.

## Scope

- Branch: `drew/zh-Hans-localization`
- Local HEAD: `305b2821f493eb2d0526a13669bbdf0fe8f74d51`
- Local HEAD subject: `docs: record phase 2 round 4 audit`
- Selected upstream stable base: `v0.2026.05.27.09.22.stable_00`
- Selected upstream stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Bundle path: `target/debug/bundle/osx/WarpOss.app`
- Bundle size: `714M`
- Release decision: `ready-for-local-use`
- Public RC status: blocked by upstream refresh and GUI evidence limits.

This is not an official Warp release. It is a community Chinese-localized build produced from the local overlay manifest.

## Release Decision

RC2 is `ready-for-local-use`.

Reasoning:

- The source-level overlay is internally consistent: `missing: 0`, `would_change: 0`, glossary validation passed, and metadata coverage reached the Phase 5 target.
- The local bundle builds and signs successfully at `target/debug/bundle/osx/WarpOss.app`.
- Core command-line, unit, search, command-palette, locale export, and bundle gates passed.
- GUI baseline evidence exists for the workspace shell, settings shell, command palette, menu anchors, and vertical tab menu.

It is not `ready-for-public-rc` yet because:

- Fresh upstream stable refs could not be fetched due network timeouts.
- No destructive confirmation has real GUI evidence from an isolated test object.
- Account, Billing, Cloud Agent, and Agent lifecycle gates still need isolated accounts, service-side state, or fixtures.

## Phase 5 Changes Since RC1

- Added Phase 5 GUI evidence rules and preserved screenshot artifacts for failed automation attempts.
- Retried upstream stable refresh; GitHub network timeouts prevented fetching newer refs, so this RC2 still uses the latest locally available stable base.
- Split destructive confirmation gates into concrete test-object requirements for custom endpoint, environment, and auth-secret deletion.
- Fixed auth-secret deletion confirmation title/buttons: `删除密钥`, `取消`, and `删除`.
- Split account, Billing, Cloud, and Agent state gates into concrete trigger requirements and blockers.
- Localized Agent status display labels for conversation/task, ambient task, pending query, and history output states.
- Raised high-value manifest metadata coverage to `5.0%` without mechanically backfilling low-value historical entries.

## Manifest Gate

```text
manifest validation passed
glossary check passed
entries: 2645
files: 194
already_applied: 2630
would_change: 0
missing: 0
```

Metadata summary:

```text
entries: 2645
key: 133 (5.0%)
context: 133 (5.0%)
status: 133 (5.0%)
preserve_terms: 13 (0.5%)
notes: 0 (0.0%)
expected_count: 133 (5.0%)
```

## Coverage Snapshot

```text
preset: release
covered: 2873
candidates: 6425
coverage: 30.9%
```

## Locale Export

```text
/tmp/zh-CN.json: 691152 bytes
/tmp/zh-CN.yaml: 564085 bytes
```

Both exports completed successfully from `script/zh_export_locale.py`.

## Test And Build Gate

Passed:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
cargo fmt --check
git diff --check
python3 script/test_zh_apply_localization.py
python3 script/test_zh_localization_inventory.py
python3 script/test_zh_export_locale.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Known warnings:

- `git fetch origin --tags` and lightweight `ls-remote` failed in P5-M1 due GitHub network timeouts. Do not claim this RC2 is based on freshly fetched upstream refs.
- `cargo check -p warp`, `cargo test -p warp command_palette`, and the bundle gate still emit the existing 46 unused-variable warnings in slash-command and remote-server code.
- `./script/run --dont-open` cannot access the private `warp-channel-config` SSH repository in this environment and skips internal channel config installation. The `oss` bundle still builds and signs successfully.
- No `.icon` bundle exists for the `oss` channel, so adaptive icon compilation is skipped.

## GUI Smoke

Updated matrix: `docs/zh-Hans-gui-smoke-matrix.md`.

Verified evidence still comes from P4-M5:

- macOS menu anchors: `文件`, `编辑`, `视图`, `标签页`, `块`, `窗口`, `帮助`.
- Workspace anchors: global search placeholder and `新会话`.
- Settings shell: `设置`, `账户`, `Agent`, `代码`, `云平台`, `团队`, `外观`, `功能`, `键盘快捷键`, `隐私`, `关于`.
- Command palette: `搜索命令`, `文件`, `操作`, `会话`, `启动配置`, and `打开主题选择器`.
- Vertical tab context menu after the P4-M5 fix: `共享会话`, `复制窗格标题`, `复制工作目录`, `重命名标签页`, `关闭标签页`, `关闭其他标签页`, `关闭下方标签页`, `另存为新配置`.

Phase 5 GUI notes:

- P5-M2 rebuilt and launched the bundle, but Computer Use timed out and AppleScript activation failed; screenshots captured only the desktop wallpaper.
- P5-M3 documented destructive confirmation trigger paths and fixed auth-secret delete confirmation text, but no safe endpoint/environment/auth-secret object was available for real GUI verification.
- P5-M4 decomposed account, Billing, Cloud, and Agent state gates into concrete triggers.
- P5-M5 fixed Agent status labels at the source/display layer; GUI still needs lifecycle-state fixtures before `GUI-AGENT-03` can be marked `verified`.

Remaining public-RC blockers:

- Fresh upstream stable refs have not been fetched successfully.
- No destructive confirmation path has real GUI evidence yet.
- Account/Billing/Cloud/Agent state gates still require isolated accounts, server-side state, or fixtures.

## Local Use Boundary

RC2 is suitable for local engineering use and continued GUI/manual gate testing. It should not be presented as a public release or official Warp build.

Build the local bundle:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Launch it:

```bash
open -n target/debug/bundle/osx/WarpOss.app
```

Do not present this as an official Warp build. The official product, service behavior, account system, and license remain governed by upstream Warp.
