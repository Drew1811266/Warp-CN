# zh-Hans Local Fixture Implementation Plan RC20

Date: 2026-06-02

## Scope

This plan prepares future local fixture implementation for zh-Hans GUI evidence.
It does not implement fixture code and does not change Rust source in this
phase.

## Production Exclusion Rules

```text
fixtures must be opt-in
fixtures must be debug/test-only or otherwise excluded from production behavior
fixtures must not read real credentials
fixtures must not log in to an account
fixtures must not create, mutate, or delete production cloud objects
fixtures must not create, mutate, or delete production managed secrets
fixtures must not create, mutate, or delete real custom endpoints
fixtures must not mutate real billing, quota, backend, or team state
fixture evidence cannot clear public-RC blockers by itself
```

## Visible GUI Only Lanes

| Lane | GUI rows | Source anchors | Trigger | Fixture data boundary | Redaction | Cleanup | Proof needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `auth-token-fallback` | `GUI-AUTH-02` | `app/src/auth/paste_auth_token_modal.rs`, `app/src/auth/login_slide.rs`, `app/src/auth/login_failure_notification.rs` | `WARP_CN_AUTH_TOKEN_SMOKE=1` if future automation needs a stable entry point; otherwise logged-out visible GUI only | Fake invalid token or invalid redirect text only. No browser callback, account, cookie, or token capture. | Crop modal only; redact any typed token marker if it resembles a real secret. | Close modal and delete local profile artifacts if created. | Accessibility anchors and cropped screenshot showing token paste/error copy in Chinese. |
| `agent-tips-visible-gui` | `GUI-AGENT-01` | `app/src/ai/agent_tips.rs`, `app/src/terminal/view/ambient_agent/tips.rs` | Visible Agent input surface; no fixture data required | No conversation, account, cloud, billing, or backend state. | Crop input/tips surface only; no user prompt history. | Close surface; delete temporary local profile if created. | Tips and shortcut copy are Chinese and do not overlap controls. |

## Debug Fixture Design Lanes

| Lane | GUI rows | Source anchors | Trigger variable | Fixture data boundary | Redaction | Cleanup | Proof needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `agent-conversation-details-fixture` | `GUI-AGENT-02` | `app/src/terminal/view/ambient_agent/view_impl.rs`, `app/src/ai/blocklist/local_agent_task_sync_model.rs` | `WARP_CN_AGENT_CONVERSATION_SMOKE=1` | Seed one disposable local Agent conversation with synthetic title, status, and timestamps. No server conversation token, account identifier, endpoint, or team ID. | Crop details panel; redact local paths if shown. | Clear fixture conversation on exit or profile cleanup. | Details panel metadata, status, and actions render in Chinese. |
| `agent-lifecycle-states-fixture` | `GUI-AGENT-03` | `app/src/ai/blocklist/local_agent_task_sync_model.rs`, `app/src/terminal/view/ambient_agent/view_impl.rs` | `WARP_CN_AGENT_LIFECYCLE_SMOKE=1` | Seed queued, pending, running, done, failed, blocked, and cancelled states in memory only. No backend task update. | Crop lifecycle list/card only. | Clear in-memory states on exit. | Lifecycle labels render in Chinese for every seeded state. |
| `agent-local-error-fixture` | `GUI-AGENT-04` local-only subset | `app/src/ai/blocklist/local_agent_task_sync_model.rs`, `app/src/terminal/view/ambient_agent/view_impl.rs` | `WARP_CN_AGENT_ERROR_SMOKE=1` | Seed local web/stream/AWS/quota fallback messages without network calls, real provider state, quota consumption, or credentials. | Crop error surface only; no logs with tokens or endpoint URLs. | Clear in-memory error state on exit. | Error fallback copy renders in Chinese without implying real quota/provider evidence. |
| `agent-environment-fallback-fixture` | `GUI-AGENT-05` | `app/src/ai/blocklist/inline_action/create_environment_modal.rs`, `app/src/terminal/view/ambient_agent/view_impl.rs` | `WARP_CN_AGENT_ENVIRONMENT_SMOKE=1` | Seed environment fallback copy only. Do not create a cloud environment or call backend environment APIs. | Crop modal/fallback copy only. | Clear fixture modal state on exit. | Environment fallback copy renders in Chinese. |
| `session-history-fixture` | `GUI-WS-02` | `app/src/workspace/close_session_confirmation_dialog.rs` | `WARP_CN_SESSION_HISTORY_SMOKE=1` | Seed disposable local session history only. No shared session, account, or cloud object. | Crop confirmation and toast only; redact local path/session title if needed. | Remove local fixture history/profile data. | Close/delete session confirmation and related copy render in Chinese. |
| `rewind-state-fixture` | `GUI-WS-03` | `app/src/workspace/rewind_confirmation_dialog.rs` | `WARP_CN_REWIND_SMOKE=1` | Seed one disposable rewindable local conversation state. No real command execution or file mutation. | Crop rewind dialog only; avoid command output. | Discard seeded state and local profile. | Rewind confirmation copy renders in Chinese and warns about Agent command cancellation. |

## Manual Only Lane

| Lane | GUI rows | Source anchors | Trigger | Boundary | Proof needed |
| --- | --- | --- | --- | --- | --- |
| `administrator-prompt-manual-only` | `GUI-WS-05` | `app/src/ai/agent_sdk/admin.rs` | Manual review only | Do not automate administrator prompts. Use only a disposable machine/profile with explicit permission. | Manual redacted evidence that shows the Chinese prompt without exposing account, shell, or privilege data. |

## Reserved Environment Variables

```text
WARP_CN_AUTH_TOKEN_SMOKE=1
WARP_CN_AGENT_CONVERSATION_SMOKE=1
WARP_CN_AGENT_LIFECYCLE_SMOKE=1
WARP_CN_AGENT_ERROR_SMOKE=1
WARP_CN_AGENT_ENVIRONMENT_SMOKE=1
WARP_CN_SESSION_HISTORY_SMOKE=1
WARP_CN_REWIND_SMOKE=1
```

## Public-RC Boundary

These fixture lanes may support local-use confidence and screenshot planning.
They cannot clear:

```text
blocked-no-isolated-account
blocked-no-backend-fixture
blocked-no-disposable-object
```

Public-RC promotion still requires matching registry status, human release
evidence, redacted GUI/backend/account artifacts, and cleanup proof.

