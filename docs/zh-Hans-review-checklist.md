# zh-Hans Translation Review Checklist

Use this checklist whenever adding or reviewing Warp CN translations. It is optimized for normal development review and avoids high-load test runs unless preparing a release candidate.

## 1. Entry Snapshot

Record:

- Branch name.
- Upstream base or release tag if relevant.
- Whether the worktree already had unrelated changes.
- Module or file scope under review.
- Whether the review is copy-only, functional-risk, GUI, or release-candidate.

## 2. Per-Entry Review

For each new or changed manifest entry:

| Check | Pass condition |
| --- | --- |
| Source context | The Rust file and nearby code prove the string is user-visible or safe to translate |
| Meaning | Chinese keeps the original product intent |
| Tone | Wording is concise and suitable for a terminal/productivity tool |
| Glossary | Stable terms follow `zh-Hans-glossary.toml` |
| Preservation | Product names, commands, providers, formats, and IDs are preserved when needed |
| Placeholder safety | `{}`, `%`, `$`, markdown, links, shortcut symbols, and dynamic values are unchanged |
| UI length | Button/menu/modal copy is short enough for the target surface |
| Status | High-risk entries include `status`, `context`, and `notes` where useful |

Do not approve a string only because it is understandable in isolation. The surrounding product state decides whether it is correct.

## 3. Functional Risk Questions

Ask these before accepting a translation:

- Is the string parsed by command, shell, search, YAML, JSON, GraphQL, URL, protocol, or regex code?
- Is the string a telemetry event, feature flag, storage key, provider ID, model ID, or action ID?
- Is the string used in tests, snapshots, fixtures, logs, debug output, or panic messages?
- Is the string copied by the user into a terminal, config file, API field, or support ticket?
- Does the translation change a destructive action, billing action, login action, security action, or permission prompt?
- Does the target keep all placeholders and markdown links intact?

If any answer is yes, review the entry against `docs/zh-Hans-functional-risk-register.md`.

## 4. Low-Load Command Gate

Run these during normal review:

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

Run module coverage when deciding the next slice:

```bash
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

## 5. GUI Review

For GUI evidence:

- Use the row IDs in `docs/zh-Hans-gui-smoke-matrix.md`.
- Prefer Computer Use accessibility text over screenshots.
- Use screenshots only as supporting evidence.
- Do not store raw full-screen desktop screenshots in git.
- Mark fixture-only evidence as `fixture-verified`, never `verified`.
- Do not use the user's main account for billing, team, cloud, auth secret, endpoint deletion, or ownership transfer.

## 6. Release Candidate Escalation

Only for release candidates, add the heavier gate:

```bash
cargo fmt --check
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Run additional targeted Rust tests only for paths changed in the review.

## 7. Review Decision

Use one of these outcomes:

| Outcome | Meaning |
| --- | --- |
| `accepted` | Translation is correct and low risk |
| `accepted-with-note` | Translation is acceptable but needs later GUI or product-state evidence |
| `needs-copy-fix` | Chinese wording is wrong, awkward, or inconsistent |
| `needs-functional-review` | The string may affect behavior or parsing |
| `blocked` | Missing account state, fixture, UI access, or safe test object |

