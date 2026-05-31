# zh-Hans localization branch

This branch is a local Chinese localization branch for Warp's open-source client.

## Current approach

Warp does not currently expose a first-party application language setting or a complete UI localization framework. Most product strings are still inline Rust string literals.

For a maintainable local fork, this branch keeps translations in:

- `resources/localization/zh-Hans-overrides.toml`
- `script/zh_apply_localization.py`
- `script/zh_export_locale.py`

The script applies exact replacements inside Rust string literals, including raw strings used for static pane content. It is idempotent: already translated strings are accepted, while missing source/target pairs report upstream drift.

## Status

Last verified release audit: 2026-05-31.

- Manifest entries: 2661.
- Covered areas: onboarding/auth, workspace shell, Warp on Web home, HOA onboarding, search and command entry points, settings core pages, AI settings deep paths, BYO API keys, AWS Bedrock credentials and user-facing credential errors, Appearance command-palette actions, conversation list actions, cloud agent capacity messaging, environment deletion confirmation, launch modals, credit and plan modals, Agent tips, Agent status/error residue, conversation details panel, CLI admin prompts, destructive confirmation dialogs, advanced settings pages, common modals/toasts, Warp Drive surfaces, tab configs, themes, terminal sharing surfaces, terminal notification banners, rewind labels, auth-secret confirmation dialogs, environment modal fallbacks, Agent management/input panels, custom inference endpoint settings, team invite basics, and vertical tab context menus.
- Dry-run summary: `entries: 2661`, `files: 197`, `already_applied: 2646`, `would_change: 0`, `missing: 0`.
- Metadata summary: `key/context/status/expected_count: 149 (5.6%)`.
- Phase 3 status: manifest v2 metadata validation, external inventory ignore rules, glossary checks, GUI smoke matrix, upstream stable sync, and JSON/YAML locale export prototype are in place. Current v1 entries remain valid, and new entries may add `key`, `context`, `status`, `preserve_terms`, `notes`, and `expected_count` metadata for future locale migration.
- Coverage snapshot:
  - `onboarding`: 266 covered, 55 candidates, 82.9%.
  - `workspace`: 598 covered, 377 candidates, 61.3%.
  - `search`: 267 covered, 26 candidates, 91.1%.
  - `settings`: 1201 covered, 827 candidates, 59.2%.
  - `modals`: 679 covered, 5145 candidates, 11.7%.
  - `release`: 2889 covered, 6409 candidates, 31.1%.
- Package note: the app crate package is currently named `warp`; the older checklist label `cargo check -p app` fails in this workspace because no package named `app` exists.
- Phase 2 command-line validation passed:
  - `python3 script/zh_apply_localization.py --dry-run --summary`
  - `python3 script/zh_localization_inventory.py --preset onboarding --coverage`
  - `python3 script/zh_localization_inventory.py --preset workspace --coverage`
  - `python3 script/zh_localization_inventory.py --preset search --coverage`
  - `python3 script/zh_localization_inventory.py --preset settings --coverage`
  - `python3 script/zh_localization_inventory.py --preset modals --coverage`
  - `python3 script/zh_localization_inventory.py --preset release --coverage`
  - `cargo fmt --check`
  - `git diff --check`
  - `python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py`
  - `cargo check -p warp`
  - `cargo test -p warp_search_core`
  - `cargo test -p warp command_palette`
  - `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- Recorded failures / manual gates:
  - `cargo check -p app` fails with `error: package ID specification 'app' did not match any packages`; use `cargo check -p warp` for the current app package.
  - Historical GUI smoke with `target/debug/bundle/osx/WarpOss.app` verified the terminal-only workspace and command palette filter chips (`文件`, `操作`, `会话`, `启动配置`).
  - Phase 2 GUI smoke was attempted on 2026-05-29. The `WarpOss` process launched, but Computer Use and AppleScript window reads timed out, `open` returned `-1712`, and the captured screenshot was black. Treat HOA onboarding, AI settings deep paths, rewind, and auth-secret confirmation as manual GUI gates until they are verified in an interactive desktop session.
  - Phase 2 Round 2 GUI smoke was attempted on 2026-05-30. `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` built, bundled, prepared resources, and signed `WarpOss.app`; `open -na target/debug/bundle/osx/WarpOss.app` launched `warp-oss` and `terminal-server` processes, but Computer Use window state reads timed out. Treat Appearance command actions, conversation actions, cloud agent capacity modal, AWS credential errors, and environment deletion confirmation as manual GUI gates until verified in an interactive desktop session.
  - Phase 2 Round 3 GUI smoke was attempted on 2026-05-30. `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` built, bundled, prepared resources, and signed `WarpOss.app`; `open -n target/debug/bundle/osx/WarpOss.app` launched `warp-oss` and `terminal-server` processes, but Computer Use window state reads timed out. Treat launch modals, credit and plan modals, Agent tips, conversation details panel, CLI admin prompts, remove endpoint confirmation, and transfer ownership confirmation as manual GUI gates until verified in an interactive desktop session.
  - Phase 2 Round 4 GUI smoke was attempted on 2026-05-30. `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` built, bundled, prepared resources, and signed `WarpOss.app`; `open -n target/debug/bundle/osx/WarpOss.app` launched `warp-oss` and `terminal-server` processes. Computer Use successfully read the window state and confirmed Chinese menu labels, the global search placeholder, and the `新会话` entry. Treat Warp on Web home, Agent status labels, Agent error residue, and environment modal fallback paths as manual GUI gates until those specific states are triggered in an interactive desktop session.
  - Interactive login/account smoke remains a manual release gate; the non-interactive bundle gate produced `target/debug/bundle/osx/WarpOss.app`.

## Phase 3 plan

Phase 3 shifts the project from broad translation coverage to localization asset maintenance. The goal is to keep the current source-level overlay working while making the manifest, terminology, ignore rules, GUI verification records, and upstream sync process easier to audit and eventually migrate to an official `zh-CN` locale if Warp adds first-party i18n.

The Phase 3 planning document is `docs/zh-Hans-localization-phase3.md`. Start with these checks before changing manifest entries:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
```

Inventory ignore rules now live in `resources/localization/zh-Hans-inventory-ignore.toml`. The default inventory workflow reads that file automatically; pass `--ignore-config <path>` only when testing an alternate review policy.

Glossary rules live in `resources/localization/zh-Hans-glossary.toml`. The first rule set is intentionally conservative: it checks stable product/technical terms, a few high-frequency translations, and forbidden target terms without forcing all historical entries to be normalized at once.

GUI verification is tracked in `docs/zh-Hans-gui-smoke-matrix.md`. Use that matrix for release smoke status instead of relying on process startup, bundle success, or scattered manual-gate notes.

Upstream stable sync is documented in `docs/zh-Hans-upstream-sync.md`. Use that checklist when selecting a new upstream base, resolving manifest drift, and recording release gate results.

