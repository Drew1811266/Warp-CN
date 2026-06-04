# zh-Hans Modals/Terminal/Agent Candidate Classification

## Purpose

This file records the first Phase 4 classification pass for the noisy `modals` inventory preset. The goal is to avoid treating terminal protocol strings, Agent transcript templates, debug labels, and diagnostic logs as ordinary UI copy.

Baseline before this pass:

```text
preset: modals
covered: 635
candidates: 5371
coverage: 10.6%
```

## Categories

| Category | Meaning | Default action |
| --- | --- | --- |
| `user-visible-ui` | Labels, buttons, banners, toasts, dialogs, permission prompts, user-facing errors. | Translate in small manifest batches. |
| `terminal-protocol` | Escape sequences, shell control text, terminal parsing, command syntax. | Do not translate. Add ignore rules when safe. |
| `agent-transcript` | Markdown transcript fragments generated for Agent context or history. | Keep stable unless a GUI review proves it is directly user-facing and safe to localize. |
| `diagnostic-log` | `Debug`/`Display` labels, lifecycle logs, telemetry-like state strings. | Do not translate. Add ignore rules when the whole path is diagnostic. |
| `test-or-template` | Fixtures, examples, test prompts, schema-like templates. | Do not translate unless shipped as visible UI. |
| `needs-runtime-trigger` | Potential UI that depends on account, cloud, Agent, billing, or terminal state. | Record in GUI matrix or split into a targeted manual gate. |

## Reviewed Paths

| Path | Classification | Decision |
| --- | --- | --- |
| `app/src/terminal/view/action.rs` | `diagnostic-log` | Added to `zh-Hans-inventory-ignore.toml` exact paths. The candidates are action enum display/debug labels such as `Scroll`, `CopySelectedText`, `OpenShareSessionModal`, and `ToggleCodeReviewPane`, not rendered UI copy. |
| `app/src/terminal/view.rs` | mixed | Contains real UI (`Warp can notify you...`, shell initialization banners, Oz permission prompts, file context menu labels) plus terminal protocol, feature-state names, logs, and command templates. Do not ignore the whole file. |
| `app/src/terminal/input.rs` | mixed | Contains command/input behavior, slash command handling, and some visible prompts. Needs a later targeted pass. |
| `app/src/terminal/view/init.rs` | mixed | Contains initialization UI and terminal setup internals. Needs runtime-triggered GUI review before broad translation. |
| `app/src/ai/agent/mod.rs` | mixed | Contains Agent transcript Markdown, debug text, web/fetch status, command/file results, and some visible state labels. Do not bulk translate transcript templates. |
| `app/src/ai/agent_sdk/driver.rs` | mixed | Contains CLI/Agent runtime errors, MCP setup diagnostics, auth errors, lifecycle logs, and harness messages. User-visible CLI errors should be translated later in a dedicated Agent/CLI slice. |
| `app/src/ai/agent_sdk/driver/output.rs` | mixed | Likely output/transcript formatting; classify with `agent-transcript` before translating. |

## Follow-Up Translation Slices

Recommended future small batches:

1. `terminal.view.notifications`: notification opt-in/error banners in `app/src/terminal/view.rs`.
2. `terminal.view.shell_init`: shell startup and SSH/completion banners in `app/src/terminal/view.rs`.
3. `terminal.view.oz_permissions`: Oz permission/confirmation prompts in `app/src/terminal/view.rs`.
4. `terminal.view.file_context_menu`: file/link context menu labels in `app/src/terminal/view.rs`.
5. `agent.driver.user_errors`: user-facing Agent/CLI errors in `app/src/ai/agent_sdk/driver.rs`.

## Phase 5 Updates

- 2026-05-30 P5-M5 completed `agent.status_labels`: localized Agent conversation/task status display labels in `app/src/ai/agent_conversations_model.rs`, ambient task status labels in `app/src/ai/ambient_agents/task.rs`, the pending query `Queued` badge in `app/src/ai/blocklist/block/pending_user_query_block.rs`, and Agent history output status labels in `app/src/ai/blocklist/history_model.rs`.
- This slice was treated as `user-visible-ui`, not `agent-transcript`: the strings are short display labels/badges returned by UI status models. Transcript Markdown, logs, protocol strings, and harness diagnostics remain out of scope.

## Phase 6 Updates

- 2026-05-31 P6-M5 completed `terminal.view.notifications`: localized the terminal inline notification discovery/error banners in `app/src/terminal/view.rs`, `app/src/terminal/view/inline_banner/notifications_discovery.rs`, and `app/src/terminal/view/inline_banner/notifications_error.rs`.
- This slice was treated as `user-visible-ui`: the strings are visible banner titles/buttons for notification setup, permission results, and notification troubleshooting.
- This slice deliberately did not translate terminal protocol, command syntax, notification telemetry action enum names, logs, or Agent transcript text.

## Non-Goals

- Do not translate escape sequences such as bracketed paste markers.
- Do not translate command syntax, keybindings, or shell snippets.
- Do not translate telemetry state names or action variant names.
- Do not translate Agent transcript Markdown unless a GUI review confirms it is user-facing and stable.
