# zh-Hans Localization Phase 64

Date: 2026-06-02 Asia/Shanghai

## Goal

Translate safe terminal residue after RC13 while preserving protocol, fixture,
debug, shell, command-template, OS, and product-contract strings.

## Scope

Created and applied:

- `.omx/tmp-phase64-manifest.toml`

Appended matching entries to:

- `resources/localization/zh-Hans-overrides.toml`

The scoped manifest contains `63` entries across `18` terminal files. It
translated `60` visible/user-facing strings and recorded `3` preserve entries.

## Translated Areas

- Codex and OpenCode plugin setup instructions.
- Inline model selector tabs, warnings, and management action.
- Rewind menu labels and accessibility text.
- Windows named-pipe and WSL registry user-facing errors.
- PTY recorder toasts and file-open action.
- Rich history metadata labels.
- New-session shell schema descriptions.
- Ambient Agent harness, host, and model selector copy.
- GitHub auth blocked copy for child Agent startup.
- Warp Drive sharing onboarding block.
- Init-environment prompt and cancellation state.
- Plugin instruction block help/copy/remote-session copy.
- Shared-session inactivity modal.
- Warpify success block.

## Preserved

The following residue stayed preserve-first:

- `app/src/terminal/model/blockgrid.rs`
- `app/src/terminal/model/blocks.rs`
- `app/src/terminal/model/block/interaction_mode.rs`
- `app/src/terminal/model/session/command_executor.rs`
- `app/src/terminal/package_installers.rs`
- `app/src/terminal/ref_tests/mod.rs`
- `app/src/terminal/writeable_pty/bootstrap_file/windows.rs`
- `app/src/terminal/find/model.rs`
- `app/src/terminal/history.rs`
- `app/src/terminal/local_tty/docker_sandbox.rs`
- `app/src/terminal/local_tty/server/protocol.rs`
- `app/src/terminal/model/iterm_image.rs`

Reasons include terminal model invariants, log/debug diagnostics, package
installer command templates, ref-test filenames, bootstrap script errors,
terminal protocol payloads, and image protocol fields.

## Scoped Dry-Run

After applying the scoped manifest:

```text
entries: 63
files: 18
already_applied: 60
would_change: 0
missing: 0
```

`already_applied` is `60` because the `3` preserve entries have
`source == target` and do not count as changed or already-applied replacements
in the script summary.

## Terminal Inventory After Phase 64

```text
| candidates | path |
| ---: | --- |
| 6 | app/src/terminal/model/blockgrid.rs |
| 6 | app/src/terminal/model/blocks.rs |
| 5 | app/src/terminal/model/block/interaction_mode.rs |
| 5 | app/src/terminal/model/session/command_executor.rs |
| 5 | app/src/terminal/package_installers.rs |
| 5 | app/src/terminal/ref_tests/mod.rs |
| 5 | app/src/terminal/writeable_pty/bootstrap_file/windows.rs |
| 4 | app/src/terminal/find/model.rs |
| 4 | app/src/terminal/history.rs |
| 4 | app/src/terminal/local_tty/docker_sandbox.rs |
| 4 | app/src/terminal/local_tty/server/protocol.rs |
| 4 | app/src/terminal/model/iterm_image.rs |
| 4 | app/src/terminal/view/init_project/lsp_server_selector.rs |
| 4 | app/src/terminal/view/inline_banner/aws_bedrock_login.rs |
| 4 | app/src/terminal/view/inline_banner/ssh.rs |
| 4 | app/src/terminal/view/open_in_warp.rs |
| 4 | app/src/terminal/view/queued_prompts_panel.rs |
| 4 | app/src/terminal/view/shared_session/viewer.rs |
| 4 | app/src/terminal/writeable_pty/pty_controller.rs |
| 4 | app/src/terminal/wsl/model.rs |
```

The previous visible UI cluster no longer leads the terminal queue. The
remaining top paths are dominated by preserve-first model, protocol, command,
fixture, and diagnostic strings, plus a new lower-count batch for future
review.

## Validation

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase64-manifest.toml --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase64-manifest.toml --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase64-manifest.toml --dry-run --summary
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt
nice -n 10 cargo fmt --check
git diff --check
```

Python tests:

```text
19 tests passed
```

## Low-Load Review

Commands were run serially with `nice -n 10` where appropriate. No GUI,
account, backend, static image, or destructive state was touched. No Rust
compile gate was run in this phase; the plan reserves `cargo check -j 2 -p warp`
for the final freeze gate unless a compile-only issue requires it sooner.

## Qualification

Phase 64 is accepted as `qualified-terminal-residue-pass-10`.

The phase is qualified because scoped dry-run is clean, terminal visible UI
residue decreased, remaining top terminal residue is documented as
preserve-first or queued for later review, and manifest validation, glossary,
Python tests, formatting, and diff checks passed.
