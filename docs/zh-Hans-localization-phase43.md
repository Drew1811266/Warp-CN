# zh-Hans Localization Phase 43

Date: 2026-06-02

## Goal

Translate remaining visible AI/MCP/Agent labels and errors without changing watcher, prompt, provider, file path, OAuth callback, or tool protocol contracts.

## Scope

Phase 43 added 98 scoped manifest entries:

```text
translated visible entries: 52
reviewed preserve entries: 46
files touched by scoped manifest: 11
main manifest entries after Phase 43: 7058
manifest context/status metadata: 100.0%
```

Translated visible copy:

| Area | Files |
| --- | --- |
| Artifact upload and attachments | `app/src/ai/agent_sdk/artifact_upload.rs`, `app/src/ai/agent_sdk/driver/attachments.rs` |
| Artifact buttons | `app/src/ai/artifacts/buttons.rs` |
| Child-agent launch failures | `app/src/ai/blocklist/action_model/execute/run_agents.rs` |
| Codebase search inline action | `app/src/ai/blocklist/inline_action/search_codebase.rs` |
| Suggested-rule modal | `app/src/ai/blocklist/suggested_rule_modal.rs` |
| MCP config and OAuth errors | `app/src/ai/mcp/file_mcp_watcher.rs`, `app/src/ai/mcp/mod.rs`, `app/src/ai/mcp/templatable_manager/oauth.rs` |

Reviewed preserves:

| Class | Files |
| --- | --- |
| Attachment filesystem logs and retry operation labels | `app/src/ai/agent_sdk/driver/attachments.rs` |
| Artifact upload GraphQL/fallback diagnostics | `app/src/ai/agent_sdk/artifact_upload.rs` |
| Child-agent prompt composition template | `app/src/ai/blocklist/action_model/execute/run_agents.rs` |
| Shared-session replay/debug diagnostics | `app/src/ai/blocklist/controller/shared_session.rs` |
| MCP template placeholders and config filenames | `app/src/ai/mcp/mod.rs` |
| OAuth callback protocol/storage diagnostics | `app/src/ai/mcp/templatable_manager/oauth.rs` |
| Skill watcher diagnostics and `SKILL.md` filenames | `app/src/ai/skills/file_watchers/skill_watcher.rs` |

## Coverage

Baseline from RC10:

```text
AI / Agent coverage: 2098 covered / 592 candidates = 78.0%
release coverage: 7427 covered / 1514 candidates = 83.1%
```

After Phase 43:

```text
AI / Agent coverage: 2204 covered / 486 candidates = 81.9%
release coverage: 7724 covered / 1221 candidates = 86.3%
```

The Phase 43 target files now have no remaining inventory candidates:

```text
python3 script/zh_localization_inventory.py --status candidate \
  app/src/ai/mcp/file_mcp_watcher.rs \
  app/src/ai/skills/file_watchers/skill_watcher.rs \
  app/src/ai/agent_sdk/driver/attachments.rs \
  app/src/ai/agent_sdk/artifact_upload.rs \
  app/src/ai/blocklist/action_model/execute/run_agents.rs \
  app/src/ai/blocklist/controller/shared_session.rs \
  app/src/ai/artifacts/buttons.rs \
  app/src/ai/blocklist/inline_action/search_codebase.rs \
  app/src/ai/mcp/mod.rs \
  app/src/ai/mcp/templatable_manager/oauth.rs \
  app/src/ai/blocklist/suggested_rule_modal.rs
```

Result:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
```

## Safety Review

No watcher path, `SKILL.md` filename, MCP config filename, provider display token, prompt composition template, JSON/template placeholder, OAuth callback path, shared-session replay diagnostic, or generated attachment filename template was localized.

User-visible translations preserve required glossary terms such as `Warp`, `Agent`, `MCP`, `Codex`, `Claude`, and `API 密钥`.

`cargo check` was intentionally not run in this phase because the changes are string-only, `cargo fmt --check` passed, and the low-load policy reserves Rust builds for Phase 48 or runtime-code changes.

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase43-manifest.toml --dry-run --summary
# entries: 98
# files: 11
# already_applied: 52
# would_change: 0
# missing: 0

python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

## Qualification

Phase 43 is accepted as `qualified-ai-mcp-child-agent-backlog-pass-4`.
