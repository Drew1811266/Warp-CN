# zh-Hans Localization Phase 28

Date: 2026-06-01

## Goal

Reduce AI/Agent residue after RC8 without breaking prompt, provider, tool, harness, command, schema, or test-fixture contracts.

## Scope

Phase 28 reviewed the AI/Agent backlog across Agent SDK CLI output, execution profiles, orchestration controls, usage views, prompt alerts, remote search errors, rules UI, and selected diagnostics.

Primary updated files:

- `app/src/ai/agent/task.rs`
- `app/src/ai/agent_sdk/api_key.rs`
- `app/src/ai/agent_sdk/artifact.rs`
- `app/src/ai/agent_sdk/common.rs`
- `app/src/ai/agent_sdk/driver/git_credentials.rs`
- `app/src/ai/agent_sdk/driver/harness/claude_code.rs`
- `app/src/ai/agent_sdk/schedule.rs`
- `app/src/ai/artifact_download.rs`
- `app/src/ai/blocklist/block/cli.rs`
- `app/src/ai/blocklist/inline_action/ask_user_question_view.rs`
- `app/src/ai/blocklist/inline_action/orchestration_controls.rs`
- `app/src/ai/blocklist/inline_action/run_agents_card_view.rs`
- `app/src/ai/blocklist/prompt/prompt_alert.rs`
- `app/src/ai/blocklist/usage/conversation_usage_view.rs`
- `app/src/ai/execution_profiles/mod.rs`
- `app/src/ai/facts/view/rule.rs`
- `app/src/ai/get_relevant_files/remote_search/native.rs`
- `app/src/ai/llms.rs`

## Manifest Changes

Phase 28 added `357` manifest entries:

- `240` translated visible/user-facing strings.
- `117` reviewed preserves for provider CLI output matching, prompt/tool contracts, schema keys, IDs, test fixtures, filenames, command templates, and diagnostics.

Two candidate preserves were intentionally removed from the Phase 28 manifest because glossary-compliant translation would break behavior:

- `Invalid API key` in the Claude runtime error pattern list.
- `Duplicate LLMModelHost entry for {:?}, using latest value` in an internal LLM diagnostic.

## Coverage

| Preset | Before Phase 28 | After Phase 28 |
| --- | ---: | ---: |
| AI root | `1502 covered / 1182 candidates = 56.0%` | `1904 covered / 780 candidates = 70.9%` |
| Modals | `3280 covered / 2316 candidates = 58.6%` | `3682 covered / 1914 candidates = 65.8%` |
| Release | `6313 covered / 2619 candidates = 70.7%` | `6715 covered / 2217 candidates = 75.2%` |

## Preserved Contract Classes

- Provider/runtime error substrings used for matching Claude, Codex, Gemini, and related harness failures.
- Provider CLI command templates, flags, file names, config keys, env vars, and shell snippets.
- Prompt and parent-bridge instructions that are sent to model/harness contracts.
- JSON/YAML/schema field names, IDs, action names, telemetry-like keys, and test fixtures.
- Diagnostic strings where translation would hide an internal identifier or violate glossary checks.

## Validation

Passed:

- `python3 script/zh_apply_localization.py --validate-manifest`
- `python3 script/zh_apply_localization.py --check-glossary`
- Phase 28 scoped dry-run using the existing replacement engine:
  - `entries: 357`
  - `files: 20`
  - `already_applied: 240`
  - `would_change: 0`
  - `missing: 0`
- `python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py`
- `cargo fmt --check`
- `git diff --check`

As in Phase 27, full-manifest dry-run is deferred to the Phase 32 RC9 gate to avoid overheating the local machine during repeated full scans.

## Qualification

Phase 28 is accepted as `qualified-ai-agent-backlog-pass-2-low-load`.

No GUI row is promoted by this source-only pass. No account, billing quota, cloud environment, secret, or team ownership state was touched.
