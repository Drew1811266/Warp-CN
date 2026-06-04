# zh-Hans Localization Phase 129

Date: 2026-06-02

## Scope

Phase 129 implemented the Phase 128 model-only fixture probe. It did not wire
the fixture into GUI, start a real Agent run, spawn tasks, call server APIs,
log in, read credentials, create billing/cloud/backend state, touch managed
secrets/endpoints, mutate team state, build a bundle, generate PNGs, or launch
GUI.

## Source Changes

```text
app/src/ai/ambient_agents/task.rs
app/src/ai/ambient_agents/task_tests.rs
```

Added debug/test-only probe data:

```text
AmbientAgentLifecycleSmokeFixtureProbe
state_query_param
label
is_working
is_terminal
is_failure_like
```

The probe reuses `AmbientAgentTaskState::as_query_param()`,
`is_working()`, `is_terminal()`, `is_failure_like()`, and `Display` instead of
duplicating lifecycle semantics.

## Fixture Boundary

```text
cfg boundary: cfg(any(debug_assertions, test))
env gate: WARP_CN_AGENT_LIFECYCLE_SMOKE
truthy values: 1, true, yes, on
default behavior: inert
fixture state: synthetic only
persisted state: none
GUI integration: none
public-RC registry change: none
```

The implementation remains a source/model probe. It can support no-GUI fixture
evidence, but it cannot mark `GUI-AGENT-03` as `fixture-verified` without a
future GUI or accessibility evidence pass.

## Verification

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
result: manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
result: glossary check passed

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0

nice -n 10 cargo fmt --check
result: passed after running rustfmt formatting

git diff --check
result: passed

CARGO_BUILD_JOBS=1 nice -n 15 cargo test -j 1 -p warp lifecycle_smoke_fixture -- --nocapture
result: 4 tests passed, 0 failed, 4715 filtered out
compile mode: single-job, nice priority
duration: 2m 58s
```

The Rust command emitted existing app crate warnings unrelated to this fixture
slice.

## Tested Cases

```text
env unset: no fixture states
env false-like: no fixture states
env truthy: deterministic lifecycle state order
localized labels: 排队中, 等待中, 已分配, 进行中, 已完成, 失败, 错误,
  已阻塞, 已取消
status metadata: query param, working, terminal, failure-like flags
```

## Qualification Review

```text
phase: 129
status: qualified-fixture-probe-implemented
debug/test-only boundary preserved: yes
default behavior inert: yes
real Agent run started: no
server/API/account/backend operations: none
billing/cloud/secret/endpoint/team operations: none
targeted Rust tests: passed
manifest/glossary/dry-run gates: passed
format and whitespace gates: passed
GUI row promoted: none
public-RC blockers cleared: none
```
