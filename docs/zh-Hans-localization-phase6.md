# Warp CN Phase 6 Public-RC Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from Phase 5 `ready-for-local-use` to a defensible public RC decision by refreshing upstream refs and producing real GUI evidence for the currently blocked release gates.

**Architecture:** Phase 6 treats the translated source tree as a generated overlay output and focuses on repeatable verification. The main work is upstream refresh, GUI fixture/profile design, destructive confirmation evidence, account/state fixture planning, targeted terminal/Agent slices, and a final RC3 decision.

**Tech Stack:** Rust/Warp client source, `resources/localization/zh-Hans-overrides.toml`, `script/zh_apply_localization.py`, `script/zh_localization_inventory.py`, `script/zh_export_locale.py`, macOS `WarpOss.app`, Computer Use/GUI smoke records, cargo test/check gates.

---

## 1. Phase 6 Positioning

Phase 5 produced RC2 and a clear release decision: `ready-for-local-use`, not `ready-for-public-rc`.

Phase 6 should not chase broad translation coverage. Its job is to close the specific evidence gaps that prevented RC2 from becoming a public RC:

- Fresh upstream stable refs were not fetched successfully.
- No destructive confirmation has real GUI evidence from an isolated test object.
- Account, Billing, Cloud Agent, and Agent lifecycle states still need isolated accounts, service-side states, local fixtures, or test harnesses.
- GUI automation became unreliable in P5-M2, so process startup and screenshots are not enough.

## 2. Current Baseline

Baseline date: 2026-05-31.

```text
entries: 2645
files: 194
already_applied: 2630
would_change: 0
missing: 0
```

Metadata:

```text
key/context/status/expected_count: 133 (5.0%)
```

Release coverage:

```text
preset: release
covered: 2873
candidates: 6425
coverage: 30.9%
```

Current RC record:

- `docs/zh-Hans-release-candidate-2026-05-30-rc2.md`
- Decision: `ready-for-local-use`
- Public RC blockers: upstream refs, destructive confirmation GUI evidence, account/Billing/Cloud/Agent state evidence.

## 3. Non-Goals

Phase 6 does not do:

- No runtime language switch or first-party i18n runtime.
- No broad `modals` coverage push.
- No dev/nightly daily release tracking.
- No destructive testing against the main personal account, production team, production billing state, or real secrets.
- No translation of terminal protocol, command syntax, telemetry, logs, test fixtures, or search tokens unless a GUI/runtime review proves the string is user-facing and safe.
- No public release claim until upstream freshness and GUI evidence are explicitly satisfied.

## 4. Files And Responsibilities

Expected files to modify during Phase 6:

- `docs/zh-Hans-localization.md`: phase status, execution record, release decision.
- `docs/zh-Hans-gui-smoke-matrix.md`: GUI fixture records, screenshots, Computer Use evidence, manual-gate outcomes.
- `docs/zh-Hans-upstream-sync.md`: refreshed stable refs, merge/rebase decision, drift results.
- `docs/zh-Hans-release-candidate-2026-05-31-rc3.md`: final Phase 6 RC3 gate and release decision.
- `resources/localization/zh-Hans-overrides.toml`: only targeted user-visible translations with metadata.
- `resources/localization/zh-Hans-inventory-ignore.toml`: only reviewed non-UI path/line ignores.
- `script/zh_apply_localization.py`: optional machine-readable metadata summary or CI failure thresholds.
- `script/test_zh_apply_localization.py`: tests for any script changes.
- `README.md`: public status and RC3 boundary if Phase 6 reaches a new decision.

## 5. Task Plan

