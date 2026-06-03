# zh-Hans Localization Phase 183

Date: 2026-06-02

## Scope

Phase 183 evaluates the Agent lifecycle evidence lane for `GUI-AGENT-03`.

This phase performs source and targeted Rust-test verification only. It does not
launch GUI, build a bundle, log in, touch backend/account state, mutate Agent
service state, or create fixture data outside the existing debug/test-only
helpers.

## Source Review

Relevant source anchors:

```text
app/src/ai/ambient_agents/task.rs
app/src/ai/ambient_agents/task_tests.rs
app/src/terminal/view/ambient_agent/model.rs
app/src/terminal/view/ambient_agent/view_impl.rs
```

`AmbientAgentTaskState` currently renders localized display labels:

```text
Queued: 排队中
Pending: 等待中
Claimed: 已分配
InProgress: 进行中
Succeeded: 已完成
Failed: 失败
Error: 错误
Blocked: 已阻塞
Cancelled: 已取消
Unknown: 失败
```

The debug/test-only fixture gate remains:

```text
WARP_CN_AGENT_LIFECYCLE_SMOKE
```

It is inert unless set to a truthy value.

## Targeted Test

Command:

```bash
CARGO_BUILD_JOBS=1 cargo test -j 1 -p warp lifecycle_smoke_fixture -- --nocapture
```

Result:

```text
Finished test profile target(s) in 35.35s
tests: 4 passed, 0 failed, 4715 filtered out
warnings: 46 existing unused-variable warnings
```

Passed tests:

```text
lifecycle_smoke_fixture_probe_is_inert_without_truthy_env_value
lifecycle_smoke_fixture_is_inert_without_truthy_env_value
lifecycle_smoke_fixture_probe_exposes_deterministic_status_metadata
lifecycle_smoke_fixture_seeds_all_localized_status_labels
```

## Decision

```text
decision: source-harness-verified
GUI evidence produced: no
GUI-AGENT-03 matrix status: remains needs-trigger
public-RC impact: none
source changes made: none
```

The existing source-only fixture proves the localized lifecycle state labels and
the inert default behavior. It does not provide rendered GUI or accessibility
evidence, so it cannot promote `GUI-AGENT-03` to `verified`.

## Review

Phase 183 is accepted.

Acceptance review:

```text
source anchors reviewed: yes
targeted Rust tests run: yes
localized lifecycle labels covered: yes
fixture default inert: yes
GUI row overpromotion avoided: yes
safe to continue to Phase 184 onboarding PNG asset lane: yes
```
