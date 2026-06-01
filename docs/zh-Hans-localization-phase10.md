# Warp CN Phase 10 Translation Review And Functional Safety Plan

**Goal:** Build a repeatable review system for the current zh-Hans overlay so every translated module can be checked for language quality, terminology consistency, UI safety, and functional safety before a release decision.

**Performance policy:** Phase 10 uses low-load validation by default. Run manifest, glossary, inventory, export, formatting, and Python tests first. Do not run full workspace builds, broad `cargo test`, or repeated GUI bundle builds unless preparing a release candidate and the machine is idle.

**Primary assets:**

- `resources/localization/zh-Hans-overrides.toml`
- `resources/localization/zh-Hans-glossary.toml`
- `resources/localization/zh-Hans-inventory-ignore.toml`
- `docs/zh-Hans-gui-smoke-matrix.md`
- `docs/zh-Hans-module-review-matrix.md`
- `docs/zh-Hans-functional-risk-register.md`
- `docs/zh-Hans-evidence-policy.md`
- `docs/zh-Hans-review-checklist.md`

## 1. Review Positioning

Phase 10 treats the localized source tree as a build artifact. The durable asset is the manifest, glossary, ignore policy, review matrix, GUI evidence, and release gate history.

The review goal is not just "more Chinese". Each accepted translation must satisfy four checks:

1. The Chinese is accurate in the current UI context.
2. The wording follows the project glossary and established product terminology.
3. The replacement does not affect parser tokens, IDs, telemetry, storage keys, protocol data, tests, logs, or search behavior.
4. The rendered UI remains usable in real Warp surfaces.

## 2. Severity Model

Translation severity:

| Level | Meaning | Release impact |
| --- | --- | --- |
| `T0` | Dangerous or misleading translation for destructive, billing, auth, security, or irreversible actions | Blocks release |
| `T1` | Incorrect meaning in a core workflow | Blocks release until fixed |
| `T2` | Awkward, inconsistent, or weak-context translation | Fix before public RC when practical |
| `T3` | Style polish only | Does not block |

Functional severity:

| Level | Meaning | Release impact |
| --- | --- | --- |
| `F0` | Can break startup, build, command parsing, persistence, auth, secure storage, or API contracts | Blocks release |
| `F1` | Can break an important feature path | Blocks affected module |
| `F2` | Can break search, layout, shortcut discoverability, or error diagnosis | Needs module owner review |
| `F3` | Low-risk visible UI text | Normal copy review |

## 3. Review Lanes

### Lane A: Manifest And Terminology

Use this lane for every manifest edit.

Required checks:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
```

Acceptance:

- Manifest schema is valid.
- Glossary check passes.
- Dry-run reports `missing: 0`.
- New high-risk entries have `key`, `context`, `status`, and `notes` where needed.

### Lane B: Inventory And Coverage

Use this lane before deciding the next translation slice.

Required checks:

```bash
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

Acceptance:

- Coverage numbers are recorded in the phase notes or release-candidate notes.
- Low-coverage modules are not promoted by percentage alone; high-risk paths still need semantic and functional review.

### Lane C: Functional Safety

Use this lane for entries that are not obviously passive UI copy.

Review against `docs/zh-Hans-functional-risk-register.md`.

Acceptance:

- Command grammar, search tokens, telemetry names, IDs, storage keys, protocol strings, logs, and tests are either preserved or explicitly justified.
- Any partial translation keeps the technical token intact.
- Any ignored path has a reason in `zh-Hans-inventory-ignore.toml` or the review matrix.

### Lane D: GUI Evidence

Use this lane before release labels such as `verified`, `ready-for-local-use`, or `ready-for-public-rc`.

Review against `docs/zh-Hans-gui-smoke-matrix.md` and `docs/zh-Hans-evidence-policy.md`.

Acceptance:

- `verified` means the Chinese text was seen in the app, not just present in source.
- `fixture-verified` is never promoted to public-RC evidence.
- Screenshots are cropped or redacted and do not expose full desktop, accounts, tokens, browser state, or private paths.

## 4. Phase 10 Task Plan

| Task | Target | Acceptance |
| --- | --- | --- |
| P10-M0 | Evidence hygiene | Screenshot rules exist, future raw screenshots are ignored, existing public artifact risk is called out |
| P10-M1 | Module review matrix | Every major Warp CN module has review focus, risk class, evidence type, and current status |
| P10-M2 | Functional risk register | Dangerous string classes and default actions are documented |
| P10-M3 | Reviewer checklist | A reviewer can run a complete low-load review without reconstructing commands |
| P10-M4 | Light validation pass | Manifest, glossary, dry-run, coverage, export, compile, and Python localization tests pass |
| P10-M5 | Release gate mapping | Heavy tests are listed as release-only gates, not continuous low-load gates |

## 5. Low-Load Gate

Run this gate during normal review work:

```bash
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
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
git diff --check
```

## 6. Release-Only Heavy Gate

Run these only for a release candidate or when a related product path was changed:

```bash
cargo fmt --check
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
cargo test -p ai custom_inference_smoke
cargo test -p warp custom_inference_smoke_override
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Do not run broad workspace tests or repeated bundle builds while doing routine copy review.

## 7. Exit Criteria

Phase 10 is complete when:

- The review plan, checklist, module matrix, risk register, and evidence policy exist.
- `.gitignore` prevents new raw GUI screenshot/video evidence from being accidentally added.
- The low-load gate passes.
- The remaining public-RC blockers are expressed as explicit account/state/evidence gates, not vague "needs testing" notes.

