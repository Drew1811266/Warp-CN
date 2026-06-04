# zh-Hans Localization Phase 72

Date: 2026-06-02 Asia/Shanghai

## Goal

Translate safe remaining terminal UI and user-facing copy while preserving
terminal protocols, shell contracts, tests, bootstrap text, command templates,
and diagnostics.

## Scoped Manifest

Created:

- `.omx/tmp-phase72-manifest.toml`

Appended `41` active manifest entries to:

- `resources/localization/zh-Hans-overrides.toml`

## Translated Files

Applied the scoped manifest to `14` terminal files:

```text
app/src/terminal/alt_screen_reporting.rs
app/src/terminal/block_list_settings.rs
app/src/terminal/input/conversations/mod.rs
app/src/terminal/input/inline_menu/message_provider.rs
app/src/terminal/input/skills/data_source.rs
app/src/terminal/view/ambient_agent/block/harness_session_header.rs
app/src/terminal/view/ambient_agent/block/setup_command_text.rs
app/src/terminal/view/ambient_agent/footer.rs
app/src/terminal/view/init_project/lsp_server_selector.rs
app/src/terminal/view/inline_banner/aws_bedrock_login.rs
app/src/terminal/view/inline_banner/ssh.rs
app/src/terminal/view/open_in_warp.rs
app/src/terminal/view/queued_prompts_panel.rs
app/src/terminal/view/shared_session/viewer.rs
```

Translated UI families:

- Terminal settings descriptions for alternate-screen reporting and block list behavior.
- Inline menu keyboard hints for conversation and skill menus.
- Skill menu empty state and project-skill badge.
- Project initialization language-support prompt and actions.
- AWS Bedrock and SSH inline banners.
- Open-in-Warp accessibility labels and help text.
- Queued prompt panel tooltips and header.
- Shared-session role menu items.
- Ambient Agent harness, setup-command, startup, and failure labels.

## Preserved

Preserved the remaining candidate families in this pass:

- Terminal block model invariants and diagnostics.
- Ref-test fixture filenames and assertions.
- Windows bootstrap filenames and shell snippets.
- Terminal server, iTerm, Kitty, tmux, and PTY protocol/control strings.
- Docker sandbox identifiers and package-manager command templates.
- Async find, shell history, shared-session internal diagnostics, and WSL identifiers.
- Shortcut label fragments in `app/src/terminal/links.rs`, pending a targeted
  composed-shortcut review.

## Checks

Scoped manifest validation:

```text
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase72-manifest.toml --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase72-manifest.toml --check-glossary
glossary check passed
```

Scoped dry-run after apply:

```text
entries: 41
files: 14
already_applied: 41
would_change: 0
missing: 0
```

Global checks:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
19 tests passed

nice -n 10 cargo fmt
nice -n 10 cargo fmt --check
git diff --check
```

The first `cargo fmt --check` reported one formatting-only diff in
`app/src/terminal/view/init_project/lsp_server_selector.rs`; `cargo fmt` was run
and the follow-up `cargo fmt --check` and `git diff --check` passed.

## Coverage Movement

Terminal coverage after Phase 72:

```text
covered: 2150
candidates: 224
coverage: 90.6%
```

RC14 terminal baseline:

```text
covered: 2106
candidates: 268
coverage: 88.7%
```

Remaining top terminal paths are mostly preserve-first contracts and internal
diagnostics:

```text
app/src/terminal/model/blockgrid.rs
app/src/terminal/model/blocks.rs
app/src/terminal/model/block/interaction_mode.rs
app/src/terminal/model/session/command_executor.rs
app/src/terminal/package_installers.rs
app/src/terminal/ref_tests/mod.rs
app/src/terminal/writeable_pty/bootstrap_file/windows.rs
app/src/terminal/local_tty/server/protocol.rs
app/src/terminal/model/iterm_image.rs
app/src/terminal/writeable_pty/pty_controller.rs
```

## Qualification

Phase 72 is accepted as `qualified-terminal-residue-pass-11`.

The phase is qualified because the scoped dry-run reports `would_change: 0` and
`missing: 0`, the terminal coverage improved from `88.7%` to `90.6%`,
preserve-first residue is documented, and manifest validation, glossary,
Python localization tests, formatting, and diff checks passed.
