# zh-Hans Localization Calibration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` for parallel lane execution, or `superpowers:executing-plans` for single-agent execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `docs/zh-Hans-localization-calibration-plan.md` into an executable, low-load calibration program for Warp CN. The program must let Codex simulate human review across every zh-Hans manifest row, produce module-level findings, detect machine-translation copy issues, protect functional tokens, check mojibake/layout risk, record performance risk without high-load runtime work, and keep public-RC readiness blocked until real safe evidence exists.

**Architecture:** Keep `resources/localization/zh-Hans-overrides.toml` as the translation source of truth and extend the existing audit/reporting scripts rather than replacing the localization overlay model. Build one dated calibration cycle directory under `docs/zh-Hans-calibration-cycles/2026-06-05/`, regenerate machine-readable ledgers there, then layer human-style review reports on top of deterministic script output. This implementation plan deliberately avoids high-load work: no `cargo fmt`, no `cargo check`, no bundle build, no `script/run`, no app launch, and no GUI smoke execution. GUI, runtime, account state, backend fixture, billing, cloud, secret, endpoint, and team ownership work are recorded as deferred evidence lanes only.

**Tech Stack:** Python 3 validation/report scripts, TOML localization manifest, JSON/TSV audit ledgers, Markdown cycle reports, `git diff --check`, and deferred Rust/Cargo, GUI, runtime, and public-RC evidence plans.

---

## Current Facts

| Item | Value |
| --- | --- |
| Calibration source document | `docs/zh-Hans-localization-calibration-plan.md` |
| Developer guide | `docs/zh-Hans-development-guide.md` |
| Translation manifest | `resources/localization/zh-Hans-overrides.toml` |
| Glossary | `resources/localization/zh-Hans-glossary.toml` |
| Public-RC blocker registry | `resources/localization/zh-Hans-public-rc-blockers.toml` |
| Existing full audit script | `script/zh_full_translation_audit.py` |
| Existing full audit artifacts | `docs/zh-Hans-full-translation-audit-0.18/` |
| Manifest entries | 7,943 |
| Covered source files | 552 |
| Dry-run status | `would_change: 0`, `missing: 0` |
| Release inventory | `covered: 8574`, `candidates: 2`, `coverage: 100.0%` |
| Existing actionable audit rows | 0 |
| Existing `blocked-public-rc` audit rows | 1,030 |
| Public-RC blockers | 11 |
| Heat-safety rule | This plan does not run high-load build, bundle, app launch, or GUI runtime commands. |

Top module concentrations from the existing audit ledger:

```text
2375 app/src/ai
1978 app/src/terminal
1873 app/src/settings_view
706  app/src/workspace
225  app/src/drive
204  app/src/search
159  crates/onboarding/src
136  app/src/auth
```

Top risk concentrations:

```text
3187 terminal-command
2226 english-preserved
1662 dynamic-placeholder
1179 team-workspace
787  environment-endpoint
482  billing-quota
459  api-key-secret
353  error-state
221  destructive-action
119  auth-login
```

## Source References

| File | Why it matters |
| --- | --- |
| `docs/zh-Hans-localization-calibration-plan.md` | Defines the calibration scope, review dimensions, lane model, and acceptance criteria. |
| `docs/zh-Hans-development-guide.md` | Defines current repo workflow, low-load validation gates, heavy gate, GUI evidence, and public-RC boundaries. |
| `docs/zh-Hans-review-checklist.md` | Existing per-entry review checklist for normal localization work. |
| `docs/zh-Hans-module-review-matrix.md` | Existing module-level review surface and status vocabulary. |
| `docs/zh-Hans-functional-risk-register.md` | Existing functional-risk classes and default preserve/translate decisions. |
| `docs/zh-Hans-gui-smoke-matrix.md` | Existing GUI evidence rows and evidence hygiene rules. |
| `docs/zh-Hans-full-translation-audit-0.18/summary.md` | Current 7,943-entry simulated audit summary. |
| `resources/localization/zh-Hans-public-rc-blockers.toml` | Machine-readable source of truth for public-RC blockers. |
| `resources/localization/zh-Hans-public-rc-evidence.toml` | Committable redacted public-RC evidence ledger. |

