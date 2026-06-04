# zh-Hans Localization Phase 35

Date: 2026-06-01

## Goal

Translate remaining visible Agent/AI copy without changing prompt, tool, model, transcript parser, or provider contracts.

## Scope

Phase 35 added `180` AI/Agent manifest entries:

- `88` translated visible/user-facing entries.
- `92` reviewed preserves for transcript parser, SSE/logging, provider command, git command, schema, filename, and prompt-contract strings.

Primary touched areas:

- Agent child-run startup errors.
- Skill resolution and clone errors.
- Auth-secret type labels.
- Grep/search-codebase action failures.
- Agent status bar labels and model fallback messages.
- Orchestration event validation errors.
- Conversation details metadata labels.
- Agent config and management CLI/table labels.
- Gemini setup serialization errors.

## Translated Classes

- User-visible Agent startup failures such as missing harness type, unsupported child harness, missing `run_id`, and initialization failure.
- Skill and repo resolution errors, while preserving `SKILL.md`, `.git`, git commands, and repo syntax examples.
- API key/auth-secret labels with provider names preserved.
- Grep/search-codebase failure messages shown to Agent/tool output consumers.
- Status-bar copy such as GitHub auth, cloud-agent cancellation, fallback model retry, setup environment, and exit input.
- Conversation details labels: credits used, run time, created date, and harness label.
- Agent management table headers and selected config errors.

## Preserved Classes

- Claude transcript filenames, JSONL paths, JSON keys, and parser diagnostics.
- Orchestration SSE streamer logs and dormant Claude wake diagnostics.
- Gemini command templates, config filenames, and trusted-folder schema filenames.
- Git command strings, shell command fragments, and provider/harness identifiers.
- Conversation loader merge/fetch logs and internal server-token diagnostics.

## Coverage

```text
AI / Agent before: 1904 covered / 780 candidates = 70.9%
AI / Agent after: 2096 covered / 590 candidates = 78.0%
release after: 7292 covered / 1645 candidates = 81.6%
```

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase35-manifest.toml --dry-run --summary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

Scoped dry-run:

```text
entries: 180
files: 15
already_applied: 88
would_change: 0
missing: 0
```

## Qualification

Phase 35 is accepted as `qualified-ai-agent-backlog-pass-3-low-load`.

The phase is qualified because AI/Agent coverage exceeded the `75.0%` target, visible Agent status/error labels follow the glossary, and transcript/prompt/tool/provider contracts were preserved instead of localized accidentally.
