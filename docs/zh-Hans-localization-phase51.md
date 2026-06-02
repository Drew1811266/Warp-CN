# zh-Hans Localization Phase 51

Date: 2026-06-02

## Goal

Reduce or classify terminal executor/bootstrap residue while preserving shell, WSL, MSYS2, SSH, bootstrap, registry, and remote-command behavior.

## Scope

Phase 51 added 79 scoped manifest entries:

```text
translated visible entries: 5
reviewed preserve entries: 74
files touched by scoped manifest: 9
main manifest entries after Phase 51: 7263
manifest context/status metadata: 100.0%
```

Translated visible copy:

| Area | File |
| --- | --- |
| Shared-session viewer reconnect/permissions/guest toasts | `app/src/terminal/shared_session/viewer/terminal_manager.rs` |

Reviewed preserves:

| Class | Examples |
| --- | --- |
| Bootstrap asset/script/template contracts | `bash.sh`, `zsh.sh`, `@@USING_CON_PTY_BOOLEAN@@`, `InitSubshell`, `export WARP_HONOR_PS1={}; {}` |
| Windows registry/env diagnostics | `System\\CurrentControlSet...`, `WarpTerminal`, registry conversion diagnostics |
| In-band generator command templates | `Warp-Run-GeneratorCommand ...`, `warp_run_generator_command ...` |
| Local/WSL/MSYS2 shell args | `-c`, `--norc`, `--no-config`, `-NoProfile`, `--distribution`, `--exec` |
| SSH command args/options | `-q`, `-o`, `PasswordAuthentication=no`, `ForwardX11=no`, `ControlPath={}` |
| Remote server executor protocol diagnostics | `SESSION_NOT_FOUND`, proto-level empty-response diagnostics |
| Shared-session viewer debug/log diagnostics | LRC update diagnostic and prompt snapshot deserialize log |

## Coverage

After Phase 51:

```text
terminal coverage: 1850 covered / 524 candidates = 77.9%
release coverage: 7954 covered / 997 candidates = 88.9%
```

The Phase 51 target files now have no remaining inventory candidates:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
```

## Safety Review

No command, shell arg, env var, bootstrap script template, registry path, WSL/MSYS2 contract, SSH option, remote-server protocol diagnostic, serialized identifier, or debug/log diagnostic was translated incorrectly.

`cargo check` was intentionally deferred to Phase 54 because Phase 51 changes are string-only, preserve-heavy, and `cargo fmt --check` passed.

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase51-manifest.toml --dry-run --summary
# entries: 79
# files: 9
# already_applied: 5
# would_change: 0
# missing: 0

python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

## Qualification

Phase 51 is accepted as `qualified-terminal-executor-protocol-preservation-pass`.
