# zh-Hans Release Candidate 2026-06-03 RC38

Date: 2026-06-03

## Scope

RC38 covers Phases 276 through 283. It adds offline redacted evidence candidate
preflight, candidate JSON/Markdown output, candidate tests, RC38 preflight docs,
runbook preflight command refreshes, lane readiness refresh, heat-safe heavy
validation gating, and the next local-use/public-RC decision freeze.

RC38 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Candidate Preflight

```text
candidate helper: script/zh_public_rc_evidence_candidate.py
candidate JSON output: available
candidate Markdown output: available
public-RC rows tracked: 11
queue rows: 11
ready rows: 0
rows promoted in RC38: 0
```

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 100.0%
```

## Public-RC Blocker Registry

```text
total: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

No blocker was cleared in RC38.

## Heavy Gate And GUI Status

```text
low-load gate: run-heavy-gate
cargo check -j 1 -p warp: passed with existing unused-variable warnings
script/run --dont-open: passed with existing unused-variable warnings
fresh bundle: refreshed in RC38
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
public-RC evidence JSON report
public-RC prioritized queue JSON
public-RC candidate preflight tests
privacy guard
Python localization, public-RC, report, queue, candidate, lint, and gate tests: 63 passed
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

RC38 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