The current Phase 8 RC5 record is `docs/zh-Hans-release-candidate-2026-05-31-rc5.md`. The Phase 7 RC4 record remains in `docs/zh-Hans-release-candidate-2026-05-31-rc4.md`, the Phase 6 RC3 record remains in `docs/zh-Hans-release-candidate-2026-05-31-rc3.md`, the Phase 5 RC2 record remains in `docs/zh-Hans-release-candidate-2026-05-30-rc2.md`, and the earlier Phase 4 release-candidate record remains in `docs/zh-Hans-release-candidate-2026-05-30.md`.

The locale export prototype does not replace the source-level overlay. It serializes the manifest into migration-friendly JSON/YAML so the translation asset can be converted later if Warp adopts a first-party locale format.

## Phase 7 plan

Phase 7 shifts from RC3 local-use readiness to GUI evidence recovery. The next work should not chase broad coverage; it should audit debug profile isolation, recover the current `WarpOss` GUI launch path, rerun base GUI smoke in the same RC cycle, verify one low-risk destructive confirmation with a disposable custom endpoint, and then produce an RC4 decision.

The Phase 7 planning document is `docs/zh-Hans-localization-phase7.md`. Start with these checks before beginning a Phase 7 slice:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

Phase 7 recovered current-cycle base GUI evidence and produced RC4. RC4 remains `ready-for-local-use`, but not public-RC ready until `GUI-WS-06` destructive confirmation evidence is recovered with an isolated test account or fixture.

## Phase 7 execution record

Execution started on 2026-05-31.

| Task | Result | Notes |
| --- | --- | --- |
| P7-M0 | Complete | Entry baseline passed on branch `drew/zh-Hans-localization`. Worktree is dirty from previous localization phases and no existing changes were reverted. Manifest validation and glossary checks passed; metadata remains `entries: 2661`, `key/context/status/expected_count: 149 (5.6%)`; dry-run reports `files: 197`, `already_applied: 2646`, `would_change: 0`, `missing: 0`; release coverage remains `2889/6409 = 31.1%`; `git diff --check` passed. Created `docs/gui-smoke-artifacts/phase7/`. RC3 GUI/destructive blockers remain active and no GUI row was promoted from historical evidence. |
| P7-M1 | Complete | Profile/path isolation audit passed. `cargo test -p warp_core path` passed 10 tests, and `WARP_DATA_PROFILE=zh-rc4 cargo test -p warp_core test_warp_home_config_dir_path` passed. The GUI matrix now records exact isolation behavior: `warp_home_config_dir()` is profile-isolated as `~/.warp-oss-zh-rc4`; macOS `data_dir()` and `config_local_dir()` still share `~/.warp-oss`; `cache_dir()` and `state_dir()` use profiled ProjectDirs; `secure_state_dir()` is runtime-dependent. Custom endpoint state is secure-storage key `AiApiKeys` under `ChannelState::data_domain()`, so `zh-smoke-delete-endpoint` may only be created if P7-M2 proves the GUI process received `WARP_DATA_PROFILE=zh-rc4`. |
| P7-M2 | Complete | Bundle rebuild passed and the app launched with `WARP_DATA_PROFILE=zh-rc4`. `pgrep` found `warp-oss` pid `80871` and `terminal-server` pid `80874`; `ps eww -p 80871` confirmed `WARP_DATA_PROFILE=zh-rc4` in the GUI process. The macOS “access other App data” permission prompt was denied per smoke policy; evidence is saved at `docs/gui-smoke-artifacts/phase7/p7-m2-launch.png` and `docs/gui-smoke-artifacts/phase7/p7-m2-after-permission-deny.png`. `/usr/bin/log show` output is saved at `docs/gui-smoke-artifacts/phase7/p7-m2-warp-oss.log.txt`. Computer Use succeeded after the prompt was denied and read the `WarpOss` menu. Launch classification is `interactive-profile-ready`. |
| P7-M3 | Complete | Recovery path selected: continue with the `zh-rc4` GUI profile from P7-M2. No shared `.warp-oss` backup was needed for the endpoint path because custom endpoints are stored in profiled secure storage and P7-M2 proved the GUI process received the profile env. Shared `data_dir()`/`config_local_dir()` remain a caveat for settings/user-preference mutations, so Phase 7 will not treat those as fully isolated. |
| P7-M4 | Complete | Current-cycle base GUI smoke passed with screenshots. Evidence: workspace `docs/gui-smoke-artifacts/phase7/p7-m4-workspace.png`, command palette `docs/gui-smoke-artifacts/phase7/p7-m4-command-palette.png`, settings shell `docs/gui-smoke-artifacts/phase7/p7-m4-settings-shell.png`, tab context menu `docs/gui-smoke-artifacts/phase7/p7-m4-tab-context-menu.png`, plus menu `docs/gui-smoke-artifacts/phase7/p7-m4-new-session-menu.png`, and File menu `docs/gui-smoke-artifacts/phase7/p7-m4-file-menu.png`. Menu, command palette, settings shell, and tab context menu anchors are Chinese. Current horizontal-tab build uses `新建终端标签页`/`终端` for the new-session entry instead of historical `新会话`; no English residue was observed. |
| P7-M5 | Blocked | `GUI-WS-06` could not be verified. P7-M1/P7-M3 made a profiled endpoint safe in principle, but the current `zh-rc4` profile is logged out after terminal-only onboarding. `UserWorkspaces::is_custom_inference_enabled()` returns false for anonymous/logged-out users, so `自定义推理` and the add endpoint UI are not shown. Evidence: `docs/gui-smoke-artifacts/phase7/p7-m5-custom-inference-blocked-logged-out.png`. No `zh-smoke-delete-endpoint` was created and no endpoint was deleted. |
| P7-M6 | Deferred | No additional state gate was probed because P7-M5 did not pass. `GUI-AUTH-02`, `GUI-AGENT-03`, and `GUI-SET-03` remain deferred with explicit owners: local fixture or test account depending on trigger path. This does not change RC4 eligibility: without destructive confirmation evidence, RC4 cannot be public-RC ready. |
| P7-M7 | Complete | Full RC4 gate passed: manifest validation, glossary, metadata summary, metadata JSON, dry-run, release coverage, JSON/YAML locale export, JSON parse, `cargo fmt --check`, `git diff --check`, Python compile checks, localization Python tests, `cargo check -p warp`, `cargo test -p warp_search_core`, `cargo test -p warp command_palette`, and bundle generation. Created `docs/zh-Hans-release-candidate-2026-05-31-rc4.md`. Decision is `ready-for-local-use`, not public RC, because P7-M5 destructive confirmation evidence is still missing. |

## Phase 7 release decision

Decision: `ready-for-local-use`.