## Deliverables

Create or update these files:

- `docs/zh-Hans-calibration-cycles/2026-06-05/summary.md`
- `docs/zh-Hans-calibration-cycles/2026-06-05/module-matrix.md`
- `docs/zh-Hans-calibration-cycles/2026-06-05/entries.json`
- `docs/zh-Hans-calibration-cycles/2026-06-05/entries.tsv`
- `docs/zh-Hans-calibration-cycles/2026-06-05/copy-review-findings.md`
- `docs/zh-Hans-calibration-cycles/2026-06-05/functional-risk-findings.md`
- `docs/zh-Hans-calibration-cycles/2026-06-05/mojibake-and-layout-findings.md`
- `docs/zh-Hans-calibration-cycles/2026-06-05/performance-probe.md`
- `docs/zh-Hans-calibration-cycles/2026-06-05/public-rc-blocker-status.md`
- `script/zh_mojibake_scan.py`
- `script/zh_module_calibration_report.py`
- `script/zh_performance_probe.py`
- `script/test_zh_mojibake_scan.py`
- `script/test_zh_module_calibration_report.py`
- `script/test_zh_performance_probe.py`

Modify these existing files only if needed:

- `script/zh_full_translation_audit.py`: add optional output fields and support writing to a dated calibration directory.
- `script/test_zh_full_translation_audit.py`: create if a focused test file does not already exist, or extend equivalent tests if present.
- `docs/zh-Hans-development-guide.md`: update only after the calibration workflow is proven and should become durable guidance.

Do not modify these without explicit evidence or approval:

- `resources/localization/zh-Hans-public-rc-blockers.toml`
- `resources/localization/zh-Hans-public-rc-evidence.toml`
- Any real account, billing, backend, cloud, secret, endpoint, or team state.
- Existing unrelated dirty files in the worktree.

## Definition Of Done

- A dated calibration cycle directory exists with all required reports.
- Every manifest row is represented in `entries.json` and `entries.tsv`.
- Entries include module, length ratio, copy score, mojibake status, UI density risk, functional risk, public-RC row mapping, and source-state status.
- Copy findings separate real machine-translation concerns from acceptable product-term English preservation.
- Functional findings separate actionable token/protocol risk from accepted display-unit or UI hint differences.
- Mojibake/layout report proves UTF-8 parsing and flags replacement characters, mojibake signatures, very long compact-UI strings, and likely truncation risks.
- Performance report records low-load script timings only and explicitly states that build, bundle, GUI, and runtime probes were skipped by heat-safety policy.
- Public-RC status report still lists all 11 blockers unless real current-cycle safe evidence was added and linted.
- `python3 script/privacy_guard.py --all-tracked` passes.
- Manifest validation, glossary check, metadata summary, dry-run, full audit, JSON parse, public-RC status/report/queue, Python compile, Python tests, and `git diff --check` pass.
- Rust/Cargo build, Rust/Cargo format, bundle build, app launch, GUI smoke, and runtime probes are explicitly deferred to a later user-approved high-load window.
- No final report claims GUI readiness, runtime performance readiness, or public-RC readiness without matching evidence. Under this low-load plan, GUI and runtime readiness are expected to remain incomplete.

## Acceptance Criteria

| Criterion | Verification |
| --- | --- |
| Full-row coverage | `entries.json` row count equals manifest replacement count. |
| Machine-readable output | `python3 -m json.tool docs/zh-Hans-calibration-cycles/2026-06-05/entries.json` passes. |
| Copy review is actionable | `copy-review-findings.md` lists `needs-copy-fix`, `accepted-with-note`, and false-positive categories separately. |
| Functional safety is actionable | `functional-risk-findings.md` lists placeholder/token/protocol/search/storage risks separately. |
| Mojibake scan is reproducible | `python3 script/zh_mojibake_scan.py --json` exits cleanly or reports explicit actionable findings. |
| Module status is clear | `module-matrix.md` has one row for every major module in the calibration plan. |
| Performance is honest | `performance-probe.md` distinguishes low-load script timing from skipped high-load runtime conclusions. |
| Public-RC boundary is honest | `public-rc-blocker-status.md` reports blocker counts and says fixture-only evidence is not public-RC proof. |
| Tests cover new scripts | New script tests pass through `python3 -m unittest ...`. |
| No unrelated churn | `git status --short` shows only planned files changed, plus pre-existing dirty files left untouched. |

