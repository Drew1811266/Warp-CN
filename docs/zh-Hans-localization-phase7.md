# Warp CN Phase 7 GUI Evidence Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from the Phase 6 RC3 `ready-for-local-use` decision to a defensible RC4 public-RC decision by recovering current-cycle GUI evidence, proving safe profile/object isolation, and verifying one low-risk destructive confirmation in the real app.

**Architecture:** Phase 7 is evidence-first. It treats the translated source tree as a generated overlay output and does not chase broad coverage. The core flow is: re-establish command-line health, audit debug profile isolation, diagnose the `WarpOss` launch hang, recover an interactive GUI profile, rerun base smoke in the same RC cycle, verify custom endpoint deletion with a disposable object, and then produce an RC4 gate.

**Tech Stack:** Rust/Warp client source, `resources/localization/zh-Hans-overrides.toml`, `script/zh_apply_localization.py`, `script/zh_localization_inventory.py`, `script/zh_export_locale.py`, macOS `WarpOss.app`, `WARP_DATA_PROFILE`, Computer Use, macOS `log`/`sample`/`screencapture`, `docs/zh-Hans-gui-smoke-matrix.md`, cargo test/check gates.

---

## 1. Phase 7 Positioning

Phase 6 produced RC3 and cleared the upstream stable freshness blocker. RC3 is still `ready-for-local-use`, not public RC, because the current RC cycle could not reproduce interactive GUI evidence and did not verify a destructive confirmation against an isolated test object.

Phase 7 should focus on that gap. It should not expand translation coverage unless the GUI smoke uncovers a small, user-visible residue that blocks the release gate.

Public RC requires current-cycle evidence for:

- Base workspace/menu/search/command-palette smoke.
- Settings shell smoke.
- Vertical tab menu smoke.
- At least one destructive confirmation verified with a disposable object.

The lowest-risk destructive path is still `GUI-WS-06`: custom endpoint deletion. It is local configuration, can use a fake URL/model, and already has translated source anchors.

## 2. Current Baseline

Baseline date: 2026-05-31.

```text
entries: 2661
files: 197
already_applied: 2646
would_change: 0
missing: 0
metadata key/context/status/expected_count: 149 (5.6%)
release coverage: 2889/6409 (31.1%)
```

Current RC record:

- `docs/zh-Hans-release-candidate-2026-05-31-rc3.md`
- Decision: `ready-for-local-use`
- Stable base: `v0.2026.05.27.09.22.stable_00`
- Stable freshness: satisfied for RC3
- GUI status: `automation-blocked`
- Blocking screenshot: `docs/gui-smoke-artifacts/phase6/p6-m2-warp-oss-not-responding-2026-05-31.png`

## 3. Non-Goals

Phase 7 does not do:

- No runtime language switch or first-party i18n framework.
- No broad `release` or `modals` coverage push.
- No dev/nightly release tracking.
- No destructive test against a real endpoint, production cloud environment, real managed secret, production team, or main personal account.
- No public RC claim from process startup, bundle success, historical screenshots, or source anchors alone.
- No removal or reset of existing user data without a copied backup and an explicit restore step in the execution record.

## 4. Profile Isolation Rules

`WARP_DATA_PROFILE` is useful, but it is not enough to assume full isolation on macOS.

Known source-level facts to recheck at execution time:

- `crates/warp_core/src/channel/state.rs` exposes `ChannelState::data_profile()`.
- `WARP_DATA_PROFILE` only works in debug builds because it is guarded by `cfg!(debug_assertions)`.
- `ChannelState::data_domain()` appends the profile name in debug builds.
- `crates/warp_core/src/paths.rs` makes `warp_home_config_dir_name()` profile-aware.
- On macOS, `data_dir()` and `config_local_dir()` still use `macos_config_dir_name()` and currently resolve to `~/.warp-oss` for the Oss channel.
- ProjectDirs-backed paths such as cache/state may include the profiled app name, but that must be verified before using them as safety boundaries.

Execution rule:

- Do not create or delete the `zh-smoke-delete-endpoint` object until P7-M1 records the exact path isolation map.
- If any custom endpoint state is stored under the shared `~/.warp-oss` path, Phase 7 must use backup/restore safeguards or skip destructive GUI verification.

## 5. Files And Responsibilities

Expected files to modify during Phase 7:

