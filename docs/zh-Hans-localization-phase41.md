# zh-Hans Localization Phase 41

Date: 2026-06-02

## Goal

Convert RC10's remaining top candidates into a safe RC11 execution queue before changing more source strings.

## Baseline

RC10 state:

```text
manifest entries: 6786
dry-run: would_change 0, missing 0
release coverage: 83.1%
terminal coverage: 61.2%
AI / Agent coverage: 78.0%
settings coverage: 99.9%
workspace coverage: 99.9%
modals coverage: 73.1%
```

## Low-Load Inventory

Re-ran low-load top-path inventories for:

```text
python3 script/zh_localization_inventory.py --preset release --top-paths 20
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
python3 script/zh_localization_inventory.py app/src/terminal --top-paths 20
python3 script/zh_localization_inventory.py app/src/ai --top-paths 20
```

The largest remaining release/modals and terminal buckets overlap heavily:

| Candidates | Path | Phase 41 classification |
| ---: | --- | --- |
| 15 | `app/src/terminal/local_tty/windows/mod.rs` | Mostly Windows ConPTY/WSL process diagnostics; translate only CLI/user-facing failures if surfaced, preserve internal logs/API strings. |
| 15 | `app/src/terminal/model/grid/ansi_handler.rs` | ANSI/protocol/control-sequence internals; preserve or ignore after inspection. |
| 14 | `app/src/terminal/local_shell/mod.rs` | Shell/PTY diagnostics and command construction; classify before translating. |
| 14 | `app/src/terminal/local_tty/unix.rs` | Unix PTY diagnostics and shell startup strings; classify before translating. |
| 14 | `app/src/terminal/local_tty/windows/conpty_api.rs` | Windows API/loader internals; preserve. |
| 14 | `app/src/terminal/settings.rs` | Visible terminal settings copy; translate in Phase 42. |
| 13 | `app/src/terminal/model/tmux/commands.rs` | tmux command literals/contracts; preserve. |
| 13 | `app/src/terminal/session_settings/working_directory_config.rs` | Working-directory config copy plus path examples; translate visible UI only. |
| 13 | `app/src/terminal/shared_session/mod.rs` | Shared-session user-facing copy plus protocol internals; split in Phase 42. |
| 13 | `app/src/terminal/view/ambient_agent/auth_secret_ftux_view.rs` | Visible auth-secret FTUX; translate in Phase 44. |

AI/Agent buckets:

| Candidates | Path | Phase 41 classification |
| ---: | --- | --- |
| 12 | `app/src/ai/mcp/file_mcp_watcher.rs` | File watcher internals plus possibly surfaced MCP config/env errors; translate user-facing failures, preserve paths/watcher internals. |
| 12 | `app/src/ai/skills/file_watchers/skill_watcher.rs` | Skill watcher internals; preserve `SKILL.md` and path literals, translate surfaced watcher errors only if visible. |
| 10 | `app/src/ai/agent_sdk/driver/attachments.rs` | Attachment download/read/size diagnostics; translate user-facing errors, preserve debug logs and file templates. |
| 10 | `app/src/ai/blocklist/action_model/execute/run_agents.rs` | Child-agent launch user-facing errors plus prompt templates; translate errors, preserve prompt/protocol fragments. |
| 10 | `app/src/ai/blocklist/controller/shared_session.rs` | Shared-session control flow; classify before translating. |
| 9 | `app/src/ai/agent_sdk/artifact_upload.rs` | Artifact upload errors; translate only surfaced errors. |
| 9 | `app/src/ai/ambient_agents/task.rs` | Agent task labels/status; verify against existing glossary in Phase 44. |
| 9 | `app/src/ai/artifacts/buttons.rs` | Visible artifact buttons; translate in Phase 43 if still uncovered. |
| 9 | `app/src/ai/blocklist/inline_action/search_codebase.rs` | Search UI/action copy; translate visible labels, preserve tool contract keys. |
| 9 | `app/src/ai/mcp/mod.rs` | MCP visible labels plus protocol/config internals; split in Phase 43. |

## Sampled Candidate Decisions

High-confidence Phase 42 translations:

- `Terminal block spacing.`
- `Normal`
- `Compact`
- `How padding is applied in full-screen terminal apps.`
- `Use the same padding as the block list.`
- `Use a custom uniform padding value.`
- `Whether to play an audible bell sound on terminal bell events.`
- `Controls the spacing between terminal blocks.`
- `The maximum number of rows in the terminal grid.`
- `Controls padding around full-screen terminal applications.`
- `Whether to show the AI zero-state block in new terminal sessions.`
- `Use an improved implementation of find to keep the UI responsive while searching for matches on large outputs.`

High-confidence Phase 44 translations:

- `e.g. My API Key`
- `Failed to save API key: {error}`
- `Please enter a name for the secret.`
- `API key '{name}' saved.`
- `Enter your credentials below.`
- `Select an API key type to use {display_name} in the cloud with Oz.`
- `Your credentials are encrypted end-to-end.  `
- `Learn more about authentication for {harness_name} in Warp.`
- `Share with team`
- `Back`
- `Cancel`
- `Continue`

High-confidence preserves:

- ANSI escape sequences such as `x1b[?62c`, `x1b[>{version}c`, `x1b[{};{}R`, and OSC clipboard/query strings.
- Terminal model assertions such as `the alt screen grid should never put any rows in flat storage`.
- Windows ConPTY loader/API strings and debug process-start logs.
- `SKILL.md` filenames.
- Attachment filename templates such as `task_attachment_{index}`.
- Prompt/protocol templates such as `{base_prompt}nn{per_agent_prompt}`.

## Phase Queue

| Phase | Scope |
| --- | --- |
| Phase 42 | Terminal settings, shared-session, SSH upload, terminal tooltips, and reviewed terminal preserves. |
| Phase 43 | MCP watcher, skill watcher, attachments, artifact upload, child-agent run errors, artifact buttons, and AI/MCP preserves. |
| Phase 44 | Auth-secret FTUX translations and local Agent fixture evidence or exact fixture blockers. |
| Phase 45 | Static onboarding PNG visual-residue policy. |
| Phase 46 | Public-RC isolated account/backend evidence if safe prerequisites exist; otherwise blocker audit. |
| Phase 47 | RC11 language quality and behavioral safety review. |
| Phase 48 | RC11 final gate and release decision. |

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
git diff --check docs/zh-Hans-localization-phase41.md
```

## Qualification

Phase 41 is accepted as `qualified-post-rc10-queue-hygiene` if validation passes.
