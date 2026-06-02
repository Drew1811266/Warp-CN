# zh-Hans Localization Phase 114

Date: 2026-06-02

## Scope

Phase 114 prepared RC20 local fixture implementation lanes. It created a
planning document only and did not modify Rust source, run GUI, compile, bundle,
generate PNGs, log in, call backend services, touch billing/cloud/team state, or
create/delete managed secrets or endpoints.

## Fixture Lane Classification

Visible GUI only:

```text
GUI-AUTH-02
GUI-AGENT-01
```

Debug fixture design:

```text
GUI-AGENT-02
GUI-AGENT-03
GUI-AGENT-04
GUI-AGENT-05
GUI-WS-02
GUI-WS-03
```

Manual only:

```text
GUI-WS-05
```

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

## Rust Anchors Reviewed

Existence check:

```text
exists app/src/auth/paste_auth_token_modal.rs
exists app/src/terminal/view/ambient_agent/tips.rs
exists app/src/terminal/view/ambient_agent/view_impl.rs
exists app/src/ai/blocklist/local_agent_task_sync_model.rs
exists app/src/workspace/close_session_confirmation_dialog.rs
exists app/src/workspace/rewind_confirmation_dialog.rs
exists app/src/ai/agent_sdk/admin.rs
```

Reviewed anchor roles:

```text
app/src/auth/paste_auth_token_modal.rs: token paste modal
app/src/terminal/view/ambient_agent/tips.rs: Agent tips copy
app/src/terminal/view/ambient_agent/view_impl.rs: Agent lifecycle, capacity, auth, error, setup, and cancelled surfaces
app/src/ai/blocklist/local_agent_task_sync_model.rs: local Agent status/state mapping
app/src/workspace/close_session_confirmation_dialog.rs: close session confirmation
app/src/workspace/rewind_confirmation_dialog.rs: rewind confirmation
app/src/ai/agent_sdk/admin.rs: administrator prompt source boundary
```

## Planning Artifact

```text
docs/zh-Hans-local-fixture-implementation-plan-rc20.md
```

## Rust Change Boundary

No Rust source edits were made for Phase 114. The current worktree already
contains pre-existing Rust localization changes from earlier phases; Phase 114
adds only the two Markdown planning records listed above.

## Qualification Review

```text
phase: 114
status: qualified
local fixture implementation plan exists: yes
each fixture lane has a source anchor and safety boundary: yes
all fixture switches are opt-in and smoke-scoped: yes
manual-only administrator prompt remains manual-only: yes
Phase 114 Rust source edits: none
external operations run: none
```
