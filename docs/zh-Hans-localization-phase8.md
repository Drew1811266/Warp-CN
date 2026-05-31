# Warp CN Phase 8 Public-RC Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC4 `ready-for-local-use` to a defensible RC5 public-RC decision by verifying `GUI-WS-06` custom endpoint deletion with an isolated real product state.

**Architecture:** Phase 8 is a narrow release-gate phase, not a coverage phase. It keeps the existing source-level localization overlay unchanged unless GUI smoke exposes a blocking English residue, and it treats the custom endpoint destructive confirmation as the minimum missing public-RC evidence. The preferred path is an isolated test account where custom inference is enabled; debug-only fixtures may be used only to unblock localization rendering investigation, not to claim public-RC readiness.

**Tech Stack:** Rust/Warp client source, `resources/localization/zh-Hans-overrides.toml`, `script/zh_apply_localization.py`, `script/zh_localization_inventory.py`, `script/zh_export_locale.py`, macOS `WarpOss.app`, `WARP_DATA_PROFILE=zh-rc5`, Computer Use, macOS `screencapture`, `docs/zh-Hans-gui-smoke-matrix.md`, cargo test/check gates.

---

## 1. Phase 8 Positioning

Phase 7 recovered the current-cycle GUI path and produced RC4. RC4 is `ready-for-local-use`, not public RC, because the last required public-RC blocker remains:

- `GUI-WS-06` custom endpoint removal confirmation has translated source anchors.
- The `zh-rc4` profile was logged out and terminal-only.
- `UserWorkspaces::is_custom_inference_enabled()` returns false for anonymous/logged-out users.
- Therefore `自定义推理` did not render, `zh-smoke-delete-endpoint` was not created, and no destructive confirmation was visible.

Phase 8 should close exactly that gap. It should not expand broad `release` coverage, translate noisy candidate buckets, or test higher-risk destructive paths such as team ownership, cloud environment deletion, or managed auth-secret deletion unless the custom endpoint path proves impossible and the user explicitly changes the release criteria.

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

- `docs/zh-Hans-release-candidate-2026-05-31-rc4.md`
- Decision: `ready-for-local-use`
- Public RC decision: not ready
- Stable base: `v0.2026.05.27.09.22.stable_00`
- GUI status: `interactive-profile-ready`
- Current-cycle base GUI evidence: passed in P7-M4
- Remaining blocker: `GUI-WS-06` destructive confirmation, blocked by logged-out product state

## 3. Public-RC Rules

Phase 8 may choose `ready-for-public-rc` only when all of these are true:

- Fresh upstream stable refs are checked for the RC5 run, or the selected stable base is explicitly revalidated.
- Command-line gates pass.
- Bundle generation passes.
- Current-cycle base GUI smoke is still valid in the RC5 profile.
- `GUI-WS-06` is verified in the real GUI with an isolated disposable endpoint.
- The endpoint flow first clicks `取消` and proves the endpoint remains.
- The endpoint flow then removes only `zh-smoke-delete-endpoint`.
- No real endpoint, real cloud environment, real managed secret, production team, or main personal account state is mutated.

Phase 8 must choose `ready-for-local-use` if the command-line and bundle gates pass but custom inference remains unavailable because no isolated test account or fixture is available.

Phase 8 must choose `blocked` if dry-run drift, tests, bundle generation, app launch, or GUI access fails.

## 4. Non-Goals

Phase 8 does not do:

- No runtime language switch or first-party i18n framework.
- No broad translation coverage push.
- No public-RC claim from debug-only bypasses, process startup, source anchors, or historical screenshots.
- No use of the user's main account for destructive or billing-adjacent validation.
- No deletion of real endpoints, cloud environments, managed secrets, team members, teams, or ownership state.
- No permanent test-only UI in release behavior.

## 5. Files And Responsibilities

Expected files to modify during Phase 8:

