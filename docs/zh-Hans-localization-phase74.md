# zh-Hans Localization Phase 74

Date: 2026-06-02 Asia/Shanghai

## Goal

Reduce false-positive inventory noise so coverage reflects user-visible
localization work instead of protocol, fixture, parser, command-template, and
diagnostic residue.

## Baseline Before Ignore Cleanup

Commands:

```text
nice -n 10 python3 script/zh_localization_inventory.py --preset modals --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/ai --coverage
```

Before Phase 74:

```text
modals: 5234 covered, 384 candidates, 93.2%
release: 8568 covered, 388 candidates, 95.7%
terminal: 2150 covered, 224 candidates, 90.6%
AI / Agent: 2537 covered, 160 candidates, 94.1%
```

## Ignore Rules Added

Updated:

- `resources/localization/zh-Hans-inventory-ignore.toml`

Added exact-path ignore rules for reviewed terminal files:

```text
app/src/terminal/find/model.rs
app/src/terminal/history.rs
app/src/terminal/local_tty/docker_sandbox.rs
app/src/terminal/local_tty/server/protocol.rs
app/src/terminal/local_tty/windows/pipes.rs
app/src/terminal/model/block/interaction_mode.rs
app/src/terminal/model/blockgrid.rs
app/src/terminal/model/blocks.rs
app/src/terminal/model/early_output.rs
app/src/terminal/model/iterm_image.rs
app/src/terminal/model/kitty.rs
app/src/terminal/model/session/command_executor.rs
app/src/terminal/package_installers.rs
app/src/terminal/ref_tests/mod.rs
app/src/terminal/writeable_pty/pty_controller.rs
```

Rationale:

- Terminal control/protocol markers and image protocols are not UI copy.
- Ref-test fixtures and filenames must remain stable.
- Package installer and command executor command templates must remain executable.
- Terminal model invariants, async find logs, history diagnostics, PTY/tmux
  diagnostics, and platform identifiers are internal behavior or diagnostic
  strings.

Added exact-path ignore rules for reviewed AI/Agent files:

```text
app/src/ai/agent/api/convert_conversation.rs
app/src/ai/agent/api/convert_from.rs
app/src/ai/blocklist/block/model/model_impl.rs
app/src/ai/blocklist/controller/response_stream.rs
app/src/ai/blocklist/handoff/touched_repos.rs
app/src/ai/blocklist/passive_suggestions/legacy.rs
app/src/ai/llms.rs
app/src/ai/mcp/reconnecting_peer.rs
app/src/ai/skills/file_watchers/utils.rs
app/src/ai/skills/skill_utils.rs
```

Rationale:

- API conversion and response-stream strings are parser/control-flow diagnostics.
- Git URL parsing and skill watcher strings are filenames, directory names, or identifiers.
- Passive suggestion and block model strings are debug diagnostics.
- LLM builtin-label detection literals must remain English because they drive
  the already-localized display-name mapping.
- MCP reconnection strings are connection diagnostics, not stable product UI.

## Files Deliberately Not Ignored

These files remain visible in inventory because they may contain user-visible UI
or composed label fragments:

```text
app/src/terminal/writeable_pty/bootstrap_file/windows.rs
app/src/terminal/links.rs
app/src/terminal/shared_session/role_change_modal/mod.rs
app/src/terminal/view/ambient_agent/view_impl.rs
app/src/terminal/view/block_banner/warpify.rs
app/src/terminal/view/inline_banner/agent_mode_setup.rs
app/src/terminal/view/inline_banner/anonymous_user_ai_sign_up.rs
app/src/terminal/view/inline_banner/aws_cli_not_installed.rs
app/src/terminal/view/inline_banner/shell_process_terminated.rs
app/src/terminal/view/ssh_remote_server_failed_banner.rs
app/src/ai/agent_management/notifications/view.rs
app/src/ai/blocklist/controller/input_context.rs
app/src/ai/agent_sdk/config_file.rs
app/src/ai/blocklist/permissions.rs
app/src/ai/document/ai_document_model.rs
app/src/ai/mcp/templatable.rs
app/src/settings_view/mod.rs
```

## Coverage After Ignore Cleanup

After Phase 74:

```text
modals: 5199 covered, 287 candidates, 94.8%
release: 8533 covered, 291 candidates, 96.7%
terminal: 2135 covered, 159 candidates, 93.1%
AI / Agent: 2517 covered, 128 candidates, 95.2%
```

The lower `covered` counts are expected because exact-path ignore rules remove
both covered and candidate rows from the inventory denominator. Candidate counts
and percentages are the useful Phase 74 signal.

## Checks

Passed:

```text
nice -n 10 python3 -m unittest script/test_zh_localization_inventory.py
4 tests passed

nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

git diff --check
```

## Qualification

Phase 74 is accepted as `qualified-inventory-precision-cleanup`.

The phase is qualified because all new ignore rules are exact-path rules tied to
reviewed non-UI residue, no visible UI or user-facing error path was hidden,
inventory tests passed, and manifest, glossary, and diff checks passed.
