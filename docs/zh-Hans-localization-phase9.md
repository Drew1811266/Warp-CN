# Warp CN Phase 9 Custom Inference Evidence Enablement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unblock future public-RC evidence collection for `GUI-WS-06` by preparing an isolated test-account runbook and a debug-only custom inference smoke fixture.

**Architecture:** Phase 9 has two evidence lanes. The real-account lane is the only lane that can satisfy public-RC criteria. The debug-only fixture lane exists to verify localized rendering and automation of the custom endpoint flow while no test account is available; it must be explicitly labeled non-public evidence in every record.

**Tech Stack:** Rust/Warp client source, `app/src/settings_view/ai_page.rs`, `resources/localization/zh-Hans-overrides.toml`, `script/zh_apply_localization.py`, `script/zh_localization_inventory.py`, `script/zh_export_locale.py`, macOS `WarpOss.app`, `WARP_DATA_PROFILE=zh-rc6`, optional `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`, Computer Use, macOS `screencapture`, cargo test/check gates.

---

## 1. Phase 9 Positioning

RC5 is `ready-for-local-use`, not public RC. The remaining public-RC blocker is not manifest drift, build failure, or base GUI automation. It is the absence of an isolated logged-in product state where Settings > AI shows `自定义推理`.

Phase 9 should make the next run less dependent on improvisation:

- Define exactly what an isolated test account must provide.
- Add a debug-only, env-gated custom inference smoke fixture if no account is available.
- Use the fixture only to verify localized UI rendering and automation mechanics.
- Preserve the rule that public RC still requires real logged-in GUI evidence from a disposable endpoint.

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

- `docs/zh-Hans-release-candidate-2026-05-31-rc5.md`
- Decision: `ready-for-local-use`
- Public RC decision: not ready
- Stable base: `v0.2026.05.27.09.22.stable_00`
- Remaining blocker: `GUI-WS-06` destructive confirmation lacks isolated logged-in GUI evidence
- Phase 8 evidence path: `no-test-account`

## 3. Evidence Rules

Evidence categories:

- `real-account-evidence`: isolated test account, real Settings > AI state, disposable endpoint, cancel-then-delete flow. This can satisfy public-RC criteria.
- `fixture-evidence`: debug-only env-gated state that renders custom inference UI without real account state. This can validate translation rendering and automation only.
- `source-anchor-evidence`: source review proving strings exist. This is useful context but never enough for public RC.

Phase 9 must not mark `GUI-WS-06` as `verified` from fixture evidence alone. Use `fixture-verified` in notes when the debug-only path succeeds.

## 4. Non-Goals

Phase 9 does not do:

- No runtime language switch or first-party i18n framework.
- No broad coverage push.
- No public-RC claim from debug-only fixture evidence.
- No main-account login.
- No real endpoint, production cloud environment, managed secret, billing, team, or ownership mutation.
- No release behavior that permanently exposes test-only custom inference controls.

## 5. Files And Responsibilities

Expected files to modify during Phase 9:

- `docs/zh-Hans-localization.md`: Phase 9 execution record and RC6 decision.
- `docs/zh-Hans-gui-smoke-matrix.md`: fixture evidence and real-account evidence separation.
- `docs/zh-Hans-release-candidate-2026-05-31-rc6.md`: final Phase 9 RC6 gate and decision.
- `docs/zh-Hans-custom-inference-test-account.md`: isolated account requirements and manual runbook.
- `docs/gui-smoke-artifacts/phase9/`: screenshots, process environment proof, logs, and GUI evidence files.
- `README.md`: Phase 9/RC6 status.
- `app/src/settings_view/ai_page.rs`, `crates/ai/src/api_keys.rs`, `app/src/lib.rs`, `crates/warp_core/src/paths.rs`: debug-only env-gated smoke fixture, in-memory endpoint seed, and prompt-free secure-storage boundary.
- `app/src/settings_view/custom_inference_modal.rs`: only if GUI smoke finds a localized copy leak in the custom inference modal.
- `resources/localization/zh-Hans-overrides.toml`: only if the fixture or real account run finds blocking English residue.