RC4 can be used for local engineering validation and continued GUI/manual-gate testing because the manifest gate, glossary gate, locale exports, Python tests, Rust checks/tests, bundle gate, and current-cycle base GUI smoke passed.

RC4 should not be published as a public release candidate yet. The remaining public-RC blocker is narrower than RC3: GUI launch and base smoke are recovered, but no destructive confirmation has real GUI evidence from an isolated disposable object. `GUI-WS-06` is blocked by logged-out product state because custom inference is hidden for anonymous/logged-out users.

Next public-RC gate: use an isolated test account or fixture where custom inference is enabled, create `zh-smoke-delete-endpoint`, verify the remove confirmation, cancel once, then remove only that disposable endpoint.

## Phase 8 plan

Phase 8 is a narrow public-RC evidence phase. The next work should not chase broad coverage; it should use a `zh-rc5` debug profile and an isolated test account, verify Settings > AI > `自定义推理`, create one disposable `zh-smoke-delete-endpoint`, prove the cancel path, delete only that endpoint, and then produce an RC5 decision.

The Phase 8 planning document is `docs/zh-Hans-localization-phase8.md`. A Superpowers handoff pointer is also saved at `docs/superpowers/plans/2026-05-31-zh-Hans-phase8-public-rc-readiness.md`.

Start with these checks before beginning a Phase 8 slice:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

Recommended first execution slice: P8-M0 through P8-M2. Do not proceed to endpoint creation unless the evidence path is `isolated-test-account`. If no isolated account or fixture can expose custom inference, RC5 remains `ready-for-local-use` at most.

## Phase 8 execution record

Execution started on 2026-05-31.

| Task | Result | Notes |
| --- | --- | --- |
| P8-M0 | Complete | Entry baseline passed on branch `drew/zh-Hans-localization`. Worktree is dirty from previous localization phases and no existing changes were reverted. Created `docs/gui-smoke-artifacts/phase8/`. Manifest validation and glossary checks passed; metadata remains `entries: 2661`, `key/context/status/expected_count: 149 (5.6%)`; dry-run reports `files: 197`, `already_applied: 2646`, `would_change: 0`, `missing: 0`; release coverage remains `2889/6409 = 31.1%`; `git diff --check` passed. RC4 blocker is carried forward: current-cycle base GUI evidence is recovered, but `GUI-WS-06` is still unverified because logged-out state hides `自定义推理`. |
| P8-M1 | Complete | `git fetch origin --tags` passed. Latest stable remains `v0.2026.05.27.09.22.stable_00` at `2566f54af7c3e71facfe1865f2c492549b14248a`; no newer stable tag appeared. `origin/master` advanced to `5767910b5e41bda196baaea041862e9505e46e20`, but RC5 stable base is unchanged. Branch distance from the selected stable remains `0 88`. Post-fetch dry-run remains `would_change: 0`, `missing: 0`. |
| P8-M2 | Complete | Evidence path selected: `no-test-account`. No isolated test account or fixture credentials were provided in the current execution context. The executor did not guess credentials and did not use the user's main account. Public-RC GUI path stops here for this run; P8-M3 through P8-M6 are deferred. Next useful fallback is a debug-only custom inference fixture that can verify dialog rendering without being counted as public-RC evidence. |
| P8-M3 | Deferred | Deferred because P8-M2 selected `no-test-account`. No logged-in `zh-rc5` profile was launched, no browser auth callback or token paste flow was attempted, and no account state was mutated. |
| P8-M4 | Deferred | Deferred because no logged-in `zh-rc5` profile is available. Phase 7 `zh-rc4` base GUI evidence remains useful for local-use context, but it is not promoted as RC5 public-RC evidence. |
| P8-M5 | Deferred | Deferred because custom inference visibility requires isolated logged-in account state. No `zh-smoke-delete-endpoint` was created and no real endpoint data was entered. |
| P8-M6 | Deferred | Deferred because no disposable endpoint exists. No remove endpoint confirmation was opened, no cancel/delete path was exercised, and no endpoint was removed. Cleanup state: `zh-smoke-delete-endpoint` was not created. |
| P8-M7 | Complete | Full RC5 gate passed: manifest validation, glossary, metadata summary, metadata JSON, dry-run, release coverage, JSON/YAML locale export, JSON parse, `cargo fmt --check`, `git diff --check`, Python compile checks, localization Python tests, `cargo check -p warp`, `cargo test -p warp_search_core`, `cargo test -p warp command_palette`, and bundle generation. Created `docs/zh-Hans-release-candidate-2026-05-31-rc5.md`. Decision is `ready-for-local-use`, not public RC, because P8-M2 selected `no-test-account` and no destructive confirmation evidence exists. |
| P8-M8 | Complete | Cleanup passed. No Phase 8 `warp-oss`/`terminal-server` GUI process remained, `launchctl getenv WARP_DATA_PROFILE` returned no value, and `zh-smoke-delete-endpoint` was never created. Phase 8 leaves no ambiguous destructive-test state. |

## Phase 8 release decision

Decision: `ready-for-local-use`.

RC5 can be used for local engineering validation and continued GUI/manual-gate testing because upstream refs were freshly checked, the manifest gate, glossary gate, locale exports, Python tests, Rust checks/tests, and bundle gate passed.

RC5 should not be published as a public release candidate yet. The remaining public-RC blocker is unchanged from the narrow Phase 8 evidence path: `GUI-WS-06` still lacks real logged-in GUI evidence from an isolated disposable endpoint. The current execution context did not provide an isolated test account, so P8-M3 through P8-M6 were safely deferred.

Next public-RC gate: provide an isolated test account where Settings > AI shows `自定义推理`, create `zh-smoke-delete-endpoint`, verify the remove confirmation, cancel once, then remove only that disposable endpoint.

## Phase 9 plan

Phase 9 turns the remaining RC5 blocker into two explicit evidence lanes. The real-account lane is the only lane that can make RC6 public-RC ready. The debug-only fixture lane can verify localized rendering and automation of the custom endpoint flow while no isolated test account is available, but it must be labeled non-public evidence.

The Phase 9 planning document is `docs/zh-Hans-localization-phase9.md`. A Superpowers handoff pointer is also saved at `docs/superpowers/plans/2026-05-31-zh-Hans-phase9-custom-inference-evidence.md`.

The isolated custom inference account runbook is `docs/zh-Hans-custom-inference-test-account.md`. It defines the required account state and disposable endpoint values without storing credentials, tokens, cookies, or magic links.

Start with these checks before beginning a Phase 9 slice:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

Recommended first execution slice: P9-M0 through P9-M2. Do not implement the debug-only fixture until the evidence boundary is accepted: fixture success may update `GUI-WS-06` notes as `fixture-verified`, but it cannot mark the row `verified` or justify `ready-for-public-rc`.

Planned Phase 9 outputs:

