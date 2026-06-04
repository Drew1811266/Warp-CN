# zh-Hans Translation Audit 0.19

Date: 2026-06-04

## Scope

This audit covers the adaptation from `0.18 / RC38` to upstream stable `v0.2026.06.03.09.49.stable_00`.

## Results

```text
manifest validation: passed
glossary check: passed
dry-run: entries=7937 files=550 already_applied=5717 would_change=0 missing=0
release inventory coverage: covered=8534 candidates=0 coverage=100.0%
```

## Reviewed 0.19 Hotspots

- Vertical tab group menu labels, rename defaults, and fallback group names.
- Queued prompt panel tooltips and immediate-send actions.
- Default prompt submission mode settings copy.
- Shared-session run metadata access messaging.
- Staging IAP credential status labels and refresh action.
- Claude Code platform plugin install/update failure copy.
- Agent orchestration duplicate-child guidance.
- Internal orchestration viewer logs, SSE diagnostics, protocol IDs, config keys, test assertions, and position IDs were explicitly ignored rather than translated.

## Public-RC Posture

The 0.19 source overlay can be considered a local-use candidate only after command-line and bundle gates pass. It is not a public RC until current-cycle GUI evidence and strict public-RC evidence lint pass.