Files to read before execution:

- `docs/zh-Hans-release-candidate-2026-05-31-rc5.md`
- `docs/zh-Hans-gui-smoke-matrix.md`
- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/custom_inference_modal.rs`
- `app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs`
- `app/src/workspaces/user_workspaces.rs`
- `crates/ai/src/api_keys.rs`

## 6. Task Plan

### P9-M0: Entry Baseline And RC5 Blocker Snapshot

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`
- Create: `docs/gui-smoke-artifacts/phase9/`

- [ ] Step 1: Record branch and dirty worktree state.

```bash
git status --short
git rev-parse --abbrev-ref HEAD
```

Expected:

```text
drew/zh-Hans-localization
```

- [ ] Step 2: Run the Phase 9 entry gate.

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

- [ ] Step 3: Create Phase 9 artifact directory.

```bash
mkdir -p docs/gui-smoke-artifacts/phase9
```

- [ ] Step 4: Record the RC5 blocker in the Phase 9 execution record.

Required record:

```text
RC5 blocker: P8 evidence path was no-test-account. GUI-WS-06 still needs isolated logged-in custom inference evidence.
```

Acceptance:

- Phase 9 starts from a clean command-line baseline.
- The blocker is narrowed to account/product-state evidence, not translation or build health.

### P9-M1: Isolated Test Account Readiness Runbook

**Files:**

- Create: `docs/zh-Hans-custom-inference-test-account.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] Step 1: Create the account readiness document with this exact checklist.

```markdown
# zh-Hans Custom Inference Test Account Runbook

## Purpose

This runbook defines the minimum safe account state needed to verify `GUI-WS-06` for a public-RC decision.

## Account Requirements

- The account is not the user's main account.
- The account is safe to use in a local debug build of `WarpOss.app`.
- Settings > AI shows `自定义推理`.
- The account can create and remove a disposable custom endpoint.
- The account has no real custom endpoint named `zh-smoke-delete-endpoint`.
- The account is not used for team ownership transfer, billing mutation, cloud environment deletion, or managed secret deletion.

## Disposable Endpoint Values

```text
Name: zh-smoke-delete-endpoint
URL: https://example.invalid/zh-smoke
API key: zh-smoke-dummy-key
Model: zh-smoke-model
Alias: zh-smoke
```

## Evidence Requirements

- Process environment proof for `WARP_DATA_PROFILE=zh-rc6`.
- Screenshot showing Settings > AI > `自定义推理`.
- Screenshot showing `zh-smoke-delete-endpoint` after creation.
- Screenshot showing `移除端点？`.
- Screenshot after clicking `取消`, proving the endpoint remains.
- Screenshot after final removal, proving the endpoint is absent.

## Secret Handling