- `docs/zh-Hans-localization.md`: Phase 7 status, execution record, RC4 decision.
- `docs/zh-Hans-gui-smoke-matrix.md`: profile isolation map, current-cycle GUI evidence, destructive confirmation outcome.
- `docs/zh-Hans-release-candidate-2026-05-31-rc4.md`: final Phase 7 RC4 gate and release decision.
- `docs/gui-smoke-artifacts/phase7/`: screenshots, samples, logs, and GUI evidence files.
- `README.md`: public status and Phase 7/RC4 boundary.
- `resources/localization/zh-Hans-overrides.toml`: only if a current-cycle GUI smoke finds a small user-visible blocker.
- `script/zh_apply_localization.py` and tests: only if a release guardrail bug is discovered.

## 6. Task Plan

### P7-M0: Phase 7 Entry And RC3 Blocker Snapshot

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`

- [x] Step 1: Confirm working baseline and record the current dirty worktree without reverting unrelated changes.

```bash
git status --short
git rev-parse --abbrev-ref HEAD
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

Expected:

```text
manifest validation passed
glossary check passed
would_change: 0
missing: 0
```

- [x] Step 2: Copy the RC3 blocker summary into the Phase 7 execution record:
  - GUI automation is `automation-blocked`.
  - `GUI-WS-06` has source anchors but no disposable endpoint evidence.
  - Base GUI rows need current-cycle evidence.
- [x] Step 3: Create `docs/gui-smoke-artifacts/phase7/` before taking screenshots or logs.

Acceptance:

- Phase 7 has a documented entry baseline.
- No GUI row is promoted from historical evidence.
- No source translation work begins before the GUI evidence path is recovered.

Execution note, 2026-05-31:

- Current branch: `drew/zh-Hans-localization`.
- Worktree is dirty from previous localization phases; no existing changes were reverted.
- `docs/gui-smoke-artifacts/phase7/` was created for Phase 7 evidence.
- `python3 script/zh_apply_localization.py --validate-manifest`: `manifest validation passed`.
- `python3 script/zh_apply_localization.py --check-glossary`: `glossary check passed`.
- `python3 script/zh_apply_localization.py --metadata-summary`: `entries: 2661`; `key/context/status/expected_count: 149 (5.6%)`.
- `python3 script/zh_apply_localization.py --metadata-summary --json`: valid JSON with `entries: 2661` and metadata percentages.
- `python3 script/zh_apply_localization.py --dry-run --summary`: `files: 197`; `already_applied: 2646`; `would_change: 0`; `missing: 0`.
- `python3 script/zh_localization_inventory.py --preset release --coverage`: `2889/6409`; `31.1%`.
- `git diff --check`: passed.

Self-review:

- P7-M0 acceptance is met.
- RC3 blockers are preserved as blockers; no historical GUI evidence was promoted.
- Next stage may proceed to P7-M1 profile/path isolation audit.

### P7-M1: Debug Profile And Path Isolation Audit

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Modify: `docs/zh-Hans-localization.md`

- [x] Step 1: Re-read the profile and path code.

```bash
rg -n "WARP_DATA_PROFILE|data_profile|data_domain|warp_home_config_dir|macos_config_dir_name|project_dirs" crates/warp_core/src
sed -n '120,165p' crates/warp_core/src/channel/state.rs
sed -n '1,130p' crates/warp_core/src/paths.rs
sed -n '190,270p' crates/warp_core/src/paths.rs
sed -n '1,220p' crates/warp_core/src/paths_tests.rs
```

- [x] Step 2: Run the path tests that are expected to pass without relying on a full profiled-path assumption.

```bash
cargo test -p warp_core path
WARP_DATA_PROFILE=zh-rc4 cargo test -p warp_core test_warp_home_config_dir_path
```

- [x] Step 3: Record an isolation map in the GUI matrix with these categories:
  - `profile-isolated`
  - `shared-with-oss`
  - `unknown-until-runtime`

- [x] Step 4: Decide whether `zh-smoke-delete-endpoint` can be created under an isolated profile.

Acceptance:

- `docs/zh-Hans-gui-smoke-matrix.md` states the exact directory behavior for `warp_home_config_dir`, `data_dir`, `config_local_dir`, `cache_dir`, and `state_dir`.
- If endpoint state may live under shared `~/.warp-oss`, Phase 7 must not delete it without a copied backup and restore note.

