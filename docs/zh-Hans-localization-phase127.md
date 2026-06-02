# zh-Hans Localization Phase 127

Date: 2026-06-02

## Scope

Phase 127 reviewed the dirty RC21 branch before adding any post-RC21 source or
evidence work. It did not edit manifest entries, launch GUI, build a bundle,
generate PNGs, log in, call backend APIs, create billing/cloud state, touch
managed secrets/endpoints, or mutate team state.

## Branch Review

```text
branch: codex/zh-Hans-post-rc20-execution
dirty tracked files: README.md, app/src/ai/ambient_agents/task.rs,
  app/src/ai/ambient_agents/task_tests.rs, docs/zh-Hans-gui-smoke-matrix.md,
  docs/zh-Hans-localization.md, docs/zh-Hans-public-rc-gate-runbook.md
new RC21 docs: docs/zh-Hans-localization-phase119.md through
  docs/zh-Hans-localization-phase126.md,
  docs/zh-Hans-release-candidate-2026-06-02-rc21.md
diff stat: 6 tracked files changed, 155 insertions, 8 deletions
AGENTS.md found: none
```

The RC21 diff remains scoped to documentation plus the debug/test-only Agent
lifecycle fixture seed helper and focused tests. No broad source translation
harvest or asset change was present.

## Public-RC Claim Review

```text
RC21 decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
fixture GUI rows promoted by RC21: none
public-RC blockers cleared by RC21: none
```

The reviewed RC21 docs keep fixture evidence separate from public-RC evidence.
`GUI-AGENT-03` remains `needs-trigger`, and the blocker registry still requires
real isolated-account, backend-fixture, and disposable-object evidence before
any public-RC promotion.

## Fixture Boundary Review

```text
cfg boundary: cfg(any(debug_assertions, test))
env gate: WARP_CN_AGENT_LIFECYCLE_SMOKE
default behavior: inert
truthy values: 1, true, yes, on
GUI promotion: none
real account/backend/billing/cloud/secret/endpoint/team state: not used
```

The helper exposes synthetic lifecycle states only when the opt-in debug/test
environment value is truthy. The tests verify the helper is inert for unset,
empty, `0`, and `false` values, and that the seeded labels stay localized.

## Low-Load Gates

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

nice -n 10 python3 script/zh_public_rc_status.py
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3

git diff --check
result: passed
```

## Qualification Review

```text
phase: 127
status: qualified-branch-stabilized
RC21 branch reviewed before new implementation: yes
public-RC overclaim found: no
fixture boundary issue found: no
manifest validation: passed
glossary: passed
dry-run: would_change 0, missing 0
public-RC blockers unchanged: 11
diff whitespace check: passed
external operations run: none
```
