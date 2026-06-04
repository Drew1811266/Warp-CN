# zh-Hans Localization Phase 70

Date: 2026-06-02 Asia/Shanghai

## Goal

Produce RC14 with a complete command-line gate and a decision that separates
source readiness, static visual assets, and public-RC external evidence.

## Consistency Review

Reviewed the Phase 63-69 records and the RC/public-RC support docs:

- `docs/zh-Hans-localization-phase63.md`
- `docs/zh-Hans-localization-phase64.md`
- `docs/zh-Hans-localization-phase65.md`
- `docs/zh-Hans-localization-phase66.md`
- `docs/zh-Hans-localization-phase67.md`
- `docs/zh-Hans-localization-phase68.md`
- `docs/zh-Hans-localization-phase69.md`
- `docs/zh-Hans-public-rc-gate-runbook.md`
- `docs/zh-Hans-gui-smoke-matrix.md`
- `docs/zh-Hans-onboarding-visual-regeneration-plan.md`

The records are consistent with the RC14 conclusion:

- Source-level localization gates pass.
- Public RC remains blocked by isolated account/backend evidence.
- Static onboarding visual residue remains blocked by regeneration or design approval.
- No GUI, account, backend, static image, or destructive state was touched.

## Final Gate

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
rg -n 'target = ".*(智能体|智能代理|智能助手|智能助理|命令调色板|端点点|帐号)' resources/localization/zh-Hans-overrides.toml
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary --json
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py --preset onboarding --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset workspace --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset search --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset settings --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset modals --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/ai --coverage
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc14.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc14.json > /tmp/warp-cn-zh-Hans-locale-rc14.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc14.yaml
nice -n 10 python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt --check
git diff --check
CARGO_BUILD_JOBS=2 nice -n 10 cargo check -j 2 -p warp
```

The forbidden/awkward target-term search returned no matches.

## Evidence

Metadata:

```json
{
  "entries": 7792,
  "key": {"count": 150, "percent": 1.9},
  "context": {"count": 7792, "percent": 100.0},
  "status": {"count": 7792, "percent": 100.0},
  "preserve_terms": {"count": 98, "percent": 1.3},
  "notes": {"count": 0, "percent": 0.0},
  "expected_count": {"count": 192, "percent": 2.5}
}
```

Full dry-run:

```text
entries: 7792
files: 475
already_applied: 5539
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 5180 covered, 435 candidates, 92.3%
release: 8514 covered, 439 candidates, 95.1%
terminal: 2106 covered, 268 candidates, 88.7%
AI / Agent: 2527 covered, 167 candidates, 93.8%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc14.json: 2518742 bytes
/tmp/warp-cn-zh-Hans-locale-rc14.pretty.json: 2946125 bytes
/tmp/warp-cn-zh-Hans-locale-rc14.yaml: 2143920 bytes
```

Python tests:

```text
19 tests passed
```

Rust compile:

```text
CARGO_BUILD_JOBS=2 nice -n 10 cargo check -j 2 -p warp
Finished dev profile successfully in 16.81s
```

Known warnings:

- Existing unused-variable warnings remain in
  `app/src/remote_server/ssh_transport/installation/scp_fallback.rs`.
- Existing unused-variable warnings remain in
  `app/src/terminal/input/slash_commands/mod.rs`.

## RC14 Decision

Created:

- `docs/zh-Hans-release-candidate-2026-06-02-rc14.md`

Updated:

- `docs/zh-Hans-localization.md`

Decision: `ready-for-local-use-with-fixture-evidence`.

Public RC decision: not ready.

Public RC is still blocked by missing isolated account/backend evidence for
auth, AI settings, AWS/Bedrock credentials, environment deletion, managed auth
secret deletion, custom endpoint removal, team ownership transfer,
billing/quota, and cloud backend states. Static onboarding imagery is also still
blocked by the 50 deferred PNGs that require regeneration or explicit design
approval.

## Low-Load Review

All final gates were run serially. Longer commands used `nice -n 10`, and the
Rust compile used `CARGO_BUILD_JOBS=2` with `cargo check -j 2 -p warp`.

Earlier full dry-run attempts were stopped when they violated the low-load
intent. The dry-run path was optimized in Phase 69 so the final RC14 dry-run
could complete quickly without repeatedly scanning the same files.

## Qualification

Phase 70 is accepted as `qualified-rc14-freeze-gate`.

The phase is qualified because manifest validation, glossary, target-term
search, metadata, full dry-run, coverage, JSON/YAML exports, JSON parse,
py_compile, Python tests, `cargo fmt --check`, `git diff --check`, and
low-concurrency `cargo check -j 2 -p warp` passed, and the RC14 decision
honestly preserves the remaining public-RC and static-image blockers.
