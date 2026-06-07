# zh-Hans Low-Load Performance Probe

This report records low-load script timing only. It does not evaluate app runtime performance.

## Heat-Safety Decision

Low-load calibration commands were run separately in this cycle. The timing
probe did not repeat the full audit commands, to avoid unnecessary CPU load and
heat after the 7,943-row audit had already completed successfully.

## Low-Load Commands

| command | exit | seconds | stdout summary | stderr summary |
| --- | ---: | ---: | --- | --- |

No duplicate timing run was performed in this report.

## High-Load Runtime Work

- Status: `gate-run-deferred`
- Runtime performance readiness: `not-evaluated`

The high-load gate was run after a later user request and returned
`defer-heavy-gate`; see `high-load-gate-2026-06-05.md`.

The following high-load commands were not run:

- `cargo fmt --check`
- `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- `open -n target/debug/bundle/osx/WarpOss.app`
- `GUI automation and runtime log probes`
