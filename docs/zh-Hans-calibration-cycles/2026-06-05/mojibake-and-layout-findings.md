# zh-Hans Mojibake And Layout Findings

This report is static and low-load. It does not prove GUI rendering readiness.

- Total findings: 6
- Actionable findings: 0

## Findings

| file | line | category | decision | snippet |
| --- | ---: | --- | --- | --- |
| `app/assets/bundled/bootstrap/subshell_bootstrap_block_command.txt` | 1 | `terminal-ansi-sequence` | `accepted-token` | \x1b[1;32mSuccess!\x1b[0m This subshell spawned by \x1b[1;34m%\x1b[0m has been Warpified. |
| `crates/editor/test_data/test_rust_file.rs` | 6289 | `replacement-character` | `fixture-only` | /// [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD], which looks like this: \ufffd |
| `crates/editor/test_data/test_rust_file.rs` | 6329 | `replacement-character` | `fixture-only` | /// assert_eq!("Hello \ufffdWorld", output); |
| `docs/zh-Hans-localization-calibration-plan.md` | 234 | `replacement-character` | `example-only` | - \u4e0d\u5305\u542b\u66ff\u6362\u5b57\u7b26 `\ufffd`\u3002 |
| `docs/zh-Hans-localization-calibration-plan.md` | 235 | `mojibake-signature` | `example-only` | - \u4e0d\u5305\u542b\u5178\u578b mojibake \u7247\u6bb5\uff0c\u4f8b\u5982 `\xc3`, `\xc2`, `\xe2\u20ac\u2122`, `\xe4\xb8`\u3002 |
| `docs/zh-Hans-localization-calibration-plan.md` | 471 | `replacement-character` | `example-only` | rg -n '\ufffd/\xc3/\xc2/\xe2\u20ac\u2122/\xe2\u20ac\u0153/\xe2\u20ac/\xe4\xb8/\xe5[\\\\x80-\\\\xBF]' resources/localization app crates docs |