Execution note, 2026-05-31:

- Re-read `ChannelState::data_profile()`, `ChannelState::data_domain()`, path helpers, and path tests.
- `cargo test -p warp_core path`: 10 tests passed.
- `WARP_DATA_PROFILE=zh-rc4 cargo test -p warp_core test_warp_home_config_dir_path`: 1 test passed.
- `warp_home_config_dir()` is profile-aware: `~/.warp-oss-zh-rc4`.
- `data_dir()` and `config_local_dir()` are shared on macOS: `~/.warp-oss`.
- `cache_dir()` and `state_dir()` use profiled `ProjectDirs` and are expected to resolve under `~/Library/Application Support/dev.warp.WarpOss-zh-rc4` if the GUI process receives `WARP_DATA_PROFILE=zh-rc4`.
- `secure_state_dir()` is `unknown-until-runtime` because app group availability is runtime-dependent.
- Custom endpoint state is stored by `ApiKeyManager` in secure storage key `AiApiKeys`; macOS secure storage uses `ChannelState::data_domain()` as the service name.
- Decision: `zh-smoke-delete-endpoint` may be created only if P7-M2 proves the GUI process is launched with `WARP_DATA_PROFILE=zh-rc4` and the UI is visible. If profile propagation is not proven, do not create or delete the endpoint.

Self-review:

- P7-M1 acceptance is met.
- The isolation map is explicit and does not overstate full macOS profile isolation.
- Next stage may proceed to P7-M2 launch diagnosis.

### P7-M2: `WarpOss` Launch Hang Diagnosis

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: files under `docs/gui-smoke-artifacts/phase7/`

- [x] Step 1: Rebuild the bundle.

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

- [x] Step 2: Launch with a debug profile only after P7-M1 records the isolation boundary. Because `open` may not reliably pass per-process shell environment to LaunchServices, use `launchctl setenv` for the GUI launch and unset it immediately after the launch command returns.

```bash
launchctl setenv WARP_DATA_PROFILE zh-rc4
open -n target/debug/bundle/osx/WarpOss.app
launchctl unsetenv WARP_DATA_PROFILE
launchctl getenv WARP_DATA_PROFILE
```

- [x] Step 3: Capture process, screenshot, accessibility, and log evidence.

```bash
pgrep -afil 'warp-oss|terminal-server'
screencapture -x docs/gui-smoke-artifacts/phase7/p7-m2-launch.png
log show --last 5m --predicate 'process == "warp-oss"' --style compact > docs/gui-smoke-artifacts/phase7/p7-m2-warp-oss.log.txt
```

Use Computer Use in this order:

```text
get_app_state("WarpOss")
get_app_state("dev.warp.WarpOss")
```

- [x] Step 4: If the app is not responding, collect a sample from the `warp-oss` process.

```bash
WARP_OSS_PID="$(pgrep -n -f 'target/debug/bundle/osx/WarpOss.app/Contents/MacOS/warp-oss')"
sample "$WARP_OSS_PID" 5 -file docs/gui-smoke-artifacts/phase7/p7-m2-warp-oss.sample.txt
```

Acceptance:

- Phase 7 classifies launch state as one of:
  - `interactive-profile-ready`
  - `profile-isolation-insufficient`
  - `app-hang`
  - `computer-use-only-blocked`
- No release gate advances unless Computer Use or screenshot evidence shows actual UI content.

Execution note, 2026-05-31:

- Bundle rebuild passed with existing Rust warnings and produced `target/debug/bundle/osx/WarpOss.app`.
- `launchctl setenv WARP_DATA_PROFILE zh-rc4`, `open -n target/debug/bundle/osx/WarpOss.app`, `launchctl unsetenv WARP_DATA_PROFILE`, and `launchctl getenv WARP_DATA_PROFILE` completed; getenv returned empty after cleanup.
- `pgrep` found `warp-oss` pid `80871` and `terminal-server` pid `80874`.
- `ps eww -p 80871` confirmed `WARP_DATA_PROFILE=zh-rc4` in the GUI process environment.
- `docs/gui-smoke-artifacts/phase7/p7-m2-launch.png` captured the macOS permission dialog `“WarpOss”想访问其他 App 的数据。`.
- The permission dialog was denied according to the GUI smoke policy. `docs/gui-smoke-artifacts/phase7/p7-m2-after-permission-deny.png` shows the Warp welcome screen.
- `/usr/bin/log show` output was saved to `docs/gui-smoke-artifacts/phase7/p7-m2-warp-oss.log.txt` with 111 lines.
- Computer Use succeeded for `WarpOss` after the permission dialog was denied and read menu labels including `文件`, `编辑`, `视图`, `标签页`, `块`, `AI`, `Drive`, `窗口`, and `帮助`.
- No sample was needed because the app was responsive.
- Launch classification: `interactive-profile-ready`.

