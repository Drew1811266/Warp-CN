# zh-Hans Localization Phase 52

Date: 2026-06-02

## Goal

Translate remaining visible AI/Agent errors and labels while preserving prompt, harness, MCP, provider, file-system, schema, and diagnostic contracts.

## Scope

Phase 52 added 109 scoped manifest entries:

```text
translated visible entries: 61
reviewed preserve entries: 48
files touched by scoped manifest: 15
main manifest entries after Phase 52: 7372
manifest context/status metadata: 100.0%
```

Translated visible areas:

| Area | Files |
| --- | --- |
| Agent details action buttons | `agent_management/details_action_buttons.rs` |
| Harness setup/temp/upload errors | `agent_sdk/driver/harness/mod.rs` |
| Terminal driver session-sharing errors | `agent_sdk/driver/terminal.rs` |
| Scheduled Agent errors | `ambient_agents/scheduled.rs` |
| AWS credential profile/error copy | `aws_credentials.rs` |
| Get relevant files action results | `blocklist/action_model/execute/get_files.rs` |
| Web fetch/search inline action UI | `blocklist/inline_action/web_fetch.rs`, `web_search.rs` |
| Local Agent task status/errors | `blocklist/local_agent_task_sync_model.rs` |
| Execution profile state labels | `execution_profiles/profiles.rs` |
| Rule editor | `facts/view/rule_editor.rs` |

Reviewed preserves:

| Class | Examples |
| --- | --- |
| AWS/OIDC/provider contracts | `sts.amazonaws.com`, token suffixes, role-session names, provider setup diagnostics |
| Harness diagnostics | transcript deserialize logs, HTTP `status 404`, debug error formatters |
| Shell command templates | `cd {escaped_target}` |
| MCP templates/headers | `{{{json}}}`, `${{{var_name}}}`, `Authorization`, `Bearer ...` |
| Outline/skill manager logs | repo outline diagnostics, `SKILL.md`, `settings_schema.json`, bundled skill IDs |
| URL display formats | `{title} ({url})`, failed URL marker |
| View IDs | `ConversationActionButtonsRow` |

## Coverage

After Phase 52:

```text
AI / Agent coverage: 2339 covered / 355 candidates = 86.8%
release coverage: 8070 covered / 883 candidates = 90.1%
```

The Phase 52 target files now have no remaining inventory candidates:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
```

## Safety Review

No prompt/tool/MCP/provider/file contract was localized incorrectly. Preserved strings cover AWS STS audiences, token filenames, MCP JSON/env-var templates, HTTP headers, bundled skill filenames, execution-profile logs, outline diagnostics, and shell command templates.

The AWS credential profile helper now avoids the prior English article/profile phrase in localized user-facing error messages.

`cargo check` was intentionally deferred to Phase 54 because Phase 52 changes are string-only and `cargo fmt --check` passed after formatting.

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase52-manifest.toml --dry-run --summary
# entries: 109
# files: 15
# already_applied: 61
# would_change: 0
# missing: 0

python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

## Qualification

Phase 52 is accepted as `qualified-ai-agent-backlog-pass-5`.
