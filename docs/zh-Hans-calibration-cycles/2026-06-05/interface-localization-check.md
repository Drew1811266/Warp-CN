# Interface Localization Check 2026-06-05

This report checks whether the internal Warp CN interfaces are localized
completely enough for source-level review. It does not claim runtime GUI
acceptance because the high-load gate blocked app launch.

## Runtime Boundary

The GUI gate was run before app launch:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Result:

```text
probe 1: load=3.02 3.01 3.11
probe 1: hot_process=WindowServer 32.3%
probe 1: hot_process=Codex (Service) 25.9%
probe 2: load=2.27 2.78 3.01
probe 2: hot_process=WindowServer 28.2%
decision: defer-heavy-gate
```

Because the gate returned `defer-heavy-gate`, the following were not run:

- `cargo check`
- `./script/run`
- Opening `WarpOss.app`
- Computer Use GUI automation
- Runtime log probes

## Static Interface Coverage

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| onboarding | 323 | 0 | 100.0% |
| workspace | 865 | 0 | 100.0% |
| search | 269 | 0 | 100.0% |
| settings | 2,024 | 0 | 100.0% |
| modals | 5,240 | 2 | 100.0% |
| release | 8,574 | 2 | 100.0% |

The 2 candidate rows are both `Agent`:

| Path | Line | Literal | Decision |
| --- | ---: | --- | --- |
| `app/src/ai/blocklist/usage/rollup.rs` | 151 | `Agent` | Preserve product term. |
| `app/src/terminal/view/ambient_agent/block/harness_session_header.rs` | 35 | `Agent` | Preserve product term. |

`Agent` is listed in `resources/localization/zh-Hans-glossary.toml` as a
preserved project term.

## Confirmed Source-Level Interface Gaps

The broad inventory is complete, but Task 7's visible-UI queue still exposes
several likely user-visible English strings. These should be fixed or explicitly
owner-approved before saying the UI is fully localized.

| Path | Literal | Current assessment |
| --- | --- | --- |
| `app/src/ai/blocklist/inline_action/code_diff_view.rs` | `Accept and continue with agent` | Visible button label; should be translated. |
| `app/src/ai/blocklist/inline_action/code_diff_view.rs` | `Iterate with agent` | Visible button label; should be translated. |
| `app/src/settings_view/referrals_page.rs` | ` If you have any questions about the referral program, please contact referrals@warp.dev.` | Visible referral terms/contact text; should be translated while preserving email address. |
| `app/src/settings_view/teams_page.rs` | `Need more seats? ` | Visible teams billing/upgrade CTA prefix; should be translated. |

## Reviewed False Positives

| Path | Literal | Decision |
| --- | --- | --- |
| `app/src/settings_view/about_page.rs` | `about warp version` | Settings search terms, not normal visible prose. |
| `app/src/workspace/close_session_confirmation_dialog.rs` | `Close session button pressed with no open confirmation dialog source` | Internal warning/log path; dialog UI itself is Chinese. |
| `app/src/ai/ai_document_view.rs` | `Skipping sending updated plan: conversation is not in progress` | Internal diagnostic path. |

## Mojibake

Fresh static scan result:

```text
total findings: 6
actionable findings: 0
```

The remaining findings are accepted ANSI/test-fixture/documentation examples,
not product UI text.

## Conclusion

Source-level interface coverage is strong, but the software cannot be called
fully GUI-verified in this cycle:

- Core interface presets are covered at 100.0%.
- No actionable product-text mojibake was found.
- Four likely visible English UI strings remain and should be corrected or
  owner-approved.
- Runtime GUI completeness is `not-evaluated` because app launch and Computer
  Use inspection were blocked by the high-load gate.