Self-review:

- P7-M2 acceptance is met.
- The GUI process is both profiled and readable through Computer Use.
- Next stage may proceed to P7-M3 and keep using `zh-rc4`.

### P7-M3: Recovery Path And Safe Profile Setup

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Modify: `docs/zh-Hans-localization.md`
- Add: files under `docs/gui-smoke-artifacts/phase7/`

- [x] Step 1: If P7-M2 is `interactive-profile-ready`, keep using `zh-rc4` and record the launch command.
- [x] Step 2: If P7-M2 is `computer-use-only-blocked`, capture screenshots manually and do not mark rows `verified` unless the anchors are readable in the screenshot.
- [x] Step 3: If P7-M2 is `profile-isolation-insufficient`, use a backup/restore workflow before touching custom endpoint state.

Required backup evidence when shared local state is involved:

```bash
BACKUP_DIR="/tmp/warp-cn-p7-state-backups/warp-oss-before-p7-20260531"
mkdir -p "/tmp/warp-cn-p7-state-backups"
ditto "$HOME/.warp-oss" "$BACKUP_DIR"
```

Restore command to record if the backup path is used:

```bash
ditto "$BACKUP_DIR" "$HOME/.warp-oss"
```

- [x] Step 4: If P7-M2 is `app-hang`, keep RC4 as non-public and record logs/sample output. Do not continue to destructive smoke.

Acceptance:

- The execution record names the selected recovery path.
- Any use of shared local state has a copied backup and a documented restore command.
- If the app remains hung, Phase 7 stops before creating test objects.

Execution note, 2026-05-31:

- Selected recovery path: `interactive-profile-ready`.
- Continue using the `zh-rc4` profile launched by:

```bash
launchctl setenv WARP_DATA_PROFILE zh-rc4
open -n target/debug/bundle/osx/WarpOss.app
launchctl unsetenv WARP_DATA_PROFILE
```

- Shared `.warp-oss` backup was not used because P7-M5's target object is stored in profiled secure storage (`AiApiKeys` under `dev.warp.WarpOss-zh-rc4`) and P7-M2 proved the GUI process received `WARP_DATA_PROFILE=zh-rc4`.
- `data_dir()` and `config_local_dir()` remain shared, so Phase 7 will avoid treating settings/user-preference mutations as fully isolated.
- P7-M4 may proceed with current-cycle GUI smoke.

Self-review:

- P7-M3 acceptance is met.
- No shared local state backup was needed for the selected endpoint path.
- The app is not hung, so Phase 7 should continue to P7-M4.

