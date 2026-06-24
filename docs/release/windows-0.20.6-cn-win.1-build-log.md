# Windows 0.20.6-cn-win.1 Build Log

## Environment

- OS: Microsoft Windows NT 10.0.26200.0
- Rust: `rustc 1.92.0 (ded5c06cf 2025-12-08)`
- Cargo: `cargo 1.92.0 (344c4567c 2025-10-21)`
- Inno Setup: 6.7.3
- Protobuf compiler: `libprotoc 35.0`
- License generator: `cargo-about 0.9.0`
- Arch: x64
- Channel: oss
- Signing: unsigned

## Commands

```powershell
python script\zh_apply_localization.py --validate-manifest
python script\zh_apply_localization.py --check-glossary
python -m unittest discover -s script -p "test_zh_*.py"
.\script\windows\bundle.ps1 -CHECK_ONLY -CHANNEL oss -ARCH x64 -RELEASE_TAG "0.20.6-cn-win.1"
.\script\windows\bundle.ps1 -CHANNEL oss -ARCH x64 -RELEASE_TAG "0.20.6-cn-win.1"
Get-FileHash .\script\windows\Output\Warp-CN-0.20.6-cn-win.1-windows-x64-oss-unsigned.exe -Algorithm SHA256
```

## Result

- Installer: `script\windows\Output\Warp-CN-0.20.6-cn-win.1-windows-x64-oss-unsigned.exe`
- Size: `114615746` bytes
- SHA256: `6938E87075D25D9C73E392878580AC60ECC077307A758D462E01FA63949B5D96`
- Build result: pass

## Notes

- The first full build produced `target\x86_64-pc-windows-msvc\rlto\warp-oss.exe`.
- Packaging then reused the built binary with `-SKIP_BUILD_BINARY` after adding missing build tools.
- The installer uses the project-pinned `script\windows\languages\ChineseSimplified.isl`, so the build does not depend on the local Inno Setup installation containing that language file.
- Local dependency fetches were stabilized with the Phase 1 archive workspace and isolated Cargo cache described in `docs\superpowers\plans\2026-06-17-windows-0.20.6-release.md`.
