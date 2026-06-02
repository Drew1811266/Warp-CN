# zh-Hans Localization Phase 38

Date: 2026-06-01

## Goal

Rebuild from current source and replace the reused-bundle GUI evidence from Phase 30 with current-source local GUI smoke evidence.

## Execution

Build command:

```text
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 CARGO_BUILD_JOBS=2 nice -n 10 ./script/run --dont-open
```

Result:

- Bundle created at `target/debug/bundle/osx/WarpOss.app`.
- Initial rebuild completed in `1m 32s`.
- Incremental rebuild after the runtime model-label fix completed in `49.89s`.
- Existing Rust warnings remain the known unused-variable warnings in `scp_fallback.rs` and `terminal/input/slash_commands/mod.rs`.

Runtime policy:

- Launched with `WARP_DATA_PROFILE=zh-rc10-local-fixture`.
- Reniced `warp-oss` and child `terminal-server` to `15`.
- Stopped the debug bundle and child process after screenshots.
- Did not use a main account, billing quota, cloud environment, secret, production object, or team ownership state.

## Evidence

Current-source screenshots:

- `docs/gui-smoke-artifacts/phase38/p38-onboarding-welcome-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-agent-choice-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-customize-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-agent-settings-runtime-residue.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-third-party-agent-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-theme-choice-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-onboarding-ai-enable-skip-login-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-disable-ai-confirmation-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-main-window-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-settings-account-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-settings-agent-current-source.png`
- `docs/gui-smoke-artifacts/phase38/p38-settings-privacy-current-source.png`

Rows with current-source evidence:

| Row | Evidence | Result |
| --- | --- | --- |
| `GUI-BASE-01` | Computer Use accessibility text | Menu bar showed `文件`、`编辑`、`视图`、`标签页`、`块`、`AI`、`Drive`、`窗口`、`帮助`. |
| `GUI-BASE-04` | Screenshot | Disabling AI reached the Chinese main window. |
| `GUI-ONB-01` | Screenshots | Welcome, Agent choice, customization, third-party Agent, and theme screens were visible in Chinese. |
| `GUI-AUTH-03` | Screenshots | `开始使用 AI`, `禁用 AI 功能`, disable-AI confirmation, and `暂时跳过` were visible in Chinese. |
| `GUI-SET-01` | Screenshots | Account, Warp Agent, and Privacy settings were visible in Chinese. |

## Residue Review

Static onboarding previews still contain embedded English UI. These remain `visual-residue` because they are PNG assets under `app/assets/async/png/onboarding/`, not Rust source string manifest drift.

The current-source smoke initially still showed `auto (cost-efficient)` in an Agent model settings view. Investigation found:

- `app/src/ai/llms.rs` source already used `自动（节省成本）`.
- `resources/localization/zh-Hans-overrides.toml` already mapped `auto (cost-efficient)` to `自动（节省成本）`.
- Repository search outside build outputs found no current source occurrence of `auto (cost-efficient)` except manifest/docs references.

Conclusion: the visible residue came from server-provided or cached model metadata. Phase 38 added a narrow exact-match runtime mapping for the built-in `auto (cost-efficient)` and `auto (responsive)` display names without changing model IDs, provider protocol fields, prompts, or arbitrary third-party model names.

The focused unit test passed:

```text
CARGO_BUILD_JOBS=2 nice -n 10 cargo test -j 2 -p warp llm_info_localizes_builtin_auto_display_names_from_wire_metadata
```

A second GUI launch after the fix did not expose a readable Warp window in this desktop session and is recorded as `automation-blocked` at:

- `docs/gui-smoke-artifacts/phase38/p38-runtime-fix-automation-blocked-desktop.png`

## Remaining Blockers

Public-RC rows remain blocked without isolated account/backend prerequisites:

- `GUI-AUTH-01`: isolated browser-login test account.
- `GUI-SET-03`: isolated account with real AI settings, Build plan, API key, and custom endpoint visibility.
- `GUI-SET-06`: disposable cloud environment `zh-smoke-delete-environment`.
- `GUI-WS-04`: disposable managed auth secret `zh-smoke-delete-secret`.
- `GUI-WS-06`: isolated account/custom inference state and disposable endpoint `zh-smoke-delete-endpoint`.
- `GUI-WS-07`: disposable owner test team `zh-smoke-public-rc-team`.
- `GUI-BILL-01`, `GUI-BILL-02`, `GUI-CLOUD-01`: safe billing/quota/backend fixture state.

## Validation

Passed:

```text
CARGO_BUILD_JOBS=2 nice -n 10 cargo test -j 2 -p warp llm_info_localizes_builtin_auto_display_names_from_wire_metadata
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
cargo fmt --check
git diff --check
```

## Qualification

Phase 38 is accepted as `qualified-current-source-gui-smoke-low-load`.

The phase is qualified because current-source evidence now covers more than five local/fixture GUI rows or concrete blockers, risky account/backend state was not touched, the reused-bundle residue was reclassified and fixed as server/cache display metadata, and debug GUI processes were stopped after capture.
