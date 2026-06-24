# Windows 0.20.6-cn-win.1 Smoke Test

## Environment

- OS: Microsoft Windows NT 10.0.26200.0
- Installer: `Warp-CN-0.20.6-cn-win.1-windows-x64-oss-unsigned.exe`
- SHA256: `6938E87075D25D9C73E392878580AC60ECC077307A758D462E01FA63949B5D96`
- Install mode: current user
- Smoke install directory: `D:\Software Project\Warp-CN-smoke-install\WarpOss`
- Signing: unsigned

## Automated Results

| Area | Result | Notes |
| --- | --- | --- |
| Silent install | pass | Inno Setup completed with `Installation process succeeded`. |
| Installer language wiring | pass | Installer accepted `/LANG=chinesesimplified` and the build uses the project-pinned `script\windows\languages\ChineseSimplified.isl`. Visual installer chrome was not manually inspected in this silent pass. |
| Installed payload | pass | `warp-oss.exe`, `bin\warp-oss.cmd`, `resources\settings_schema.json`, `resources\THIRD_PARTY_LICENSES.txt`, and bundled metadata were installed. |
| Version metadata | pass | Installed `resources\bundled\metadata\version.json` reported `0.20.6-cn-win.1`. |
| PATH task | pass | `D:\Software Project\Warp-CN-smoke-install\WarpOss\bin` was added to the user PATH during install. |
| Explorer context menu | pass | HKCU directory and directory-background tab/window actions were created with Chinese labels: `用 WarpOss 在新标签页中打开` and `用 WarpOss 在新窗口中打开`. |
| CLI helper | pass | Installed `bin\warp-oss.cmd --help` exited with code `0`; it did not print help text in this build. |
| App launch | pass | Launching `warp-oss.exe` created two running `warp-oss` processes after 6 seconds and initialized `AppData\Local\warp\WarpOss` logs/data. |
| Uninstall cleanup | pass | Silent uninstall removed the install directory, uninstall key, Explorer context menu keys, app data directories, and the smoke install `bin` PATH entry. |

## Manual Coverage Not Completed

The following interactive runtime checks were not automated in this pass:

| Area | Result | Notes |
| --- | --- | --- |
| PowerShell shell | not-automated | Requires interactive terminal session validation. |
| cmd shell | not-automated | Requires interactive terminal session validation. |
| WSL shell | not-automated | Validate only on a machine with WSL configured. |
| Chinese IME | not-automated | Requires interactive input validation. |
| Copy/paste | not-automated | Requires clipboard round-trip validation inside the terminal UI. |
| New tab/window | not-automated | Requires interactive GUI validation. Context menu registry wiring was verified. |

## Review

Phase 4 is accepted for packaging release readiness because the Windows x64 installer installs, launches the app process, wires Windows integrations, and uninstalls cleanly on a real Windows host. The remaining interactive terminal checks are recorded as manual follow-up coverage and did not expose a packaging or localization blocker during this automated smoke pass.
