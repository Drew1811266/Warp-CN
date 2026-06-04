# zh-Hans Localization Phase 174

Date: 2026-06-02

## Scope

Phase 174 refreshed the RC26 locale export package and swept the localization
Python scripts. It used low-load Python commands only. It did not launch GUI,
compile Rust, build a bundle, generate PNGs, log in, call backend APIs, read
credentials, create billing or cloud state, create managed secrets/endpoints, or
mutate team state.

## Locale Export Commands

```text
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc26.json
result: passed

python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc26.json > /tmp/warp-cn-zh-Hans-locale-rc26.pretty.json
result: passed

nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc26.yaml
result: passed
```

Export sizes:

```text
 2566862 /tmp/warp-cn-zh-Hans-locale-rc26.json
 3004049 /tmp/warp-cn-zh-Hans-locale-rc26.pretty.json
 2184303 /tmp/warp-cn-zh-Hans-locale-rc26.yaml
 7755214 total
```

## Python Maintenance Commands

```text
nice -n 10 python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/zh_public_rc_status.py script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py
result: passed

nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py
result: 25 tests passed
```

## Decision

```text
Phase 174 decision: qualified-locale-export-and-script-sweep
continue automatically: yes
```

Phase 174 is qualified. RC26 export artifacts are valid in `/tmp`, and the
localization script tests remain green.

## Qualification Review

```text
phase: 174
status: qualified
JSON export: passed
JSON parse: passed
YAML export: passed
export sizes recorded: yes
py_compile: passed
Python unittest: 25 passed
external operations run: none
heavy operations run: none
```