## Implementation Tasks

### Task 1: Protect Worktree And Create Calibration Cycle Skeleton

**Files:**
- Create: `docs/zh-Hans-calibration-cycles/2026-06-05/`
- Create: initial Markdown files listed in Deliverables
- Read: `docs/zh-Hans-localization-calibration-plan.md`
- Read: `docs/zh-Hans-development-guide.md`

- [ ] **Step 1: Record worktree state before any edit**

Run:

```bash
git status --short --branch
```

Acceptance:

- Existing dirty files are listed in the cycle summary.
- Plan execution does not revert or overwrite unrelated dirty files.

- [ ] **Step 2: Create the cycle directory**

Create:

```text
docs/zh-Hans-calibration-cycles/2026-06-05/
```

Acceptance:

- Directory exists.
- Summary file states this is a calibration execution record, not a release approval.

- [ ] **Step 3: Write the initial cycle snapshot**

Record:

- Branch name.
- Manifest entries.
- Dry-run `would_change` and `missing`.
- Release inventory coverage.
- Public-RC blocker count.
- Confirmation that high-load gates and runtime probes are skipped by policy.

Acceptance:

- `summary.md` has a `Snapshot` table and a `Current Boundary` section.

### Task 2: Add Dated Output Support To Full Audit

**Files:**
- Modify: `script/zh_full_translation_audit.py`
- Create or modify: `script/test_zh_full_translation_audit.py`
- Output: `docs/zh-Hans-calibration-cycles/2026-06-05/entries.json`
- Output: `docs/zh-Hans-calibration-cycles/2026-06-05/entries.tsv`

- [ ] **Step 1: Add optional calibration fields**

Add fields to each audit row:

- `module`
- `module_group`
- `length_ratio`
- `target_length`
- `source_length`
- `machine_copy_score`
- `mojibake_status`
- `ui_density_risk`
- `review_lane`

Rules:

- Keep existing output fields stable.
- Do not change existing `docs/zh-Hans-full-translation-audit-0.18/` output unless explicitly regenerating it.
- New fields must be deterministic.

Acceptance:

- Existing `--fail-on-actionable` behavior is unchanged.
- New fields are present when writing to the calibration cycle output directory.

- [ ] **Step 2: Implement module grouping**

Use path prefixes:

| Prefix | Module group |
| --- | --- |
| `app/src/ai` | `ai-agent` |
| `app/src/terminal` | `terminal-command` |
| `app/src/settings_view` | `settings` |
| `app/src/workspace` | `workspace` |
| `app/src/drive` | `warp-drive` |
| `app/src/search` | `search-command-palette` |
| `crates/onboarding` | `onboarding` |
| `app/src/auth` | `auth-account` |
| billing paths | `billing-quota` |
| team paths | `teams-ownership` |
| everything else | `other-reviewed` |

Acceptance:

- Every row has a non-empty `module_group`.
- `module-matrix.md` can aggregate rows by `module_group`.

- [ ] **Step 3: Implement copy scoring**

Suggested scoring:

- `0`: actionable copy risk.
- `1`: awkward or note-worthy copy risk.
- `2`: acceptable source-level copy.

Copy score signals:

- Forbidden target term.
- Empty target.
- TODO/FIXME marker in target.
- English preserved without known preserve reason.
- Target much longer than source in compact UI.
- Destructive wording mismatch.
- Chinese source text lost in target.

Acceptance:

- Scores are deterministic.
- `0` scores map to `needs-copy-fix` or equivalent actionable output.
- `1` scores appear in `copy-review-findings.md`.

- [ ] **Step 4: Implement mojibake and UI density flags**

Flag:

- Replacement character.
- Mojibake signatures.
- Suspicious control characters.
- Target length ratio above configured threshold.
- Compact UI surface plus long target.

Acceptance:

- Known intentional examples in the calibration plan are not treated as product findings when scanning the plan document itself.
- Manifest/source findings are separated from documentation examples.

