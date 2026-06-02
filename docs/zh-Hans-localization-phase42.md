# zh-Hans Localization Phase 42

Date: 2026-06-02

## Goal

Reduce terminal backlog residue while preserving terminal protocol, shell command, ANSI, tmux, ConPTY, WSL, parser, URL, and telemetry contracts.

## Scope

Phase 42 added 174 scoped manifest entries:

```text
translated visible entries: 74
reviewed preserve entries: 100
files touched by scoped manifest: 14
main manifest entries after Phase 42: 6960
manifest context/status metadata: 100.0%
```

Translated visible terminal copy:

| Area | Files |
| --- | --- |
| Terminal settings | `app/src/terminal/settings.rs`, `app/src/terminal/session_settings/working_directory_config.rs` |
| Prompt/loading states | `app/src/terminal/prompt_render_helper.rs` |
| Terminal tooltips | `app/src/terminal/view/tooltips.rs` |
| SSH file upload | `app/src/terminal/view/ssh_file_upload.rs` |
| Shared-session tombstone/menu/toasts | `app/src/terminal/view/shared_session/conversation_ended_tombstone_view.rs`, `app/src/terminal/view/shared_session/view_impl.rs` |

Reviewed preserves:

| Class | Files |
| --- | --- |
| Shell command templates and env vars | `app/src/terminal/local_shell/mod.rs`, `app/src/terminal/local_tty/unix.rs` |
| Windows ConPTY/WSL/PTTY diagnostics and API symbols | `app/src/terminal/local_tty/windows/conpty_api.rs`, `app/src/terminal/local_tty/windows/mod.rs` |
| ANSI/control-sequence and terminal-grid invariants | `app/src/terminal/model/grid/ansi_handler.rs` |
| tmux command literals and parser regexes | `app/src/terminal/model/tmux/commands.rs` |
| Shared-session telemetry/status/URL templates | `app/src/terminal/shared_session/mod.rs` |
| Prompt/save-position IDs | `app/src/terminal/prompt_render_helper.rs` |

## Coverage

Baseline from RC10:

```text
terminal coverage: 1448 covered / 918 candidates = 61.2%
release coverage: 7427 covered / 1514 candidates = 83.1%
```

After Phase 42:

```text
terminal coverage: 1639 covered / 731 candidates = 69.2%
release coverage: 7618 covered / 1327 candidates = 85.2%
```

The Phase 42 target files now have no remaining inventory candidates:

```text
python3 script/zh_localization_inventory.py --status candidate \
  app/src/terminal/settings.rs \
  app/src/terminal/prompt_render_helper.rs \
  app/src/terminal/session_settings/working_directory_config.rs \
  app/src/terminal/view/tooltips.rs \
  app/src/terminal/view/ssh_file_upload.rs \
  app/src/terminal/view/shared_session/conversation_ended_tombstone_view.rs \
  app/src/terminal/view/shared_session/view_impl.rs \
  app/src/terminal/local_shell/mod.rs \
  app/src/terminal/local_tty/unix.rs \
  app/src/terminal/local_tty/windows/conpty_api.rs \
  app/src/terminal/local_tty/windows/mod.rs \
  app/src/terminal/model/grid/ansi_handler.rs \
  app/src/terminal/model/tmux/commands.rs \
  app/src/terminal/shared_session/mod.rs
```

Result:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
```

## Safety Review

No terminal command, env var, escape sequence, tmux literal, WSL/ConPTY API literal, telemetry status, URL template, or prompt position ID was localized. These were recorded as active preserve entries in the manifest instead.

User-visible strings translated in this phase preserve product terms required by the glossary, including `Warp` and `Agent`.

`cargo check` was intentionally not run in this phase because the changes are string-only, `cargo fmt --check` passed, and the low-load policy reserves Rust builds for Phase 48 or runtime-code changes.

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase42-manifest.toml --dry-run --summary
# entries: 174
# files: 14
# already_applied: 74
# would_change: 0
# missing: 0

python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

## Qualification

Phase 42 is accepted as `qualified-terminal-backlog-pass-5`.
