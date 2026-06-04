# zh-Hans Release Candidate 2026-06-02 RC37

Date: 2026-06-02

## Scope

RC37 covers Phases 268 through 275. It adds a prioritized public-RC evidence
queue helper, JSON and Markdown queue renderers, queue-specific tests, RC37
queue documentation, runbook queue-command refreshes, lane readiness refresh,
heat-safe heavy validation gating, and the next local-use/public-RC decision
freeze.

RC37 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Queue

```text
queue helper: script/zh_public_rc_evidence_queue.py
full JSON queue: script/zh_public_rc_evidence_queue.py --json
scoped JSON queue: script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
backend Markdown queue: script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
public-RC rows tracked: 11
queue rows: 11
ready rows: 0
rows promoted in RC37: 0
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

No blocker was cleared in RC37.

## Heavy Gate And GUI Status

```text
low-load gate: defer-heavy-gate
reason: probe 1 load average exceeds 2.50
cargo check -j 1 -p warp: skipped-with-heat-safety
script/run --dont-open: skipped-with-heat-safety
fresh bundle: not refreshed in RC37
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
public-RC row-scoped missing-action JSON
public-RC backend missing-action Markdown
public-RC prioritized queue JSON
public-RC row-scoped queue JSON
public-RC backend queue Markdown
privacy guard
Python localization, public-RC, report, queue, lint, and gate tests: 56 passed
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

RC37 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
