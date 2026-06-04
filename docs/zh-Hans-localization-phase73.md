# zh-Hans Localization Phase 73

Date: 2026-06-02 Asia/Shanghai

## Goal

Translate safe remaining AI/Agent UI and user-facing copy while preserving
provider IDs, schemas, parser values, transcript markers, MCP contracts, tool
execution payloads, and debug diagnostics.

## Scoped Manifest

Created:

- `.omx/tmp-phase73-manifest.toml`

Appended `10` active manifest entries to:

- `resources/localization/zh-Hans-overrides.toml`

## Translated Files

Applied the scoped manifest to `3` AI/Agent files:

```text
app/src/ai/agent_sdk/provider.rs
app/src/ai/execution_profiles/model_menu_items.rs
app/src/ai/facts/view/mod.rs
```

Translated UI families:

- Provider CLI setup-scope error.
- Provider CLI connection status and table headers.
- Execution-profile model menu default badge.
- AI rules page offline notice and page titles.

## Preserved

Preserved the remaining candidate families in this pass:

- Notification position IDs and keyboard labels.
- Agent management harness labels and already-localized metadata rows.
- Agent task popup and notification toast internal UI names.
- CLI controller diagnostics and handoff logs.
- Regexes and attachment disambiguation formats.
- Git remote parsing values.
- Passive suggestion diagnostics.
- Permission setting IDs and command parsing snippets.
- AI document persisted SQLite diagnostics and the `Plans` folder constant.
- LLM host dedupe logs and builtin `auto (` / `cost-efficient` detection
  literals.
- MCP template placeholders, uniqueness keys, and connection diagnostics.
- Skill filenames and skill identifiers.

## Checks

Scoped manifest validation:

```text
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase73-manifest.toml --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase73-manifest.toml --check-glossary
glossary check passed
```

Scoped dry-run after apply:

```text
entries: 10
files: 3
already_applied: 10
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

nice -n 10 cargo fmt --check
git diff --check
```

## Coverage Movement

AI/Agent coverage after Phase 73:

```text
covered: 2537
candidates: 160
coverage: 94.1%
```

RC14 AI/Agent baseline:

```text
covered: 2527
candidates: 167
coverage: 93.8%
```

Remaining top AI/Agent paths are mostly preserve-first contracts and internal
diagnostics:

```text
app/src/ai/agent_management/notifications/view.rs
app/src/ai/blocklist/block/cli_controller.rs
app/src/ai/blocklist/controller/input_context.rs
app/src/ai/blocklist/handoff/touched_repos.rs
app/src/ai/skills/file_watchers/utils.rs
app/src/ai/agent/api/convert_conversation.rs
app/src/ai/agent/api/convert_from.rs
app/src/ai/agent_sdk/config_file.rs
app/src/ai/blocklist/controller/response_stream.rs
app/src/ai/mcp/reconnecting_peer.rs
```

## Qualification

Phase 73 is accepted as `qualified-ai-agent-residue-pass-9`.

The phase is qualified because the scoped dry-run reports `would_change: 0` and
`missing: 0`, AI/Agent coverage improved from `93.8%` to `94.1%`,
preserve-first residue is documented, and manifest validation, glossary,
Python localization tests, formatting, and diff checks passed.
