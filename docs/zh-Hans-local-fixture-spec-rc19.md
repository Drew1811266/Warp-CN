# zh-Hans Local Fixture Spec RC19

Date: 2026-06-02

## Purpose

This spec defines non-public local fixture lanes for zh-Hans GUI evidence that
is useful for local readiness but insufficient for public-RC promotion. It is a
planning artifact only; it does not add debug fixture code.

## Fixture Rules

```text
fixtures must be debug-only or env-gated
fixtures must not read production state
fixtures must not use real credentials
fixtures must not log into an account
fixtures must not purchase credits or consume quota
fixtures must not create, mutate, or delete cloud objects
fixtures must not create, mutate, or delete managed secrets
fixtures must not modify endpoint or team ownership state outside disposable fixtures
fixture evidence cannot promote public-RC rows by itself
```

## Lanes

| Lane | Rows | Readiness | Source Anchors | Evidence Goal |
| --- | --- | --- | --- | --- |
| `auth-token-fallback` | `GUI-AUTH-02` | `ready-for-visible-gui-only` | `app/src/auth/paste_auth_token_modal.rs`, `app/src/auth/login_slide.rs`, `app/src/auth/login_failure_notification.rs` | Paste an invalid redirect/token in a logged-out visible GUI and verify Chinese modal/error copy. |
| `agent-tips-visible-gui` | `GUI-AGENT-01` | `ready-for-visible-gui-only` | `app/src/ai/agent_tips.rs`, `app/src/terminal/view/ambient_agent/tips.rs` | Open the Agent input surface and verify translated tips do not overlap input or controls. |
| `agent-conversation-details-fixture` | `GUI-AGENT-02` | `ready-for-debug-fixture-design` | `app/src/terminal/view/ambient_agent/view_impl.rs`, `app/src/ai/blocklist/local_agent_task_sync_model.rs` | Seed a disposable local Agent conversation with safe metadata and open the details panel. |
| `agent-lifecycle-states-fixture` | `GUI-AGENT-03` | `ready-for-debug-fixture-design` | `app/src/ai/blocklist/local_agent_task_sync_model.rs`, `app/src/terminal/view/ambient_agent/view_impl.rs` | Seed queued, pending, running, done, failed, blocked, and cancelled lifecycle states. |
| `agent-local-error-fixture` | `GUI-AGENT-04` local-only subset | `ready-for-debug-fixture-design` | `app/src/ai/blocklist/local_agent_task_sync_model.rs`, `app/src/terminal/view/ambient_agent/view_impl.rs` | Trigger local web/stream fallback copy without touching AWS, billing, quota, or account state. |
| `agent-environment-fallback-fixture` | `GUI-AGENT-05` | `ready-for-debug-fixture-design` | `app/src/ai/blocklist/inline_action/create_environment_modal.rs`, `app/src/terminal/view/ambient_agent/view_impl.rs` | Seed Agent Assisted Environment fallback copy without creating cloud resources. |
| `session-history-fixture` | `GUI-WS-02` | `ready-for-debug-fixture-design` | `app/src/workspace/close_session_confirmation_dialog.rs` | Seed disposable session history and verify session menu/delete toast copy. |
| `rewind-state-fixture` | `GUI-WS-03` | `ready-for-debug-fixture-design` | `app/src/workspace/rewind_confirmation_dialog.rs` | Seed a disposable rewindable conversation state and verify rewind confirmation copy. |
| `administrator-prompt-manual-only` | `GUI-WS-05` | `manual-only-unsafe-to-automate` | `app/src/ai/agent_sdk/admin.rs` | Do not automate; verify only on a disposable machine/profile with explicit permission for admin prompts. |

## Public-RC Boundary

```text
local fixture evidence may support RC local-use confidence
local fixture evidence may not clear isolated-account rows
local fixture evidence may not clear backend/disposable-object rows
local fixture evidence may not clear billing, cloud, managed-secret, endpoint,
or team-ownership rows
```

## Future Implementation Guardrails

Any future fixture code should:

```text
use a narrowly named env var such as WARP_CN_<LANE>_SMOKE=1
compile only in debug or explicit test/fixture builds
seed disposable in-memory state where possible
avoid Keychain/App Group prompts unless the lane explicitly requires manual review
emit no secrets, tokens, account identifiers, endpoint URLs, or team IDs
include a tracked phase record before any public-RC decision changes
```

