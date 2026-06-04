# zh-Hans Localization Phase 34

Date: 2026-06-01

## Goal

Reduce Terminal backlog while preserving shell, tmux, parser, and terminal protocol behavior.

## Scope

Phase 34 added `185` Terminal manifest entries:

- `82` translated visible/user-facing entries.
- `103` reviewed preserves for parser/protocol/internal/test/log strings.

Primary touched areas:

- `app/src/terminal/input/models/data_source.rs`
- `app/src/terminal/input/terminal_message_bar.rs`
- `app/src/terminal/universal_developer_input.rs`
- `app/src/terminal/ssh/install_tmux.rs`
- `app/src/terminal/model/secrets.rs`
- `app/src/terminal/writeable_pty/remote_server_controller.rs`
- `app/src/terminal/view/block_onboarding/onboarding_agentic_suggestions_block.rs`
- `app/src/terminal/local_tty/terminal_manager.rs`
- `app/src/terminal/view/load_ai_conversation.rs`
- Reviewed preserve coverage for tmux parser, grid handler, early output, command examples, diagnostics, and test fixtures.

## Translated Classes

- Universal input tooltips: context attachment, file attachment, slash commands, voice input, terminal/Agent mode.
- Terminal message-bar hints: new conversation, plan with Agent, continue conversation, execute/send/open actions, autodetected mode, attached command/text context.
- Model picker and inference hints: Bedrock/API-key inference, free-user upgrade hint, selected/disabled markers.
- SSH/tmux install prompts and Warpify explanations.
- Secret detector display labels where provider/product names are preserved.
- Local terminal sharing fallback errors.
- Conversation restore directory prompts.
- Agentic onboarding suggestion prompts that are visible to the user.

## Preserved Classes

- tmux protocol literals such as `%end`, `%error`, `%output`, and window-close events.
- Parser state names and internal parse diagnostics.
- ANSI/grid control internals and typeahead debug messages.
- SSH test hostnames, command examples, shell paths, OS names, and telemetry labels.
- Claude/Agent restore diagnostics that are logs rather than UI copy.
- Component/debug identifiers such as `TerminalInputMessageBar` and block view names.

## Coverage

```text
terminal before: 1231 covered / 1134 candidates = 52.1%
terminal after: 1434 covered / 932 candidates = 60.6%
release after: 7100 covered / 1835 candidates = 79.5%
```

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase34-manifest.toml --dry-run --summary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

Scoped dry-run:

```text
entries: 185
files: 12
already_applied: 82
would_change: 0
missing: 0
```

## Qualification

Phase 34 is accepted as `qualified-terminal-backlog-pass-4-low-load`.

The phase is qualified because Terminal coverage exceeded the `58.0%` target, all scoped replacements are applied or intentionally preserved, and the validation gate passed without shell/protocol/tmux literal localization errors.
