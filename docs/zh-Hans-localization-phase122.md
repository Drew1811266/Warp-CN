# zh-Hans Localization Phase 122

Date: 2026-06-02

## Scope

Phase 122 implemented the first debug-only local fixture slice for the
post-RC20 plan: `agent-lifecycle-states-fixture`. It did not launch GUI,
generate screenshots, build a bundle, log in, read credentials, call backend
APIs, create cloud objects, mutate billing/quota state, touch managed secrets,
create or delete endpoints, or mutate team state.

## Source Changes

```text
app/src/ai/ambient_agents/task.rs
app/src/ai/ambient_agents/task_tests.rs
```

The implementation adds a debug/test-only fixture helper gated by:

```text
WARP_CN_AGENT_LIFECYCLE_SMOKE=1
```

Default behavior is inert:

```text
env var unset: no fixture states
env var empty/0/false: no fixture states
env var 1/true/yes/on: seed local lifecycle states
```

Seeded states and labels:

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
```

The helper is compiled only under `debug_assertions` or tests. It is a local
seed description layer only; Phase 122 does not wire it into GUI rendering or
mark GUI evidence as verified.

## Validation

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
result: passed after applying cargo fmt

git diff --check
result: passed
```

Targeted Rust test:

```text
CARGO_BUILD_JOBS=1 nice -n 15 cargo test -j 1 -p warp lifecycle_smoke_fixture -- --nocapture
result: passed
tests: 2 passed, 0 failed, 4715 filtered out
compile mode: single-job, nice priority
warnings: existing app crate warnings unrelated to the fixture slice
```

## Qualification Review

```text
phase: 122
status: qualified-fixture-slice
fixture lane implemented: agent-lifecycle-states-fixture
fixture gate: WARP_CN_AGENT_LIFECYCLE_SMOKE
default behavior inert: yes
debug/test-only boundary: yes
real credentials read: no
account/backend/billing/cloud/secret/endpoint/team state touched: no
Python localization gates: passed
format and whitespace gates: passed
targeted Rust tests: passed
GUI evidence produced: no
public-RC blockers cleared: none
```
