# zh-Hans Localization Phase 27

Date: 2026-06-01

## Goal

Raise Terminal source-level coverage while preserving terminal behavior, shell commands, parser/protocol literals, environment variables, and debug/test fixtures.

## Scope

Reviewed and updated Phase 27 manifest coverage for:

- `app/src/terminal/input.rs`
- `app/src/terminal/event.rs`
- `app/src/terminal/available_shells.rs`
- `app/src/terminal/cli_agent.rs`
- `app/src/terminal/local_tty/shell.rs`
- `app/src/terminal/cli_agent_sessions/plugin_manager/claude.rs`
- `app/src/terminal/cli_agent_sessions/plugin_manager/gemini.rs`
- `app/src/terminal/model/session.rs`
- `app/src/terminal/model/terminal_model.rs`
- `app/src/terminal/shared_session/sharer/network.rs`
- `app/src/terminal/view/init.rs`

## Manifest Changes

Phase 27 added `284` manifest entries:

- `77` translated visible or user-facing Terminal strings.
- `207` reviewed preserves for shell commands, parser/protocol/debug strings, environment variables, product names, and test fixtures.

The preserved entries are intentional. They include command templates, shell probes, protocol literals, model/provider names, plugin identifiers, file paths, and diagnostic/test strings that should not be localized without changing runtime behavior or matching contracts.

## Coverage

Terminal preset coverage improved from the Phase 27 baseline:

| Preset | Before Phase 27 | After Phase 27 |
| --- | ---: | ---: |
| Terminal | `873 covered / 1455 candidates = 37.5%` | `1231 covered / 1134 candidates = 52.1%` |
| Release | `5955 covered / 2940 candidates = 66.9%` | `6313 covered / 2619 candidates = 70.7%` |

## Validation

Passed:

- `python3 script/zh_apply_localization.py --validate-manifest`
- `python3 script/zh_apply_localization.py --check-glossary`
- Phase 27 scoped dry-run using the existing replacement engine:
  - `phase27_entries: 284`
  - `entries: 284`
  - `files: 11`
  - `already_applied: 77`
  - `would_change: 0`
  - `missing: 0`
- `python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py`
- `cargo fmt --check`
- `git diff --check`

The initial full-manifest dry-run exposed one invalid embedded quote in the Claude plugin post-install note. The source and manifest target were corrected to avoid an unescaped Rust string quote.

Because the local machine became hot during full-manifest scanning, Phase 27 uses the scoped Phase 27 dry-run as its phase-local qualification gate. A full manifest dry-run remains required in Phase 32 before RC9 status is assigned.

## Remaining Terminal Risk Classes

- Parser probes, shell startup probes, escape sequences, and tmux/control-mode literals remain preserved.
- Shell commands and command templates remain preserved.
- Environment variable names, plugin identifiers, provider/model names, and file paths remain preserved.
- Debug/log/test-fixture strings are reviewed preserves unless they are clearly surfaced to users.

## Qualification

Phase 27 is accepted as `qualified-terminal-backlog-pass-3-low-load`.

No GUI row is promoted by this source-only pass. No account, billing quota, cloud environment, secret, or team ownership state was touched.
