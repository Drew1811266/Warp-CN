# Warp CN zh-Hans Development Guide

Last updated: 2026-06-03

This guide is the working entry point for maintaining the Warp CN Simplified
Chinese localization fork. It covers local setup, localization editing,
full-entry review, validation gates, GUI evidence, public-RC blockers, upstream
sync, and release handoff.

## Current Baseline

| Item | Value |
| --- | --- |
| Project version | `0.18` |
| Current conclusion | `ready-for-local-use-with-fixture-evidence` |
| Manifest | `resources/localization/zh-Hans-overrides.toml` |
| Manifest entries | 7,943 |
| Covered source files | 552 |
| Applied entries | 5,690 |
| Pending apply changes | 0 |
| Missing or drifted entries | 0 |
| Public-RC blockers | 11 |

Important boundary:

- The fork is suitable for local engineering use and continued verification.
- It is not a Warp official Chinese release.
- It is not public-RC ready until GUI evidence, isolated-account evidence,
  backend fixture evidence, disposable-object evidence, and visual asset review
  are complete.

## Repository Model

Warp CN currently uses a source-level localization overlay:

1. English upstream source strings remain the reference.
2. zh-Hans translations live in a TOML manifest.
3. `script/zh_apply_localization.py` applies the manifest to source files.
4. The Chinese source tree is treated as regenerable build output.
5. The durable assets are the manifest, glossary, ignore rules, audit reports,
   evidence records, and validation scripts.

Do not treat edited Chinese Rust files as the only source of truth. If a source
string is changed, keep the corresponding manifest entry in sync.

## Required Local Preparation

Clone and fetch Git LFS assets:

```bash
git clone https://github.com/Drew1811266/Warp-CN.git
cd Warp-CN
git lfs install
git lfs pull
```

Install local privacy hooks:

```bash
sh script/install_privacy_hooks.sh
```

Check the working tree before starting:

```bash
git status --short --branch
git remote -v
git branch --show-current
```

If unrelated user changes exist, do not overwrite or revert them. Work around
them or ask before touching the same files.

## Core Files

| File | Purpose |
| --- | --- |
| `resources/localization/zh-Hans-overrides.toml` | Main translation manifest |
| `resources/localization/zh-Hans-glossary.toml` | Stable terms, required translations, forbidden target terms |
| `resources/localization/zh-Hans-inventory-ignore.toml` | Inventory ignore rules |
| `resources/localization/zh-Hans-public-rc-blockers.toml` | Machine-readable public-RC blocker registry |
| `resources/localization/zh-Hans-public-rc-evidence.toml` | Redacted public-RC evidence ledger |
| `script/zh_apply_localization.py` | Manifest apply, drift check, metadata, glossary checks |
| `script/zh_localization_inventory.py` | Candidate string inventory and coverage |
| `script/zh_full_translation_audit.py` | Full per-entry simulated review ledger |
| `script/zh_export_locale.py` | JSON/YAML locale export for future runtime i18n |
| `script/zh_public_rc_status.py` | Public-RC blocker status summary |
| `script/zh_public_rc_evidence_lint.py` | Evidence metadata and artifact lint |
| `script/zh_public_rc_evidence_report.py` | Evidence readiness reports and action packets |
| `script/zh_public_rc_evidence_queue.py` | Prioritized public-RC evidence queue |
| `script/privacy_guard.py` | Tracked-file privacy and artifact safety scan |

## Normal Development Workflow

Use this sequence for ordinary localization work:

1. Inspect current state.
2. Identify candidate strings or drift.
3. Add or update manifest entries.
4. Apply the manifest.
5. Review the changed source context.
6. Run low-load validation gates.
7. Update audit or phase docs if the work changes release posture.

