# zh-Hans Release Candidate 2026-05-30

This record captures the Phase 4 release-candidate gate for the Warp CN source-level localization overlay.

## Scope

- Branch: `drew/zh-Hans-localization`
- Local HEAD: `305b2821f493eb2d0526a13669bbdf0fe8f74d51`
- Local HEAD subject: `docs: record phase 2 round 4 audit`
- Selected upstream stable base: `v0.2026.05.27.09.22.stable_00`
- Selected upstream stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Bundle path: `target/debug/bundle/osx/WarpOss.app`
- Status: release-candidate gate passed with manual GUI gates still documented.

This is not an official Warp release. It is a community Chinese-localized build produced from the local overlay manifest.

## Manifest Gate

```text
manifest validation passed
glossary check passed
entries: 2619
files: 190
already_applied: 2604
would_change: 0
missing: 0
```

Metadata summary:

```text
entries: 2619
key: 78 (3.0%)
context: 78 (3.0%)
status: 78 (3.0%)
preserve_terms: 7 (0.3%)
notes: 0 (0.0%)
expected_count: 78 (3.0%)
```

## Coverage Snapshot

```text
preset: workspace
covered: 598
candidates: 377
coverage: 61.3%

preset: settings
covered: 1201
candidates: 827
coverage: 59.2%

preset: modals
covered: 635
candidates: 5189
coverage: 10.9%

preset: release
covered: 2845
candidates: 6453
coverage: 30.6%
```

## Locale Export

```text
/tmp/zh-CN.json: 680118 bytes
/tmp/zh-CN.yaml: 554347 bytes
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

- `git fetch origin --tags` failed during P4-M7 rehearsal because the environment could not reliably reach GitHub. The RC uses the latest locally available stable tag; retry fetch before public release.
- `cargo check -p warp` and `cargo test -p warp command_palette` still emit the existing 46 unused-variable warnings in slash-command and remote-server code.
- `./script/run --dont-open` cannot access the private `warp-channel-config` SSH repository in this environment and skips internal channel config installation. The `oss` bundle still builds and signs successfully.
- No `.icon` bundle exists for the `oss` channel, so adaptive icon compilation is skipped.

## GUI Smoke

Updated matrix: `docs/zh-Hans-gui-smoke-matrix.md`.

Verified in P4-M5:

- macOS menu anchors: `文件`, `编辑`, `视图`, `标签页`, `块`, `窗口`, `帮助`.
- Workspace anchors: global search placeholder and `新会话`.
- Settings shell: `设置`, `账户`, `Agent`, `代码`, `云平台`, `团队`, `外观`, `功能`, `键盘快捷键`, `隐私`, `关于`.
- Command palette: `搜索命令`, `文件`, `操作`, `会话`, `启动配置`, and `打开主题选择器`.
- Vertical tab context menu after the P4-M5 fix: `共享会话`, `复制窗格标题`, `复制工作目录`, `重命名标签页`, `关闭标签页`, `关闭其他标签页`, `关闭下方标签页`, `另存为新配置`.

Remaining manual GUI gates:

- Login/account flows.
- Endpoint, environment, auth-secret deletion confirmations.
- Team ownership transfer confirmation.
- Billing, cloud Agent capacity, plan migration, and usage-limit states.
- Agent task status/error states and Warp on Web home.

## Run Locally

Build the local bundle:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Launch it:

```bash
open -n target/debug/bundle/osx/WarpOss.app
```

Do not present this as an official Warp build. The official product, service behavior, account system, and license remain governed by upstream Warp.
