# zh-Hans Localization Phase 78

Date: 2026-06-02 Asia/Shanghai

## Goal

Produce RC15 with a complete low-load command-line gate and an honest decision
that separates source readiness, static visual assets, and public-RC external
evidence.

## Consistency Review

Reviewed Phase 71-77 records:

- `docs/zh-Hans-localization-phase71.md`
- `docs/zh-Hans-localization-phase72.md`
- `docs/zh-Hans-localization-phase73.md`
- `docs/zh-Hans-localization-phase74.md`
- `docs/zh-Hans-localization-phase75.md`
- `docs/zh-Hans-localization-phase76.md`
- `docs/zh-Hans-localization-phase77.md`

The records are consistent with the RC15 conclusion:

- Source-level localization gates pass.
- Preserve/ignore rules are exact-path and documented.
- Translation quality audit found no forced glossary migration.
- Public-RC evidence is prepared but still blocked by disposable prerequisites.
- Visual asset scripts are prepared but PNGs are not regenerated or approved.
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
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc15.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc15.json > /tmp/warp-cn-zh-Hans-locale-rc15.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc15.yaml
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
  "entries": 7843,
  "key": {"count": 150, "percent": 1.9},
  "context": {"count": 7843, "percent": 100.0},
  "status": {"count": 7843, "percent": 100.0},
  "preserve_terms": {"count": 113, "percent": 1.4},
  "notes": {"count": 0, "percent": 0.0},
  "expected_count": {"count": 195, "percent": 2.5}
}
```

Full dry-run:

```text
entries: 7843
files: 492
already_applied: 5590
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 5199 covered, 287 candidates, 94.8%
release: 8533 covered, 291 candidates, 96.7%
terminal: 2135 covered, 159 candidates, 93.1%
AI / Agent: 2517 covered, 128 candidates, 95.2%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc15.json: 2534285 bytes
/tmp/warp-cn-zh-Hans-locale-rc15.pretty.json: 2964752 bytes
/tmp/warp-cn-zh-Hans-locale-rc15.yaml: 2156891 bytes
```

Python tests:

```text
19 tests passed
```

Rust compile:

```text
CARGO_BUILD_JOBS=2 nice -n 10 cargo check -j 2 -p warp
Finished dev profile successfully in 15.03s
```

Known warnings:

- Existing unused-variable warnings remain in
  `app/src/remote_server/ssh_transport/installation/scp_fallback.rs`.
- Existing unused-variable warnings remain in
  `app/src/terminal/input/slash_commands/mod.rs`.

## RC15 Decision

Created:

- `docs/zh-Hans-release-candidate-2026-06-02-rc15.md`

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

No GUI, account, backend, static image, billing, cloud, team, environment,
managed secret, endpoint, or destructive state mutation was performed.

## Qualification

Phase 78 is accepted as `qualified-rc15-freeze-gate`.

The phase is qualified because manifest validation, glossary, target-term
search, metadata, full dry-run, coverage, JSON/YAML exports, JSON parse,
py_compile, Python tests, `cargo fmt --check`, `git diff --check`, and
low-concurrency `cargo check -j 2 -p warp` passed, and the RC15 decision
honestly preserves the remaining public-RC and static-image blockers.
