# zh-Hans Localization Phase 138

Date: 2026-06-02

## Scope

Phase 138 reviewed whether `WARP_CN_AGENT_LIFECYCLE_SMOKE` can be connected to
a rendered GUI or accessibility path. It did not edit source, launch GUI, build
a bundle, start a real Agent run, call backend APIs, log in, read credentials,
or touch account, billing, cloud, secret, endpoint, or team state.

## Reviewed Anchors

```text
app/src/ai/ambient_agents/task.rs
app/src/ai/ambient_agents/task_tests.rs
app/src/terminal/view/ambient_agent/model.rs
app/src/terminal/view/ambient_agent/view_impl.rs
docs/zh-Hans-local-fixture-implementation-plan-rc20.md
docs/zh-Hans-gui-smoke-matrix.md
```

Current model/view runtime path:

```text
AmbientAgentEvent::StateChanged
Status::WaitingForSession
AmbientAgentViewModelEvent::ProgressUpdated
render_ambient_agent_progress()
progress.setup_status_text()
```

The RC22 model probe remains safe and deterministic, but the rendered GUI path
still depends on `WaitingForSession` model state and view-model event handling.
Driving that path would require a fresh bundle/GUI run or a carefully isolated
render harness.

## Decision

```text
chosen option: Option A, keep source-anchor only
source changes in this phase: none
GUI promotion: none
public-RC registry change: none
```

Reasons:

```text
fresh Phase 136 bundle available: no
Phase 137 GUI launch: skipped-no-fresh-bundle
secondary heat/load status: elevated
Option B risk: touches WaitingForSession and ProgressUpdated state
Option C risk: no existing safe render harness was proven in this phase
```

Option B remains a future candidate only after a fresh bundle/GUI or existing
render harness can be safely used and after deterministic cleanup is defined.

## Trigger, Cleanup, And Proof Requirements For Future Work

```text
trigger: WARP_CN_AGENT_LIFECYCLE_SMOKE=1, true, yes, or on
default behavior: inert
cfg boundary: cfg(any(debug_assertions, test))
fixture data: synthetic lifecycle states and localized labels only
cleanup: no persisted state, no real run, no backend object
proof needed for GUI-AGENT-03: accessibility anchors or cropped/redacted GUI
  evidence showing rendered lifecycle labels
```

## Qualification Review

```text
phase: 138
status: qualified-source-anchor-only
chosen option documented: yes
rejected alternatives documented: yes
real account/backend state required: no
production behavior change required: no
GUI row promoted: none
public-RC blockers cleared: none
external operations run: none
```
