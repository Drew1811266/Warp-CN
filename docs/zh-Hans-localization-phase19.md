# zh-Hans Localization Phase 19

Date: 2026-06-01

## Goal

Recover low-load GUI evidence after RC7 and use local fixtures or reproducible blockers without rebuilding the bundle or using account/server-state resources.

## Low-Load Policy

- Reused the existing `target/debug/bundle/osx/WarpOss.app`.
- Did not run `./script/run`, bundle rebuild, or `cargo check`.
- Launched `warp-oss` with `WARP_DATA_PROFILE=zh-p19-lowload`, `WARP_SKIP_COMMON_SKILLS_INSTALL=1`, and `nice -n 10`.
- Stopped the launched `warp-oss` and child `terminal-server` processes after capture.

## Evidence

Computer Use successfully read the local `WarpOss` window and menu bar.

Captured:

- `docs/gui-smoke-artifacts/phase19/p19-settings-agent-readable.png`
- `docs/gui-smoke-artifacts/phase19/p19-command-palette-readable.png`
- `docs/gui-smoke-artifacts/phase19/p19-warp-drive-english-residue.png`

Current-cycle verified rows:

- `GUI-BASE-02`: command palette / command search anchors.
- `GUI-SET-01`: settings shell and settings navigation anchors.

## Finding And Fix

The logged-out Warp Drive settings page still showed English copy:

- `To use Warp Drive, please create an account.`
- `Sign up`
- `Warp Drive is a workspace in your terminal where you can save Workflows, Notebooks, Prompts, and Environment Variables for personal use or to share with a team.`

Added Phase 19 manifest entries and applied source replacements in `app/src/settings_view/warp_drive_page.rs`.

Because this phase intentionally avoided rebuilding the app, the after-fix visual confirmation is deferred to the next bundle/GUI gate.

## Still Blocked / Needs Fixture

The following remain blocked or needs-trigger with concrete causes:

| Row | Cause |
| --- | --- |
| `GUI-ONB-01` | Requires fresh onboarding state and Agent path trigger. |
| `GUI-AUTH-02` | Requires token fallback trigger or invalid token fixture. |
| `GUI-AUTH-03` | Requires fresh onboarding/login privacy or skip-login path. |
| `GUI-AGENT-01` | Requires Agent input/tips fixture. |
| `GUI-AGENT-03` | Requires Agent lifecycle state fixture. |
| `GUI-AGENT-04` | Requires Agent error fixture. |
| `GUI-AGENT-05` | Requires environment modal fallback fixture. |

No main account, billing quota, cloud environment, secret, or team ownership state was used.

## Validation

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --dry-run --summary
entries: 4379
files: 255
already_applied: 3574
would_change: 0
missing: 0
```

## Decision

Phase 19 is accepted as `qualified-low-load-gui-source-fix`.

Proceed to Phase 20: public-RC account and server-state runbooks.