| Task | Target | Public-RC impact |
| --- | --- | --- |
| P9-M0 | Re-establish Phase 9 entry baseline and restate the RC5 blocker | Confirms no translation/build drift before new work |
| P9-M1 | Create `docs/zh-Hans-custom-inference-test-account.md` | Defines the real account state needed for public-RC evidence |
| P9-M2 | Review custom inference gates and document fixture boundaries | Prevents fixture evidence from being promoted incorrectly |
| P9-M3 | Add `WARP_CN_CUSTOM_INFERENCE_SMOKE=1` debug-only UI gate | Enables non-public fixture smoke only |
| P9-M4 | Run fixture GUI smoke for endpoint create/cancel/remove | May produce `fixture-verified` notes only |
| P9-M5 | Run real-account GUI smoke without the fixture env | Required before `ready-for-public-rc` |
| P9-M6 | Produce RC6 gate and decision | Chooses `ready-for-public-rc`, `ready-for-local-use`, or `blocked` |
| P9-M7 | Audit process/env cleanup and endpoint state | Ensures no fixture leak or ambiguous test object remains |

## Phase 9 execution record

Execution started on 2026-05-31.

| Task | Result | Notes |
| --- | --- | --- |
| P9-M0 | Complete | Entry baseline passed on branch `drew/zh-Hans-localization`. Worktree is dirty from previous localization phases and no existing changes were reverted. Created `docs/gui-smoke-artifacts/phase9/`. Manifest validation and glossary checks passed; metadata remains `entries: 2661`, `key/context/status/expected_count: 149 (5.6%)`; dry-run reports `files: 197`, `already_applied: 2646`, `would_change: 0`, `missing: 0`; release coverage remains `2889/6409 = 31.1%`; `git diff --check` passed. RC5 blocker is carried forward exactly: P8 evidence path was `no-test-account`, and `GUI-WS-06` still needs isolated logged-in custom inference evidence. |
| P9-M1 | Complete | Created `docs/zh-Hans-custom-inference-test-account.md`. The runbook requires a non-main account where Settings > AI shows `自定义推理`, allows creating/removing one disposable `zh-smoke-delete-endpoint`, and forbids team ownership, billing, cloud environment, or managed secret mutations. It records dummy endpoint values and evidence requirements while explicitly prohibiting passwords, tokens, cookies, magic links, and real API keys in repository docs. |
| P9-M2 | Complete | Re-read the custom inference gates. `UserWorkspaces::is_custom_inference_enabled()` blocks anonymous/logged-out users; `AISettingsPageView::can_use_custom_inference_controls()` gates add/edit/remove actions behind feature flag, AI availability, and workspace eligibility; `AISettingsWidget::render_provider_keys_section()` controls whether `自定义推理` is rendered. Updated `docs/zh-Hans-gui-smoke-matrix.md` with the Phase 9 fixture boundary: `WARP_CN_CUSTOM_INFERENCE_SMOKE=1` may be used only as a `debug_assertions` localization smoke override, and fixture evidence cannot mark `GUI-WS-06` verified or justify public-RC readiness. |
| P9-M3 | Complete | Implemented the debug-only custom inference smoke path. `app/src/settings_view/ai_page.rs` exposes custom inference rendering/control gates only when `WARP_CN_CUSTOM_INFERENCE_SMOKE=1` in debug builds; `crates/ai/src/api_keys.rs` seeds one in-memory `zh-smoke-delete-endpoint` fixture and skips secure-storage writes in smoke mode; `app/src/lib.rs` registers no-op secure storage for the smoke session; `crates/warp_core/src/paths.rs` skips the App Group secure-state directory under the same debug env to avoid macOS privacy prompts. Verification passed: `cargo fmt`, `cargo test -p ai custom_inference_smoke`, `cargo test -p warp custom_inference_smoke_override`, `cargo check -p warp`, `git diff --check`, and `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`. Existing unused-variable warnings remain in `scp_fallback.rs` and `terminal/input/slash_commands/mod.rs`. |
| P9-M4 | Complete | Fixture GUI smoke passed and is recorded as `fixture-verified`, not public-RC `verified`. Launched `WarpOss.app` with `WARP_DATA_PROFILE=zh-rc6` and `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`; Settings > AI showed the seeded `zh-smoke-delete-endpoint`; the edit modal showed `编辑自定义端点`, `https://example.com`, `zh-smoke-model`, alias `zh-smoke`, and after a manifest/source fix the delete button now reads `移除` instead of `Remove`. Verified remove confirmation anchors `移除端点？`, `确定要移除此端点吗？`, `取消`, `移除端点`; clicked `取消` and captured the endpoint still present; reopened and removed it, capturing `端点已移除` and absence from the list. Evidence: `docs/gui-smoke-artifacts/phase9/p9-m4-fixture-endpoint-seeded.png`, `p9-m4-fixture-edit-modal.png`, `p9-m4-fixture-remove-confirmation.png`, `p9-m4-fixture-after-cancel.png`, `p9-m4-fixture-after-remove.png`. The fixture endpoint is in-memory only and cannot satisfy the real-account public-RC gate. |
| P9-M5 | Complete | Real-account public-RC path remains unavailable in this execution context. No isolated test account, credentials, magic link, or callback path was provided, and the executor did not use the user's main account. A no-fixture `zh-rc6` launch proved the process had `WARP_DATA_PROFILE=zh-rc6` and no `WARP_CN_CUSTOM_INFERENCE_SMOKE`; without the debug no-op storage, macOS requested Keychain access for `dev.warp.WarpOss-zh-rc6` and App data access, both of which were denied. Evidence: `docs/gui-smoke-artifacts/phase9/p9-m5-no-fixture-desktop.png`, `p9-m5-no-fixture-keychain-denied.png`, `p9-m5-no-fixture-after-deny.png`. `GUI-WS-06` therefore stays non-public: fixture evidence exists, but no real logged-in workspace has created/cancelled/removed the disposable endpoint. |
| P9-M6 | Complete | RC6 release gate passed and `docs/zh-Hans-release-candidate-2026-05-31-rc6.md` was created. Current manifest state: `entries: 2662`, metadata fields `150 (5.6%)`, dry-run `already_applied: 2647`, `would_change: 0`, `missing: 0`; release coverage `2890/6408 = 31.1%`; JSON/YAML exports passed; Python unit tests passed `18 tests`; Rust focused gates passed (`ai custom_inference_smoke`, `warp custom_inference_smoke_override`, `endpoint_form_valid_accepts_complete_valid_form`, `warp_search_core`, `warp command_palette`); `cargo check -p warp` and bundle gate passed. RC6 decision remains `ready-for-local-use`, not public-RC, because P9-M5 has no real isolated account evidence. |
| P9-M7 | Complete | Cleanup and fixture safety audit passed. No `WarpOss.app`, `warp-oss`, or `terminal-server` process remains; `launchctl getenv WARP_CN_CUSTOM_INFERENCE_SMOKE` and `launchctl getenv WARP_DATA_PROFILE` are empty; `security find-generic-password -s dev.warp.WarpOss-zh-rc6 -a AiApiKeys` reports absent without printing secrets. Source audit confirms the smoke override still requires `cfg!(debug_assertions)` and exact env value `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`; the fixture endpoint is in-memory only; secure-storage writes are skipped only under the same debug smoke helper; `secure_state_dir()` skips the App Group path only under `cfg!(debug_assertions)` plus exact env match. Final `git diff --check` passed. |