- Do not write passwords, tokens, cookies, magic links, or real API keys to docs.
- Redact account identifiers if screenshots reveal private information.
- Store screenshots only under `docs/gui-smoke-artifacts/phase9/`.
```

- [ ] Step 2: Link this runbook from `docs/zh-Hans-localization.md`.

Acceptance:

- A future executor can ask for the correct account state without handling credentials in docs.
- The runbook distinguishes safe endpoint mutation from unsafe account/billing/team mutations.

### P9-M2: Debug-Only Fixture Design Review

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] Step 1: Re-read the exact control gates.

```bash
sed -n '492,514p' app/src/workspaces/user_workspaces.rs
sed -n '1760,1775p' app/src/settings_view/ai_page.rs
sed -n '7440,7555p' app/src/settings_view/ai_page.rs
```

Expected findings:

```text
UserWorkspaces::is_custom_inference_enabled blocks anonymous/logged-out users.
AISettingsPageView::can_use_custom_inference_controls gates add/edit/remove actions.
AISettingsWidget::render_provider_keys_section controls whether 自定义推理 is rendered.
```

- [ ] Step 2: Record the fixture strategy.

Required record:

```text
Fixture strategy: add a debug_assertions-only env-gated override in ai_page.rs, controlled by WARP_CN_CUSTOM_INFERENCE_SMOKE=1. The override may render and enable custom inference controls for localization smoke only. Fixture evidence is non-public and cannot mark GUI-WS-06 verified.
```

Acceptance:

- The implementation target is one UI file, not a broad auth/workspace bypass.
- The docs explicitly state fixture evidence is not public-RC evidence.

### P9-M3: Implement Debug-Only Custom Inference Smoke Override

**Files:**

- Modify: `app/src/settings_view/ai_page.rs`
- May also modify `crates/ai/src/api_keys.rs`, `app/src/lib.rs`, and `crates/warp_core/src/paths.rs` if GUI smoke needs an in-memory endpoint fixture and prompt-free secure-storage path.

- [ ] Step 1: Add a helper inside `impl AISettingsPageView`.

Insert this helper near `can_use_custom_inference_controls`:

```rust
    fn custom_inference_smoke_override_enabled() -> bool {
        let smoke_override = std::env::var("WARP_CN_CUSTOM_INFERENCE_SMOKE").ok();
        Self::custom_inference_smoke_override_value_is_enabled(smoke_override.as_deref())
    }

    fn custom_inference_smoke_override_value_is_enabled(value: Option<&str>) -> bool {
        cfg!(debug_assertions) && value == Some("1")
    }
```

- [ ] Step 2: Update `can_use_custom_inference_controls`.

Expected implementation:

```rust
    fn can_use_custom_inference_controls(app: &AppContext) -> bool {
        let smoke_override_enabled = Self::custom_inference_smoke_override_enabled();

        (FeatureFlag::CustomInferenceEndpoints.is_enabled() || smoke_override_enabled)
            && (AISettings::as_ref(app).is_any_ai_enabled(app) || smoke_override_enabled)
            && (UserWorkspaces::as_ref(app).is_custom_inference_enabled(app)
                || smoke_override_enabled)
    }
```

- [ ] Step 3: Update `AISettingsWidget::render_provider_keys_section`.

Within the function, add:

```rust
        let custom_inference_smoke_override_enabled =
            AISettingsPageView::custom_inference_smoke_override_enabled();
```

Then change these calculations:

```rust
        let custom_inference_controls_enabled =
            is_any_ai_enabled && is_custom_inference_enabled;
        let custom_inference_flag_on = FeatureFlag::CustomInferenceEndpoints.is_enabled();
        let show_custom_inference = custom_inference_flag_on && is_custom_inference_enabled;
```

to:

```rust
        let custom_inference_controls_enabled =
            (is_any_ai_enabled && is_custom_inference_enabled)
                || custom_inference_smoke_override_enabled;
        let custom_inference_flag_on = FeatureFlag::CustomInferenceEndpoints.is_enabled()
            || custom_inference_smoke_override_enabled;
        let show_custom_inference = custom_inference_flag_on
            && (is_custom_inference_enabled || custom_inference_smoke_override_enabled);
```

- [ ] Step 4: Add unit tests for the pure helper.

Add this test module near the bottom of `app/src/settings_view/ai_page.rs`:

```rust
#[cfg(test)]
mod custom_inference_smoke_override_tests {
    use super::AISettingsPageView;

    #[test]
    fn smoke_override_enabled_only_for_exact_one() {
        assert!(AISettingsPageView::custom_inference_smoke_override_value_is_enabled(Some("1")));
        assert!(!AISettingsPageView::custom_inference_smoke_override_value_is_enabled(Some("true")));
        assert!(!AISettingsPageView::custom_inference_smoke_override_value_is_enabled(Some("0")));
        assert!(!AISettingsPageView::custom_inference_smoke_override_value_is_enabled(None));
    }
}
```

- [ ] Step 5: Verify the code compiles and the focused test passes.

```bash
cargo fmt --check
cargo test -p warp custom_inference_smoke_override
cargo check -p warp
git diff --check
```

Expected:

```text
1 passed
Finished dev profile
```

Acceptance:

- The override is debug-only through `cfg!(debug_assertions)`.
- The override requires `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`.
- The override affects only custom inference smoke behavior and prompt avoidance in a debug env-gated session.
- Any seeded endpoint must be in-memory only and must not write real Keychain/App Group state.
- No public-RC docs treat this as real account evidence.

### P9-M4: Fixture GUI Smoke For Custom Endpoint Flow

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase9/`

