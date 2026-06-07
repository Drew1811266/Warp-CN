# zh-Hans Calibration Cycle 2026-06-05

This cycle executes the low-load portion of
`docs/superpowers/plans/2026-06-05-zh-Hans-localization-calibration-implementation-plan.md`.
It does not run Rust/Cargo, bundle build, app launch, GUI automation, runtime
logs, account state, billing state, cloud state, secrets, endpoints, or team
ownership work.

## Snapshot

| Item | Value |
| --- | --- |
| Branch | `codex/zh-Hans-post-rc26-execution` |
| Worktree state | Dirty before execution; unrelated user changes preserved |
| Manifest entries | 7,943 |
| Covered source files | 552 |
| Already applied entries | 5,690 |
| Dry-run would_change | 0 |
| Dry-run missing | 0 |
| Existing public-RC blockers | 11 |
| High-load policy | `skipped-by-heat-safety-policy` |

## Generated Artifacts

| Artifact | Purpose |
| --- | --- |
| `audit-summary.md` | Full audit aggregate summary preserved from the audit generator. |
| `entries.json` | 7,943-row enhanced machine-readable audit ledger. |
| `entries.tsv` | 7,943-row tabular audit ledger. |
| `module-matrix.md` | Module-level calibration aggregation. |
| `copy-review-findings.md` | Copy and machine-translation review queues. |
| `functional-risk-findings.md` | Placeholder, source-state, command, protocol, and public-RC risk queues. |
| `mojibake-and-layout-findings.md` | Static mojibake and layout-risk scan. |
| `performance-probe.md` | Low-load performance boundary and high-load deferral record. |
| `public-rc-blocker-status.md` | Missing public-RC evidence action list. |
| `gui-smoke-deferred.md` | Explicit GUI deferral and future accessibility-anchor checklist. |
| `high-load-gate-2026-06-05.md` | User-approved high-load request gate result. |
| `task7-copy-lane-review.md` | Task 7 copy-lane review result. |
| `task7-copy-lane-decisions.tsv` | 2,251-row copy-lane decision ledger. |
| `task8-functional-risk-review.md` | Task 8 functional-risk review result. |
| `task8-functional-risk-decisions.tsv` | 7,943-row functional-risk decision ledger. |
| `task9-mojibake-layout-gui-review.md` | Task 9 static mojibake/layout and GUI gate result. |
| `interface-localization-check.md` | Static internal-interface localization check and GUI gate boundary. |

## Audit Results

| Metric | Result |
| --- | ---: |
| Rows reviewed | 7,943 |
| `simulated-accepted` | 1,774 |
| `simulated-accepted-with-note` | 5,139 |
| `blocked-public-rc` | 1,030 |
| `needs-copy-review` | 0 |
| `needs-functional-review` | 0 |
| `mojibake_status=clean` | 7,943 |
| `ui_density_risk=clean` | 7,943 |

Review lane counts:

| Lane | Rows |
| --- | ---: |
| `accepted` | 4,938 |
| `copy` | 2,125 |
| `functional` | 130 |
| `public-rc` | 750 |

Machine copy score counts:

| Score | Rows | Meaning |
| ---: | ---: | --- |
| 1 | 2,251 | Note-worthy review queue, mostly English-preserved or copy notes. |
| 2 | 5,692 | Source-level copy accepted. |

## Mojibake And Layout

Static scan result:

```text
total findings: 6
actionable findings: 0
```

The remaining findings are classified as:

- `accepted-token`: terminal ANSI escape sequence in bootstrap text.
- `fixture-only`: editor test data intentionally containing U+FFFD examples.
- `example-only`: documentation examples in the calibration plan.

No product-text mojibake finding was produced in this low-load static scan.

## Public-RC Status

Public-RC remains blocked:

| Category | Count |
| --- | ---: |
| `backend_fixture` | 5 |
| `disposable_object` | 3 |
| `isolated_account` | 3 |

No blocker row was promoted. No account, backend fixture, billing state, cloud
object, secret, endpoint, or team state was touched.

