# Task 7 Copy Lane Review

Task 7 reviewed the copy lane from `entries.json` and wrote a row-level
decision ledger to `task7-copy-lane-decisions.tsv`.

## Scope

| Item | Count |
| --- | ---: |
| Copy note rows reviewed | 2,251 |
| `needs-copy-fix` rows from generated report | 0 |
| Manifest edits made in this task | 0 |

## Row-Level Decisions

| Decision | Rows | Meaning |
| --- | ---: | --- |
| `intentional-preserve-command-code-token` | 1,500 | Command, placeholder, code, path, format, endpoint, or protocol token should remain stable. |
| `intentional-preserve-telemetry-feature-id` | 338 | CamelCase action, telemetry, feature, or enum identifier should not be localized. |
| `intentional-preserve-short-token-or-label` | 200 | Short product label, token, or non-sentence text preserved. |
| `needs-owner-review-source-state` | 126 | Exact source string did not match current source; treat as escaped/newline or source drift queue before editing. |
| `intentional-preserve-product-provider-term` | 40 | Glossary/product/provider term is intentionally preserved. |
| `needs-owner-review-schema-description` | 22 | Settings/schema description may be developer/config metadata rather than visible UI. |
| `needs-owner-review-internal-log-or-error` | 16 | English diagnostic/error string may be internal or runtime-visible; needs owner visibility decision. |
| `needs-translation-candidate-visible-ui` | 7 | Likely visible UI copy remains English; translate after GUI/runtime owner confirmation. |
| `needs-owner-review-search-keywords` | 2 | Search keyword blob may affect discoverability; translate only with owner decision. |

## Manual Context Checks

Representative checks were made against source context:

- `ToggleCopyOnSelect` and related `FeaturesPageAction` strings are telemetry/action IDs and were kept.
- Settings search keyword blobs such as `link open desktop native redirect url intent deep link deeplink` are search/discoverability data, not normal prose.
- Glossary terms such as `Warp Drive`, `Agent`, `Codex`, `Claude`, `Gemini`, `MCP`, and `CLI` are intentionally preserved.

## Decision

No manifest target was changed in Task 7. The copy lane has no confirmed
machine-translation defect. It still has owner-review queues for visible English
copy, source-state drift, schema descriptions, runtime diagnostics, and search
keywords.