- `docs/zh-Hans-localization.md`: Phase 8 execution record and RC5 decision.
- `docs/zh-Hans-gui-smoke-matrix.md`: `GUI-WS-06` evidence, profile/account notes, and any blocker updates.
- `docs/zh-Hans-release-candidate-2026-05-31-rc5.md`: final RC5 gate and release decision.
- `docs/gui-smoke-artifacts/phase8/`: screenshots, process environment proof, logs, and GUI evidence files.
- `README.md`: public status and Phase 8/RC5 boundary.
- `resources/localization/zh-Hans-overrides.toml`: only if the RC5 GUI pass finds a small blocking English residue in the custom endpoint flow.
- `script/zh_apply_localization.py` and tests: only if a release guardrail bug is discovered.

Files to read before execution:

- `docs/zh-Hans-release-candidate-2026-05-31-rc4.md`
- `docs/zh-Hans-gui-smoke-matrix.md`
- `app/src/workspaces/user_workspaces.rs`
- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/custom_inference_modal.rs`
- `app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs`
- `crates/ai/src/api_keys.rs`

## 6. Required Test Account Or Fixture

Preferred path: isolated real test account.

The test account must satisfy:

- It is not the user's main account.
- It is safe to log into the local `WarpOss.app` debug build.
- It can show Settings > AI > `自定义推理`.
- It has no real custom endpoints that should be preserved, or the smoke uses a uniquely named endpoint and verifies only that endpoint.
- It does not rely on production team ownership, billing mutation, or cloud environment mutation.

Fallback path: debug-only localization fixture.

If no isolated test account is available, Phase 8 may plan a separate fixture slice that renders the custom endpoint UI in a debug-only smoke state. That fixture can prove translated dialog rendering and screenshot automation, but it cannot satisfy `ready-for-public-rc` by itself because it bypasses the real logged-in product gate.

## 7. Task Plan

### P8-M0: Entry Baseline And RC4 Blocker Snapshot

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`
- Create: `docs/gui-smoke-artifacts/phase8/`

- [x] Step 1: Record worktree and branch state without reverting unrelated changes.

```bash
git status --short
git rev-parse --abbrev-ref HEAD
```

Expected:

```text
drew/zh-Hans-localization
```

The worktree is expected to be dirty from prior localization phases. Do not reset it.

- [x] Step 2: Run the Phase 8 entry gate.

```bash
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
entries: 2661
would_change: 0
missing: 0
```

- [x] Step 3: Create the Phase 8 artifact directory.

```bash
mkdir -p docs/gui-smoke-artifacts/phase8
```

- [x] Step 4: Copy the RC4 blocker into the execution record:
  - Current-cycle GUI launch recovered.
  - Current-cycle base GUI smoke passed.
  - `GUI-WS-06` remains unverified because logged-out state hides `自定义推理`.
  - No endpoint was created or deleted in Phase 7.

Acceptance:

- Phase 8 has a documented entry baseline.
- `docs/gui-smoke-artifacts/phase8/` exists before any new screenshots.
- No GUI row is promoted based on RC4 evidence alone.

Execution note, 2026-05-31:

- Current branch: `drew/zh-Hans-localization`.
- Worktree is dirty from previous localization phases; no existing changes were reverted.
- `docs/gui-smoke-artifacts/phase8/` was created.
- `python3 script/zh_apply_localization.py --validate-manifest`: `manifest validation passed`.
- `python3 script/zh_apply_localization.py --check-glossary`: `glossary check passed`.
- `python3 script/zh_apply_localization.py --metadata-summary`: `entries: 2661`; `key/context/status/expected_count: 149 (5.6%)`.
- `python3 script/zh_apply_localization.py --metadata-summary --json`: valid JSON with `entries: 2661` and metadata percentages.
- `python3 script/zh_apply_localization.py --dry-run --summary`: `files: 197`; `already_applied: 2646`; `would_change: 0`; `missing: 0`.
- `python3 script/zh_localization_inventory.py --preset release --coverage`: `2889/6409`; `31.1%`.
- `git diff --check`: passed.
- RC4 blocker carried forward: current-cycle GUI base smoke is recovered, but `GUI-WS-06` remains unverified because logged-out state hides `自定义推理`. No endpoint was created or deleted in Phase 7.