### Task 3: Add Mojibake Scanner

**Files:**
- Create: `script/zh_mojibake_scan.py`
- Create: `script/test_zh_mojibake_scan.py`
- Output: `docs/zh-Hans-calibration-cycles/2026-06-05/mojibake-and-layout-findings.md`

- [ ] **Step 1: Build scanner CLI**

Support:

```bash
python3 script/zh_mojibake_scan.py --help
python3 script/zh_mojibake_scan.py --json
python3 script/zh_mojibake_scan.py --markdown
python3 script/zh_mojibake_scan.py --paths resources/localization app crates docs
```

Acceptance:

- CLI defaults scan localization-relevant paths.
- Output includes file, line, category, snippet, and decision.

- [ ] **Step 2: Add categories**

Categories:

- `replacement-character`
- `mojibake-signature`
- `invalid-utf8`
- `control-character`
- `overlong-compact-ui-target`
- `markdown-or-token-escape-risk`

Acceptance:

- JSON output is parseable.
- Markdown output is usable as a cycle finding report.

- [ ] **Step 3: Add tests**

Test fixtures:

- Clean Chinese target.
- Replacement character.
- Typical mojibake.
- Escaped URL/token false positive.
- Documentation example that should be classified as example-only.

Acceptance:

- `python3 -m unittest script/test_zh_mojibake_scan.py` passes.

### Task 4: Add Module Calibration Report

**Files:**
- Create: `script/zh_module_calibration_report.py`
- Create: `script/test_zh_module_calibration_report.py`
- Output: `docs/zh-Hans-calibration-cycles/2026-06-05/module-matrix.md`
- Output: `docs/zh-Hans-calibration-cycles/2026-06-05/copy-review-findings.md`
- Output: `docs/zh-Hans-calibration-cycles/2026-06-05/functional-risk-findings.md`

- [ ] **Step 1: Build report CLI**

Support:

```bash
python3 script/zh_module_calibration_report.py --help
python3 script/zh_module_calibration_report.py --audit-json docs/zh-Hans-calibration-cycles/2026-06-05/entries.json --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
python3 script/zh_module_calibration_report.py --audit-json docs/zh-Hans-calibration-cycles/2026-06-05/entries.json --json
```

Acceptance:

- Report reads the audit JSON rather than re-parsing the manifest.
- Report can regenerate Markdown outputs deterministically.

- [ ] **Step 2: Generate module status**

For each module group, compute:

- Entry count.
- Decisions.
- Copy score counts.
- Functional status counts.
- Mojibake status counts.
- Public-RC row counts.
- Top source files.
- Required evidence status.
- Proposed next action.

Acceptance:

- `module-matrix.md` covers all major modules from the calibration plan.
- Public-RC evidence requirements are not collapsed into source-level success.

- [ ] **Step 3: Generate copy findings**

Sections:

- `Needs Copy Fix`
- `Machine Translation Risk Notes`
- `English Preserved Review Queue`
- `Long Compact UI Text`
- `Accepted False Positives`

Acceptance:

- Findings include entry index, manifest line, path, source, target, and required action.

- [ ] **Step 4: Generate functional findings**

Sections:

- `Critical Token Mismatches`
- `Source State Review`
- `Placeholder And URL Risks`
- `Command And Slash Command Risks`
- `Search, Action, Storage, Protocol Risks`
- `Public-RC Evidence Gated`

Acceptance:

- No public-RC row is marked cleared unless registry/evidence state proves it.

### Task 5: Add Low-Load Performance Probe

**Files:**
- Create: `script/zh_performance_probe.py`
- Create: `script/test_zh_performance_probe.py`
- Output: `docs/zh-Hans-calibration-cycles/2026-06-05/performance-probe.md`

- [ ] **Step 1: Build low-load timing mode**