## Phase 6 plan

Phase 6 shifts from local-use RC2 to public-RC readiness. The next work should not chase broad coverage; it should close the blockers that kept RC2 from being public: fresh upstream refs, reliable GUI evidence, at least one destructive confirmation verified with an isolated object, and clearer account/Billing/Cloud/Agent state fixtures.

The Phase 6 planning document is `docs/zh-Hans-localization-phase6.md`. Start with these checks before beginning a Phase 6 slice:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
git diff --check
```

Recommended first execution slice: P6-M1, upstream stable refresh. Phase 5 RC2 is `ready-for-local-use`, but not public-RC ready until upstream freshness and GUI evidence blockers are resolved.

## Phase 6 execution record

Execution started on 2026-05-31.

| Task | Result | Notes |
| --- | --- | --- |
| P6-M0 | Complete | Entry baseline passed: manifest validation and glossary checks passed; metadata remains `entries: 2645`, `key/context/status/expected_count: 133 (5.0%)`; dry-run reports `files: 194`, `already_applied: 2630`, `would_change: 0`, `missing: 0`; release coverage remains `2873/6425 = 30.9%`; `git diff --check` passed. No upstream freshness or GUI verification claim is made yet. |
| P6-M1 | Complete | `git fetch origin --tags` passed on 2026-05-31. No newer stable tag appeared; selected base remains `v0.2026.05.27.09.22.stable_00` at `2566f54af7c3e71facfe1865f2c492549b14248a`. Current branch is `0` behind and `88` ahead of that stable tag. Post-fetch dry-run remains `would_change: 0`, `missing: 0`. Stable freshness blocker is cleared for RC3, while GUI/state evidence blockers remain. |
| P6-M2 | Complete | Bundle gate passed and `warp-oss`/`terminal-server` processes launched, but Computer Use timed out for `WarpOss` and `dev.warp.WarpOss`. A macOS screenshot shows `你不能打开应用程序 “WarpOss”，因为它没有响应。` Evidence is saved at `docs/gui-smoke-artifacts/phase6/p6-m2-warp-oss-not-responding-2026-05-31.png`. Phase 6 GUI profile status is `automation-blocked`; no business path was promoted to `verified`. |
| P6-M3 | Complete | No destructive confirmation was verified because P6-M2 left the app `automation-blocked`. `GUI-WS-06`, `GUI-SET-06`, and `GUI-WS-04` now each have concrete blockers in the GUI matrix: missing disposable endpoint, missing isolated cloud environment, missing isolated managed auth secret, plus the current GUI automation blocker. Source anchors were rechecked for all three dialogs, and no real endpoint, environment, or secret was deleted. |
| P6-M4 | Complete | Added fixture ownership categories to the GUI matrix for account/auth, Billing, Cloud, Agent, and related web/onboarding rows. Rows now distinguish `local-fixture`, `test-account`, `server-state`, and `manual-only` owners with concrete triggers and blockers. No gate is left as a vague “needs account state” item. |
| P6-M5 | Complete | Completed exactly one targeted user-visible slice: `terminal.view.notifications`. Added 16 metadata-backed manifest entries and applied them to terminal notification discovery/error banners. Current dry-run: `entries: 2661`, `files: 197`, `already_applied: 2646`, `would_change: 0`, `missing: 0`; metadata `key/context/status/expected_count` is now `149 (5.6%)`; release coverage is `2889/6409 = 31.1%`. Verification passed: manifest validation, glossary check, dry-run, `cargo fmt --check`, `git diff --check`, and `cargo check -p warp`. |
| P6-M6 | Complete | Added machine-readable metadata summary output via `python3 script/zh_apply_localization.py --metadata-summary --json`, plus tests for JSON percentages/output. `--json` is scoped to `--metadata-summary` and errors clearly if used alone. No hard CI threshold was added. Verification passed: `python3 script/test_zh_apply_localization.py` (11 tests), JSON command, `py_compile`, and `git diff --check`. |
| P6-M7 | Complete | Created RC3: `docs/zh-Hans-release-candidate-2026-05-31-rc3.md`. Full command-line gate passed, including locale export, Python tests, `cargo check -p warp`, `cargo test -p warp_search_core`, `cargo test -p warp command_palette`, and bundle generation. Decision remains `ready-for-local-use`, not public RC, because GUI automation is `automation-blocked` and no destructive confirmation has real current-cycle GUI evidence. |

## Phase 5 plan

Phase 5 shifts from release-candidate creation to release hardening. The next development work should refresh upstream stable refs, reduce GUI manual-gate ambiguity with safer test objects and evidence records, continue only targeted terminal/Agent user-visible slices, and produce a second release-candidate decision.

The Phase 5 planning document is `docs/zh-Hans-localization-phase5.md`. Start with these checks before beginning a Phase 5 slice:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
```

Recommended first execution slice: P5-M1, upstream stable refresh. Phase 4's sync rehearsal used the latest locally available stable tag because `git fetch origin --tags` failed on network errors; do not make a public-release freshness claim until fetch succeeds or the limitation is explicitly documented.

## Phase 5 execution record

Executed on 2026-05-30.

