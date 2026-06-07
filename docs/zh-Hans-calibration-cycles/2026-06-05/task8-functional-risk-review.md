# Task 8 Functional Risk Review

Task 8 reviewed token, placeholder, source-state, public-RC, and protocol
risks. A row-level decision ledger for all 7,943 manifest rows was written to
`task8-functional-risk-decisions.tsv`.

## Scope

| Item | Count |
| --- | ---: |
| Manifest rows reviewed | 7,943 |
| Critical token mismatches | 0 |
| Source-state review rows | 130 |
| Public-RC evidence-gated rows | 1,030 |
| Manifest edits made in this task | 0 |

## Row-Level Decisions

| Decision | Rows | Meaning |
| --- | ---: | --- |
| `preserve-intentional-token-safe` | 4,996 | Risk tags present but token audit is clean; preserve placeholders, commands, URLs, endpoints, or account-state text. |
| `accepted-functional-clean` | 1,790 | No functional token/source-state risk detected. |
| `needs-owner-review-public-rc-evidence-gated` | 1,026 | Public-RC blocker evidence is required; do not promote from source-level audit alone. |
| `preserve-intentional-command-template-source-state` | 115 | Command/template/protocol row should stay stable; source-state miss is a normalization/drift queue. |
| `needs-owner-review-source-state-visible-english` | 11 | English source-state miss may be visible copy; owner should confirm before translation. |
| `add-ignore-rule-candidate-source-state-normalization` | 4 | Translated target is represented in current source but exact source count failed; normalize escaped/newline matching before treating as a defect. |
| `accepted-functional-token-note-display-marker` | 1 | `<cancelled>` became `<已取消>` with angle brackets retained; context confirms this is a user-readable display marker. |

Public-RC counts differ by 4 rows in the decision table because those rows also
fall into source-state normalization; they remain public-RC blocked unless
separate safe evidence is supplied.

## Manual Context Checks

Representative checks were made against source context:

- `# 在文件中查找 "foo"` is present in `app/src/search/command_search/zero_state.rs`.
- The two `osascript` administrator prompts are present in `app/src/workspace/cli_install.rs` with placeholders preserved.
- Agent Markdown templates such as `**Command Executed:**` use newline/template formatting that the static source counter flags as source-state drift.
- `<已取消>` is defined as `CANCELLED_MESSAGE` in `app/src/ai/agent_sdk/driver/output.rs`; it is user-facing formatted output, not a protocol enum.

## Decision

No functional token break was confirmed. No manifest edit was made in Task 8.
The remaining work is owner review for public-RC evidence, source-state
normalization, and visible English source-state rows.