Measure:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
python3 script/zh_localization_inventory.py --preset release --coverage
```

Acceptance:

- Probe records elapsed time, exit code, command, and interpretation.
- Probe never runs build, bundle, app launch, GUI, or runtime commands in this implementation plan.

- [ ] **Step 2: Build high-load skip mode**

Support:

```bash
python3 script/zh_performance_probe.py --record-high-load-skipped
```

Behavior:

- Do not call `cargo`, `script/run`, `open`, GUI automation, or runtime log probes.
- Record that build, bundle, GUI, and runtime performance checks are skipped by heat-safety policy.
- List the exact deferred commands as documentation only, marked `not-run`.

Acceptance:

- There is no flag in this script that runs high-load commands.
- Runtime evidence is recorded as `skipped-by-heat-safety-policy`, not pass or fail.

- [ ] **Step 3: Add tests**

Test:

- Timing parser.
- High-load skip report.
- Proof that no high-load subprocess command is constructed or executed.

Acceptance:

- `python3 -m unittest script/test_zh_performance_probe.py` passes.

### Task 6: Generate First Calibration Cycle Artifacts

**Files:**
- Output all cycle files under `docs/zh-Hans-calibration-cycles/2026-06-05/`

- [ ] **Step 1: Run low-load validation stack**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
python3 -m json.tool docs/zh-Hans-calibration-cycles/2026-06-05/entries.json > /tmp/warp-cn-calibration-entries.pretty.json
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_report.py --json > /tmp/warp-cn-public-rc-evidence-report.json
python3 script/zh_public_rc_evidence_queue.py --json > /tmp/warp-cn-public-rc-evidence-queue.json
```

Acceptance:

- All command outputs are recorded in `summary.md`.
- Any failure gets an exact failure section and stops promotion claims.

- [ ] **Step 2: Generate module and finding reports**

Run:

```bash
python3 script/zh_module_calibration_report.py --audit-json docs/zh-Hans-calibration-cycles/2026-06-05/entries.json --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
python3 script/zh_mojibake_scan.py --markdown > docs/zh-Hans-calibration-cycles/2026-06-05/mojibake-and-layout-findings.md
python3 script/zh_performance_probe.py --output docs/zh-Hans-calibration-cycles/2026-06-05/performance-probe.md
```

Acceptance:

- Reports exist and reference the exact audit JSON used.
- Reports distinguish actionable findings from note-only findings.

- [ ] **Step 3: Generate public-RC blocker status**

Run:

```bash
python3 script/zh_public_rc_status.py > /tmp/warp-cn-public-rc-status.txt
python3 script/zh_public_rc_evidence_report.py --missing-actions > docs/zh-Hans-calibration-cycles/2026-06-05/public-rc-blocker-status.md
```

Acceptance:

- `public-rc-blocker-status.md` states whether blocker count remains 11.
- It does not claim any row cleared without evidence.

### Task 7: Execute Copy Lane Review

**Files:**
- Read: `docs/zh-Hans-calibration-cycles/2026-06-05/copy-review-findings.md`
- Modify only if needed: `resources/localization/zh-Hans-overrides.toml`
- Update: `docs/zh-Hans-calibration-cycles/2026-06-05/summary.md`

- [ ] **Step 1: Review actionable copy findings**

For every `needs-copy-fix` candidate:

- Open surrounding source context.
- Confirm whether the target is wrong, awkward, too machine-translated, too long, or a false positive.
- Patch manifest target only when a real copy issue is confirmed.

Acceptance:

- Each actionable row has a decision and rationale.
- No entry is changed solely because it is English preserved.

- [ ] **Step 2: Review high-volume English preservation**

Prioritize:

- `terminal-command`
- `search-command-palette`
- provider/model/API terms
- product names
- command names and flags

Acceptance:

- English preservation queue is classified into `intentional-preserve`, `needs-translation`, or `needs-owner-review`.