- [ ] Step 1: Build the app bundle.

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
Successfully bundled
target/debug/bundle/osx/WarpOss.app
```

- [ ] Step 2: Launch with fixture env and fresh profile.

```bash
launchctl setenv WARP_DATA_PROFILE zh-rc6
launchctl setenv WARP_CN_CUSTOM_INFERENCE_SMOKE 1
open -n target/debug/bundle/osx/WarpOss.app
launchctl unsetenv WARP_CN_CUSTOM_INFERENCE_SMOKE
launchctl unsetenv WARP_DATA_PROFILE
launchctl getenv WARP_CN_CUSTOM_INFERENCE_SMOKE
launchctl getenv WARP_DATA_PROFILE
```

Expected:

```text
The final getenv outputs are empty.
```

- [ ] Step 3: Prove the GUI process received the fixture env.

```bash
WARP_OSS_PID="$(pgrep -n -f 'target/debug/bundle/osx/WarpOss.app/Contents/MacOS/warp-oss')"
ps eww -p "$WARP_OSS_PID" | tr ' ' '\n' | rg 'WARP_DATA_PROFILE|WARP_CN_CUSTOM_INFERENCE_SMOKE|__CFBundleIdentifier'
```

Expected:

```text
WARP_DATA_PROFILE=zh-rc6
WARP_CN_CUSTOM_INFERENCE_SMOKE=1
__CFBundleIdentifier=dev.warp.WarpOss
```

- [ ] Step 4: Verify Settings > AI shows `自定义推理`.

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase9/p9-m4-custom-inference-fixture-visible.png
```

Expected anchors:

```text
自定义推理
添加自定义端点
```

- [ ] Step 5: Verify the disposable fixture endpoint is seeded.

Use:

```text
Name: zh-smoke-delete-endpoint
URL: https://example.com
API key: sk-zh-smoke-dummy-key
Model: zh-smoke-model
Alias: zh-smoke
```

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase9/p9-m4-fixture-endpoint-seeded.png
```

- [ ] Step 6: Open the remove confirmation and capture it.

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase9/p9-m4-fixture-remove-confirmation.png
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

- [ ] Step 7: Click `取消`, then verify the endpoint remains.

Screenshot:

```bash
screencapture -x docs/gui-smoke-artifacts/phase9/p9-m4-fixture-after-cancel.png
```

- [ ] Step 8: Reopen the confirmation and remove the disposable endpoint.

Screenshot after removal:

```bash
screencapture -x docs/gui-smoke-artifacts/phase9/p9-m4-fixture-after-remove.png
```

Expected:

```text
zh-smoke-delete-endpoint is absent.
```

Acceptance:

- The matrix records this as `fixture-verified`, not `verified`.
- The fixture endpoint is removed from the current in-memory process or explicitly documented for cleanup.
- This stage does not alter the public-RC decision by itself.

### P9-M5: Real Account Public-RC Path

**Files:**

- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Add: screenshots under `docs/gui-smoke-artifacts/phase9/`

- [ ] Step 1: Check whether the isolated test account from `docs/zh-Hans-custom-inference-test-account.md` is available.

Record one value:

```text
P9 real-account path: available
P9 real-account path: not-available
```

- [ ] Step 2: If available, launch without `WARP_CN_CUSTOM_INFERENCE_SMOKE`.

```bash
launchctl setenv WARP_DATA_PROFILE zh-rc6-real
open -n target/debug/bundle/osx/WarpOss.app
launchctl unsetenv WARP_DATA_PROFILE
launchctl getenv WARP_DATA_PROFILE
```

Expected:

```text
The final getenv output is empty.
```

- [ ] Step 3: Complete login without storing secrets in docs.

Evidence rule:

```text
No passwords, tokens, cookies, or magic links are written to repository files.
```

- [ ] Step 4: Repeat the endpoint creation, cancel, and removal sequence from P9-M4 using the real account.

Required screenshots:

```text
docs/gui-smoke-artifacts/phase9/p9-m5-real-custom-inference-visible.png
docs/gui-smoke-artifacts/phase9/p9-m5-real-endpoint-created.png
docs/gui-smoke-artifacts/phase9/p9-m5-real-remove-confirmation.png
docs/gui-smoke-artifacts/phase9/p9-m5-real-after-cancel.png
docs/gui-smoke-artifacts/phase9/p9-m5-real-after-remove.png
```

Acceptance:

- `GUI-WS-06` may be marked `verified` only if this real-account path passes.
- The real path must not use `WARP_CN_CUSTOM_INFERENCE_SMOKE`.
- The real path deletes only `zh-smoke-delete-endpoint`.

### P9-M6: RC6 Gate And Release Decision

**Files:**

- Add: `docs/zh-Hans-release-candidate-2026-05-31-rc6.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `README.md`