| Task | Result | Notes |
| --- | --- | --- |
| P5-M0 | Complete | Phase 5 planning document, README entry, and maintenance entry are in place. Baseline checks passed: `entries: 2619`, `files: 190`, `would_change: 0`, `missing: 0`; release coverage is 30.6%. |
| P5-M1 | Complete | Retried upstream stable refresh. `git fetch origin --tags` and lightweight `ls-remote` both failed due GitHub network timeouts, so no merge/rebase was performed. Current branch remains `88` ahead and `0` behind local `v0.2026.05.27.09.22.stable_00`; public release freshness remains blocked until refs can be refreshed. |
| P5-M2 | Complete | Added GUI profile/evidence policy to the smoke matrix. Bundle and process startup succeeded, but Computer Use timed out and AppleScript activation failed; screenshots captured only the desktop, so no new UI path was marked verified. Evidence paths are recorded in `docs/gui-smoke-artifacts/`. |
| P5-M3 | Complete | Reviewed destructive confirmation paths for custom endpoint, environment, and auth secret deletion. `GUI-SET-06`、`GUI-WS-04`、`GUI-WS-06` now name concrete trigger paths and missing safe objects; auth-secret deletion title/buttons were added to manifest and replaced. Current dry-run: `entries: 2622`, `already_applied: 2607`, `would_change: 0`, `missing: 0`. |
| P5-M4 | Complete | Split auth, Billing, Cloud, and Agent status manual gates into concrete trigger/state requirements. Login/token/privacy, cloud capacity, credits banner, Build migration, and Agent lifecycle rows now identify whether they need a test account, fresh profile, service-side state, local fixture, or P5-M5 translation slice. |
| P5-M5 | Complete | Completed the Agent status label slice with metadata-backed manifest entries for conversation/task statuses, ambient task statuses, pending query badge, and history output statuses. Current dry-run: `entries: 2645`, `files: 194`, `already_applied: 2630`, `would_change: 0`, `missing: 0`; release coverage is 30.9%. |
| P5-M6 | Complete | Raised high-value metadata coverage to the Phase 5 target: `key/context/status/expected_count: 133 (5.0%)`. The added metadata focuses on auth/login/token fallback gates and P5 status-label entries, not low-value mechanical backfill. Locale JSON/YAML exports and Python tests passed; `--metadata-summary --json` is deferred because text output is sufficient for the current RC record. |
| P5-M7 | Complete | Created `docs/zh-Hans-release-candidate-2026-05-30-rc2.md` and reran the RC2 release gate. Manifest, glossary, dry-run, release coverage, locale exports, Python tests, `cargo fmt --check`, `git diff --check`, `cargo check -p warp`, `cargo test -p warp_search_core`, `cargo test -p warp command_palette`, and bundle gate passed. RC2 is documented as local-use ready, with public-RC blockers still called out. |
| P5-M8 | Complete | Final Phase 5 release decision is `ready-for-local-use`. RC2 is not `ready-for-public-rc` because fresh upstream refs could not be fetched and no destructive confirmation has real GUI evidence from an isolated test object. |

## Phase 5 release decision

Decision: `ready-for-local-use`.

RC2 can be used for local engineering validation and continued GUI/manual-gate testing because the manifest gate, glossary gate, locale exports, Python tests, Rust checks/tests, and bundle gate passed.

RC2 should not be published as a public release candidate yet. The remaining public-RC blockers are:

- Fresh upstream stable refs could not be fetched in P5-M1 because GitHub network requests timed out.
- Destructive confirmation dialogs have source-level fixes and concrete trigger plans, but no isolated endpoint/environment/auth-secret object has been verified in the GUI.
- Account, Billing, Cloud Agent, and Agent lifecycle states still need isolated accounts, service-side states, or test fixtures before they can be marked GUI verified.

## Phase 4 plan

Phase 4 shifts from asset scaffolding to release-quality execution. The next development work should use the Phase 3 tooling to close high-value workspace/settings residues, classify noisy modals/terminal/Agent candidates, advance real GUI smoke verification, and prepare a reproducible release candidate record.

The Phase 4 planning document is `docs/zh-Hans-localization-phase4.md`. Start with these checks before beginning a Phase 4 slice:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
```

Recommended first execution slice: P4-M1, high-value manifest v2 metadata enrichment. That work should focus on entries tied to workspace, settings, and GUI manual gates before adding broad new translations.

The first `modals`/terminal/Agent classification pass is tracked in `docs/zh-Hans-modal-candidate-classification.md`. Use it before translating noisy `modals` candidates so terminal protocol strings, Agent transcript templates, debug labels, and diagnostics are not mistaken for normal UI copy.

## Phase 4 execution record

Executed on 2026-05-30.

| Task | Result | Notes |
| --- | --- | --- |
| P4-M0 | Complete | Phase 4 planning document, README entry, and maintenance entry are in place. |
| P4-M1 | Complete | Added `--metadata-summary`; first high-value metadata slice covers 15 workspace/settings entries. |
| P4-M2 | Complete | First workspace slice localized the right panel code review controls, update banner actions, Oz command title, and AI usage upgrade title. Workspace coverage moved from 59.9% to 61.3%. |
| P4-M3 | Complete | First settings slice localized custom inference endpoint fields and team creation/invite basics, and normalized historical `API key(s)` translations to `API 密钥`. Settings coverage moved from 57.8% to 59.2%. |
| P4-M4 | Complete | Classified the highest-volume terminal/Agent `modals` candidates, ignored diagnostic terminal action labels, and recorded follow-up translation slices. `modals` candidates moved from 5371 to 5189. |
| P4-M5 | Complete | Rebuilt and launched `WarpOss.app`; GUI verified base workspace anchors, settings shell, command palette, and vertical tab context menu. A tab-menu English residue found during smoke was fixed in `app/src/tab.rs`. Destructive confirmations remain manual-gated because no safe local test object was available. |
| P4-M6 | Complete | Created `docs/zh-Hans-release-candidate-2026-05-30.md`; release gate passed with dry-run, glossary, metadata summary, locale export, Python tests, cargo check/tests, bundle gate, and GUI matrix updates. |
| P4-M7 | Complete | Ran the stable sync rehearsal against local `v0.2026.05.27.09.22.stable_00`; current branch is `88` commits ahead and `0` behind that stable base. Upstream fetch failed due GitHub network errors, so a fresh fetch remains required before public release. |

P4-M2 reviewed these workspace candidates and intentionally did not translate them in the first slice:

- `app/src/workspace/view.rs` internal logs and feature-state labels such as `tab_drag:*`, `Workspace_*`, `AutoupdateState_*`, `start_local_to_cloud_handoff:*`, `opencode.json`, and performance sampling messages.
- `app/src/workspace/mod.rs` debug-only command palette actions and keybinding tokens.
- `app/src/workspace/tab_settings.rs` settings keys and schema descriptions; these need a separate settings/search-token review before translation.
- Dynamic synchronized-input toasts in `app/src/workspace/view.rs` because they interpolate the English `enabled` / `disabled` verb; translating them cleanly requires a code-level branch rather than a manifest-only replacement.

P4-M3 reviewed these settings candidates and intentionally left them for later slices:

- `app/src/settings_view/features_page.rs` search keywords, action IDs, and feature metadata such as `ToggleCopyOnSelect`, `copy on select`, and keyword-only strings.
- `app/src/settings_view/mod.rs` route/parser tokens such as `WarpDrive`, `AgentProfiles`, and `CloudEnvironments`.
- `app/src/settings_view/teams_page.rs` billing-plan and capacity strings, because they need account state and billing UI review before translation.
- Example values such as `e.g. ~/code-repos/repo`, `e.g. sk-...`, and domain validation examples; these should remain recognizable as examples unless a later GUI review proves otherwise.

P4-M4 reviewed the highest-volume `modals` candidates and intentionally did not bulk translate them:

- `app/src/terminal/view/action.rs` is now ignored by inventory because it contains terminal action enum display/debug labels, not end-user UI copy.
- `app/src/terminal/view.rs`, `app/src/terminal/input.rs`, and `app/src/terminal/view/init.rs` remain mixed terminal paths; user-visible banners, permission prompts, and context menus should be split into targeted translation slices.
- `app/src/ai/agent/mod.rs`, `app/src/ai/agent_sdk/driver.rs`, and `app/src/ai/agent_sdk/driver/output.rs` remain mixed Agent paths; transcript Markdown, lifecycle logs, and harness strings should not be translated without a GUI/runtime trigger.
- Follow-up categories and decisions are recorded in `docs/zh-Hans-modal-candidate-classification.md`.

P4-M5 GUI smoke notes:

- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` rebuilt and signed `target/debug/bundle/osx/WarpOss.app`.
- `open -n target/debug/bundle/osx/WarpOss.app` launched the local bundle, and Computer Use verified `文件`/`编辑`/`视图`/`标签页` menu anchors, global search placeholder, `新会话`, the settings shell, `Cmd-P` command palette chips, and the vertical tab context menu.
- The first tab-context-menu pass exposed visible English labels in `app/src/tab.rs`; P4-M5 added manifest entries for the menu and rechecked the rebuilt UI showing `共享会话`、`复制窗格标题`、`复制工作目录`、`重命名标签页`、`关闭标签页`、`关闭其他标签页`、`关闭下方标签页`、`另存为新配置`.
- macOS briefly prompted for `WarpOss` access to other App data after rebuild. The permission was not granted; the prompt was dismissed and GUI reading continued.
- Destructive confirmations such as endpoint/environment/auth-secret deletion and team ownership transfer still require isolated test objects or account state, so they remain GUI manual gates.

