# zh-Hans Release Candidate 2026-06-01 RC7

RC7 is the Phase 13-18 follow-up localization record for Warp CN.

Decision: `ready-for-local-use-source-level`

Public RC decision: not ready.

## Scope

RC7 includes:

- Candidate classification and inventory metric hygiene.
- High-visibility Settings and Workspace pass.
- Terminal visible-surface pass.
- AI / Agent classification and visible UI pass.
- Onboarding/Auth, Tab configs, Themes, Billing, and Warp Drive small completion passes.
- Command-line, export, Python test, formatting, diff, and `cargo check -p warp` gates.

RC7 does not claim first-party runtime i18n support, complete whole-repository localization, or public-RC GUI readiness.

## Manifest And Coverage

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --metadata-summary
entries: 4376
key: 150 (3.4%)
context: 1862 (42.6%)
status: 1862 (42.6%)
preserve_terms: 18 (0.4%)
notes: 0 (0.0%)
expected_count: 150 (3.4%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 4376
files: 254
already_applied: 3571
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 655 covered, 211 candidates, 75.6%
search: 269 covered, 0 candidates, 100.0%
settings: 1548 covered, 477 candidates, 76.4%
modals: 2098 covered, 3459 candidates, 37.8%
release: 4746 covered, 4147 candidates, 53.4%
```

Phase-specific coverage:

```text
AI / Agent: 1131 covered, 1553 candidates, 42.1%
Terminal: 420 covered, 1906 candidates, 18.1%
Onboarding/Auth: 323 covered, 0 candidates, 100.0%
Tab configs: 69 covered, 0 candidates, 100.0%
Themes: 58 covered, 0 candidates, 100.0%
Billing: 20 covered, 0 candidates, 100.0%
Warp Drive: 253 covered, 0 candidates, 100.0%
```

Locale exports:

```text
/tmp/zh-CN.json: 1258794 bytes
/tmp/zh-CN.pretty.json: 1510075 bytes
/tmp/zh-CN.yaml: 1048597 bytes
```

## Command-Line Gate

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 -m json.tool /tmp/zh-CN.json > /tmp/zh-CN.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_export_locale.py script/test_zh_localization_inventory.py
cargo fmt --check
git diff --check
cargo check -p warp
```

Python tests:

```text
19 tests passed
```

Rust compile gate:

```text
cargo check -p warp
Finished dev profile successfully
```

Known command-line warnings:

- `cargo check -p warp` reports existing unused-variable warnings in `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` and `app/src/terminal/input/slash_commands/mod.rs`.

## GUI Evidence

No new GUI rows are promoted to `verified` in RC7.

RC7 only promotes source-level and command-line confidence. The GUI matrix still requires current-cycle visual evidence before public promotion, and RC7 does not use a main account, production billing quota, real cloud environment, real secret, or real team ownership state.

Existing historical/fixture evidence remains valid only at its previous level:

- Base workspace, command palette, settings shell, and tab context menu have historical verified anchors.
- Custom inference endpoint removal remains fixture-verified only.
- Account, Billing, Cloud, destructive confirmation, and Agent lifecycle states remain gated by isolated account/state or fixture requirements.

## Release Decision

RC7 is `ready-for-local-use-source-level`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Locale exports are generated and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -p warp` pass.
- Release preset source-level coverage improved from 31.7% at the plan baseline to 53.4%.

RC7 is not `ready-for-public-rc` because public-RC criteria require current-cycle GUI evidence for account/state paths. The following remain manual or fixture gates:

- Fresh Agent onboarding.
- Browser login and token fallback.
- AI settings deep paths, BYO API keys, custom endpoint real-account path.
- Environment deletion and auth-secret deletion confirmations.
- Agent lifecycle status and error states.
- Billing, cloud capacity, credits, and plan modals.

## Next Gate

Before public RC:

1. Use an isolated disposable profile and account.
2. Do not use the user's main account, real billing quota, real production environment, or real secrets.
3. Rebuild or launch the local bundle in that isolated profile.
4. Capture cropped/redacted screenshots for the manual GUI rows listed above.
5. Promote fixture evidence separately from true account-verified evidence.
6. Re-run the command-line gate and reconsider `ready-for-public-rc`.
