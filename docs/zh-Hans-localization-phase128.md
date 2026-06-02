# zh-Hans Localization Phase 128

Date: 2026-06-02

## Scope

Phase 128 selected the narrowest post-RC21 lifecycle fixture integration path.
It reviewed the Agent model/view flow and did not edit source, launch GUI, build
a bundle, generate PNGs, call backend APIs, log in, or mutate account, billing,
cloud, secret, endpoint, or team state.

## Reviewed Anchors

```text
app/src/ai/ambient_agents/task.rs
app/src/terminal/view/ambient_agent/model.rs
app/src/terminal/view/ambient_agent/view_impl.rs
docs/zh-Hans-local-fixture-implementation-plan-rc20.md
docs/zh-Hans-gui-smoke-matrix.md
```

Existing runtime path:

```text
AmbientAgentEvent::StateChanged
Status::WaitingForSession
AmbientAgentViewModelEvent::ProgressUpdated
render_ambient_agent_progress()
progress.setup_status_text()
```

The path can render lifecycle progress in GUI, but it depends on a real
`WaitingForSession` model state and view-model event handling. Driving that path
would require extra UI-adjacent state setup and cleanup beyond the current
RC21 helper.

## Decision

```text
chosen path: Option A, model-only fixture probe
implementation target: app/src/ai/ambient_agents/task.rs
GUI row promotion: none
public-RC registry change: none
```

Option A is selected for RC22 because it is the lowest-risk way to make
`WARP_CN_AGENT_LIFECYCLE_SMOKE` observable and testable without starting a real
Agent run, session, server call, or GUI. The probe can expose deterministic
localized lifecycle summaries in debug/test builds and give Phase 130 source
anchors plus unit-test evidence.

## Rejected Alternatives

```text
Option B: debug-only ambient-agent model event seed
status: deferred
reason: useful for future GUI evidence, but it touches WaitingForSession and
  ProgressUpdated state and needs a fresh bundle/GUI pass for real proof.

Option C: debug-only standalone fixture panel or command
status: rejected for RC22
reason: larger UI footprint and easier to drift from the product path.
```

Option B remains the next viable step only after the machine can safely run a
bundle/GUI pass and after a cleanup contract for seeded view-model state is
defined.

## Trigger, Cleanup, And Proof Requirements

```text
trigger: WARP_CN_AGENT_LIFECYCLE_SMOKE=1, true, yes, or on
default behavior: inert
cfg boundary: cfg(any(debug_assertions, test))
fixture data: synthetic lifecycle states and localized labels only
cleanup: no persisted state, no real run, no process state, no backend object
proof: focused Rust tests plus source anchors
evidence label: source-anchor or fixture-prep, not GUI evidence
```

The probe must not read or mutate account, backend, billing, cloud, secret,
endpoint, team, login, token, or workspace state.

## Qualification Review

```text
phase: 128
status: qualified-design-selected
chosen option documented: yes
rejected alternatives documented: yes
trigger and cleanup documented: yes
production behavior change required: no
real account/backend state required: no
GUI promotion allowed in this phase: no
public-RC blockers cleared: none
external operations run: none
```
