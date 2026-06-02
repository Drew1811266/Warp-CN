# zh-Hans Localization Phase 75

Date: 2026-06-02 Asia/Shanghai

## Goal

Audit high-frequency translation quality and glossary consistency without
chasing additional coverage.

## Checks

Initial checks:

```text
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary --json
{
  "entries": 7843,
  "key": {"count": 150, "percent": 1.9},
  "context": {"count": 7843, "percent": 100.0},
  "status": {"count": 7843, "percent": 100.0},
  "preserve_terms": {"count": 113, "percent": 1.4},
  "notes": {"count": 0, "percent": 0.0},
  "expected_count": {"count": 195, "percent": 2.5}
}

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

rg -n 'target = ".*(智能体|智能代理|智能助手|智能助理|命令调色板|端点点|帐号)' resources/localization/zh-Hans-overrides.toml
no matches
```

Final checks:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7843
files: 492
already_applied: 5590
would_change: 0
missing: 0

nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
19 tests passed

git diff --check
```

## Term Review

Reviewed high-frequency target families:

| Term family | Decision |
| --- | --- |
| Agent | Preserve English `Agent`; forbidden Chinese variants returned no matches. |
| Command Palette | Use `命令面板`; forbidden `命令调色板` returned no matches. |
| endpoint | Use `端点`; forbidden typo `端点点` returned no matches. |
| account | Use `账户`; forbidden `帐号` returned no matches. |
| workspace | Use `工作区` where product context requires it. |
| workflow | Use `工作流`. |
| permission | Use `权限`. |
| environment | Use `环境`. |
| secret | Use `密钥`. |
| conversation | Use `对话`. |
| profile | Use `配置档` for execution/model/account profile contexts. |
| rule | Use `规则`. |
| MCP server | Mixed intentionally: user-facing settings often use `MCP 服务器`; protocol/provider contexts may preserve `MCP server`. |
| harness | Preserve `harness` where it is a product/CLI execution concept; translate only where existing UI already uses an accepted Chinese phrase. |

## Translation Corrections

No translation corrections were made in Phase 75.

Reasoning:

- The glossary checker passed.
- Forbidden/awkward target-term search returned no matches.
- The remaining visible differences are deliberate preserve-term choices or
  require a focused UI-context review rather than a broad glossary rewrite.
- Adding broad glossary rules for `MCP server` or `harness` now would break
  accepted preserve-term entries and should wait for a dedicated terminology
  migration decision.

## Glossary Changes

No glossary rules were changed in Phase 75.

The current glossary remains conservative and catches real known mistakes without
forcing all historical preserve-term entries into a single translation style.

## Qualification

Phase 75 is accepted as `qualified-translation-quality-audit`.

The phase is qualified because metadata and glossary checks passed, forbidden
target search returned no matches, dry-run reported `would_change: 0` and
`missing: 0`, Python localization tests passed, no unnecessary translation churn
was introduced, and `git diff --check` passed.