- [ ] **Step 3: Reapply and regenerate if copy changes are made**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py
python3 script/zh_full_translation_audit.py --fail-on-actionable --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
```

Acceptance:

- Dry-run returns `would_change: 0`, `missing: 0` after reapply.
- Copy findings are regenerated.
- Rust formatting checks are deferred in this low-load plan; record this explicitly if Rust source changed.

### Task 8: Execute Functional Risk Lane

**Files:**
- Read: `docs/zh-Hans-calibration-cycles/2026-06-05/functional-risk-findings.md`
- Modify only if needed: manifest, ignore rules, targeted tests

- [ ] **Step 1: Triage token and placeholder risks**

Prioritize:

- Critical token mismatches.
- Source-state review.
- Placeholder/URL/slash command differences.
- Search/action/storage/protocol strings.

Acceptance:

- Each item has one of: `fix-manifest`, `preserve-intentional`, `add-ignore-rule`, `add-targeted-test`, or `needs-owner-review`.

- [ ] **Step 2: Add targeted tests for confirmed functional risks**

Candidate tests:

- Command palette labels and search behavior.
- Slash command hint text.
- Terminal copy/select labels.
- Settings form field labels that include provider/model/API tokens.
- JSON/YAML/exported locale token preservation.

Acceptance:

- Tests are scoped to the changed behavior.
- Tests do not require real account, billing, backend, cloud, secret, endpoint, or team state.

- [ ] **Step 3: Re-run functional gates**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
```

Acceptance:

- No `needs-functional-review` row remains unless explicitly documented as owner-blocked.

### Task 9: Execute Mojibake And Layout Lane

**Files:**
- Read: `docs/zh-Hans-calibration-cycles/2026-06-05/mojibake-and-layout-findings.md`
- Modify only if needed: manifest target wording or GUI report

- [ ] **Step 1: Resolve static mojibake findings**

For each finding:

- Confirm whether it is real product text, documentation example, or acceptable token.
- Fix real product mojibake in the manifest or source.
- Keep documentation examples out of product bug counts.

Acceptance:

- Static mojibake report has zero unexplained product-text findings.

- [ ] **Step 2: Triage layout risk queue**

Prioritize:

- Buttons.
- Menu items.
- Compact modal titles.
- Toasts.
- Terminal inline labels.
- Settings navigation and toggles.

Acceptance:

- Each risk has `shorten-copy`, `needs-gui-evidence`, or `accepted-with-note`.

- [ ] **Step 3: Prepare GUI layout smoke checklist**

Create anchors for:

- Onboarding.
- Main menu.
- Terminal view.
- Command palette.
- Settings shell.
- AI settings.
- Billing entry.
- Teams entry.
- Workspace tab context menu.

Acceptance:

- Checklist is ready before any GUI launch.
- It does not require unsafe account state.

### Task 10: Execute Low-Load Performance Lane

**Files:**
- Read and update: `docs/zh-Hans-calibration-cycles/2026-06-05/performance-probe.md`

- [ ] **Step 1: Record low-load script timings**

Run:

```bash
python3 script/zh_performance_probe.py --output docs/zh-Hans-calibration-cycles/2026-06-05/performance-probe.md
```

Acceptance:

- Report includes script-level timing and exit codes.
- It explicitly says script timing is not app runtime performance.

- [ ] **Step 2: Record high-load runtime deferral**

Do not run:

- `python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25`
- `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- `open -n target/debug/bundle/osx/WarpOss.app`
- `/usr/bin/log show ...`

Acceptance:

- `performance-probe.md` states these commands were skipped to avoid heat and high CPU load.
- Runtime performance readiness remains `not-evaluated`.

- [ ] **Step 3: Prepare deferred runtime checklist**

Write a future checklist, marked `not-run`:

- Low-load gate.
- Rust compile.
- Bundle build.
- GUI launch.
- Accessibility anchor collection.
- Runtime logs.

Acceptance:

- Checklist is present for a later approved window.
- No runtime conclusion is made in this low-load cycle.

### Task 11: Prepare GUI Lane Without Running GUI

**Files:**
- Update: `docs/zh-Hans-calibration-cycles/2026-06-05/summary.md`
- Create: `docs/zh-Hans-calibration-cycles/2026-06-05/gui-smoke-deferred.md`
- Do not commit raw full-screen screenshots.

- [ ] **Step 1: Record GUI deferral**

Record:

- GUI was not launched in this implementation cycle.
- No Computer Use GUI session was attempted.
- No screenshots were captured.
- No account, billing, cloud, secret, endpoint, or team state was touched.

Acceptance:

- `gui-smoke-deferred.md` exists and states `GUI readiness: incomplete`.

- [ ] **Step 2: Prepare future accessibility anchor checklist**

Prepare anchors for a later approved low-temperature window:

- Welcome/onboarding labels.
- Main menu labels.
- Terminal view labels.
- Command palette.
- Settings shell.
- AI settings visible labels.
- Billing entry visible labels.
- Teams entry visible labels.

Acceptance:

- The checklist is ready.
- It is clearly marked `not-run`.

- [ ] **Step 3: Preserve public-RC GUI blockers**

Record that these remain blocked unless separate safe evidence exists:

- Isolated account rows.
- Backend fixture rows.
- Disposable object rows.

Acceptance:

- GUI readiness and public-RC readiness are reported separately.

### Task 12: Execute Public-RC Lane

**Files:**
- Read: `resources/localization/zh-Hans-public-rc-blockers.toml`
- Read: `resources/localization/zh-Hans-public-rc-evidence.toml`
- Update only with real safe evidence: blocker/evidence TOML and cycle report

- [ ] **Step 1: Generate missing-action queue**

Run:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown
python3 script/zh_public_rc_evidence_report.py --missing-actions
```

