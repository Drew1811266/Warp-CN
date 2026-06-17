# Warp CN Windows 打包说明

## 目标

Windows 版不重新翻译主界面。它复用仓库现有的 `resources/localization/zh-Hans-overrides.toml` 源码级 overlay，只补 Windows 专属用户可见面：

- Inno Setup 安装器语言包。
- “添加到 PATH”安装任务。
- 资源管理器右键菜单中的“新标签页打开”和“新窗口打开”动作。
- Windows OSS 安装包输出命名。

## 依赖

在 Windows 上构建安装器需要：

- Git for Windows。
- Rust MSVC toolchain。
- Visual Studio 2022 Build Tools 和 Windows SDK。
- CMake、jq、cargo 构建辅助工具。
- Inno Setup 6，并确保 `ISCC.exe` 在 `PATH` 中。

可以先运行：

```powershell
.\script\windows\bootstrap.ps1
```

## 构建 Windows OSS 安装器

先运行汉化和 Windows 专属回归测试：

```powershell
python script\zh_apply_localization.py --validate-manifest
python script\zh_apply_localization.py --check-glossary
python -m unittest discover -s script -p "test_zh_*.py"
```

构建 x64：

```powershell
.\script\windows\bundle.ps1 -CHANNEL oss -ARCH x64 -RELEASE_TAG "0.20.6-cn-win.1"
```

构建 ARM64：

```powershell
.\script\windows\bundle.ps1 -CHANNEL oss -ARCH arm64 -RELEASE_TAG "0.20.6-cn-win.1"
```

未签名 OSS 安装器输出到 `script\windows\Output`，命名格式为：

```text
Warp-CN-<version>-windows-<x64|arm64>-oss-unsigned.exe
```

如果通过 `-SIGN_TOOL_CMD` 参数或 `SIGN_TOOL_CMD` 环境变量传入 signtool 命令，输出名会使用 `signed` 后缀，并由 Inno Setup 对安装器和卸载器执行签名。

## 手动编译 Inno Setup 脚本

通常应使用 `bundle.ps1`，因为它会先构建二进制、复制 bundled resources、写入版本元数据并传入正确的预处理参数。只有调试安装器脚本本身时，才直接调用：

```powershell
ISCC .\script\windows\windows-installer.iss `
  /DReleaseChannel=oss `
  /DMyAppExeName=warp-oss.exe `
  /DTargetProfileDir=target\x86_64-pc-windows-msvc\rlto `
  /DMyAppName=WarpOss `
  /DMyAppVersion=0.20.6-cn-win.1 `
  /DArch=x64 `
  /DOutputName=Warp-CN-0.20.6-cn-win.1-windows-x64-oss-unsigned
```

## 验证重点

安装后至少检查：

- 安装向导显示简体中文。
- PATH 任务显示“将 Warp 添加到 PATH”。
- 资源管理器目录和目录背景右键菜单显示中文动作。
- `warp-oss.cmd` 可从 PATH 调起。
- PowerShell、cmd、WSL 常用 shell 能正常打开。
- 中文输入法、复制、粘贴、新建 tab/window 正常。
- 卸载后清理 `{app}\bin` 和 PATH 项。

未签名安装器可能触发 Windows SmartScreen。公开 release 前应在 release notes 中明确写出未签名状态和 SHA256。
