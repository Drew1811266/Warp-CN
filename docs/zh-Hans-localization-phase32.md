# zh-Hans Localization Phase 32

Date: 2026-06-01

## Goal

Review, freeze, and produce the RC9 localization gate after Phase 26-31 source, fixture-GUI, and account-state audits.

## Final Gate

Completed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_localization_inventory.py app/src/terminal --coverage
python3 script/zh_localization_inventory.py app/src/ai --coverage
python3 script/zh_export_locale.py --format json
python3 -m json.tool
python3 script/zh_export_locale.py --format yaml
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
cargo check -j 2 -p warp
```

The full manifest dry-run was executed with a throttled wrapper because repeated full scans had overheated the local machine. The Python command emitted a complete clean summary:

```text
entries: 6294
files: 301
already_applied: 4760
would_change: 0
missing: 0
```

The wrapper itself exited nonzero because of STOP/CONT throttling signal behavior after the clean summary was printed; no manifest drift or replacement failure was reported.

## Coverage

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 817 covered, 49 candidates, 94.3%
search: 269 covered, 0 candidates, 100.0%
settings: 1953 covered, 74 candidates, 96.3%
modals: 3682 covered, 1914 candidates, 65.8%
release: 6897 covered, 2037 candidates, 77.2%
terminal: 1231 covered, 1134 candidates, 52.1%
AI / Agent: 1904 covered, 780 candidates, 70.9%
```

Manifest metadata:

```text
entries: 6294
key: 150 (2.4%)
context: 6294 (100.0%)
status: 6294 (100.0%)
preserve_terms: 18 (0.3%)
notes: 0
expected_count: 150 (2.4%)
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc9.json: 2028430 bytes
/tmp/warp-cn-zh-Hans-locale-rc9.pretty.json: 2381488 bytes
/tmp/warp-cn-zh-Hans-locale-rc9.yaml: 1726169 bytes
```

## Rust Gate

`cargo check -j 2 -p warp` completed successfully.

Known warnings remain unchanged from this localization line:

- `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` has one unused-variable warning.
- `app/src/terminal/input/slash_commands/mod.rs` has unused binding warnings for slash command match arms.

## GUI Evidence

Phase 30 collected current-cycle local fixture screenshots under `docs/gui-smoke-artifacts/phase30/` without rebuilding the bundle.

Accepted fixture evidence:

- `GUI-ONB-01`: Chinese onboarding path was reachable, with residue from embedded English preview images and the reused pre-Phase-28 bundle.
- `GUI-AUTH-03`: logged-out privacy and disable-AI confirmation path showed Chinese anchors.
- `GUI-WS-01`: main window, left panel, search, and Settings navigation were readable in Chinese.
- `GUI-SET-03`: logged-out Settings > Agent was readable, but account-state subpaths still require an isolated account.

Phase 31 did not promote public-RC account/state rows because the required disposable test account, team, billing/quota state, cloud environment, managed auth secret, and custom endpoint were not available.

## Qualification

Phase 32 is accepted as `qualified-rc9-gate`.

RC9 decision: `ready-for-local-use-with-fixture-evidence`.

Public RC decision: not ready.

The project is suitable for local source-level and fixture-evidence review because manifest drift, glossary, export, Python tests, formatting, diff, and low-concurrency Rust compile gates are clean. It is not ready for public RC because required current-cycle isolated account/state evidence remains blocked.
