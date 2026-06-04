# zh-Hans Localization Phase 18

Date: 2026-06-01

## Goal

Convert the Phase 13-17 source work into a release decision and record which GUI evidence gates remain before public RC promotion.

## Result

- Created `docs/zh-Hans-release-candidate-2026-06-01-rc7.md`.
- Updated the GUI evidence matrix with a current-cycle Phase 18 record.
- Recomputed current coverage and export artifacts.
- Ran command-line, Python, formatting, diff, and Rust compile gates.
- Did not promote any GUI matrix row to `verified` without current-cycle visual evidence.

## Decision

Phase 18 is accepted as `qualified-source-rc`.

RC7 is `ready-for-local-use-source-level`, but not `ready-for-public-rc`.

## Remaining Public-RC Gates

- Fresh Agent onboarding.
- Browser login and token fallback.
- AI settings deep paths and real-account custom endpoint path.
- Environment deletion and auth-secret deletion confirmations.
- Agent lifecycle status and error states.
- Billing, cloud capacity, credits, and plan modals.

These require isolated disposable accounts, fixtures, or backend state. They were not exercised with a main account or real paid/cloud resources.

## Validation

```text
manifest validation passed
glossary check passed
dry-run: entries 4376, files 254, would_change 0, missing 0
release coverage: 4746 covered, 4147 candidates, 53.4%
locale exports: json/yaml generated
Python localization tests: 19 passed
cargo fmt --check: passed
git diff --check: passed
cargo check -p warp: passed with existing unused-variable warnings
```