## Phase 2 Round 2 execution record

Executed on 2026-05-30.

| Task | Result | Evidence |
| --- | --- | --- |
| Round 2 implementation plan | Complete | `05b719f4 docs: plan phase 2 round 2 zh-Hans localization` |
| Appearance command-palette actions | Complete | `81672827 feat: localize appearance command actions` |
| Conversation list actions and delete toasts | Complete | `25d71e8c feat: localize conversation actions` |
| Cloud agent capacity modal | Complete | `4c31e506 feat: localize cloud agent capacity modal` |
| AWS credential errors and environment deletion confirmation | Complete | `43613337 feat: localize credential and environment dialogs` |

Round 2 intentionally skipped these strings:

- Appearance strings `dim inactive panes`, `focus follows mouse`, and `jump to bottom of block button`, because they also appear as settings search keyword strings in `app/src/settings_view/appearance_page.rs`; the current manifest applies exact replacements per file, so translating them would also mutate search metadata.
- Cloud capacity dynamic strings containing `${price}/month`, `2x`, and `5x`, because they combine runtime pricing or multiplier fragments and need UI review before translation.
- Theme names and example values such as `Aurora`, `Classic 1`, `Glow`, `Warp 1`, `{value}%`, and command/example tokens.

Round 2 command-line validation passed:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
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

## Phase 2 Round 3 execution record

Executed on 2026-05-30.

Round 3 continued the second-stage cleanup by targeting launch modals, plan/credit billing modals, Agent tips, conversation details metadata, CLI administrator prompts, and destructive confirmation dialogs.

| Task | Result | Evidence |
| --- | --- | --- |
| Round 3 implementation plan | Complete | `9fa400ff docs: plan phase 2 round 3 zh-Hans localization` |
| Launch modals | Complete | `524db95b feat: localize launch modals` |
| Credit and plan modals | Complete | `9511f730 feat: localize credit and plan modals` |
| Agent tips | Complete | `d3e7a2c6 feat: localize agent tips` |
| Conversation details panel | Complete | `c551a024 feat: localize conversation details panel` |
| CLI prompts and destructive confirmations | Complete | `b046da1f feat: localize cli and confirmation prompts` |

Round 3 final dry-run:

```text
entries: 2543
files: 184
already_applied: 2528
would_change: 0
missing: 0
```

Round 3 final coverage snapshot:

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| `onboarding` | 266 | 55 | 82.9% |
| `workspace` | 582 | 392 | 59.8% |
| `search` | 267 | 40 | 87.0% |
| `settings` | 1170 | 860 | 57.6% |
| `modals` | 626 | 5813 | 9.7% |
| `release` | 2789 | 7139 | 28.1% |

Round 3 command-line validation passed:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Round 3 notes:

- The AppleScript CLI install/uninstall prompts require escaped inner quotes in Rust string literals. The manifest entry is valid TOML, and the applied Rust code was manually checked so `cargo fmt --check` and `cargo check -p warp` both pass.
- `open -na target/debug/bundle/osx/WarpOss.app` treats the path as an application name and fails. Use `open -n target/debug/bundle/osx/WarpOss.app` for the local bundle path.
- Automatic GUI inspection remains manual-gated because Computer Use timed out while reading the running `WarpOss` window state.

## Phase 2 Round 4 execution record

Executed on 2026-05-30.

Round 4 shifted the next slice from broad translation to release-quality audit work: inventory review modes, conservative denominator cleanup, raw-string manifest support, Warp on Web home copy, Agent status/error residue, and Agent Assisted Environment fallbacks.

| Task | Result | Evidence |
| --- | --- | --- |
| Round 4 implementation plan | Complete | `9e2f93a3 docs: plan phase 2 round 4 zh-Hans localization` |
| Inventory review modes | Complete | `436d526d chore: add zh-Hans inventory review modes` |
| Inventory noise filters | Complete | `1926d03a chore: refine zh-Hans inventory noise filters` |
| Warp on Web home | Complete | `da976cff feat: localize Warp on Web home` |
| Agent status residue | Complete | `a3e004fc feat: localize agent status residue` |
| Environment modal fallbacks | Complete | `67ce0d9f feat: localize environment modal fallbacks` |

Round 4 final dry-run:

```text
entries: 2556
files: 186
already_applied: 2541
would_change: 0
missing: 0
```

Round 4 final coverage snapshot:

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| `onboarding` | 266 | 55 | 82.9% |
| `workspace` | 584 | 391 | 59.9% |
| `search` | 267 | 26 | 91.1% |
| `settings` | 1172 | 856 | 57.8% |
| `modals` | 635 | 5371 | 10.6% |
| `release` | 2802 | 6678 | 29.6% |

Round 4 top remaining candidate paths:

| Preset | Top paths |
| --- | --- |
| `workspace` | `app/src/workspace/view.rs` (119), `app/src/workspace/mod.rs` (66), `app/src/workspace/tab_settings.rs` (54) |
| `settings` | `app/src/settings_view/features_page.rs` (182), `app/src/settings_view/mod.rs` (172), `app/src/settings_view/teams_page.rs` (146) |
| `modals` | `app/src/terminal/view.rs` (334), `app/src/terminal/view/action.rs` (182), `app/src/terminal/input.rs` (159) |

