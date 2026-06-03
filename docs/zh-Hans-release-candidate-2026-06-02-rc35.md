# zh-Hans Release Candidate 2026-06-02 RC35

Date: 2026-06-02

## Scope

RC35 covers Phases 252 through 259. It adds strict row-specific artifact path
checks, JSON evidence report output, JSON missing-action output, RC35 evidence
automation docs, lane readiness refresh, low-load heavy validation retry, and
the next local-use/public-RC decision freeze.

RC35 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Automation

```text
text report: script/zh_public_rc_evidence_report.py
JSON report: script/zh_public_rc_evidence_report.py --json
text missing actions: script/zh_public_rc_evidence_report.py --missing-actions
JSON missing actions: script/zh_public_rc_evidence_report.py --missing-actions-json
strict evidence linter: script/zh_public_rc_evidence_lint.py --strict-artifacts
row-specific artifact path guard: enabled
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC35: 0
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

No blocker was cleared in RC35.

## Heavy Gate And GUI Status

Phase 258 ran the helper with two probes:

```text
probe 1: load=2.12 2.29 2.47
probe 2: load=1.85 2.22 2.44
decision: run-heavy-gate
```

Decision:

```text
Rust compile: passed
fresh bundle: passed
bundle path: target/debug/bundle/osx/WarpOss.app
GUI launch: not run
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
public-RC evidence text report
public-RC evidence JSON report
public-RC missing-action text report
public-RC missing-action JSON report
privacy guard
Python localization, public-RC, report, and gate tests: 47 passed
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

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC35 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