## Commands Run

| Command | Result |
| --- | --- |
| `python3 script/privacy_guard.py --all-tracked` | passed |
| `python3 script/zh_apply_localization.py --validate-manifest` | `manifest validation passed` |
| `python3 script/zh_apply_localization.py --check-glossary` | `glossary check passed` |
| `python3 script/zh_apply_localization.py --metadata-summary` | `entries: 7943`, `context: 100.0%`, `status: 100.0%` |
| `python3 script/zh_apply_localization.py --dry-run --summary` | `would_change: 0`, `missing: 0` |
| `python3 script/zh_full_translation_audit.py --fail-on-actionable --output-dir docs/zh-Hans-calibration-cycles/2026-06-05` | passed, 7,943 rows |
| `python3 script/zh_module_calibration_report.py ...` | passed, 11 module groups |
| `python3 script/zh_mojibake_scan.py --markdown` | passed, 0 actionable product findings |
| `python3 script/zh_performance_probe.py --record-high-load-skipped ...` | passed |
| `python3 script/zh_public_rc_evidence_report.py --missing-actions` | passed |
| `python3 -m json.tool docs/zh-Hans-calibration-cycles/2026-06-05/entries.json` | passed |
| `python3 -m py_compile ...` | passed |
| `python3 -m unittest ...` | 79 tests passed |
| Task 7/8 TSV row count check | `task7=2251`, `task8=7943` |
| Cycle UTF-8 and trailing-whitespace check | passed |
| Current Task 7-9 focused `python3 -m unittest ...` rerun | 34 tests passed |
| `git diff --check` | passed |
| `python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25` | `defer-heavy-gate`; load and hot process thresholds exceeded |

## Task 7-9 Review Result

| Task | Result |
| --- | --- |
| Task 7 copy lane | 2,251 copy-note rows classified; no confirmed machine-translation defect; no manifest edit. |
| Task 8 functional risk | 7,943 rows classified; no confirmed token break; 1 `<cancelled>` token note accepted as display translation; no manifest edit. |
| Task 9 mojibake/layout/GUI | Static mojibake/layout clean for product text; GUI not run because high-load gate deferred. |

## High-Load Gate Result

The user approved a high-load validation window, so the heat/load gate was run.
It returned `defer-heavy-gate`:

```text
probe 1: load=2.88 2.77 3.19
probe 1: hot_process=WindowServer 35.4%
probe 2: load=2.75 2.75 3.15
probe 2: hot_process=WindowServer 38.7%
probe 2: hot_process=Codex (Service) 34.5%
decision: defer-heavy-gate
```

Because the gate failed, Rust/Cargo, runtime, app launch, GUI automation, and
runtime log probes were not run in this cycle.

## Explicitly Not Run

These were skipped to avoid high CPU load, heat, and GUI/runtime pressure:

- `cargo fmt --check`
- `cargo check`
- Bundle build.
- `./script/run`
- Opening `WarpOss.app`.
- GUI automation.
- Runtime logs.
- Public-RC evidence collection that requires account, backend, billing, cloud,
  secret, endpoint, or team state.

## Final Decision

```text
source-level calibration: passed
copy quality: passed source-level review with owner-review queues
functional safety: passed source-level review; no confirmed token break
mojibake-layout: passed static scan, 0 product actionable findings
performance: low-load script execution only; high-load runtime gate deferred
GUI readiness: incomplete / gate-blocked
public-RC readiness: blocked with 11 rows
```

## Next Actions

1. Review `copy-review-findings.md` for note-only English-preserved and wording
   queues before changing any manifest target.
2. Review `functional-risk-findings.md` source-state rows and public-RC
   evidence-gated rows separately.
3. Re-run the high-load gate during a lower-temperature window before Rust,
   Cargo, runtime, or GUI checks.
4. Keep public-RC blocked until isolated account, backend fixture, disposable
   object evidence, cleanup proof, and strict artifact lint are all available.
