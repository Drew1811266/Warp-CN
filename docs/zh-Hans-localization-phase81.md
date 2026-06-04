# zh-Hans Localization Phase 81

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 81 translates or classifies remaining safe AI/Agent residue after RC15 and
Phase 79. The phase focuses on user-visible Agent SDK CLI messages, AI action
errors, blocklist buttons, cloud Agent labels, MCP object naming, and local child
harness notices while preserving SDK, MCP, provider, model, schema, cache, and
tool identifiers.

## Translated AI / Agent String Families

Phase 81 added and applied translations for:

- Agent SDK config-file parse, supported-keys, and WASM unsupported messages.
- Provider setup, API-key, integration retry, and authorization instructions.
- Agent SDK MCP/profile/model table headers and OAuth wait text.
- Fetch conversation, read MCP resource, read skill, and computer-use action
  errors.
- Debug block empty-output message.
- Recommended badge, toggle-selection hint, requested action buttons, and
  suggested Agent workflow prompt label.
- Remote handoff snapshot and environment creation errors.
- Orchestration usage rollup fallback label.
- Cloud Agent config, third-party harness model setting, and cloud environment
  object type strings.
- Conversation fallback title, AI document plan label, AI rule object type, and
  remote codebase search fallback/unavailable messages.
- Local Claude Code and Codex child-Agent disabled messages.
- Templatable MCP object type name.

## Preserved SDK / MCP / Provider Contracts

Phase 81 added exact-path or exact-literal ignore rules for:

```text
feature flags
source-location format strings
markdown/control-code wrappers
task/conversation IDs
notification and UI position IDs
admin CLI unsupported option diagnostics
harness support argument validation
secret handling assertions
passive-suggestion logs
action cancellation diagnostics
parser regexes
persistence diagnostics
request-usage logs
schema/cache identifiers
MCP credential keys
log file names
cost formatting snippets
```

The following visible or semi-visible terms are intentionally preserved:

```text
Agent
Warp
MCP
Claude Code
Codex
harness
schema keys such as name, environment_id, model_id, base_prompt, mcp_servers
```

## Coverage Before And After

Before Phase 81 after Phase 79:

```text
AI / Agent: 2517 covered, 114 candidates, 95.7%
```

After Phase 81:

```text
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0

AI / Agent: 2515 covered, 1 candidate, 100.0%
remaining AI / Agent candidate:
app/src/ai/blocklist/usage/rollup.rs: Agent
```

The lower covered count is expected because Phase 81 moved reviewed non-UI
residue into exact ignore policy. The only remaining AI/Agent candidate is the
intentional `Agent` preserve term.

## Acceptance Checks

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0

nice -n 10 python3 script/zh_localization_inventory.py app/src/ai --coverage
preset: custom
covered: 2515
candidates: 1
coverage: 100.0%

nice -n 10 python3 script/zh_localization_inventory.py app/src/ai --status candidate
candidate: app/src/ai/blocklist/usage/rollup.rs: Agent

nice -n 10 cargo fmt --check
passed

git diff --check
passed
```

## Qualification Result

Qualified.

Phase 81 passed because manifest validation, glossary, dry-run, AI/Agent
coverage, formatting, and diff checks all passed. SDK, MCP, provider, model,
schema, and tool identifiers were preserved, and the only remaining AI/Agent
candidate is the intentional `Agent` glossary term.
