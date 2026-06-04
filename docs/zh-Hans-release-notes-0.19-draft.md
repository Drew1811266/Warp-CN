# zh-Hans 0.19 Release Notes Draft

Date: 2026-06-04

## Status

This is a draft for the Warp CN `0.19` localization adaptation. It is not an
official Warp release note and does not represent a public RC.

```text
release posture: ready-for-source-localization; heavy-gates-deferred
upstream stable tag: v0.2026.06.03.09.49.stable_00
upstream stable commit: 2249469e5d24e472cee6ce97d3d324293f67db71
public RC: not ready
```

## Highlights

- Rebased the Warp CN zh-Hans overlay onto the official upstream stable source
  baseline `v0.2026.06.03.09.49.stable_00`.
- Repaired all manifest drift introduced by the upstream 0.19 source movement
  and string changes.
- Applied the zh-Hans overlay idempotently across 550 source files.
- Reviewed the 0.19 release inventory and reduced release candidates to 0.
- Added translations for visible 0.19 updates including vertical tab group
  menus, queued prompt actions, AI prompt submission settings, staging IAP
  credential status, shared-session metadata access, Claude Code platform plugin
  user errors, and duplicate child-agent guidance.
- Preserved internal-only logs, protocol IDs, config keys, position IDs, test
  assertions, and orchestration diagnostics through narrow ignore rules instead
  of translating them.
- Generated deterministic full translation audit artifacts for all 7,937
  manifest rows.

## Validation Snapshot

```text
manifest entries: 7937
covered files: 550
already applied: 5717
would change: 0
missing: 0
release coverage: 100.0%
release candidates: 0
full audit actionable rows: 0
public-RC blockers: 11
```

Passed validation includes privacy guard, manifest validation, glossary check,
metadata summary, dry-run summary, release inventory coverage, full translation
audit, public-RC status/report/queue generation, Python compile, localization
and public-RC unit tests, full-audit tests, `cargo fmt --check`, and
`git diff --check`.

`cargo check -q` passed during Task 7 review after the 0.19 translation update.
The current cycle did not rerun the serial heavy compile gate after the
low-load gate returned `defer-heavy-gate`.

## Deferred Gates

- `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- Fresh bundle refresh
- GUI launch and current-cycle GUI smoke evidence
- Strict public-RC evidence artifact lint

These gates should be rerun only after `script/zh_low_load_gate.py` returns
`decision: run-heavy-gate` and after the user approves GUI evidence collection.

## Known Public-RC Blockers

The public-RC registry still contains 11 required evidence rows:

| Category | Count |
| --- | ---: |
| `backend_fixture` | 5 |
| `disposable_object` | 3 |
| `isolated_account` | 3 |

No public-RC blocker was cleared in this adaptation cycle.

## User-Facing Wording Boundary

Recommended wording:

```text
Warp CN 0.19 has completed source-level zh-Hans localization adaptation against
the latest selected upstream stable baseline. It remains an engineering
verification candidate until heavy build, bundle, GUI, and public-RC evidence
gates pass.
```

Avoid wording that implies:

- this is an official Warp Chinese release,
- public RC is ready,
- GUI evidence exists for the current source cycle,
- publishing or tagging has already happened,
- billing/cloud/account/destructive flows were verified with real external
  state.
