# zh-Hans Release Candidate 2026-06-02 RC34

Date: 2026-06-02

## Scope

RC34 covers Phases 244 through 251. It adds row-level missing-action evidence
output, positive-path strict artifact regression coverage, RC34 evidence action
and lane readiness packages, asset/GUI dependency refresh, low-load heavy
validation retry, and the next local-use/public-RC decision freeze.

RC34 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Readiness

```text
evidence report: script/zh_public_rc_evidence_report.py
missing-action report: script/zh_public_rc_evidence_report.py --missing-actions
strict evidence linter: script/zh_public_rc_evidence_lint.py --strict-artifacts
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC34: 0
```

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

## Public-RC Blocker Registry

```text
registry: resources/localization/zh-Hans-public-rc-blockers.toml
script: script/zh_public_rc_status.py
total: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

No blocker was cleared in RC34.

## Heavy Gate And GUI Status

Phase 250 ran the helper with two probes:

```text
probe 1: load=2.17 2.42 2.66
probe 1: hot_process=WindowServer 44.0%
probe 2: load=2.10 2.35 2.61
probe 2: hot_process=WindowServer 44.7%
probe 2: hot_process=Codex (Service) 33.6%
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
current branch PNG changes: none
asset lane: blocked-no-asset-approval
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
public-RC evidence report
public-RC missing-action report
privacy guard
Python localization, public-RC, report, and gate tests: 43 passed
cargo fmt --check
git diff --check
```

Expected blocker signal:

```text
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
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

RC34 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, fresh bundle/current-cycle
GUI evidence exists, onboarding PNG visual status is approved or regenerated,
and publication is explicitly approved by the user.