- [ ] Step 1: Run the full RC6 command-line gate.

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
cargo test -p warp custom_inference_smoke_override
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

- [ ] Step 2: Choose one release decision.

Decision rules:

```text
ready-for-public-rc: command-line/bundle gates pass and P9-M5 real-account path passes.
ready-for-local-use: command-line/bundle gates pass, fixture path may pass, but P9-M5 real-account path is unavailable or incomplete.
blocked: dry-run drift, tests, bundle generation, app launch, or fixture implementation is broken.
```

Acceptance:

- RC6 explains fixture evidence separately from real-account evidence.
- README and `docs/zh-Hans-localization.md` match the RC6 decision.
- Public-RC language is used only if the real-account path passes.

### P9-M7: Cleanup And Fixture Safety Audit

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] Step 1: Verify no GUI process is left running unless intentionally kept open.

```bash
pgrep -afil 'target/debug/bundle/osx/WarpOss.app|warp-oss|terminal-server'
```

- [ ] Step 2: Verify LaunchServices env cleanup.

```bash
launchctl getenv WARP_CN_CUSTOM_INFERENCE_SMOKE
launchctl getenv WARP_DATA_PROFILE
```

Expected:

```text
No value is printed.
```

- [ ] Step 3: Record endpoint cleanup state.

Record one value:

```text
zh-smoke-delete-endpoint cleanup: deleted
zh-smoke-delete-endpoint cleanup: not created
zh-smoke-delete-endpoint cleanup: left in isolated fixture profile for manual cleanup
```

- [ ] Step 4: Confirm fixture gate remains debug-only.

```bash
rg -n "WARP_CN_CUSTOM_INFERENCE_SMOKE|custom_inference_smoke_override|custom_inference_smoke_fixture" app/src crates
```

Expected:

```text
The override is env-gated and uses cfg!(debug_assertions).
```

Acceptance:

- No LaunchServices env leak remains.
- No ambiguous endpoint test object remains.
- The fixture is documented as debug-only and non-public evidence.

## 7. Self-Review

Spec coverage:

- Test-account readiness is covered by P9-M1.
- Debug-only fixture design and implementation are covered by P9-M2 through P9-M4.
- Real-account public-RC path is covered by P9-M5.
- RC6 release decision is covered by P9-M6.
- Cleanup and fixture safety are covered by P9-M7.

Placeholder scan:

- No task uses placeholder markers or open-ended implementation language.
- Conditional paths have explicit release-decision consequences.

Risk review:

- The plan does not use the main account.
- The fixture cannot be counted as public-RC evidence.
- The fixture is debug-only and env-gated.
