# zh-Hans Localization Phase 71

Date: 2026-06-02 Asia/Shanghai

## Goal

Classify the post-RC14 residue before translating more strings, so the next
passes do not accidentally translate protocol, parser, test, fixture, shell, or
provider contracts.

## RC14 Baseline

Evidence:

- `docs/zh-Hans-release-candidate-2026-06-02-rc14.md`
- `docs/zh-Hans-localization-phase70.md`
- `docs/zh-Hans-localization.md`

```text
manifest entries: 7792
dry-run: entries 7792, files 475, already_applied 5539, would_change 0, missing 0
metadata: context/status 7792 (100.0%)
release coverage: 8514 covered, 439 candidates, 95.1%
terminal coverage: 2106 covered, 268 candidates, 88.7%
AI / Agent coverage: 2527 covered, 167 candidates, 93.8%
```

## Candidate Snapshots

Commands:

```text
nice -n 10 python3 script/zh_localization_inventory.py --preset release --status candidate --top-paths 40
nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --status candidate --top-paths 40
nice -n 10 python3 script/zh_localization_inventory.py app/src/ai --status candidate --top-paths 40
```

Release top paths remain concentrated in terminal model/command paths, terminal
protocol/test/bootstrap paths, and AI provider/parser/tool-control paths.

## Classification

| Path | Candidate family | Classification | Next action |
| --- | --- | --- | --- |
| `app/src/terminal/ref_tests/mod.rs` | `*.recording`, `*.json`, ref-test failure text | fixture-or-test-residue | Preserve-first; do not translate test fixture filenames or assertions. |
| `app/src/terminal/writeable_pty/bootstrap_file/windows.rs` | temporary-file errors and `pwsh.ps1` bootstrap filename | shell-or-bootstrap-contract | Preserve-first for bootstrap filename; review errors only if surfaced to users. |
| `app/src/terminal/local_tty/server/protocol.rs` | recvmsg/fd/cmsg/message-size protocol errors | terminal-protocol-contract | Preserve-first; translating could make protocol diagnostics less searchable. |
| `app/src/terminal/model/iterm_image.rs` | iTerm image protocol values and labels | terminal-protocol-contract | Preserve-first; `File`, `MultipartFile`, `preserveAspectRatio` are protocol tokens. |
| `app/src/terminal/writeable_pty/pty_controller.rs` | tmux control mode diagnostics and source marker | shell-or-bootstrap-contract | Preserve-first unless a later UI pass proves a visible user-facing error. |
| `app/src/terminal/alt_screen_reporting.rs` | settings descriptions for forwarding mouse/scroll/focus events | visible-ui | Move to Phase 72 safe-review queue. |
| `app/src/terminal/links.rs` | shortcut label fragments `Cmd +`, `Ctrl +`, `Middle` | visible-ui-fragment | Preserve until a targeted shortcut-label pass can verify composition and spacing. |
| `app/src/terminal/local_tty/spawner.rs` | platform and fallback diagnostics | log-or-debug-residue | Preserve-first; review only if later evidence shows end-user display. |
| `app/src/terminal/model/early_output.rs` | handler invariant diagnostics | log-or-debug-residue | Preserve-first; internal invariant text. |
| `app/src/terminal/model/kitty.rs` | Kitty graphics protocol and image-size diagnostics | terminal-protocol-contract | Preserve-first for protocol values and diagnostics. |
| `app/src/ai/skills/file_watchers/utils.rs` | `SKILL.md`, `.git` | parser-or-schema-contract | Preserve-first; filenames and directory names. |
| `app/src/ai/agent/api/convert_conversation.rs` | conversion errors for tool call/file/screenshot payloads | parser-or-schema-contract | Preserve-first; API conversion diagnostics. |
| `app/src/ai/agent/api/convert_from.rs` | conversion errors for tool/action/citation payloads | parser-or-schema-contract | Preserve-first; API conversion diagnostics. |
| `app/src/ai/agent_sdk/config_file.rs` | JSON/YAML parse errors and supported config keys | parser-or-schema-contract | Preserve-first for schema keys; user-facing parse error can be reviewed later only with CLI context. |
| `app/src/ai/agent_sdk/provider.rs` | provider setup/account requirement, table headers, connection status | transcript-or-tool-output | Move visible CLI table/status strings to Phase 73 safe-review queue; preserve provider slugs. |
| `app/src/ai/blocklist/controller/response_stream.rs` | MultiAgent retry diagnostics | log-or-debug-residue | Preserve-first; retry diagnostics and parser/control flow. |
| `app/src/ai/llms.rs` | duplicate host warning, `cost-efficient`, auto label fragment | provider-or-model-identifier | Preserve-first for provider/model metadata; review visible label fragments only in Phase 73 if UI context is clear. |
| `app/src/ai/mcp/reconnecting_peer.rs` | service/reconnection/model-dropped errors | parser-or-schema-contract | Preserve-first; MCP connection diagnostics. |
| `app/src/ai/mcp/templatable.rs` | template placeholder, MCP server label, uniqueness key | parser-or-schema-contract | Preserve template and uniqueness key; review `MCP server` only if visible. |
| `app/src/ai/skills/skill_utils.rs` | skill IDs and `SKILL.md` filenames | parser-or-schema-contract | Preserve-first; filenames and skill identifiers. |

## Phase 72 Queue Adjustment

Add these to Phase 72 safe-review queue because they are likely visible UI or
visible fragments and should not be ignored:

- `app/src/terminal/alt_screen_reporting.rs`
- `app/src/terminal/links.rs`

## Phase 73 Queue Adjustment

Add these to Phase 73 safe-review queue because they may render in CLI/provider
or model-selection contexts:

- `app/src/ai/agent_sdk/provider.rs`
- `app/src/ai/llms.rs`
- `app/src/ai/mcp/templatable.rs`

## Ignore Policy Decision

No ignore rules were changed in Phase 71.

Reasoning:

- Several candidates are clearly preserve-first, but Phase 74 is the dedicated
  inventory-precision phase.
- Some candidates are visible UI fragments or CLI table/status output and need
  a translation review before any ignore rule is safe.
- Avoiding new ignore rules here keeps the Phase 72 and Phase 73 translation
  queues honest.

## Checks

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
git diff --check
```

## Qualification

Phase 71 is accepted as `qualified-post-rc14-residue-classification`.

The phase is qualified because the current candidate snapshots were refreshed,
the preserve-first candidates were classified with explicit rationale, no source
translations were made, no potentially visible candidate was hidden by ignore
rules, and the manifest, glossary, and diff checks passed.
