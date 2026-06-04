# zh-Hans Functional Risk Register

This register defines string classes that can cause bugs when translated. Default to preserving these strings unless source context proves they are passive user-visible copy.

## Risk Classes

| Class | Examples | Default action | Why it is risky |
| --- | --- | --- | --- |
| Command syntax | shell commands, CLI flags, slash commands, install commands | Preserve executable tokens; translate surrounding explanation only | Translation can make copied commands fail |
| Search tokens | `search_tags`, `search_keywords`, command palette tags | Preserve unless the product intentionally searches Chinese labels | Translation can break command discoverability or tests |
| Action IDs and internal names | `id!`, enum variant display used as keys, action identifiers | Preserve | Translation can break lookup or serialization |
| Telemetry | `TelemetryEvent`, analytics names, event properties | Preserve | Translation changes metrics contracts |
| Storage keys | keychain service names, config keys, secure storage keys | Preserve | Translation can orphan user data or break migration |
| Protocol and schema | serde names, GraphQL, JSON/YAML fields, URLs, headers | Preserve | Translation breaks API contracts |
| Provider/model identifiers | model IDs, provider names, endpoint fields | Preserve exact IDs; translate labels only | Translation breaks external provider configuration |
| Tests and fixtures | snapshot strings, test data, parser fixtures | Preserve unless test intentionally checks localized UI | Translation can invalidate tests without product value |
| Logs and diagnostics | `log::`, `tracing::`, `debug!`, `panic!`, `anyhow!` | Usually preserve | Logs are for developers and support; translation can reduce debuggability |
| Markdown and links | docs links, markdown anchors, inline code | Preserve syntax and URLs | Translation can break rendering or navigation |
| Placeholders | `{name}`, `%s`, `${var}`, markdown substitutions | Preserve exactly | Translation can crash formatting or show wrong dynamic values |
| Destructive actions | delete, remove, reset, transfer, revoke, disable | Translate only after context review | Wrong copy can mislead irreversible operations |
| Billing and quota | credits, plan, auto reload, billing, team seats | Translate with high scrutiny | Wrong copy can misrepresent cost or entitlement |
| Auth and security | login, token, keychain, secret, permission, privacy | Translate with high scrutiny | Wrong copy can cause unsafe authorization choices |

## Default Decisions

Use these decisions during review:

| Decision | Use when |
| --- | --- |
| `preserve` | The string is part of behavior, storage, protocol, telemetry, or diagnostics |
| `partial-translate` | The string mixes visible explanation with a command, provider, ID, or field name |
| `translate` | The string is clearly passive user-facing UI copy |
| `needs-owner-review` | Source context is ambiguous or the string appears in multiple roles |
| `ignore-in-inventory` | The string class should never be surfaced as a translation candidate |

## Required Notes For High-Risk Entries

Manifest entries in these areas should include `context` or `notes`:

- Destructive confirmation titles and buttons.
- Login, token, Keychain, privacy, and permission messages.
- Billing, plan, credit, quota, or team-seat copy.
- AI provider, API key, model, endpoint, or custom inference copy.
- Search or command palette labels that sit near search tags or keywords.
- Any entry where only part of the source should be translated.

## Review Examples

| Source type | Safe target pattern |
| --- | --- |
| `Run warp --help` | `运行 warp --help` |
| `API key` | `API 密钥` |
| `AWS Bedrock profile` | `AWS Bedrock 配置文件` |
| `Delete environment?` | `删除环境？` with object name and cancel path visible |
| `TelemetryEvent::OpenSettings` | Preserve and ignore |
| `search_tags = ["theme", "appearance"]` | Preserve unless search behavior is intentionally localized |

## Ignore Rule Maintenance

When adding ignore rules to `resources/localization/zh-Hans-inventory-ignore.toml`:

- Prefer precise path or line patterns.
- Do not hide visible labels, buttons, descriptions, toasts, dialogs, or user-facing errors.
- Add a comment explaining the reviewed class.
- Re-run release coverage after changes.

