# zh-Hans Release Candidate 2026-06-02 RC36

Date: 2026-06-02

## Scope

RC36 covers Phases 260 through 267. It adds row/category filters for missing
evidence actions, Markdown missing-action packet output, RC36 evidence action
package docs, filtered command updates in public-RC runbooks, lane readiness
refresh, low-load heavy validation retry, and the next local-use/public-RC
decision freeze.

RC36 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Packetization

```text
text report: script/zh_public_rc_evidence_report.py
JSON report: script/zh_public_rc_evidence_report.py --json
filtered text missing actions: script/zh_public_rc_evidence_report.py --missing-actions --row-id GUI-SET-05
filtered JSON missing actions: script/zh_public_rc_evidence_report.py --missing-actions-json --category backend_fixture
filtered Markdown packet: script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-05
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC36: 0
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

No blocker was cleared in RC36.

## Heavy Gate And GUI Status

```text
low-load gate: defer-heavy-gate
reason: probe 1 load average exceeds 2.50
cargo check -j 1 -p warp: skipped-with-heat-safety
script/run --dont-open: skipped-with-heat-safety
fresh bundle: not refreshed in RC36
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
public-RC filtered missing-action JSON
public-RC filtered missing-action Markdown
privacy guard
Python localization, public-RC, report, and gate tests: 51 passed
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

RC36 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
