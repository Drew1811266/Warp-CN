# zh-Hans Localization Phase 33

Date: 2026-06-01

## Goal

Turn the RC9 remaining candidate set into a safe post-RC9 execution queue before changing more source strings.

## Baseline

RC9 remains the baseline for Phase 33:

```text
manifest entries: 6294
manifest files: 301
dry-run: would_change 0, missing 0
release coverage: 6897 covered / 2037 candidates = 77.2%
terminal coverage: 1231 covered / 1134 candidates = 52.1%
AI / Agent coverage: 1904 covered / 780 candidates = 70.9%
settings coverage: 1953 covered / 74 candidates = 96.3%
workspace coverage: 817 covered / 49 candidates = 94.3%
modals coverage: 3682 covered / 1914 candidates = 65.8%
```

Phase 33 made no source-code changes.

## Candidate Classification

| Area | Representative paths | Classification | Next action |
| --- | --- | --- | --- |
| Terminal tmux/grid parser | `app/src/terminal/model/tmux/parser.rs`, `app/src/terminal/model/grid/grid_handler.rs` | Parser/protocol/error diagnostics. Literals include `%end`, `%error`, tmux event names, parser state labels, and parse error diagnostics. | Preserve or ignore after source inspection; do not translate protocol literals. |
| Terminal secrets | `app/src/terminal/model/secrets.rs` | Security detector display labels such as `IPv4 Address`, `GitHub OAuth Access Token`, and API key detector names. | Translate only if rendered as user-visible detector names; otherwise preserve product/provider names. |
| Terminal remote server | `app/src/terminal/writeable_pty/remote_server_controller.rs`, `app/src/terminal/ssh/install_tmux.rs` | Mixed diagnostics, SSH host examples, remote host labels, and install state messages. | Translate visible/user-facing diagnostics; preserve test hostnames and command examples. |
| Terminal input | `app/src/terminal/universal_developer_input.rs`, `app/src/terminal/input/terminal_message_bar.rs` | High-value visible UI: attach context, voice input, slash commands, mode switch tooltips, message-bar hints. | Phase 34 translation target. |
| AI transcript/harness | `app/src/ai/agent_sdk/driver/harness/claude_transcript.rs` | Transcript file names, JSON keys, parser diagnostics, and Claude storage paths. | Preserve parser/file/schema literals; translate only user-facing failures if rendered. |
| AI orchestration stream | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Logs/SSE lifecycle diagnostics. | Preserve/internal or ignore after source inspection. |
| AI action errors | `app/src/ai/blocklist/action_model/execute/start_agent.rs`, `app/src/ai/skills/resolve_skill_spec.rs` | Mixed user-facing errors and internal harness/git diagnostics. | Translate visible errors; preserve git commands, filenames, repo paths, and harness identifiers. |
| Settings polish | `app/src/settings_view/features/startup_shell.rs`, billing usage files, MCP/platform/Warp Drive settings | Small visible labels plus internal IDs. | Phase 36 translation target for visible labels; preserve IDs. |
| Workspace polish | `app/src/workspace/view/conversation_list/view.rs`, `app/src/workspace/view.rs`, left/vertical tabs | Conversation list empty/search labels and sync input toast copy, plus logs/IDs. | Phase 36 translation target for visible labels; preserve logs/IDs. |
| GUI evidence | Phase 30 screenshots and public-RC rows | Reused-bundle residue, embedded English imagery, missing account/backend state. | Phase 37-39 evidence work; do not weaken public-RC criteria. |

## Confirmed Phase Queue

Phase 34 should start with Terminal input/message-bar/user-facing remote-server surfaces and classify parser/protocol files conservatively.

Phase 35 should focus on visible Agent action errors, lifecycle/status copy, skill resolution errors, and conversation details. Transcript parser, SSE, provider command, prompt, and schema literals should remain preserved/internal unless product requirements change.

Phase 36 should take the low-risk Settings/Workspace polish files first because they are small, visible, and likely to improve practical coverage without heavy verification.

Phase 37-39 should handle GUI fixture design, current-source screenshot evidence, and isolated account/backend public-RC evidence separately from source translation coverage.

## Qualification

Phase 33 is accepted as `qualified-post-rc9-queue-hygiene`.

This phase is qualified because the Phase 34-36 queues were confirmed against current inventory, high-risk protocol/prompt/parser classes were separated from visible UI work, and no source strings were changed.
