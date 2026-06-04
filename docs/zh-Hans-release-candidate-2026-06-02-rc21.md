# zh-Hans Release Candidate 2026-06-02 RC21

Date: 2026-06-02

## Scope

RC21 covers Phases 119 through 126. It adds one debug/test-only local fixture
seed helper for Agent lifecycle status smoke preparation and records the
post-RC20 evidence decisions. It does not add manifest translations, change PNG
assets, produce GUI evidence, build a bundle, log in, create backend fixtures,
touch billing/cloud state, create or delete managed secrets/endpoints, or mutate
team state.

The RC21 delta is:

```text
post-RC20 drift sentinel
heat-safe full compile and bundle decision
no-account GUI smoke decision
debug/test-only Agent lifecycle fixture seed helper
fixture GUI evidence decision
public-RC external-prerequisite handoff
onboarding PNG asset-branch decision
RC21 readiness freeze
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

Coverage remains inherited from RC20 because RC21 did not add source
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

## Fixture Seed Delta

```text
file: app/src/ai/ambient_agents/task.rs
tests: app/src/ai/ambient_agents/task_tests.rs
env gate: WARP_CN_AGENT_LIFECYCLE_SMOKE
scope: debug/test-only local lifecycle status seed helper
default behavior: inert
GUI evidence produced: no
public-RC impact: none
```

Seeded local labels:

```text
排队中
等待中
已分配
进行中
已完成
失败
错误
已阻塞
已取消
```

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

No blocker was cleared in RC21.

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
targeted Rust fixture tests: 2 passed
cargo fmt --check
git diff --check
PNG diff/status check: no PNG changes
```

Skipped or blocked:

```text
full Rust compile: skipped-with-heat-safety
bundle build / GUI launch: skipped-with-heat-safety
PNG regeneration: not approved, no generation
public-RC external evidence: blocked-no-prerequisites
```

## Static Visual Asset Status

```text
current branch PNG changes: none
PNG generation: not run
future asset branch: codex/zh-Hans-onboarding-assets-rc20
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc20.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration, design
approval, before/after contact sheets, binary scope proof, and visual QA.

## Low-Load Review

All validation commands were run serially. The targeted Rust test used
`CARGO_BUILD_JOBS=1`, `-j 1`, and `nice -n 15`. Full Rust compile, bundle, GUI,
account, backend, billing, cloud, managed-secret, endpoint, team, and PNG
generation workflows were not run because this goal prioritized heat-safe local
execution.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC21 is acceptable for local use and continued fixture development. It is not
acceptable as public RC until full Rust compile and bundle can run safely,
current-cycle GUI evidence is complete, isolated account evidence is complete,
backend/disposable fixture evidence is complete, and onboarding PNG visual
evidence is regenerated or design-approved.