### P7-M4: Current-Cycle Base GUI Smoke

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase7/`

- [x] Step 1: Verify `GUI-BASE-01` macOS menu labels in the current RC cycle.
- [x] Step 2: Verify `GUI-BASE-02` global search placeholder in the current RC cycle.
- [x] Step 3: Verify `GUI-BASE-03` `新会话` entry in the current RC cycle.
- [x] Step 4: Verify `GUI-BASE-05` command palette chips and command search entry in the current RC cycle.
- [x] Step 5: Verify `GUI-SET-01` settings shell navigation in the current RC cycle.
- [x] Step 6: Verify `GUI-WS-08` vertical tab context menu in the current RC cycle.

Expected anchors:

```text
文件
编辑
视图
标签页
块
窗口
帮助
新会话
搜索命令
文件
操作
会话
启动配置
账户
Agent
代码
云平台
团队
外观
功能
键盘快捷键
隐私
关于
共享会话
复制窗格标题
复制工作目录
重命名标签页
关闭标签页
关闭其他标签页
关闭下方标签页
另存为新配置
```

Acceptance:

- Each row gets a 2026-05-31 Phase 7 evidence note or remains blocked with a specific reason.
- Process startup alone is not accepted.
- Historical Phase 4 evidence can be referenced, but it cannot satisfy RC4 by itself.

Execution note, 2026-05-31:

- Completed onboarding in `zh-rc4` by choosing terminal-only mode and dark theme.
- `docs/gui-smoke-artifacts/phase7/p7-m4-workspace.png`: current-cycle workspace evidence.
- `docs/gui-smoke-artifacts/phase7/p7-m4-command-palette.png`: `Cmd-P` shows `搜索命令`, `文件`, `操作`, `会话`, `启动配置`, and `打开主题选择器`.
- `docs/gui-smoke-artifacts/phase7/p7-m4-settings-shell.png`: settings shell shows `设置`, `账户`, `Agent`, `代码`, `云平台`, `团队`, `外观`, `功能`, `键盘快捷键`, `隐私`, and `关于`.
- `docs/gui-smoke-artifacts/phase7/p7-m4-tab-context-menu.png`: current tab context menu shows `共享会话`, `复制标签页标题`, `重命名标签页`, `左移标签页`, `关闭标签页`, `关闭其他标签页`, `关闭右侧标签页`, and `另存为新配置`.
- `docs/gui-smoke-artifacts/phase7/p7-m4-new-session-menu.png`: `+` menu shows `终端`, `新建 worktree 配置`, and `新建标签页配置`.
- `docs/gui-smoke-artifacts/phase7/p7-m4-file-menu.png`: system `文件` menu shows `新建终端标签页` and related entries.
- Current build uses horizontal tabs from onboarding. `GUI-WS-08` was verified as the current tab context menu rather than a vertical-tab-only menu.
- `GUI-BASE-03` current label variant is `新建终端标签页`/`终端`, not historical `新会话`; no English residue was observed.

Self-review:

- P7-M4 acceptance is met for current-cycle base GUI evidence.
- The label variants are documented instead of silently normalizing them to older wording.
- Next stage may proceed to P7-M5 custom endpoint destructive confirmation.

### P7-M5: Disposable Custom Endpoint Destructive Confirmation

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase7/`

- [x] Step 1: Confirm P7-M1 and P7-M3 allow safe endpoint creation.
- [ ] Step 2: In Settings > AI > 自定义推理, create a local endpoint named `zh-smoke-delete-endpoint`.

Use these disposable values:

```text
Name: zh-smoke-delete-endpoint
URL: https://example.invalid/zh-smoke
API key: zh-smoke-dummy-key
Model: zh-smoke-model
Alias: zh-smoke
```

- [ ] Step 3: Open the remove confirmation for the disposable endpoint.
- [ ] Step 4: Capture evidence before confirming deletion.

Expected anchors:

```text
移除端点？
确定要移除此端点吗？
zh-smoke-delete-endpoint
zh-smoke-model
取消
移除端点
```

- [ ] Step 5: Click `取消` first and confirm the endpoint still exists.
- [ ] Step 6: If the object is confirmed disposable and isolated, reopen the confirmation and click `移除端点`; otherwise leave the object in place and document why deletion was not performed.

Acceptance:

- `GUI-WS-06` is marked `verified` only if the confirmation dialog itself is visible and readable.
- No real endpoint is removed.
- The execution record names whether the disposable endpoint was deleted or intentionally left for manual cleanup.

Execution note, 2026-05-31:

- P7-M1/P7-M3 isolation conditions were sufficient for a profiled custom endpoint if the UI were available.
- P7-M5 did not create `zh-smoke-delete-endpoint`.
- Current `zh-rc4` GUI profile is logged out after terminal-only onboarding. The settings page shows account registration/login state and API key fields but does not show `自定义推理`.
- Source gate rechecked: `UserWorkspaces::is_custom_inference_enabled()` returns false for anonymous or logged-out users before checking workspace/customer state.
- Screenshot: `docs/gui-smoke-artifacts/phase7/p7-m5-custom-inference-blocked-logged-out.png`.
- No endpoint was created or deleted.

Self-review:

- P7-M5 acceptance is not met because the destructive confirmation dialog was not visible.
- The failure is a legitimate product-state blocker, not a launch or automation failure.
- Do not use the main account to bypass this gate. RC4 cannot be `ready-for-public-rc` unless another safe test account or fixture is provided.

