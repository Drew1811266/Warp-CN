# zh-Hans Localization Phase 65

Date: 2026-06-02 Asia/Shanghai

## Goal

Translate safe AI/Agent residue after RC13 while preserving protocol, MCP,
schema, response-stream, conversion, watcher, git, and diagnostic strings.

## Scope

Created and applied:

- `.omx/tmp-phase65-manifest.toml`

Appended matching entries to:

- `resources/localization/zh-Hans-overrides.toml`

The scoped manifest contains `48` entries across `17` AI/Agent files.

## Translated Areas

- Agent TODO popup and AI block TODO labels.
- Agent notification filter labels.
- Warp CLI authentication messages.
- Ambient Agent quota, overload, task ID, and follow-up failure messages.
- MCP tool-call user-facing errors.
- Request-file-edits save and diff-generation errors.
- Artifact upload errors.
- Pending prompt block actions.
- AI block attached-context chips.
- Requested script status labels.
- Plan/todo chip tooltips and actions.
- Suggestion chip tooltips.
- Summarization cancellation dialog.
- Orchestration config block labels and helper copy.
- Relevant-files outline errors.

## Preserved

The following residue stayed preserve-first:

- `app/src/ai/agent_management/notifications/view.rs`: keyboard and position IDs.
- `app/src/ai/blocklist/block/cli_controller.rs`: CLI control diagnostics.
- `app/src/ai/blocklist/controller/input_context.rs`: regex/context parser strings.
- `app/src/ai/blocklist/handoff/touched_repos.rs`: git command/domain literals.
- `app/src/ai/skills/file_watchers/utils.rs`: `SKILL.md` and `.git` path contracts.
- `app/src/ai/agent/api/convert_conversation.rs`: conversion/tool-result diagnostics.
- `app/src/ai/agent/api/convert_from.rs`: conversion diagnostics.
- `app/src/ai/agent_sdk/config_file.rs`: config parser/schema copy.
- `app/src/ai/agent_sdk/provider.rs`: provider/account setup contracts.
- `app/src/ai/blocklist/controller/response_stream.rs`: retry diagnostics.
- `app/src/ai/blocklist/passive_suggestions/legacy.rs`: passive suggestion logs.
- `app/src/ai/blocklist/permissions.rs`: permission IDs and parser literals.

## Scoped Dry-Run

After applying the scoped manifest:

```text
entries: 48
files: 17
already_applied: 48
would_change: 0
missing: 0
```

## AI/Agent Inventory After Phase 65

```text
| candidates | path |
| ---: | --- |
| 4 | app/src/ai/agent_management/notifications/view.rs |
| 4 | app/src/ai/blocklist/block/cli_controller.rs |
| 4 | app/src/ai/blocklist/controller/input_context.rs |
| 4 | app/src/ai/blocklist/handoff/touched_repos.rs |
| 4 | app/src/ai/skills/file_watchers/utils.rs |
| 3 | app/src/ai/agent/api/convert_conversation.rs |
| 3 | app/src/ai/agent/api/convert_from.rs |
| 3 | app/src/ai/agent_sdk/config_file.rs |
| 3 | app/src/ai/agent_sdk/provider.rs |
| 3 | app/src/ai/blocklist/block/model/model_impl.rs |
| 3 | app/src/ai/blocklist/controller/response_stream.rs |
| 3 | app/src/ai/blocklist/passive_suggestions/legacy.rs |
| 3 | app/src/ai/blocklist/permissions.rs |
| 3 | app/src/ai/document/ai_document_model.rs |
| 3 | app/src/ai/execution_profiles/model_menu_items.rs |
| 3 | app/src/ai/facts/view/mod.rs |
| 3 | app/src/ai/llms.rs |
| 3 | app/src/ai/mcp/reconnecting_peer.rs |
| 3 | app/src/ai/mcp/templatable.rs |
| 3 | app/src/ai/skills/skill_utils.rs |
```

The previous safe visible UI cluster no longer leads the AI/Agent queue. The
remaining top paths are dominated by preserve-first parser, schema, protocol,
identifier, git, MCP, provider, and diagnostic strings.

## Validation

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase65-manifest.toml --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase65-manifest.toml --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase65-manifest.toml --dry-run --summary
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
compile gate was run in this phase.

## Qualification

Phase 65 is accepted as `qualified-ai-agent-residue-pass-8`.

The phase is qualified because scoped dry-run is clean, AI/Agent visible UI
residue decreased, remaining top AI/Agent residue is documented as
preserve-first or queued for later review, and manifest validation, glossary,
Python tests, formatting, and diff checks passed.
