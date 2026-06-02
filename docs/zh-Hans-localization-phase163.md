# zh-Hans Localization Phase 163

Date: 2026-06-02

## Scope

Phase 163 refreshed the locale export artifacts for future official `zh-CN`
i18n readiness. It did not edit the manifest, change source, build, launch GUI,
generate PNGs, log in, call backend APIs, or touch account, billing, cloud,
secret, endpoint, or team state.

## Export Commands

```text
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc25.json
result: passed

python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc25.json > /tmp/warp-cn-zh-Hans-locale-rc25.pretty.json
result: passed

nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc25.yaml
result: passed
```

Export sizes:

```text
/tmp/warp-cn-zh-Hans-locale-rc25.json: 2566862 bytes
/tmp/warp-cn-zh-Hans-locale-rc25.pretty.json: 3004049 bytes
/tmp/warp-cn-zh-Hans-locale-rc25.yaml: 2184303 bytes
```

The export sizes match the RC24 export sizes because no manifest entries changed
in this cycle.

## Exporter Tests

```text
nice -n 10 python3 -m py_compile script/zh_export_locale.py script/test_zh_export_locale.py
result: passed

nice -n 10 python3 -m unittest script/test_zh_export_locale.py
result: 4 tests passed
```

## Qualification Review

```text
phase: 163
status: qualified-locale-export-ready
JSON export: passed
JSON parse: passed
YAML export: passed
export sizes recorded: yes
exporter py_compile: passed
exporter tests: 4 passed
unexpected export change: no
external operations run: none
continue to Phase 164: yes
```
