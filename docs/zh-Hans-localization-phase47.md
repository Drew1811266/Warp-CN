# zh-Hans Localization Phase 47

Date: 2026-06-02

## Goal

Audit RC11 changes for terminology, UI wording consistency, preserve safety, and behavioral risk before the final release gate.

## Review Scope

Phase 47 reviewed the post-RC10 source passes:

| Phase | Entries | Visible translations | Reviewed preserves | Qualification |
| --- | ---: | ---: | ---: | --- |
| Phase 42 | 174 | 74 | 100 | `qualified-terminal-backlog-pass-5` |
| Phase 43 | 98 | 52 | 46 | `qualified-ai-mcp-child-agent-backlog-pass-4` |
| Phase 44 | 30 | 25 | 5 | `qualified-auth-secret-ftux-source-and-agent-fixture-blockers` |

Static visual residue and public-RC account/backend blockers were reviewed in Phase 45 and Phase 46, but those phases did not introduce source string translations.

## Terminology Review

The glossary gate passed. Required product/technical terms remain stable:

- `Warp`
- `Warp Drive`
- `Warp Agent`
- `Agent`
- `MCP`
- `CLI`
- `GitHub`
- `AWS Bedrock`
- `Oz`
- `Codex`
- `Claude Code`
- `Gemini`
- `API 密钥`
- `端点`
- `团队`

Forbidden/awkward target search:

```text
rg -n 'target = ".*(智能体|智能代理|智能助手|智能助理|命令调色板|端点点|帐号)' resources/localization/zh-Hans-overrides.toml
```

Result: no matches.

## Preserve And Ignore Safety

Reviewed preserve classes remain behaviorally safe:

| Class | Decision |
| --- | --- |
| Terminal command templates, env vars, shell paths, tmux commands, ANSI sequences, WSL/ConPTY API strings | Preserved; translating these would break shell/terminal/protocol behavior. |
| Prompt/tool/model contracts, JSON/schema fragments, file watcher paths, `SKILL.md` filenames | Preserved; translating these would break Agent/MCP/tooling contracts. |
| Product/source names such as `Linear`, `Slack`, `Oz Web`, `GitHub Action`, and fallback `Agent` | Preserved; these are proper names or product labels. |
| Inventory ignore additions from earlier phases | Reviewed as parser/input fixtures, snapshot upload internals, git command args, blob names, diagnostics, and debug state; no visible UI copy is hidden by the Phase 42-44 passes. |

No preserve/ignore entry from the post-RC10 source passes hides a known visible user-facing string without a documented rationale.

## Focused Inventory

Focused coverage after Phase 47:

```text
release coverage: 7757 covered / 1191 candidates = 86.7%
terminal coverage: 1653 covered / 718 candidates = 69.7%
AI / Agent coverage: 2223 covered / 469 candidates = 82.6%
```

The Phase 42-44 target-file candidate inventory is empty:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
```

Manifest metadata remains complete:

```text
entries: 7088
context: 7088 / 7088 = 100.0%
status: 7088 / 7088 = 100.0%
```

Full dry-run remains clean:

```text
entries: 7088
files: 367
already_applied: 5124
would_change: 0
missing: 0
```

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

`cargo check` was intentionally deferred to Phase 48 per the low-load policy.

## Qualification

Phase 47 is accepted as `qualified-rc11-language-quality-and-safety-review`.
