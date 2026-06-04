# zh-Hans Localization Phase 153

Date: 2026-06-02

## Scope

Phase 153 reviewed the RC24 branch baseline and reran the low-load drift
sentinel before any compile, bundle, GUI, fixture, asset, account, backend,
billing, cloud, secret, endpoint, or team work.

## Branch Review

```text
branch: codex/zh-Hans-post-rc20-execution
tracked dirty files: README.md, app/src/ai/ambient_agents/task.rs,
  app/src/ai/ambient_agents/task_tests.rs, docs/zh-Hans-gui-smoke-matrix.md,
  docs/zh-Hans-localization.md, docs/zh-Hans-public-rc-gate-runbook.md
new RC docs present: docs/zh-Hans-localization-phase119.md through
  docs/zh-Hans-localization-phase152.md,
  docs/zh-Hans-release-candidate-2026-06-02-rc21.md through
  docs/zh-Hans-release-candidate-2026-06-02-rc24.md
diff stat: 6 tracked files changed, 488 insertions, 18 deletions
```

`README.md`, `docs/zh-Hans-localization.md`, and
`docs/zh-Hans-release-candidate-2026-06-02-rc24.md` all point to RC24 as the
current record and keep public RC as `not ready`.

## Low-Load Baseline Gates

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
result: manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
result: glossary check passed

nice -n 10 python3 script/zh_apply_localization.py --metadata-summary
entries: 7943
key: 150 (1.9%)
context: 7943 (100.0%)
status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
notes: 0 (0.0%)
expected_count: 195 (2.5%)

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

## Drift Sentinel

```text
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
preset: release
covered: 8574
candidates: 2
coverage: 100.0%

nice -n 10 python3 script/zh_localization_inventory.py --coverage app/src/terminal
preset: custom
covered: 2178
candidates: 1
coverage: 100.0%

nice -n 10 python3 script/zh_localization_inventory.py --coverage app/src/ai
preset: custom
covered: 2515
candidates: 1
coverage: 100.0%
```

The counts match the RC24 baseline. No new unexpected source drift was found,
so no narrow translation slice is needed before heavy-gate work.

## Qualification Review

```text
phase: 153
status: qualified-rc24-baseline-stable
RC24 current record confirmed: yes
public-RC overclaim found: no
manifest validation: passed
glossary: passed
dry-run: would_change 0, missing 0
public-RC blockers unchanged: 11
drift sentinel changed from RC24 baseline: no
diff whitespace check: passed
external operations run: none
continue to Phase 154: yes
```
