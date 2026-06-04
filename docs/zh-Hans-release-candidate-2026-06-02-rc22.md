# zh-Hans Release Candidate 2026-06-02 RC22

Date: 2026-06-02

## Scope

RC22 covers Phases 127 through 134. It reviews and stabilizes the dirty RC21
branch, chooses a model-only integration path for the Agent lifecycle fixture,
adds a debug/test-only lifecycle probe, packages no-GUI fixture evidence,
refreshes public-RC prerequisites, rechecks onboarding PNG approval, and freezes
the next readiness decision.

RC22 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, or mutate team state.

The RC22 delta is:

```text
RC21 branch review and low-load stabilization
model-only lifecycle fixture integration design
debug/test-only Agent lifecycle fixture probe
no-GUI source-anchor evidence package
heat-safe GUI/bundle reattempt decision
public-RC prerequisite recheck
onboarding PNG approval recheck
RC22 readiness freeze
```

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context/status: 7943 (100.0%)
```

Coverage remains inherited from RC21/RC20 because RC22 did not add source
translation entries:

```text
onboarding: covered 323, candidates 0, coverage 100.0%
workspace: covered 865, candidates 0, coverage 100.0%
search: covered 269, candidates 0, coverage 100.0%
settings: covered 2024, candidates 0, coverage 100.0%
modals: covered 5240, candidates 2, coverage 100.0%
release: covered 8574, candidates 2, coverage 100.0%
terminal: covered 2178, candidates 1, coverage 100.0%
AI / Agent: covered 2515, candidates 1, coverage 100.0%
```

Remaining source candidates are intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Fixture Probe Delta

```text
file: app/src/ai/ambient_agents/task.rs
tests: app/src/ai/ambient_agents/task_tests.rs
env gate: WARP_CN_AGENT_LIFECYCLE_SMOKE
scope: debug/test-only local lifecycle model probe
default behavior: inert
GUI evidence produced: no
public-RC impact: none
```

Probe fields:

```text
state_query_param
label
is_working
is_terminal
is_failure_like
```

Seeded local labels:

```text
QUEUED: 排队中
PENDING: 等待中
CLAIMED: 已分配
INPROGRESS: 进行中
SUCCEEDED: 已完成
FAILED: 失败
ERROR: 错误
BLOCKED: 已阻塞
CANCELLED: 已取消
```

This is source-anchor and fixture-prep evidence only. `GUI-AGENT-03` remains
`needs-trigger` until a future safe GUI or accessibility pass verifies rendered
lifecycle labels.

## Public-RC Blocker Registry

```text
registry: resources/localization/zh-Hans-public-rc-blockers.toml
script: script/zh_public_rc_status.py
```

Summary:

```text
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
backend_fixture: 5
disposable_object: 3
isolated_account: 3
```

No blocker was cleared in RC22.

## Command-Line Gate Results

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
public-RC blocker summary
JSON locale export
JSON parse
YAML locale export
Python compile checks
Python localization tests: 25 passed
targeted Rust fixture tests: 4 passed
cargo fmt --check
git diff --check
PNG diff/status check: no PNG changes
```

Skipped or blocked:

```text
full Rust compile: skipped-with-heat-safety
bundle build / GUI launch: skipped-with-heat-safety
PNG regeneration: blocked-no-asset-approval
public-RC external evidence: blocked-no-prerequisites
```

## Static Visual Asset Status

```text
current branch PNG changes: none
PNG generation: not run
future asset branch: codex/zh-Hans-onboarding-assets-rc20
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc20.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration,
design/product approval, before/after contact sheets, binary scope proof, and
visual QA.

## Low-Load Review

All validation commands were run serially. The targeted Rust test used
`CARGO_BUILD_JOBS=1`, `-j 1`, and `nice -n 15`. Phase 131 skipped full compile,
bundle, and GUI because the machine already showed elevated desktop/Codex CPU
usage and load averages despite no macOS thermal warning.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC22 is acceptable for local use and continued fixture development. It is not
acceptable as public RC until full Rust compile and bundle can run safely,
current-cycle GUI evidence is complete, isolated account evidence is complete,
backend/disposable fixture evidence is complete, and onboarding PNG visual
evidence is regenerated or design-approved.