Self-review:

- P8-M0 acceptance is met.
- The entry baseline is clean and the artifact directory exists.
- No GUI row was promoted from RC4 evidence alone.

### P8-M1: Upstream Stable Freshness Recheck

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-upstream-sync.md` only if the workflow has changed

- [x] Step 1: Refresh upstream refs.

```bash
git fetch origin --tags
```

Expected:

```text
exit code 0
```

- [x] Step 2: Record the selected stable base and branch distance.

```bash
git tag --list 'v*.stable_*' --sort=-creatordate | head -5
UPSTREAM_BASE="$(git tag --list 'v*.stable_*' --sort=-creatordate | head -1)"
git rev-parse "$UPSTREAM_BASE"
git show -s --format=%s "$UPSTREAM_BASE"
git rev-list --left-right --count "$UPSTREAM_BASE...HEAD"
```

Expected:

```text
The selected base is a stable tag.
The branch distance is recorded in docs.
```

- [x] Step 3: If a newer stable tag appears, run dry-run against the current tree before changing translations.

```bash
python3 script/zh_apply_localization.py --dry-run --summary
```

Expected:

```text
would_change: 0
missing: 0
```

Acceptance:

- RC5 has a fresh upstream ref statement.
- If refs cannot be fetched, RC5 cannot be `ready-for-public-rc`; document it as a public-RC blocker.

Execution note, 2026-05-31:

- `git fetch origin --tags` passed.
- `origin/master` advanced to `5767910b5e41bda196baaea041862e9505e46e20` (`Add ./script/format for customized cargo fmt invocation. (#11747)`).
- Latest stable tags after fetch:
  - `v0.2026.05.27.09.22.stable_00`
  - `v0.2026.05.20.09.21.stable_00`
  - `v0.2026.05.13.09.14.stable_00`
  - `v0.2026.05.06.09.12.stable_00`
  - `v0.2026.04.29.08.56.stable_00`
- Selected stable base remains `v0.2026.05.27.09.22.stable_00`.
- Selected stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`.
- Selected stable subject: `Enable async find on dogfood, add toggle for Preview/Stable (#11555)`.
- Branch distance from selected stable remains `0 88`.
- Post-fetch dry-run remains clean: `files: 197`; `already_applied: 2646`; `would_change: 0`; `missing: 0`.

Self-review:

- P8-M1 acceptance is met.
- RC5 has a fresh upstream refs statement.
- No newer stable tag appeared, and no manifest drift was introduced by the fetch.

### P8-M2: Evidence Path Selection

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [x] Step 1: Decide whether an isolated test account is available.

Record exactly one value:

```text
P8 evidence path: isolated-test-account
P8 evidence path: no-test-account
```

- [x] Step 2: If the path is `isolated-test-account`, record the account safety constraints without storing credentials:
  - account is not the user's main account
  - account can be mutated for local endpoint settings
  - account can show Settings > AI > `自定义推理`
  - no billing/team/cloud destructive actions will be performed

- [x] Step 3: If the path is `no-test-account`, stop the public-RC path for this phase and document the next useful fallback as a separate debug-only fixture slice.

Acceptance:

- Phase 8 does not ask the executor to guess credentials.
- The release decision rules remain clear: no test account means no public-RC decision.

Execution note, 2026-05-31:

```text
P8 evidence path: no-test-account
```

- No isolated test account or fixture credentials were provided in the current execution context.
- The executor did not guess credentials and did not use the user's main account.
- Public-RC evidence path stops here for this run.
- P8-M3 through P8-M6 are deferred for the public-RC path because they require a logged-in isolated account where `自定义推理` is visible.
- Next useful fallback: add a separate debug-only custom inference fixture slice that can render the custom endpoint list and remove-confirmation dialog without real account state. That fixture can help verify rendering and screenshots, but it cannot by itself satisfy `ready-for-public-rc`.

Self-review:

- P8-M2 acceptance is met.
- The evidence path is explicit and does not ask the executor to invent credentials.
- RC5 can still proceed to command-line/bundle gate, but the release decision cannot be `ready-for-public-rc`.

### P8-M3: Launch `zh-rc5` Profile And Complete Safe Login

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase8/`

- [ ] Step 1: Build the app bundle.

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
Successfully bundled
target/debug/bundle/osx/WarpOss.app
```

- [ ] Step 2: Launch with the RC5 profile.

```bash
launchctl setenv WARP_DATA_PROFILE zh-rc5
open -n target/debug/bundle/osx/WarpOss.app
launchctl unsetenv WARP_DATA_PROFILE
launchctl getenv WARP_DATA_PROFILE
```

Expected:

```text
The final getenv output is empty.
```

- [ ] Step 3: Prove the GUI process received the profile.

```bash
pgrep -afil 'warp-oss|terminal-server'
WARP_OSS_PID="$(pgrep -n -f 'target/debug/bundle/osx/WarpOss.app/Contents/MacOS/warp-oss')"
ps eww -p "$WARP_OSS_PID" | tr ' ' '\n' | rg 'WARP_DATA_PROFILE|__CFBundleIdentifier|dev\.warp'
```

Expected:

```text
WARP_DATA_PROFILE=zh-rc5
__CFBundleIdentifier=dev.warp.WarpOss
```

- [ ] Step 4: Use Computer Use to confirm the app is interactive.

```text
get_app_state("WarpOss")
```

Expected anchors:

```text
文件
编辑
视图
标签页
窗口
帮助
```

- [ ] Step 5: Log into the isolated test account only if P8-M2 selected `isolated-test-account`.

Evidence rules:

- Do not record passwords, tokens, cookies, or magic links in docs.
- Screenshots may show generic logged-in UI, but must not expose secrets.
- If browser callback fails, record the exact visible error and stop before creating endpoint objects.

Acceptance:

- The RC5 GUI profile is interactive and profile-propagated.
- Login is completed only for an isolated test account.
- If login cannot be completed, Phase 8 remains `ready-for-local-use` at most.

Execution note, 2026-05-31:

- P8-M3 was deferred because P8-M2 selected `no-test-account`.
- The executor did not launch a logged-in `zh-rc5` profile and did not attempt login.
- No browser auth callback, token paste flow, or account mutation was attempted.

Self-review:

- P8-M3 public-RC acceptance is not met.
- The deferral is expected under the P8-M2 `no-test-account` path and prevents unsafe credential guessing.

### P8-M4: Revalidate Current-Cycle Base GUI In Logged-In Profile

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase8/`

- [ ] Step 1: Capture workspace/menu evidence.

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m4-workspace.png
```

Expected anchors:

```text
文件
编辑
视图
标签页
块
窗口
帮助
```

- [ ] Step 2: Capture command palette evidence.

Trigger:

```text
Cmd-P
```

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m4-command-palette.png
```

Expected anchors:

```text
搜索命令
文件
操作
会话
启动配置
```

- [ ] Step 3: Capture settings shell evidence.

Expected anchors:

```text
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
```

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m4-settings-shell.png
```

Acceptance:

- P8 uses current-cycle GUI evidence from `zh-rc5`, not only P7 screenshots.
- If logged-in state changes the shell, the changed labels are recorded rather than normalized to older wording.

Execution note, 2026-05-31:

- P8-M4 was deferred because P8-M2 selected `no-test-account`.
- No logged-in `zh-rc5` profile was available, so current-cycle logged-in base GUI evidence was not collected.
- Phase 7 `zh-rc4` base GUI evidence remains valid for local-use context, but it is not promoted as RC5 public-RC evidence.

Self-review:

- P8-M4 public-RC acceptance is not met.
- The deferral is expected under the P8-M2 `no-test-account` path.

### P8-M5: Verify Custom Inference Visibility And Create Disposable Endpoint

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase8/`

- [ ] Step 1: Navigate to Settings > AI and verify `自定义推理` is visible.

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m5-custom-inference-visible.png
```

Expected anchors:

```text
自定义推理
添加自定义端点
```

- [ ] Step 2: If `自定义推理` is not visible, record the account/product-state blocker and stop before creating any endpoint.

Record one blocker:

```text
custom inference hidden: logged-out
custom inference hidden: feature flag off
custom inference hidden: enterprise workspace without entitlement
custom inference hidden: unknown
```

- [ ] Step 3: Create a disposable endpoint with these exact values.

```text
Name: zh-smoke-delete-endpoint
URL: https://example.invalid/zh-smoke
API key: zh-smoke-dummy-key
Model: zh-smoke-model
Alias: zh-smoke
```

- [ ] Step 4: Capture evidence that the endpoint exists.

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m5-endpoint-created.png
```

Expected anchors:

```text
zh-smoke-delete-endpoint
zh-smoke
编辑
```

Acceptance:

- Only `zh-smoke-delete-endpoint` is created.
- No real endpoint URL or API key is entered.
- If the endpoint cannot be created, no destructive confirmation is attempted.

Execution note, 2026-05-31:

- P8-M5 was deferred because P8-M2 selected `no-test-account`.
- No `zh-smoke-delete-endpoint` was created.
- No real endpoint URL, API key, or model was entered.

Self-review:

- P8-M5 public-RC acceptance is not met.
- The safe behavior is correct: without isolated logged-in account state, do not create endpoint objects.

### P8-M6: Verify Remove Endpoint Confirmation With Cancel-Then-Confirm

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase8/`

- [ ] Step 1: Open the edit modal for `zh-smoke-delete-endpoint`.

Expected anchors:

```text
编辑自定义端点
zh-smoke-delete-endpoint
zh-smoke-model
移除端点
```

- [ ] Step 2: Click `移除端点` to open the destructive confirmation.

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m6-remove-endpoint-confirmation.png
```

Expected anchors:

```text
移除端点？
确定要移除此端点吗？
zh-smoke-delete-endpoint
zh-smoke
取消
移除端点
```

- [ ] Step 3: Click `取消` first.

Screenshot after cancel:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m6-after-cancel-endpoint-still-present.png
```

Expected anchors:

```text
zh-smoke-delete-endpoint
编辑
```

- [ ] Step 4: Reopen the confirmation and click `移除端点`.

Screenshot before final removal:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m6-before-final-remove.png
```

Expected anchors:

```text
移除端点？
zh-smoke-delete-endpoint
移除端点
```

- [ ] Step 5: Capture evidence after deletion.

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase8/p8-m6-after-remove-endpoint-absent.png
```

Expected:

```text
zh-smoke-delete-endpoint is not visible in the custom endpoints list.
```

Acceptance:

- `GUI-WS-06` is marked `verified` only after the confirmation dialog is visible and readable.
- The cancel path is proven before deletion.
- Only `zh-smoke-delete-endpoint` is deleted.
- The execution record states whether the disposable endpoint was deleted or intentionally left for manual cleanup.

Execution note, 2026-05-31:

- P8-M6 was deferred because P8-M5 did not create a disposable endpoint.
- No remove endpoint confirmation was opened.
- No endpoint was removed.
- `zh-smoke-delete-endpoint cleanup: not created`.

Self-review:

- P8-M6 public-RC acceptance is not met.
- No destructive action was performed without a disposable isolated object.

### P8-M7: RC5 Gate And Release Decision

**Files:**

- Add: `docs/zh-Hans-release-candidate-2026-05-31-rc5.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`

- [x] Step 1: Run the full RC5 command-line gate.

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

Expected:

```text
manifest validation passed
glossary check passed
would_change: 0
missing: 0
all Python tests pass
Rust tests pass
Successfully bundled
```

- [x] Step 2: Record GUI evidence from P8-M4 through P8-M6.

- [x] Step 3: Choose exactly one release decision:

```text
ready-for-public-rc
ready-for-local-use
blocked
```

Decision rules:

- Choose `ready-for-public-rc` only if P8-M1, P8-M4, P8-M5, P8-M6, and the RC5 command-line gate all pass.
- Choose `ready-for-local-use` if command-line and bundle gates pass but the test-account/custom-inference/destructive-confirmation evidence is incomplete.
- Choose `blocked` if dry-run drift, tests, bundle generation, app launch, or GUI access is broken.

Acceptance:

- RC5 explains the decision with exact evidence paths.
- README and `docs/zh-Hans-localization.md` match the RC5 decision.
- No public release language is used unless `ready-for-public-rc` is selected.

Execution note, 2026-05-31:

- Full RC5 command-line gate passed.
- Manifest validation and glossary checks passed.
- Metadata remains `entries: 2661`; `key/context/status/expected_count: 149 (5.6%)`; `preserve_terms: 18 (0.7%)`.
- Dry-run remains clean: `files: 197`; `already_applied: 2646`; `would_change: 0`; `missing: 0`.
- Release coverage remains `2889/6409 = 31.1%`.
- Locale exports passed: `/tmp/zh-CN.json` is 697971 bytes and `/tmp/zh-CN.yaml` is 570094 bytes; `python3 -m json.tool /tmp/zh-CN.json` passed.
- `cargo fmt --check`, `git diff --check`, Python compile checks, and all localization Python tests passed.
- `cargo check -p warp`, `cargo test -p warp_search_core`, and `cargo test -p warp command_palette` passed with existing unused-variable warnings in `scp_fallback.rs` and `slash_commands/mod.rs`.
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` passed and generated `target/debug/bundle/osx/WarpOss.app`.
- GUI evidence from P8-M4 through P8-M6 is deferred due P8-M2 `no-test-account`.
- RC5 record created: `docs/zh-Hans-release-candidate-2026-05-31-rc5.md`.
- Decision: `ready-for-local-use`, not `ready-for-public-rc`.

Self-review:

- P8-M7 acceptance is met.
- RC5 is not blocked because command-line, test, and bundle gates pass.
- RC5 cannot be public-RC ready because no isolated test account was available and no destructive confirmation evidence exists.

### P8-M8: Post-Decision Cleanup And Handoff

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Modify: `docs/zh-Hans-localization.md`

- [x] Step 1: Verify no `warp-oss` GUI process is left running unless the user wants it open.

```bash
pgrep -afil 'target/debug/bundle/osx/WarpOss.app|warp-oss|terminal-server'
```

Expected:

```text
Either no Phase 8 debug process remains, or the remaining process is explicitly documented.
```

- [x] Step 2: Verify LaunchServices environment cleanup.

```bash
launchctl getenv WARP_DATA_PROFILE
```

Expected:

```text
No value is printed.
```

- [x] Step 3: If the disposable endpoint was intentionally left in place, document cleanup ownership.

Record:

```text
zh-smoke-delete-endpoint cleanup: deleted
```

or:

```text
zh-smoke-delete-endpoint cleanup: left in isolated test account for manual cleanup
```

Acceptance:

- Phase 8 leaves no ambiguous destructive-test state.
- The next phase starts from a clear RC5 decision and a clean evidence record.

Execution note, 2026-05-31:

- `pgrep -afil 'target/debug/bundle/osx/WarpOss.app|warp-oss|terminal-server'` returned no Phase 8 GUI process.
- `launchctl getenv WARP_DATA_PROFILE` returned no value.
- `zh-smoke-delete-endpoint cleanup: not created`.
- No destructive-test object is left behind.

Self-review:

- P8-M8 acceptance is met.
- Phase 8 leaves no ambiguous process, LaunchServices environment, or endpoint cleanup state.

## 8. Self-Review

Spec coverage:

- RC4 blocker is covered by P8-M2 through P8-M6.
- Upstream freshness is covered by P8-M1.
- Command-line and bundle release gate is covered by P8-M7.
- Cleanup and handoff are covered by P8-M8.

Placeholder scan:

- No task uses placeholder markers or open-ended implementation language.
- Conditional branches have explicit release-decision consequences.

Risk review:

- The plan does not use the main account.
- The plan does not delete real user objects.
- The plan does not treat debug-only fixture evidence as public-RC evidence.