Acceptance:

- Queue is attached or summarized in `public-rc-blocker-status.md`.

- [ ] **Step 2: Decide whether prerequisites exist**

Required prerequisites:

- Isolated browser-login test account.
- Backend billing/quota/AWS/capacity fixtures.
- Disposable named objects for environment, secret, endpoint, and owner test team.
- Explicit approval for destructive evidence paths.

Acceptance:

- If prerequisites are absent, status remains blocked and no mutation happens.

- [ ] **Step 3: If prerequisites exist, collect evidence row by row**

For each row:

- Capture accessibility anchors.
- Capture cropped/redacted screenshots only when useful.
- Record cleanup proof.
- Run evidence candidate preflight.
- Update evidence ledger only after lintable evidence exists.

Acceptance:

- No row is promoted on fixture-only evidence.
- No real secrets, account identifiers, billing IDs, endpoint URLs, team IDs, or tokens enter the repo.

- [ ] **Step 4: Run strict artifact lint only after evidence exists**

Run:

```bash
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

Acceptance:

- Failure is expected while rows are missing.
- Passing strict lint is required before any public-RC ready claim.

### Task 13: Final Verification And Freeze

**Files:**
- Update: `docs/zh-Hans-calibration-cycles/2026-06-05/summary.md`
- Optional update after approval: `docs/zh-Hans-development-guide.md`

- [ ] **Step 1: Run final low-load validation**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
python3 -m json.tool docs/zh-Hans-calibration-cycles/2026-06-05/entries.json > /tmp/warp-cn-calibration-entries.pretty.json
python3 script/zh_public_rc_status.py
python3 -m py_compile script/zh_full_translation_audit.py script/zh_mojibake_scan.py script/zh_module_calibration_report.py script/zh_performance_probe.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py script/test_zh_public_rc_evidence_candidate.py script/test_zh_mojibake_scan.py script/test_zh_module_calibration_report.py script/test_zh_performance_probe.py
git diff --check
```

Acceptance:

- All pass, or exact failures are documented with next actions.
- Rust/Cargo checks are not part of this heat-safe verification cycle and must be listed as deferred if Rust source changed.

- [ ] **Step 2: Write final decision**

Final decision must include:

- Source-level calibration result.
- Copy quality result.
- Functional safety result.
- Mojibake/layout result.
- Performance result.
- GUI readiness.
- Public-RC readiness.

Acceptance:

- Each readiness category is separate.
- Missing GUI or public-RC evidence is not softened.

- [ ] **Step 3: Update durable guide only after successful cycle**

If the workflow is proven:

- Add a short link or summary to `docs/zh-Hans-development-guide.md`.
- Do not paste the whole cycle report into the durable guide.

Acceptance:

- Durable guide stays concise.
- Cycle details stay in dated directory.

