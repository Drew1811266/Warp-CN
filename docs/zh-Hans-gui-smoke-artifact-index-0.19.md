# zh-Hans GUI Smoke Artifact Index - 0.19

## Scope

This index records current-cycle GUI smoke evidence for Warp CN 0.19 self-defined complete release. Do not commit raw private screenshots, recordings, account identifiers, callback URLs, endpoint URLs, billing IDs, team IDs, tokens, cookies, or magic links.

`known-limitation-documented` is a 0.19-local documentation status for this
self-defined release. It does not replace the central GUI smoke matrix statuses,
does not clear public-RC evidence rows, and does not mean static assets were
regenerated or design-approved.

## Required Rows

| ID | Area | Canonical Status | Artifact or Reviewer Note |
| --- | --- | --- | --- |
| GUI-SD-01 | App launch | verified-current-cycle | current-cycle reviewer note: `WarpOss.app` opened a foreground `~` workspace window and a `设置` window; menu bar and visible chrome were readable |
| GUI-SD-02 | Onboarding visible copy | known-limitation-documented | static onboarding PNG residue documented in `docs/zh-Hans-onboarding-visual-regeneration-plan.md`; source-level UI localization remains complete |
| GUI-SD-03 | Workspace shell | verified-current-cycle | current-cycle reviewer note: `文件 > 新建窗口` opened workspace window `~`; sidebar showed `搜索标签页...` and `新会话`; accessibility exposed `输入 shell 命令` / `命令输入`; no shell command was executed |
| GUI-SD-04 | Command search（界面文案：命令搜索） | verified-current-cycle | current-cycle reviewer note: `视图 > 命令搜索` opened command search panel with `命令搜索`, `我想找...`, `历史记录`, `示例查询`, and search placeholder `搜索历史记录、工作流等` |
| GUI-SD-05 | Settings core pages | verified-current-cycle | current-cycle reviewer note: `设置` window displayed readable navigation including `搜索`, `账号`, `Agent`, `代码`, `云平台`, `团队`, `外观`, `功能`, `键盘快捷键`, `Warpify`, `推荐`, `Warp Drive`, `隐私`, `关于` |
| GUI-SD-06 | AI settings entry | verified-current-cycle | current-cycle reviewer note: `Warp Agent` settings page displayed readable AI copy including `启用 AI`, `下一条命令`, `提示词建议`, `代码建议横幅`, `注册`; no credentials were entered |
| GUI-SD-07 | Dangerous confirmation cancel path | blocked-no-disposable-object | no disposable object was approved for this cycle; no real delete, transfer, billing, Cloud, secret, environment, endpoint, or team mutation was attempted |

## Known Limitations

Billing, Cloud quota, official backend capacity, real team ownership transfer, real secret deletion, real environment deletion, and real endpoint deletion are not required for 0.19 self-defined complete release.
