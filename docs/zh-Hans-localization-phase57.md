# zh-Hans Localization Phase 57

Date: 2026-06-02 Asia/Shanghai

## Goal

Reduce terminal-facing residue in CLI agent sessions, ambient-agent blocks, zero-state content, docker sandbox errors, prompt suggestions, SSH choice views, and Warpify footer copy while preserving session, plugin, shell, OS, and bootstrap contracts.

## Scope

Scoped manifest:

- `.omx/tmp-phase57-manifest.toml`

Primary files:

- `app/src/terminal/cli_agent_sessions/listener/mod.rs`
- `app/src/terminal/cli_agent_sessions/plugin_manager/mod.rs`
- `app/src/terminal/view/ambient_agent/model.rs`
- `app/src/terminal/view/ambient_agent/block/entry.rs`
- `app/src/terminal/view/ambient_agent/first_time_setup.rs`
- `app/src/terminal/view/docker_sandbox/mod.rs`
- `app/src/terminal/view/inline_banner/open_in_warp.rs`
- `app/src/terminal/view/inline_banner/prompt_suggestions.rs`
- `app/src/terminal/view/zero_state_block.rs`
- `app/src/terminal/view/agent_view.rs`
- `app/src/terminal/view/ssh_remote_server_choice_view.rs`
- `app/src/terminal/view/use_agent_footer/warpify_footer.rs`
- `app/src/terminal/ssh/warpify.rs`

## Changes

Added `91` scoped manifest entries:

- `67` source replacements applied.
- `24` reviewed preserves.

Translated visible areas:

- CLI agent plugin install/update errors and success toasts.
- SSH Warpify title, description, and docs link.
- Agent view start/send hints and user-facing blocked state.
- Ambient-agent default title, setup progress, task status, first-time setup copy, docs link, and free-credit banner.
- Docker sandbox user-facing setup errors.
- Open-in-Warp inline banner copy and actions.
- Prompt suggestion tooltips and query prompts.
- SSH remote-server choice dialog labels, descriptions, checkbox, and settings link.
- Warpify/use-Agent footer buttons and tooltips.
- Terminal zero-state title, shortcut hints, NLD hint, and dismiss action.

Reviewed preserves:

- CLI agent notification test fixtures and shell-command fixtures.
- CLI command transcript formats such as `$ {display_cmd}n`.
- SSH bootstrap hook `InitSsh`, OS selector `Darwin`, and view identifiers.
- Diagnostic logs and internal invariants in agent view and ambient-agent model.
- Docker sandbox environment ID and internal `view dropped` async errors.
- Accessibility/position ID `open_in_warp_banner_button_{view_id}`.

## Review Results

Scoped dry-run after apply:

```text
entries: 91
files: 13
already_applied: 67
would_change: 0
missing: 0
```

Target-file inventory after apply:

```text
no remaining candidates
```

Coverage:

```text
terminal: 2040 covered / 334 candidates = 85.9%
release: 8260 covered / 693 candidates = 92.3%
```

Manifest metadata:

```text
entries: 7549
context: 7549 (100.0%)
status: 7549 (100.0%)
expected_count: 181 (2.4%)
```

## Validation

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase57-manifest.toml --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase57-manifest.toml --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py <phase57 files> --status candidate
nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt --check
git diff --check <phase57 files and manifests>
```

`cargo fmt --check` initially reported formatting-only wrapping differences after string replacement; `nice -n 10 cargo fmt` was run, and the follow-up check passed.

## Low-Load Review

All checks were run serially. No GUI was launched, no Rust compile gate was run, and no account/backend/destructive state was touched.

## Qualification

Phase 57 is accepted as `qualified-terminal-cli-ambient-zero-state-pass`.

The phase is qualified because the scoped dry-run is clean, target files have no remaining candidates, terminal/release coverage improved, manifest validation and glossary passed, Python localization tests passed, formatting and diff checks passed, and CLI/session/shell/bootstrap contracts were preserved with explicit context.