### P6-M0: Phase 6 Entry And Baseline

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`

- [x] Step 1: Run baseline checks.

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

Expected:

```text
manifest validation passed
glossary check passed
missing: 0
would_change: 0
```

- [x] Step 2: Record Phase 6 start state in `docs/zh-Hans-localization.md`.
- [x] Step 3: Add a README pointer to this Phase 6 plan.

Execution note, 2026-05-31:

- `python3 script/zh_apply_localization.py --validate-manifest`: `manifest validation passed`
- `python3 script/zh_apply_localization.py --check-glossary`: `glossary check passed`
- `python3 script/zh_apply_localization.py --metadata-summary`: `entries: 2645`; `key/context/status/expected_count: 133 (5.0%)`
- `python3 script/zh_apply_localization.py --dry-run --summary`: `files: 194`; `already_applied: 2630`; `would_change: 0`; `missing: 0`
- `python3 script/zh_localization_inventory.py --preset release --coverage`: `2873/6425`; `30.9%`
- `git diff --check`: passed

Acceptance:

- Phase 6 has a documented baseline.
- No release freshness or GUI verification claim is made yet.

### P6-M1: Upstream Stable Refresh Or Explicit Freshness Block

**Files:**

- Modify: `docs/zh-Hans-upstream-sync.md`
- Modify: `docs/zh-Hans-localization.md`

- [x] Step 1: Inspect remotes and local stable refs.

```bash
git remote -v
git tag --sort=-v:refname | rg 'stable' | head -20
git rev-parse v0.2026.05.27.09.22.stable_00^{commit}
```

- [x] Step 2: Retry upstream fetch.

```bash
git fetch origin --tags
```

Expected if network works:

```text
exit 0
```

Expected if network still fails:

```text
fatal: unable to access ...
```

- [x] Step 3: If fetch succeeds, select the newest stable tag and run drift checks.

```bash
UPSTREAM_BASE="$(git tag --sort=-v:refname | rg 'stable' | head -1)"
git rev-parse "$UPSTREAM_BASE^{commit}"
python3 script/zh_apply_localization.py --dry-run --summary
```

- [x] Step 4: If fetch fails, run a lightweight ref check and document the failure. Not needed on 2026-05-31 because `git fetch origin --tags` succeeded.

```bash
git -c http.version=HTTP/1.1 ls-remote --tags origin '*stable*'
```

Acceptance:

- Either a freshly fetched stable base is selected, or RC3 remains blocked on upstream freshness with exact command output recorded.
- `missing` is `0` after any overlay drift repair.

Execution note, 2026-05-31:

- `git remote -v`: `origin` points at `https://github.com/warpdotdev/warp.git`; `github` points at `https://github.com/Drew1811266/Warp-CN.git`.
- Latest stable tags after fetch: newest is `v0.2026.05.27.09.22.stable_00`.
- `git fetch origin --tags`: passed. It refreshed branches and added dev tags `v0.2026.05.29.09.24.dev_00` and `v0.2026.05.30.08.57.dev_00`; no newer stable tag appeared.
- Selected stable base: `v0.2026.05.27.09.22.stable_00`.
- Selected stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`.
- Selected stable subject: `Enable async find on dogfood, add toggle for Preview/Stable (#11555)`.
- Current `origin/master`: `74d256646c24f5ac8cc93af1792e57e35062cc44`, `[4/5] Use remote-aware skill locations in UI consumers (#11581)`.
- Ahead/behind against selected stable tag: `0 88` from `git rev-list --left-right --count "$UPSTREAM_BASE...HEAD"`.
- Dry-run after refresh: `entries: 2645`; `files: 194`; `already_applied: 2630`; `would_change: 0`; `missing: 0`.

### P6-M2: GUI Automation Recovery And Isolated Profile Strategy

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [x] Step 1: Rebuild the local bundle.

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

- [x] Step 2: Launch and collect process/window evidence.

```bash
open -n target/debug/bundle/osx/WarpOss.app
pgrep -afil 'warp-oss|terminal-server'
```

- [x] Step 3: Try Computer Use window capture before deeper GUI work.

Expected verified evidence:

```text
Computer Use can read menu/workspace text such as 文件, 编辑, 新会话.
```

Blocked evidence:

```text
Computer Use timeout or screenshot showing only desktop wallpaper.
```

- [x] Step 4: Document whether Phase 6 can use current local profile or must use a new isolated profile strategy.

Acceptance:

- GUI matrix says one of:
  - `interactive-profile-ready`
  - `automation-blocked`
  - `requires-isolated-profile`
- No business path is marked `verified` from process evidence alone.

Execution note, 2026-05-31:

- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`: passed and rebuilt `target/debug/bundle/osx/WarpOss.app`.
- Build warnings were existing Rust unused-variable warnings in `scp_fallback.rs` and `terminal/input/slash_commands/mod.rs`; no build failure.
- `open -n target/debug/bundle/osx/WarpOss.app`: returned successfully.
- `pgrep -afil 'warp-oss|terminal-server'`: found `warp-oss` and `terminal-server`.
- `mcp__computer_use.get_app_state` for `WarpOss` and `dev.warp.WarpOss`: `Computer Use server error -10005: timeoutReached`.
- macOS screenshot showed a system alert: `你不能打开应用程序 “WarpOss”，因为它没有响应。`
- Screenshot evidence: `docs/gui-smoke-artifacts/phase6/p6-m2-warp-oss-not-responding-2026-05-31.png`
- `/usr/bin/log show --last 3m --predicate 'process == "warp-oss"' --style compact`: no useful app log rows.
- P6-M2 status: `automation-blocked`.
- No business GUI row was promoted to `verified` from process evidence.

### P6-M3: Low-Risk Destructive Confirmation GUI Evidence

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Modify: `docs/zh-Hans-localization.md`

- [x] Step 1: Try the lowest-risk path first: custom endpoint deletion.

Safe object requirement:

```text
Create a disposable local custom endpoint named zh-smoke-delete-endpoint with a non-production URL and dummy model label, then open edit/remove confirmation.
```

Expected Chinese anchors:

```text
移除端点？
确定要移除此端点吗？
移除端点
取消
```

- [x] Step 2: If custom endpoint cannot be triggered, document the exact feature/plan blocker.
- [x] Step 3: If custom endpoint works, capture Computer Use evidence or screenshot path and mark `GUI-WS-06` verified. Not applicable on 2026-05-31 because the app is `automation-blocked`.
- [x] Step 4: Only after endpoint succeeds, consider environment deletion with an isolated cloud environment.
- [x] Step 5: Auth-secret deletion remains blocked unless an isolated managed secret can be created and deleted without touching real credentials.

Acceptance:

- At least one of `GUI-WS-06`, `GUI-SET-06`, or `GUI-WS-04` is `verified`, or each row has a concrete blocker with feature/account/object reason.
- No real endpoint, production environment, or real secret is deleted.

Execution note, 2026-05-31:

- `GUI-WS-06` custom endpoint deletion was not triggered because P6-M2 showed `WarpOss` is `automation-blocked` and the current profile has no disposable `zh-smoke-delete-endpoint` object.
- Source anchors were rechecked: `app/src/settings_view/ai_page.rs` routes `CustomEndpointModalEvent::RemoveEndpoint` to `show_remove_custom_endpoint_confirmation_dialog`; `app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs` contains `移除端点？`, `确定要移除此端点吗？之后你将无法在 Agent 会话中使用它的模型。`, `取消`, and `移除端点`.
- `GUI-SET-06` environment deletion was not attempted because endpoint deletion did not verify first, the app is `automation-blocked`, and there is no isolated cloud environment object.
- Source anchors were rechecked: `app/src/settings_view/update_environment_form.rs`, `app/src/settings_view/environments_page.rs`, and `app/src/settings_view/delete_environment_confirmation_dialog.rs` contain `删除环境`, `删除环境？`, and `确定要移除 ... 环境吗？`.
- `GUI-WS-04` auth-secret deletion remains blocked because there is no isolated managed auth secret and the app is `automation-blocked`.
- Source anchors were rechecked: `app/src/terminal/view/ambient_agent/auth_secret_selector.rs` opens the delete action, and `app/src/terminal/view/ambient_agent/delete_auth_secret_confirmation_dialog.rs` contains `删除密钥`, `确定要删除 ... 吗？此操作无法撤销。任何引用此密钥的 Agent 或环境都将无法再访问它。`, `取消`, and `删除`.
- No real endpoint, cloud environment, or secret was deleted.

### P6-M4: Account, Billing, Cloud, And Agent Fixture Strategy

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Optionally Modify: `script/zh_localization_inventory.py` only if fixture-related filtering is needed.

- [x] Step 1: Split account gates into local/fresh-profile and test-account categories.
- [x] Step 2: Split Billing gates into model-testable conditions and real-account-only conditions.
- [x] Step 3: Split Cloud Agent gates into local fixture, server state, and cannot-test-without-service categories.
- [x] Step 4: Split Agent lifecycle gates into state labels that can be model-tested and GUI states that require real/fixture conversations.

Acceptance:

- Each account/Billing/Cloud/Agent row has an owner category:
  - `local-fixture`
  - `test-account`
  - `server-state`
  - `manual-only`
- No gate says only “需要账号状态” without a concrete trigger.

Execution note, 2026-05-31:

- Added a P6-M4 ownership map to `docs/zh-Hans-gui-smoke-matrix.md`.
- Account/auth rows now distinguish `test-account` (`GUI-AUTH-01`) from `local-fixture` (`GUI-AUTH-02`, `GUI-AUTH-03`).
- Billing rows distinguish model-testable/local fixture work (`GUI-BILL-01`) from service-side team agreement state (`GUI-BILL-02`).
- Cloud Agent capacity remains `server-state` because the public GUI state depends on quota/capacity service responses.
- Agent rows now distinguish fixture conversations/statuses from stateful service/account errors.
- Existing matrix text contains no row whose only blocker is “需要账号状态”.

### P6-M5: Targeted Terminal/Agent User-Visible Slice

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify: `docs/zh-Hans-modal-candidate-classification.md`
- Modify: source file for selected slice after applying manifest.

Recommended priority order:

1. `terminal.view.notifications`
2. `terminal.view.shell_init`
3. `terminal.view.oz_permissions`
4. `terminal.view.file_context_menu`
5. `agent.driver.user_errors`

- [x] Step 1: Inspect top `modals` candidates.

```bash
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

- [x] Step 2: Pick exactly one slice and record why it is user-visible UI.
- [x] Step 3: Add manifest entries with `key`, `context`, `status`, and `expected_count`.
- [x] Step 4: Apply the manifest.

```bash
python3 script/zh_apply_localization.py
```

- [x] Step 5: Verify.

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
cargo fmt --check
git diff --check
cargo check -p warp
```

Acceptance:

- One targeted slice lands with metadata.
- No protocol/log/transcript bulk translation is added.

Execution note, 2026-05-31:

- `python3 script/zh_localization_inventory.py --preset modals --top-paths 20`: top paths still include broad mixed files such as `app/src/terminal/view.rs`; no broad translation was attempted.
- Selected exactly one slice: `terminal.view.notifications`.
- Rationale: notification discovery/error banners are user-visible inline terminal UI, not terminal protocol, command syntax, telemetry, logs, or Agent transcript text.
- Added 16 metadata-backed manifest entries:
  - `app/src/terminal/view.rs`: four `NotificationsTrigger::discovery_banner_copy` strings.
  - `app/src/terminal/view/inline_banner/notifications_discovery.rs`: discovery banner buttons and permission/result copy.
  - `app/src/terminal/view/inline_banner/notifications_error.rs`: notification error banner buttons.
- `python3 script/zh_apply_localization.py`: applied overlay to `app/src/terminal/view.rs`, `app/src/terminal/view/inline_banner/notifications_discovery.rs`, and `app/src/terminal/view/inline_banner/notifications_error.rs`.
- `cargo fmt`: applied mechanical formatting required by the new Chinese strings.
- Verification passed:
  - `python3 script/zh_apply_localization.py --validate-manifest`
  - `python3 script/zh_apply_localization.py --check-glossary`
  - `python3 script/zh_apply_localization.py --dry-run --summary`: `entries: 2661`; `files: 197`; `already_applied: 2646`; `would_change: 0`; `missing: 0`
  - `cargo fmt --check`
  - `git diff --check`
  - `cargo check -p warp`
- Metadata summary after the slice: `key/context/status/expected_count: 149 (5.6%)`.
- Release coverage after the slice: `2889/6409 = 31.1%`.

### P6-M6: Release Automation Guardrails

**Files:**

- Modify: `script/zh_apply_localization.py`
- Modify: `script/test_zh_apply_localization.py`
- Modify: `docs/zh-Hans-localization.md`

- [x] Step 1: Add JSON output for metadata summary only if it directly helps RC records or CI.

Proposed command:

```bash
python3 script/zh_apply_localization.py --metadata-summary --json
```

Expected shape:

```json
{
  "entries": 2645,
  "key": {"count": 133, "percent": 5.0},
  "context": {"count": 133, "percent": 5.0},
  "status": {"count": 133, "percent": 5.0},
  "expected_count": {"count": 133, "percent": 5.0}
}
```

- [x] Step 2: Add tests for the JSON output.
- [x] Step 3: Do not add a hard CI threshold unless the current project has CI wired for localization gates.

Acceptance:

```bash
python3 script/test_zh_apply_localization.py
python3 script/zh_apply_localization.py --metadata-summary --json
git diff --check
```

Execution note, 2026-05-31:

- Added `python3 script/zh_apply_localization.py --metadata-summary --json`.
- The JSON output is intentionally scoped to `--metadata-summary`; `python3 script/zh_apply_localization.py --json` exits with an argparse error instead of changing apply/dry-run behavior.
- Added `metadata_summary_report(...)` and tests for JSON percentages/output in `script/test_zh_apply_localization.py`.
- Did not add a hard CI threshold because this repository does not currently have a localization CI gate wired for metadata coverage thresholds.
- Verification passed:
  - `python3 script/test_zh_apply_localization.py`: 11 tests passed
  - `python3 script/zh_apply_localization.py --metadata-summary --json`
  - `python3 -m py_compile script/zh_apply_localization.py script/test_zh_apply_localization.py`
  - `git diff --check`

### P6-M7: RC3 Gate And Public-RC Decision

**Files:**

- Create: `docs/zh-Hans-release-candidate-2026-05-31-rc3.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`

- [x] Step 1: Run the full release gate.

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

- [x] Step 2: Decide one of:
  - `ready-for-local-use`
  - `ready-for-public-rc`
  - `blocked`

- [x] Step 3: Public RC can only be selected if:
  - upstream stable refs have been freshly fetched or the public release notes explicitly say the build is pinned to the last locally known stable;
  - `missing: 0`;
  - bundle gate passes;
  - GUI matrix has real evidence for base workspace, settings shell, command palette, vertical tab menu, and at least one destructive confirmation;
  - account/Billing/Cloud/Agent gates have concrete trigger conditions and blockers.

Acceptance:

- RC3 document records commands, outputs, warnings, GUI evidence, and the decision.
- README and maintenance docs point at RC3 if created.

Execution note, 2026-05-31:

- Created `docs/zh-Hans-release-candidate-2026-05-31-rc3.md`.
- Full command-line gate passed, including locale export, Python tests, `cargo check -p warp`, `cargo test -p warp_search_core`, `cargo test -p warp command_palette`, and bundle generation.
- Decision: `ready-for-local-use`.
- Public RC was not selected because P6-M2 remains `automation-blocked` and no destructive confirmation has real current-cycle GUI evidence.

## 6. Recommended Execution Order

1. P6-M0: Establish baseline.
2. P6-M1: Refresh upstream stable refs before adding work.
3. P6-M2: Recover GUI automation or document exact environment blocker.
4. P6-M3: Close at least one destructive confirmation with real evidence.
5. P6-M4: Turn state gates into fixture/test-account tasks.
6. P6-M5: Add one targeted user-visible slice only if it does not distract from release blockers.
7. P6-M6: Add release automation guardrails only if useful for RC3.
8. P6-M7: Build RC3 and make a release decision.

## 7. Self-Review Checklist

- [x] Does every public-RC blocker from RC2 map to a Phase 6 task?
- [x] Does every GUI verification task distinguish process evidence from real UI evidence?
- [x] Are destructive tests limited to disposable objects?
- [x] Are account/Billing/Cloud states separated by trigger type?
- [x] Does the plan avoid broad low-value translation work?
- [x] Are verification commands concrete and repeatable?

## 8. Execution Handoff

Plan complete and saved to `docs/zh-Hans-localization-phase6.md`.

Two execution options:

1. Subagent-Driven: dispatch a fresh subagent per task and review between tasks.
2. Inline Execution: execute tasks in this session using executing-plans, with checkpoint review after each milestone.