## Risks And Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Existing dirty worktree is overwritten | User work lost | Record status first, avoid unrelated files, patch only planned files. |
| Script output is mistaken for human proof | False readiness claim | Keep source-level, GUI, performance, and public-RC statuses separate. |
| Full audit grows noisy | Review fatigue | Split findings into actionable, note-only, and false-positive buckets. |
| Machine-copy score overreaches | Good translations get churned | Require source-context confirmation before manifest changes. |
| Mojibake scanner flags documentation examples | False positives | Add category for documentation examples and exclude from product finding totals. |
| High-load commands run by mistake | Mac stalls or overheats | This plan forbids build, bundle, app launch, GUI, runtime logs, and Rust/Cargo checks; record them as deferred. |
| Public-RC evidence uses unsafe state | Privacy or account damage | Use isolated accounts, fixtures, exact disposable names, and linted redacted artifacts only. |
| Fixture evidence is over-promoted | Public-RC status becomes inaccurate | Keep fixture-only evidence out of public-RC verified status. |

## Verification Plan

Low-load verification:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_full_translation_audit.py --fail-on-actionable --output-dir docs/zh-Hans-calibration-cycles/2026-06-05
python3 -m json.tool docs/zh-Hans-calibration-cycles/2026-06-05/entries.json > /tmp/warp-cn-calibration-entries.pretty.json
python3 script/zh_public_rc_status.py
python3 -m unittest script/test_zh_mojibake_scan.py script/test_zh_module_calibration_report.py script/test_zh_performance_probe.py
git diff --check
```

Deferred high-load verification, not run in this plan:

- `python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25`
- `cargo fmt --check`
- `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- `open -n target/debug/bundle/osx/WarpOss.app`
- GUI automation and runtime log probes.

Public-RC verification:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-actions
python3 script/zh_public_rc_evidence_queue.py --markdown
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

Expected current public-RC result unless real safe evidence is added:

```text
blocked: 11 public-RC evidence rows remain
```

## Execution Order

1. Task 1: Skeleton and snapshot.
2. Task 2: Full audit field extension.
3. Task 3: Mojibake scanner.
4. Task 4: Module calibration report.
5. Task 5: Performance probe.
6. Task 6: First cycle artifact generation.
7. Task 7 and Task 8: Copy and functional lanes, parallel if using team workers.
8. Task 9: Mojibake/layout lane.
9. Task 10: Low-load performance lane.
10. Task 11: GUI deferred-plan lane, no GUI execution.
11. Task 12: Public-RC planning/status lane only, unless safe prerequisites already exist and the user separately approves evidence collection.
12. Task 13: Final verification and freeze.

## Staffing Guidance

Recommended worker lanes:

| Worker | Reasoning level | Scope |
| --- | --- | --- |
| Audit/tooling worker | High | `zh_full_translation_audit.py`, audit row fields, deterministic JSON/TSV output. |
| Mojibake/layout worker | Medium | `zh_mojibake_scan.py`, layout risk heuristics, tests. |
| Module report worker | High | Aggregation, copy/functional/public-RC report generation. |
| Performance worker | Medium | Low-load timing probe and explicit high-load deferral report. |
| Copy reviewer | High | Confirm real machine-translation issues before manifest edits. |
| Functional reviewer | High | Tokens, placeholders, command/search/protocol risk and targeted tests. |
| Verifier | High | Final gates, status separation, public-RC boundary review. |

Suggested `$team` launch brief:

```text
Use docs/superpowers/plans/2026-06-05-zh-Hans-localization-calibration-implementation-plan.md.
Implement Tasks 1-6 first. Do not run cargo check, cargo fmt, bundle build, script/run, app launch, GUI automation, runtime logs, or high-load probes in this cycle. Do not mutate account, billing, backend, cloud, secret, endpoint, or team state. Keep public-RC blocked unless real safe evidence exists and strict artifact lint passes.
```

Suggested `$ralph` single-agent brief:

```text
Execute the plan sequentially through Task 13. Prioritize deterministic scripts and cycle artifacts first. Do not run high-load commands in this cycle; record Rust, GUI, and runtime work as deferred by heat-safety policy. Keep all readiness categories separate in the final summary.
```

## Final Output Shape

When execution finishes, the final report should say:

```text
source-level calibration: passed / failed / blocked
copy quality: passed / findings remain
functional safety: passed / findings remain
mojibake-layout: passed / findings remain
performance: low-load script timing only / deferred high-load runtime
GUI readiness: incomplete / deferred
public-RC readiness: ready / blocked with N rows
```

Do not collapse these statuses into one release claim.