Commands:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
```

Apply translations when `would_change` is greater than 0:

```bash
python3 script/zh_apply_localization.py
cargo fmt
```

## Adding Or Updating Manifest Entries

Use manifest v2 metadata for every new entry when possible:

```toml
[[replace]]
key = "settings.example.open"
path = "app/src/example.rs"
source = "Open"
target = "打开"
context = "Example toolbar action"
status = "active"
preserve_terms = ["Warp"]
expected_count = 1
```

Required review rules:

- Confirm the nearby Rust code proves the string is user-visible or safe to
  translate.
- Preserve product terms from `zh-Hans-glossary.toml`.
- Preserve `{}`, named placeholders, markdown links, URLs, shortcuts, long
  flags, command names, provider names, model IDs, and config keys.
- Do not translate telemetry event names, feature flags, storage keys, protocol
  fields, tests, fixtures, schema IDs, or internal diagnostics unless they are
  proven user-facing.
- Keep button, menu, tab, and compact modal text short enough for the UI.
- For destructive, billing, auth, cloud, endpoint, secret, and team ownership
  strings, record the GUI/public-RC evidence requirement instead of promoting
  the row from source review alone.

## Candidate Inventory

Use presets to find remaining candidate English strings:

```bash
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

Drill into candidates:

```bash
python3 script/zh_localization_inventory.py --preset settings --status candidate
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

Current expected posture:

- Core preset coverage remains effectively complete.
- Remaining candidates may be intentional product terms or internal strings.
- Do not translate a candidate only because it is English.

## Full Per-Entry Review

Run the full simulated review whenever:

- New manifest entries are added.
- Source strings are changed.
- Upstream sync or merge may have moved strings.
- Preparing a release or public-RC evidence cycle.

Command:

```bash
python3 script/zh_full_translation_audit.py --fail-on-actionable
```

Artifacts:

```text
docs/zh-Hans-full-translation-audit-0.18/entries.tsv
docs/zh-Hans-full-translation-audit-0.18/entries.json
docs/zh-Hans-full-translation-audit-0.18/summary.md
```

Interpretation:

| Decision | Meaning |
| --- | --- |
| `simulated-accepted` | No machine-detected copy, token, or risk issue |
| `simulated-accepted-with-note` | Acceptable, but has risk tags or source-state notes |
| `blocked-public-rc` | Copy is not the blocker; final promotion requires external evidence |
| `needs-copy-review` | Wording should be inspected and fixed |
| `needs-functional-review` | Translation may affect placeholders, parsing, or behavior |

`--fail-on-actionable` must pass before release handoff.

## Low-Load Validation Gate

Run these for normal localization, docs, and script changes:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable
python3 -m json.tool docs/zh-Hans-full-translation-audit-0.18/entries.json > /tmp/warp-cn-full-audit-entries.pretty.json
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py --json > /tmp/warp-cn-public-rc-evidence-report.json
python3 script/zh_public_rc_evidence_queue.py --json > /tmp/warp-cn-public-rc-evidence-queue.json
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/zh_public_rc_status.py script/zh_public_rc_evidence_lint.py script/zh_public_rc_evidence_report.py script/zh_public_rc_evidence_queue.py script/zh_public_rc_evidence_candidate.py script/privacy_guard.py script/zh_full_translation_audit.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py script/test_zh_public_rc_evidence_candidate.py
cargo fmt --check
git diff --check
```

Expected current results:

- Manifest validation passes.
- Glossary check passes.
- Dry-run reports `would_change: 0` and `missing: 0`.
- Full audit reports 7,943 entries and no actionable rows.
- Unit tests pass.
- Public-RC status still reports 11 blocked rows.

## Heavy Build And GUI Gate

Before running Rust compile, bundle build, or GUI launch, run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Proceed only when it prints:

```text
decision: run-heavy-gate
```

Then run heavy gates serially:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

If the gate prints `decision: defer-heavy-gate`, record the reasons and do not
retry repeatedly in the same cycle.

## GUI Smoke Evidence

Minimum non-destructive anchors for a current-source GUI smoke:

- Welcome and onboarding labels.
- Main menu labels: File, Edit, View, Tabs, Blocks, AI, Drive, Window, Help.
- Command palette and command search.
- Settings shell, Appearance, AI settings, billing entry, teams entry.
- Basic modal/toast surfaces that do not require account or destructive state.

Evidence rules:

- Prefer accessibility text over screenshots.
- Commit screenshots only when cropped and redacted.
- Do not commit raw full-screen screenshots or recordings.
- Do not capture account identifiers, tokens, cookies, private local paths, API
  keys, billing IDs, team names, or endpoint secrets.
- Fixture-only evidence can support `fixture-verified`, not public-RC
  `verified`.

## Public-RC Blocker Workflow

The current public-RC blocker registry has 11 required rows:

