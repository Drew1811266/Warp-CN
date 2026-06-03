# zh-Hans Release Candidate 2026-06-02 RC32

Date: 2026-06-02

## Scope

RC32 covers Phases 228 through 235. It adds structured public-RC evidence
intake linting, documents evidence metadata rules, reclassifies backend,
isolated-account, disposable-object, asset, heavy validation, and GUI readiness,
and freezes the next local-use/public-RC decision.

RC32 does not add manifest translations, change PNG assets, produce GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Intake

```text
evidence ledger: resources/localization/zh-Hans-public-rc-evidence.toml
evidence linter: script/zh_public_rc_evidence_lint.py
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC32: 0
evidence linter exit code: 1
evidence linter decision: fail
```

The linter failure is expected for RC32 because all 11 rows remain marked as
missing evidence. It is a blocker signal, not a validation crash.

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context/status coverage: 100.0%
release: covered 8574, candidates 2, coverage 100.0%
```

Remaining source candidates are still intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Public-RC Blocker Registry

```text
registry: resources/localization/zh-Hans-public-rc-blockers.toml
script: script/zh_public_rc_status.py
total: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

No blocker was cleared in RC32.

## Heavy Gate And GUI Status

Phase 234 ran the helper with two probes:

```text
probe 1: load=3.75 3.54 3.02
probe 1: hot_process=WindowServer 44.7%
probe 2: load=4.99 3.88 3.17
probe 2: hot_process=mds_stores 124.0%
probe 2: hot_process=WindowServer 45.0%
decision: defer-heavy-gate
```

Decision:

```text
Rust compile: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
bundle build: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```

## PNG Asset Status

```text
onboarding PNG total: 54
current branch PNG changes: none
deferred asset count: 50
accepted decorative/brand asset count: 4
asset branch: deferred
decision: blocked-no-asset-approval
```

## Command-Line Gates

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
release inventory coverage
public-RC blocker summary
privacy guard
Python localization, public-RC, and gate tests: 35 passed
cargo fmt --check
git diff --check
```

Expected blocker signal:

```text
python3 script/zh_public_rc_evidence_lint.py
exit_code: 1
decision: fail
reason: 11 rows still missing evidence
```

Skipped for heat-safety:

```text
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC32 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until the evidence linter passes with real
matching evidence, the raw evidence is reviewed, fresh bundle/current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
