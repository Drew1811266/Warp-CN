# zh-Hans Localization Phase 30

Date: 2026-06-01

## Goal

Collect low-load current-cycle GUI evidence for local-fixture rows without rebuilding the bundle, logging in, spending credits, creating secrets, deleting objects, or touching the user's main account.

## Execution

Used existing bundle:

- `target/debug/bundle/osx/WarpOss.app`
- Launched with `WARP_DATA_PROFILE=zh-rc9-local-fixture`.
- Lowered process priority with `renice 15` after startup CPU spiked.
- Stopped the `WarpOss` and child `terminal-server` processes after evidence capture.

No bundle rebuild was performed because the local machine had already overheated during full scans. This means Phase 30 GUI evidence reflects the existing May 31 bundle, not the Phase 27-29 source updates.

## Evidence

Captured screenshots:

- `docs/gui-smoke-artifacts/phase30/p30-onboarding-welcome-local-fixture-window.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-agent-choice.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-customize.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-agent-settings-residue.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-third-party-agent.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-theme-choice.png`
- `docs/gui-smoke-artifacts/phase30/p30-onboarding-ai-enable-skip-login.png`
- `docs/gui-smoke-artifacts/phase30/p30-disable-ai-confirmation.png`
- `docs/gui-smoke-artifacts/phase30/p30-main-window-local-fixture.png`
- `docs/gui-smoke-artifacts/phase30/p30-settings-account-local-fixture.png`
- `docs/gui-smoke-artifacts/phase30/p30-settings-agent-local-fixture.png`
- `docs/gui-smoke-artifacts/phase30/p30-settings-privacy-local-fixture.png`

## Row Results

| Row | Phase 30 result | Evidence / blocker |
| --- | --- | --- |
| `GUI-ONB-01` | `fixture-evidence-with-residue` | Fresh onboarding opened in Chinese and Agent path was selectable. Screenshots show Chinese onboarding anchors, but the static product preview image still contains embedded English UI and the reused bundle still showed `auto (cost-efficient)` before Phase 28 source fixes were rebuilt. |
| `GUI-AUTH-03` | `fixture-evidence` | Local no-login path showed `隐私设置`, `服务条款`, `禁用 AI 功能`, and disable-AI confirmation in Chinese. |
| `GUI-WS-01` | `accessibility-evidence` + `cropped-screenshot-evidence` | Main window and left panel loaded in the isolated profile with Chinese menu/window anchors such as `搜索会话、Agent、文件...`, `搜索标签页...`, `新会话`, and Settings navigation. |
| `GUI-SET-03` | `local-fixture-only` | Settings > Agent is readable in Chinese in a logged-out profile, but the row still requires isolated account evidence for Build plan/API key/custom endpoint state. |
| `GUI-AUTH-02` | `blocked-trigger` | Token paste fallback was not reachable from the observed local onboarding path without auth callback/token fixture. |
| `GUI-WS-02` | `blocked-fixture` | No disposable session history existed, so delete menu/toast could not be safely triggered. |
| `GUI-WS-03` | `blocked-fixture` | No rewindable command history existed in the isolated profile. |
| `GUI-WS-05` | `manual-only` | Admin permission prompt requires install/uninstall command flow and macOS permission interaction; not triggered in this low-load pass. |
| `GUI-AGENT-01` | `partial-fixture-evidence` | Agent onboarding/settings copy is readable, but input-area tips were not triggered because AI was disabled to avoid login. |
| `GUI-AGENT-02` | `blocked-fixture` | No disposable Agent conversation fixture existed. |
| `GUI-AGENT-03` | `blocked-fixture` | No lifecycle fixture for queued, pending, running, done, failed, blocked, and cancelled states existed. |
| `GUI-AGENT-04` | `blocked-fixture` | No safe web/AWS/quota/stream error fixture existed; main account/quota was not used. |
| `GUI-AGENT-05` | `blocked-fixture` | No environment modal fallback fixture existed in the logged-out local profile. |

## Residue

- Static onboarding product preview images contain embedded English UI text. This is image/content residue, not a Rust string manifest miss.
- The reused bundle showed `auto (cost-efficient)` in onboarding model selection. Phase 28 source now translates this to `自动（节省成本）`, but the bundle was not rebuilt in Phase 30.
- Theme names such as `Phenomenon`, `Dark`, `Light`, and `Adeberry` remain English in the reused bundle and need product/design review before deciding whether to localize names or treat them as theme identifiers.

## Qualification

Phase 30 is accepted as `qualified-gui-evidence-low-load-with-residue`.

The phase satisfies the low-load evidence requirement because more than five local-fixture/manual rows received current-cycle screenshot evidence or concrete reproducible blockers. It does not promote the project to public RC, and it does not promote account/state rows to verified.

No account, billing quota, cloud environment, secret, production object, or team ownership state was touched.
