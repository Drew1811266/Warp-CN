# zh-Hans Localization Phase 50

Date: 2026-06-02

## Goal

Translate high-confidence visible terminal UI residue while preserving shell, URL, command, serialization, time-format, and diagnostic contracts.

## Scope

Phase 50 added 96 scoped manifest entries:

```text
translated visible entries: 71
reviewed preserve entries: 25
files touched by scoped manifest: 10
main manifest entries after Phase 50: 7184
manifest context/status metadata: 100.0%
```

Translated visible areas:

| Area | Files |
| --- | --- |
| Auth-secret FTUX dropdown and selector | `auth_secret_ftux_dropdown.rs`, `auth_secret_selector.rs` |
| Cloud Agent loading/auth/cancel screens | `loading_screen.rs` |
| Prompt onboarding | `onboarding_prompt_block.rs` |
| Shared-session inline banners | `inline_banner/shared_sessions.rs` |
| Link hover tooltips | `link_detection.rs` |
| Shell termination banner | `shell_terminated_banner.rs` |
| Use Agent footer | `use_agent_footer/mod.rs` |
| Warpify setting descriptions/options | `warpify/settings.rs` |

Reviewed preserves:

| Class | Examples |
| --- | --- |
| View `ui_name` identifiers | `AuthSecretSelector`, `AuthSecretFtuxDropdown`, `OnboardingPromptBlock`, `ShellTerminatedBanner`, `UseAgentToolbar` |
| Serialization enum names | `HighlightedLink`, `Url`, `File` |
| Rule filenames | `AGENTS.md`, `WARP.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md` |
| Formatting/runtime contracts | `%l:%M%P`, `{pty_spawn_error:#}`, `{}CPU, {}GB` |
| Internal diagnostics/thread names | `HighlightedLink is not within...`, `Compute file paths`, base64 decode log |

## Coverage

After Phase 50:

```text
terminal coverage: 1758 covered / 613 candidates = 74.1%
release coverage: 7862 covered / 1086 candidates = 87.9%
```

The Phase 50 target files now have no remaining inventory candidates:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
```

## Safety Review

No URL scheme, shell command, command arg, profile identifier, serialized enum variant, strftime format, prompt fixture text, filename convention, debug error format, or thread name was translated incorrectly.

`cargo check` was intentionally deferred to Phase 54 per the low-load policy because Phase 50 changes are string-only and `cargo fmt --check` passed after formatting.

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase50-manifest.toml --dry-run --summary
# entries: 96
# files: 10
# already_applied: 71
# would_change: 0
# missing: 0

python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

## Qualification

Phase 50 is accepted as `qualified-terminal-visible-ui-backlog-pass-6`.
