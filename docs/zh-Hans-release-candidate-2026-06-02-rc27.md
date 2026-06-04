# zh-Hans Release Candidate 2026-06-02 RC27

Date: 2026-06-02

## Scope

RC27 covers Phases 177 through 186. It confirms the RC26 baseline, reruns the
source drift and release inventory gates, records heat-safe bundle and GUI
skips, rechecks all public-RC external prerequisite lanes, verifies the Agent
lifecycle source harness, rechecks onboarding PNG approval status, confirms
upstream stable freshness, runs a low-concurrency Rust compile gate, and freezes
the next readiness decision.

RC27 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, or mutate team state.

The RC27 delta is:

```text
RC26 baseline and drift confirmation
fresh bundle gate skipped under heat-safety rules
no-account GUI smoke skipped because no fresh bundle exists
isolated-account public-RC lane blocked
backend-fixture public-RC lane blocked
disposable-object public-RC lane blocked
Agent lifecycle source harness verified by targeted Rust tests
onboarding PNG asset approval gate rechecked
upstream latest stable freshness confirmed
low-concurrency Rust compile passed
RC27 readiness freeze
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

Coverage remains inherited from RC26 because RC27 did not add source
translation entries:

```text
release: covered 8574, candidates 2, coverage 100.0%
```

Remaining source candidates are intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Heat-Safe Bundle And GUI Status

Phase 178 ran two probes with a 60-second cooling interval. No macOS thermal or
performance warning was found, but the desktop process mix remained active
enough that a fresh bundle build was not run.

```text
probe 1 load: 3.96 3.34 2.80
probe 2 load: 2.77 3.09 2.75
bundle build: skipped-with-heat-safety
```

Phase 179 checked the existing app bundle and found only a historical bundle.
It was not used for RC27 promotion.

```text
existing bundle: target/debug/bundle/osx/WarpOss.app
mtime: Jun 1 21:53:26 2026
no-account GUI smoke: skipped-no-fresh-bundle
```

## Agent Lifecycle Fixture

Phase 183 verified the debug/test-only Agent lifecycle source harness with
targeted Rust tests.

```text
command: CARGO_BUILD_JOBS=1 cargo test -j 1 -p warp lifecycle_smoke_fixture -- --nocapture
result: 4 passed, 0 failed, 4715 filtered out
duration: 35.35s
labels: 排队中, 等待中, 已分配, 进行中, 已完成, 失败, 错误, 已阻塞, 已取消
GUI-AGENT-03 status: needs-trigger
public-RC impact: none
```

The source harness is valid evidence that localized lifecycle labels are seeded
deterministically, but it does not replace current-cycle rendered GUI evidence.

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

No blocker was cleared in RC27. No account, backend, billing, cloud, managed
secret, custom endpoint, disposable object, or team state was read or mutated.

## Static Visual Asset Status

```text
current branch PNG changes: none
PNG generation: not run
onboarding PNG total: 54
future asset branch: codex/zh-Hans-onboarding-assets-rc20
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc20.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration,
design/product approval, before/after contact sheets, binary scope proof, and
visual QA.

## Upstream Freshness

Phase 185 attempted to refresh upstream refs and checked the latest stable tag.

```text
git fetch origin --tags: exit code 1
reason: existing tag conflicts rejected with "would clobber existing tag"
forced tag overwrite: not attempted
latest remote stable tag: v0.2026.05.27.09.22.stable_00
latest stable commit: 7ed8bbd5dbf701c453ce90a6961f4e6dbcc8d6b4
current branch contains latest stable: yes
origin/master after fetch: ac4225c1805811a46bfa9df7531e6a4f0058ab12
```

There is no newer stable tag to adopt. `origin/master` has advanced, but it is
treated as preflight information rather than the release baseline.

## Command-Line Gate Results

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
release inventory coverage
public-RC blocker summary
Python localization tests: 25 passed
cargo fmt --check
git diff --check
privacy guard
low-concurrency Rust compile: CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

Targeted fixture evidence:

```text
Agent lifecycle source harness tests: 4 passed, 0 failed, 4715 filtered out
```

Skipped or blocked:

```text
bundle build: skipped-with-heat-safety
no-account GUI smoke: skipped-no-fresh-bundle
isolated account evidence: blocked-no-isolated-account
backend fixture evidence: blocked-no-backend-fixture
disposable object evidence: blocked-no-disposable-object
PNG regeneration: blocked-no-asset-approval
tag refresh: partial fetch only; conflicting tags not force-updated
```

## Low-Load Review

All validation commands were run serially. Rust compile was run with
`CARGO_BUILD_JOBS=1` and `-j 1`. Bundle build and GUI launch were not run after
the heat-safety decision because they are the two highest-risk local load
operations for this cycle.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC27 is acceptable for local use and continued fixture/evidence development. It
is not acceptable as a public RC until a fresh bundle can be built safely,
current-cycle GUI evidence is complete, isolated account evidence is complete,
backend/disposable fixture evidence is complete, and onboarding PNG visual
evidence is regenerated or design-approved.
