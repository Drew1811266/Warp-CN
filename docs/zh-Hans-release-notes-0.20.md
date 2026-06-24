# Warp CN 0.20 发行说明

Date: 2026-06-07

Status: self-defined-complete-release-snapshot

## 说明

这份文档是 Warp CN 自定义汉化版 `0.20` 的发行说明。它不是 Warp 官方发行说明，
不代表 Warp 官方发布、官方中文版本或官方 release。

## 当前状态

```text
source overlay status: clean
packaging preflight: pass
current-cycle GUI smoke: verified-current-cycle-with-known-limitations-documented
onboarding static assets: known-limitation-documented
public-RC evidence: incomplete
backend_fixture: 5
isolated_account: 3
disposable_object: 3
```

当前基线验证结果如下：

```text
manifest validation passed
glossary check passed
entries: 7937
files: 550
already_applied: 5717
would_change: 0
missing: 0
zh-Hans public-RC blocker status
total: 11
public_rc_required: 11
```

## 版本范围

`0.20` 表示 Warp CN 自定义简体中文汉化版当前开发快照，不代表 public-RC readiness。

## Completed Scope

- 简体中文源码级 overlay 保持干净。
- 2026-06-07 packaging preflight 通过：`privacy_guard`、`git diff --check`、`cargo check -p warp` 和 bundle preparation 均通过。
- 高频用户界面、设置、工作区、Command search（界面文案：命令搜索）和核心 Agent 文案已纳入汉化清单。
- 当前周期 GUI smoke 已验证 app launch、workspace shell、command search、Settings core pages 和 AI settings entry。
- 发行说明明确非官方 fork 边界。
- 官方后端状态和高风险对象路径按 known limitations 管理。

## Windows 支线

Windows 版复用同一套简体中文源码级 overlay，不单独维护第二份主界面翻译。当前 Windows 专属补充范围是项目内固定的 Inno Setup 简体中文安装器语言包、安装任务、资源管理器右键菜单和 OSS 安装包命名。

Windows OSS 安装器由 `script/windows/bundle.ps1` 生成，推荐优先验证 `x64`：

```powershell
python script\zh_apply_localization.py --validate-manifest
python script\zh_apply_localization.py --check-glossary
python -m unittest discover -s script -p "test_zh_*.py"
.\script\windows\bundle.ps1 -CHANNEL oss -ARCH x64 -RELEASE_TAG "0.20.6-cn-win.1"
```

未签名输出命名为 `Warp-CN-0.20.6-cn-win.1-windows-x64-oss-unsigned.exe`。公开发布时需要附带 SHA256，并明确未签名安装器可能触发 Windows SmartScreen。

## Known Limitations

Warp CN 0.20 自定义汉化版不声称以下官方后端或高风险对象路径已完成 full public-RC evidence closure：

- Billing、credits、quota、build-plan migration。
- Cloud capacity 或官方后端容量状态。
- AWS Bedrock 真实凭据和真实 provider credential。
- 真实 team ownership transfer。
- 真实 managed secret、environment、endpoint 删除。
- 个人主账号 login callback 和认证材料。
- Onboarding static PNG assets may retain inherited English text until the visual asset regeneration lane completes.

Backend and high-risk object paths remain in the public-RC evidence registry as future higher-assurance validation work. They are not hard blockers for the `0.20` self-defined complete release snapshot.

## Backend Fixture Request

当前 backend fixture 请求地址：

- [warpdotdev/warp#12129](https://github.com/warpdotdev/warp/issues/12129)
