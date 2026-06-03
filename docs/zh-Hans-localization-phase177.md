# zh-Hans Localization Phase 177

Date: 2026-06-02

## Scope

Phase 177 freezes the post-RC26 execution baseline before bundle, GUI, account,
backend, disposable-object, Agent lifecycle, PNG, upstream freshness, or RC27
work. It does not add translations, change source code, launch GUI, build a
bundle, log in, touch backend state, create/delete objects, or mutate team,
billing, cloud, endpoint, or managed-secret state.

## Git Baseline

```text
branch: codex/zh-Hans-post-rc26-execution
status: clean
HEAD: 16f25705027665df5a3638d0251443b3ce44eca7
github/main: 16f25705027665df5a3638d0251443b3ce44eca7
tag 0.15 object: ea9d968cabf32b4ca040652d8dc4bfe12614a1c8
tag 0.15 target: 16f25705027665df5a3638d0251443b3ce44eca7
```

The execution branch starts from the same commit as `github/main`, and tag
`0.15` resolves to the same commit.

## Localization Baseline

```text
manifest validation: passed
glossary check: passed
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context: 7943 (100.0%)
metadata status: 7943 (100.0%)
release inventory: 8574 covered, 2 candidates, 100.0%
```

The two release candidates remain the intentional preserved `Agent` product
term residues, not unexpected untranslated UI copy.

## Public-RC Registry

```text
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

No public-RC blocker was cleared in this phase. Phase 177 is a baseline freeze,
not an external evidence phase.

## Command Results

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
python3 script/privacy_guard.py --all-tracked
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py
cargo fmt --check
git diff --check
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

Rust compile result:

```text
Finished dev profile target(s) in 1.47s
warnings: 46 existing unused-variable warnings
errors: none
```

The warnings are pre-existing unused-variable warnings in app source paths and
are not caused by this phase.

## Review

Phase 177 is accepted.

Acceptance review:

```text
source overlay clean: yes
manifest drift: none
release inventory unexpected candidates: none
public-RC blocker registry readable: yes
privacy guard: passed
Python tests: passed
cargo fmt: passed
git diff check: passed
cargo check -p warp: passed
safe to continue to Phase 178 fresh bundle gate: yes
```
