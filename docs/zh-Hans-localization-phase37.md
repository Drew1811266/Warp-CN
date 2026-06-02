# zh-Hans Localization Phase 37

Date: 2026-06-01

## Goal

Prepare GUI fixture paths and decide how to handle embedded English visual residue before current-source GUI smoke.

## Visual Residue Findings

Phase 30's visible English residue comes from two different classes:

1. Reused-bundle source residue:
   - `auto (cost-efficient)` appeared because Phase 30 reused an older bundle.
   - This should disappear after Phase 38 rebuilds from current source.

2. Static PNG content residue:
   - Onboarding preview images are bundled bitmap assets under `app/assets/async/png/onboarding/`.
   - They are referenced by onboarding/login source files such as:
     - `crates/onboarding/src/slides/intention_slide.rs`
     - `crates/onboarding/src/slides/customize_slide.rs`
     - `crates/onboarding/src/slides/theme_picker_slide.rs`
     - `crates/onboarding/src/slides/third_party_slide.rs`
     - `app/src/auth/login_slide.rs`

Representative asset roots:

- `app/assets/async/png/onboarding/welcome_agent.png`
- `app/assets/async/png/onboarding/welcome_terminal.png`
- `app/assets/async/png/onboarding/agent_intention/`
- `app/assets/async/png/onboarding/terminal_intention/`
- `app/assets/async/png/onboarding/thirdparty_*.png`

These bitmap residues are not manifest drift and should not be counted as missing Rust localization entries.

## Policy Decision

| Residue | Decision | Rationale |
| --- | --- | --- |
| Reused-bundle `auto (cost-efficient)` | Rebuild current source in Phase 38 and re-screenshot. | Source was already localized before RC9, but Phase 30 did not rebuild. |
| Static onboarding preview PNG English | Track as `visual-residue` until localized images are regenerated or product accepts English imagery. | Replacing bitmap assets is a design/content task, not a string manifest task. |
| Theme names such as `Phenomenon`, `Dark`, `Light`, `Adeberry` | Preserve pending product/design decision. | They may be theme identifiers/brand names rather than translatable UI labels. |

## Fixture Plan

Phase 38 should use:

- `zh-rc10-local-fixture` for current-source logged-out onboarding, privacy/disable-AI, workspace, and token fallback checks.
- `zh-rc10-agent-fixture` for local Agent tips, conversation details, lifecycle labels, error states, and environment fallback.

Fixture rules:

- Fixture evidence remains `fixture-evidence`; it cannot promote public RC by itself.
- Debug-only fixture gates, if added, must require an explicit env var and must be inert without that env var.
- Fixtures must not create accounts, spend credits, create/delete cloud objects, reveal secrets, or mutate team ownership.
- Static image residue should be recorded separately from GUI text evidence.

## Runbook Updates

Updated:

- `docs/zh-Hans-public-rc-gate-runbook.md`
- `docs/zh-Hans-gui-smoke-matrix.md`

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

## Qualification

Phase 37 is accepted as `qualified-gui-fixture-visual-residue-prep`.

The phase is qualified because every Phase 30 visual residue now has a policy decision, fixture evidence remains separated from public-RC evidence, and no risky account/backend/source fixture mutation was introduced.
