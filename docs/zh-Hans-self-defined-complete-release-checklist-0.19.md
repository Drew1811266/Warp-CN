# Warp CN 0.19 自定义汉化完成版 Checklist

创建日期：2026-06-06
最后更新：2026-06-07

策略更新：2026-06-07 用户已取消低负载开发限制；后续 heavy gate 不再等待
`zh_low_load_gate.py` 通过。

## Release Identity

- [x] 发行名称使用 `Warp CN 0.19 自定义汉化完成版`。
- [x] README 明确写明非官方 Warp 中文版本。
- [x] Release notes 明确写明不代表 Warp 官方发布。
- [x] public-RC blocker 未被伪造清零。

## Localization Gates

- [x] `python3 script/zh_apply_localization.py --validate-manifest` 通过。
- [x] `python3 script/zh_apply_localization.py --check-glossary` 通过。
- [x] `python3 script/zh_apply_localization.py --metadata-summary` 通过。
- [x] `python3 script/zh_apply_localization.py --dry-run --summary` 显示 `would_change: 0` 和 `missing: 0`。
- [x] `python3 script/zh_localization_inventory.py --preset release --coverage` 显示 release coverage 100.0%。

## GUI Gates

- [x] 当前周期启动界面已验证。
- [x] 工作区 shell、tab、Command search（界面文案：命令搜索）已验证。
- [x] Settings 核心页已验证。
- [ ] 常见弹窗和危险确认取消路径已验证。当前无已批准 disposable object，本轮未触发真实危险确认。

说明：官方后端状态路径不属于当前 GUI pass 证据；其范围声明保留在 release notes
和后续 public-RC evidence lane。

## Packaging Gates

- [x] `python3 script/privacy_guard.py --all-tracked` 通过。
- [x] `git diff --check` 通过。
- [x] 低负载开发限制已取消；2026-06-06 的 `defer-heavy-gate` 只保留为历史记录。
- [x] `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp` 通过。
- [x] 本地启动或 bundle 验证通过。

## Publication Gates

- [ ] 用户批准 tag。
- [ ] 用户批准 push。
- [ ] 用户批准 GitHub release。

## Current Stop Point

```text
privacy_guard: pass
git diff --check: pass
dry_run: would_change 0, missing 0
release_inventory: coverage 100.0%
low_load_gate: no-longer-required-after-2026-06-07
cargo_check: pass
bundle_or_launch: pass
gui_smoke: verified-current-cycle-with-known-limitations-documented
onboarding_static_assets: known-limitation-documented
publication: not approved
```
