# zh-Hans 0.19 Next Development Tasks

Date: 2026-06-04

This task list starts after the 0.19 source-localization adaptation recorded in
`docs/zh-Hans-release-candidate-2026-06-04-rc39.md`.

## Current Handoff State

```text
source localization: ready for continued engineering verification
manifest drift: repaired
release inventory candidates: 0
full audit actionable rows: 0
heavy gate: deferred by low-load protection
bundle refresh: deferred
GUI evidence: deferred and requires explicit approval
public RC: not ready
publish/tag: not approved and not performed
```

## Immediate Gates

1. Re-run the low-load gate when the Mac is cool and idle enough:

   ```bash
   python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
   ```

2. Only if it prints `decision: run-heavy-gate`, run the deferred heavy compile
   gate:

   ```bash
   CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
   ```

3. If compile passes, refresh the bundle without launching:

   ```bash
   TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
   ```

4. Request explicit approval before launching the GUI or collecting current-cycle
   GUI evidence.

## GUI Evidence Gate

Minimum non-destructive GUI anchors:

- Welcome/onboarding shell.
- Main menu labels.
- Command palette and command search.
- Settings shell, Appearance, AI settings, billing entry, and teams entry.
- Non-account, non-destructive modal/toast surfaces.

Rules:

- Prefer accessibility text logs over screenshots.
- Do not commit raw full-screen screenshots or recordings.
- Do not expose account identifiers, tokens, cookies, billing IDs, endpoint
  secrets, private local paths, team names, or API keys.
- Do not use the user's main account.

## Public-RC Evidence Work

Resolve the 11 required public-RC rows only with safe current-cycle evidence:

| Category | Count | Rows |
| --- | ---: | --- |
| `backend_fixture` | 5 | `GUI-BILL-01`, `GUI-BILL-02`, `GUI-CLOUD-01`, `GUI-SET-04`, `GUI-SET-05` |
| `disposable_object` | 3 | `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07` |
| `isolated_account` | 3 | `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06` |

Use these commands to generate the next evidence packets:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown
python3 script/zh_public_rc_evidence_report.py --missing-actions
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

The strict lint failure is expected until every row has matching redacted
artifacts and ledger metadata.

## Static Asset Review

Review onboarding and other static PNG assets separately from source text:

- Identify assets that still contain English UI text.
- Decide whether to regenerate, redesign, crop, or defer each asset.
- Keep raw design/export artifacts out of Git unless they are approved and
  privacy-safe.

## Release Publication Preconditions

Do not publish, tag, push, or mark a public release until all of these are true:

- Low-load gate allows heavy work.
- Serial `cargo check -j 1 -p warp` passes in the current source cycle.
- Bundle refresh passes.
- GUI evidence is explicitly approved and collected.
- All 11 public-RC blocker rows are cleared with lintable redacted evidence.
- Static asset review is complete.
- The user explicitly approves GitHub publication and version tagging.

## Recommended Next Record

After the deferred gates are rerun, create a new RC record instead of modifying
RC39 in place. Suggested filename:

```text
docs/zh-Hans-release-candidate-2026-06-04-rc40.md
```