### P7-M6: One Additional State Gate Or Explicit Deferral

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] Step 1: If P7-M4 and P7-M5 pass, choose exactly one additional low-risk state gate to probe:
  - `GUI-AUTH-02` token paste fallback with an invalid local token.
  - `GUI-AGENT-03` status labels with an existing local/mockable conversation lifecycle state.
  - `GUI-SET-03` AI settings deep path if the isolated profile exposes custom inference UI without requiring a paid account.
- [ ] Step 2: Record the trigger, evidence, and result.
- [x] Step 3: If no additional state gate can be triggered safely, explicitly defer it and keep RC4 evaluation based on the public-RC minimum gates.

Acceptance:

- Phase 7 does not spend time on broad account/Billing/Cloud gates unless the state is already available.
- Deferred gates name their owner category: `test-account`, `server-state`, `local-fixture`, or `manual-only`.

Execution note, 2026-05-31:

- P7-M6 was explicitly deferred because P7-M5 did not pass.
- `GUI-AUTH-02`, `GUI-AGENT-03`, and `GUI-SET-03` were not probed further in this cycle.
- Owner categories remain:
  - `GUI-AUTH-02`: `local-fixture` for invalid token fallback, but still needs visible logged-out auth flow.
  - `GUI-AGENT-03`: `local-fixture` or `test-account`, depending on whether a mockable lifecycle state exists.
  - `GUI-SET-03`: `test-account`, because custom inference is hidden for anonymous/logged-out users.

Self-review:

- P7-M6 acceptance is met as an explicit deferral.
- The deferral does not change RC4 eligibility: without P7-M5 destructive confirmation evidence, RC4 cannot be `ready-for-public-rc`.

### P7-M7: RC4 Gate And Public-RC Decision

**Files:**

- Add: `docs/zh-Hans-release-candidate-2026-05-31-rc4.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`

- [x] Step 1: Run the full RC4 command-line gate.

```bash
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

- [x] Step 2: Record the GUI gate result from P7-M4 and P7-M5.
- [x] Step 3: Choose exactly one release decision:
  - `ready-for-public-rc`
  - `ready-for-local-use`
  - `blocked`

Decision rules:

- Choose `ready-for-public-rc` only if command-line gates pass, bundle gate passes, current-cycle base GUI smoke passes, and `GUI-WS-06` has real evidence from the disposable endpoint confirmation.
- Choose `ready-for-local-use` if command-line and bundle gates pass but GUI/destructive evidence is still incomplete.
- Choose `blocked` if dry-run drift, tests, bundle generation, or app launch is broken.

Acceptance:

- RC4 explains the decision with exact evidence paths.
- README and `docs/zh-Hans-localization.md` match the RC4 decision.
- No public release language is used unless `ready-for-public-rc` is selected.

Execution note, 2026-05-31:

- Full RC4 command-line gate passed.
- Manifest validation and glossary checks passed.
- Metadata remains `entries: 2661`; `key/context/status/expected_count: 149 (5.6%)`; `preserve_terms: 18 (0.7%)`.
- Dry-run remains clean: `files: 197`; `already_applied: 2646`; `would_change: 0`; `missing: 0`.
- Release coverage remains `2889/6409 = 31.1%`.
- Locale exports passed: `/tmp/zh-CN.json` is 697971 bytes and `/tmp/zh-CN.yaml` is 570094 bytes; `python3 -m json.tool /tmp/zh-CN.json` passed.
- `cargo fmt --check`, `git diff --check`, Python compile checks, and all localization Python tests passed.
- `cargo check -p warp`, `cargo test -p warp_search_core`, and `cargo test -p warp command_palette` passed with existing unused-variable warnings in `scp_fallback.rs` and `slash_commands/mod.rs`.
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` passed and generated `target/debug/bundle/osx/WarpOss.app`.
- Current-cycle base GUI evidence from P7-M4 passed.
- P7-M5 destructive confirmation remains blocked by logged-out product state; no disposable endpoint was created or deleted.
- RC4 record created: `docs/zh-Hans-release-candidate-2026-05-31-rc4.md`.
- Decision: `ready-for-local-use`, not `ready-for-public-rc`.

Self-review:

- P7-M7 acceptance is met.
- RC4 is not blocked because the command-line, bundle, and base GUI gates pass.
- RC4 cannot be public-RC ready because the minimum destructive confirmation evidence is still missing.
