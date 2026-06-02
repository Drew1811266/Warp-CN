# zh-Hans Localization Phase 112

Date: 2026-06-02

## Scope

Phase 112 added a lightweight public-RC blocker status script and unit tests. It
did not run GUI, compile Rust, bundle, PNG generation, account login, backend,
billing, cloud, managed-secret, endpoint, or team operations.

## Runtime Note

The local `python3` runtime is Python 3.9.6, so `tomllib` is not available.
`script/zh_public_rc_status.py` therefore uses a small dependency-free parser
for the registry subset used here:

```text
[[blocker]]
quoted strings
quoted string arrays
booleans
```

This keeps the script compatible with the current machine without installing
packages or changing the system Python.

## Files

```text
script: script/zh_public_rc_status.py
tests: script/test_zh_public_rc_status.py
registry: resources/localization/zh-Hans-public-rc-blockers.toml
```

## Commands Run

```text
nice -n 10 python3 -m py_compile script/zh_public_rc_status.py script/test_zh_public_rc_status.py
result: passed

nice -n 10 python3 script/zh_public_rc_status.py
result: passed

nice -n 10 python3 script/zh_public_rc_status.py --json
result: passed

nice -n 10 python3 -m unittest script/test_zh_public_rc_status.py
result: 6 tests passed

nice -n 10 python3 script/zh_public_rc_status.py --json > /tmp/warp-cn-public-rc-blockers-rc20.json
python3 -m json.tool /tmp/warp-cn-public-rc-blockers-rc20.json > /tmp/warp-cn-public-rc-blockers-rc20.pretty.json
result: passed

git diff --check -- resources/localization/zh-Hans-public-rc-blockers.toml docs/zh-Hans-localization-phase111.md script/zh_public_rc_status.py script/test_zh_public_rc_status.py
result: passed
```

## Summary Output

```text
zh-Hans public-RC blocker status
total: 11
public_rc_required: 11
statuses:
  blocked-no-backend-fixture: 5
  blocked-no-disposable-object: 3
  blocked-no-isolated-account: 3
categories:
  backend_fixture: 5
  disposable_object: 3
  isolated_account: 3
```

## JSON Export

```text
raw JSON: /tmp/warp-cn-public-rc-blockers-rc20.json
pretty JSON: /tmp/warp-cn-public-rc-blockers-rc20.pretty.json
```

## Test Coverage

The unit tests cover:

```text
valid registry summary
duplicate blocker id rejection
missing required field rejection
missing handoff_doc rejection
JSON output shape
default registry smoke
```

## Qualification Review

```text
phase: 112
status: qualified
script validates required schema fields: yes
script rejects duplicate IDs: yes
script verifies handoff_doc paths: yes
unit tests: 6 passed
real registry summary matches RC19 blocker counts: yes
external operations run: none
```