| Category | Count | Rows |
| --- | ---: | --- |
| `isolated_account` | 3 | `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06` |
| `backend_fixture` | 5 | `GUI-SET-04`, `GUI-SET-05`, `GUI-BILL-01`, `GUI-BILL-02`, `GUI-CLOUD-01` |
| `disposable_object` | 3 | `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07` |

Safety rules:

- Never use the user's main account.
- Never spend money, buy credits, attach payment methods, or mutate production
  billing state.
- Never enter real API keys, AWS credentials, tokens, cookies, or magic links.
- Never delete or transfer real teams, environments, endpoints, or secrets.
- Destructive tests must use exact allowlisted object names from the blocker
  registry and must cancel first.

Generate the current evidence queue:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown
python3 script/zh_public_rc_evidence_report.py --missing-actions
```

Strict artifact lint is expected to fail until all required redacted evidence
exists:

```bash
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

Do not promote a blocker row unless three sources agree:

1. `zh-Hans-public-rc-blockers.toml` status is updated.
2. Human phase/release evidence records the cleared state.
3. The required GUI/backend/account artifact exists and passes lint.

## Upstream Sync Workflow

Use this workflow only after deciding the target upstream baseline.

Preflight:

```bash
git status --short --branch
git remote -v
git branch --show-current
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
```

Fetch only when explicitly intended:

```bash
git fetch origin --tags
```

If tags conflict, do not force-update or delete local `v0.2026.*` tags without
explicit approval. Compare remote truth using `git ls-remote --tags origin`.

After merging or replaying the overlay:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable
```

If `missing` is greater than 0, inspect each missing row and update `path`,
`source`, `target`, or `status`. Do not paper over drift with broad string
replacement.

## Release Handoff

A local-use release may be documented when:

- Manifest validation passes.
- Glossary check passes.
- Dry-run reports no missing or pending changes.
- Full audit has no actionable rows.
- Privacy guard passes.
- Unit tests pass.
- `cargo fmt --check` passes.
- Heavy build gate is either passed or explicitly deferred with reasons.

A public RC may be documented only when all local-use requirements pass and:

- Fresh current-source GUI smoke evidence exists.
- All 11 public-RC blockers are cleared with redacted evidence.
- Strict public-RC evidence artifact lint passes.
- Static visual asset review is complete.
- No unsafe account, billing, cloud, secret, endpoint, or team state was used.

## Execution Records

Use execution records to preserve what was actually run in a specific goal,
phase, or RC cycle:

- `docs/zh-Hans-development-guide-execution-2026-06-03.md`

## Troubleshooting

### `dry-run --summary` reports `missing`

Likely causes:

- Upstream changed or removed the English source string.
- The source file moved.
- The target was manually edited without updating the manifest.
- Escapes in the manifest do not match the parser representation.

Fix:

1. Open the reported path.
2. Find the current upstream/source string.
3. Update the manifest entry.
4. Re-run dry-run until `missing: 0`.

### `check-glossary` fails

Fix the target wording or update the glossary only if the term policy itself has
changed. Do not bypass glossary failures for convenience.

### `zh_full_translation_audit.py --fail-on-actionable` fails

Open the listed rows in `entries.tsv`. Decide whether each row is:

- a real copy issue,
- a token or placeholder issue,
- a functional-risk issue,
- a script heuristic false positive.

Fix real issues first. If it is a false positive, improve the script rule so the
ledger remains useful.

### Low-load gate defers heavy commands

Record the probe output. Do not run `cargo check`, bundle build, or GUI launch
until the gate allows it.

### Public-RC evidence lint fails

This is expected while evidence rows are missing. Use queue/report commands to
generate row-specific action packets, then collect only safe redacted evidence.

## Completion Checklist

Before handing a development cycle back:

- [ ] `git status --short --branch` reviewed.
- [ ] Manifest validation passed.
- [ ] Glossary check passed.
- [ ] Dry-run reports `would_change: 0`, `missing: 0`.
- [ ] Full audit has 0 actionable rows.
- [ ] Privacy guard passed.
- [ ] Relevant unit tests passed.
- [ ] `cargo fmt --check` passed for source changes.
- [ ] `git diff --check` passed.
- [ ] Public-RC status is reported honestly.
- [ ] Heavy/GUI gates are either executed or explicitly deferred with low-load
      reasons.
- [ ] Any new docs describe what was tested, what was skipped, and why.