Round 4 notes:

- `script/zh_localization_inventory.py` now supports `--status` and `--top-paths` for candidate review.
- `script/zh_apply_localization.py` now supports escaped `\n` in manifest values and raw string replacement, used by `app/src/workspace/home.rs`.
- The low `modals` coverage remains dominated by terminal and Agent internals; Round 4 documents exact non-UI exclusions instead of translating protocol/schema strings for coverage.
- GUI automation successfully read the app window in Round 4 and confirmed the base workspace chrome is Chinese. The deeper Round 4 states remain manual GUI gates because they were not triggered in this smoke pass.

## Apply translations after syncing upstream

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run
python3 script/zh_apply_localization.py
cargo fmt
```

If `--dry-run` fails, inspect the upstream file, update the matching `source` entry, and rerun the script.

## Inventory workflow

Use the inventory script to find remaining likely user-visible English strings before adding a new batch of replacements:

```bash
python3 script/zh_localization_inventory.py --preset onboarding > /tmp/zh-onboarding.md
python3 script/zh_localization_inventory.py --preset workspace > /tmp/zh-workspace.md
python3 script/zh_localization_inventory.py --preset search > /tmp/zh-search.md
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
python3 script/zh_localization_inventory.py --preset modals > /tmp/zh-modals.md
```

Use focused review modes before editing broad presets:

```bash
python3 script/zh_localization_inventory.py --preset workspace --status candidate
python3 script/zh_localization_inventory.py --preset settings --status covered-target
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

Review only `candidate` rows. Add manifest entries in small batches, then rerun:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
```

The inventory script intentionally filters telemetry files, keybindings, filter tokens, placeholder-only strings, and settings search tags. These strings are not treated as untranslated UI unless they are also rendered directly in a visible control.

Path and line-pattern filters are configured in `resources/localization/zh-Hans-inventory-ignore.toml`. Before adding an ignore entry, inspect the path directly and record why it is not user-visible UI:

```bash
python3 script/zh_localization_inventory.py app/src/example.rs --status candidate
```

Coverage counts are available for release tracking:

```bash
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

`search` includes the app search surfaces and the shared `warp_search_core` crate, where common filter chip labels and search placeholders live. `release` is an aggregate preset across the named high-visibility source roots. Keep the per-surface commands in release notes so regressions remain easy to locate.

## Local release checklist

Run this command-line checklist after syncing upstream and applying the manifest:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
./script/run
```

Current workspace notes:

- `cargo check -p app` is not part of the current checklist. Older planning docs used `app` as the app-crate label; in the current workspace the package is named `warp`, so `cargo check -p app` fails with `package ID specification 'app' did not match any packages`.
- Use `TERM=xterm-256color ./script/run --dont-open` for a non-interactive bundle/build check. Without that `TERM`, `cargo-bundle` may panic while printing colored status output with `Error(Term(ColorOutOfRange), ...)`.
- Use `./script/run` or `open -n target/debug/bundle/osx/WarpOss.app` for the interactive app smoke pass after the bundle gate is green.
- Phase 2 local automatic GUI smoke is currently manual-gated on this machine because the app process starts but window automation times out.

2026-05-29 recorded failure output:

```text
$ cargo check -p app
error: package ID specification `app` did not match any packages

help: a package with a similar name exists: `aes`
```

```text
$ WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
Cannot access ssh://git@github.com/warpdotdev/warp-channel-config.git (no SSH access?). Skipping install.
Skipping internal channel config installation (no repo access).
Bundling app (bin: warp-oss)...
warning: `warp` (lib) generated 46 warnings (run `cargo fix --lib -p warp` to apply 46 suggestions)
Finished `dev` profile [unoptimized + debuginfo] target(s) in 2m 24s

thread 'main' panicked at src/main.rs:164:37:
called `Result::unwrap()` on an `Err` value: Error(Term(ColorOutOfRange), State { next_error: None, backtrace: InternalBacktrace { backtrace: None } })
```

2026-05-29 non-interactive bundle success output:

```text
$ TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
Cannot access ssh://git@github.com/warpdotdev/warp-channel-config.git (no SSH access?). Skipping install.
Skipping internal channel config installation (no repo access).
Bundling app (bin: warp-oss)...
Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.20s
Bundling WarpOss.app
Finished 1 bundle at:
        /Users/drew/Project/Warp CN/target/debug/bundle/osx/WarpOss.app
Successfully bundled...
Successfully prepared bundled resources in target/debug/bundle/osx/WarpOss.app/Contents/Resources
Codesigning app...
target/debug/bundle/osx/WarpOss.app: replacing existing signature
```

Manual smoke paths:

- Fresh onboarding: Agent path.
- Fresh onboarding: terminal-only path.
- Login: browser login.
- Login: token paste fallback.
- Login: privacy settings.
- Workspace: user menu.
- Workspace: left and right panels.
- Workspace: vertical tabs.
- Search: command palette.
- Search: command search.
- Search: slash command.
- Settings: Account, Appearance, Features, Privacy, AI, Code, MCP, Billing, and Environments.
- Modals/toasts: update toast, destructive dialog, theme modal, tab config modal, terminal share modal.

Record every failed item with the exact command output or manual path, then either update `resources/localization/zh-Hans-overrides.toml` or document why the item is outside the current local-fork scope.

## Upstream sync workflow

The full stable-first workflow lives in `docs/zh-Hans-upstream-sync.md`. The short path is:

```bash
git switch drew/zh-Hans-localization
git fetch origin --tags
UPSTREAM_BASE=<tag-or-commit>
git merge "$UPSTREAM_BASE"
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

For larger upstream changes, use `git rebase "$UPSTREAM_BASE"` instead of merge if you explicitly want a linear local history. User-facing releases should follow a stable tag, release branch, or explicitly recorded upstream commit; `origin/master` is suitable for preflight checks but should not silently become the release base.

## Translation scope

The first pass focuses on high-visibility UI:

- onboarding screens
- login / AI opt-out screens
- vertical tabs labels
- search placeholders and top-level navigation labels
- settings core and advanced pages
- command palette, command search, and slash commands
- common modals, toasts, themes, tab configs, Warp Drive, terminal sharing, and Agent management surfaces

Prioritize remaining work from candidate strings surfaced by the inventory script, especially low-signal broad presets where internal protocol, test, and diagnostic literals are still intentionally filtered manually.

## Build notes

Official local run path:

```bash
./script/bootstrap --skip-common-skills
./script/run
```

`script/bootstrap` may install development dependencies and can request `gcloud` authentication. For localization-only iteration, prefer starting with `cargo check` on the touched crates before running the full app build.
