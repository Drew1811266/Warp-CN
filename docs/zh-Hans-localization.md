# zh-Hans localization branch

This branch is a local Chinese localization branch for Warp's open-source client.

## Current approach

Warp does not currently expose a first-party application language setting or a complete UI localization framework. Most product strings are still inline Rust string literals.

For a maintainable local fork, this branch keeps translations in:

- `resources/localization/zh-Hans-overrides.toml`
- `script/zh_apply_localization.py`

The script applies exact replacements inside Rust double-quoted strings. It is idempotent: already translated strings are accepted, while missing source/target pairs report upstream drift.

## Status

Last verified release audit: 2026-05-29.

- Manifest entries: 2260.
- Covered areas: onboarding/auth, workspace shell, search and command entry points, settings core pages, advanced settings pages, common modals/toasts, Warp Drive surfaces, tab configs, themes, terminal sharing surfaces, and Agent management/input panels.
- Dry-run summary: `entries: 2260`, `files: 166`, `already_applied: 2245`, `would_change: 0`, `missing: 0`.
- Coverage snapshot:
  - `onboarding`: 266 covered, 92 candidates, 74.3%.
  - `workspace`: 451 covered, 529 candidates, 46.0%.
  - `search`: 216 covered, 52 candidates, 80.6%.
  - `settings`: 1126 covered, 946 candidates, 54.3%.
  - `modals`: 560 covered, 6278 candidates, 8.2%.
  - `release`: 2497 covered, 7871 candidates, 24.1%.
- Package note: the app crate package is currently named `warp`; the older checklist label `cargo check -p app` fails in this workspace because no package named `app` exists.
- Passed validation:
  - `python3 script/zh_apply_localization.py --dry-run --summary`
  - `python3 script/zh_localization_inventory.py --preset onboarding --coverage`
  - `python3 script/zh_localization_inventory.py --preset workspace --coverage`
  - `python3 script/zh_localization_inventory.py --preset search --coverage`
  - `python3 script/zh_localization_inventory.py --preset settings --coverage`
  - `python3 script/zh_localization_inventory.py --preset modals --coverage`
  - `python3 script/zh_localization_inventory.py --preset release --coverage`
  - `cargo fmt --check`
  - `git diff --check`
  - `cargo check -p onboarding`
  - `cargo check -p warp`
  - `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- Recorded failures / manual gates:
  - `cargo check -p app` fails with `error: package ID specification 'app' did not match any packages`; use `cargo check -p warp` for the current app package.
  - Interactive `./script/run` smoke remains a manual release gate; the non-interactive bundle gate produced `target/debug/bundle/osx/WarpOss.app`.

## Apply translations after syncing upstream

```bash
python3 script/zh_apply_localization.py --dry-run
python3 script/zh_apply_localization.py
cargo fmt
```

If `--dry-run` fails, inspect the upstream file, update the matching `source` entry, and rerun the script.

## Inventory workflow

Use the inventory script to find remaining likely user-visible English strings before adding a new batch of replacements:

```bash
python3 script/zh_localization_inventory.py --preset onboarding > /tmp/zh-onboarding.md
python3 script/zh_localization_inventory.py --preset workspace > /tmp/zh-workspace.md
python3 script/zh_localization_inventory.py --preset search > /tmp/zh-search.md
python3 script/zh_localization_inventory.py --preset settings > /tmp/zh-settings.md
python3 script/zh_localization_inventory.py --preset modals > /tmp/zh-modals.md
```

Review only `candidate` rows. Add manifest entries in small batches, then rerun:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
```

Coverage counts are available for release tracking:

```bash
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

`release` is an aggregate preset across the named high-visibility source roots. Keep the per-surface commands in release notes so regressions remain easy to locate.

## Local release checklist

Run this command-line checklist after syncing upstream and applying the manifest:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
cargo fmt --check
git diff --check
cargo check -p onboarding
cargo check -p app
cargo check -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
./script/run
```

Current workspace notes:

- `cargo check -p app` is retained because older planning docs used `app` as the app-crate label. In the current workspace the package is named `warp`; expect `cargo check -p app` to fail with `package ID specification 'app' did not match any packages`.
- Use `TERM=xterm-256color ./script/run --dont-open` for a non-interactive bundle/build check. Without that `TERM`, `cargo-bundle` may panic while printing colored status output with `Error(Term(ColorOutOfRange), ...)`.
- Use `./script/run` for the interactive app smoke pass after the bundle gate is green.

2026-05-29 recorded failure output:

```text
$ cargo check -p app
error: package ID specification `app` did not match any packages

help: a package with a similar name exists: `aes`
```

```text
$ WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
Cannot access ssh://git@github.com/warpdotdev/warp-channel-config.git (no SSH access?). Skipping install.
Skipping internal channel config installation (no repo access).
Bundling app (bin: warp-oss)...
warning: `warp` (lib) generated 46 warnings (run `cargo fix --lib -p warp` to apply 46 suggestions)
Finished `dev` profile [unoptimized + debuginfo] target(s) in 2m 24s

thread 'main' panicked at src/main.rs:164:37:
called `Result::unwrap()` on an `Err` value: Error(Term(ColorOutOfRange), State { next_error: None, backtrace: InternalBacktrace { backtrace: None } })
```

2026-05-29 non-interactive bundle success output:

```text
$ TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
Cannot access ssh://git@github.com/warpdotdev/warp-channel-config.git (no SSH access?). Skipping install.
Skipping internal channel config installation (no repo access).
Bundling app (bin: warp-oss)...
Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.20s
Bundling WarpOss.app
Finished 1 bundle at:
        /Users/drew/Project/Warp CN/target/debug/bundle/osx/WarpOss.app
Successfully bundled...
Successfully prepared bundled resources in target/debug/bundle/osx/WarpOss.app/Contents/Resources
Codesigning app...
target/debug/bundle/osx/WarpOss.app: replacing existing signature
```

Manual smoke paths:

- Fresh onboarding: Agent path.
- Fresh onboarding: terminal-only path.
- Login: browser login.
- Login: token paste fallback.
- Login: privacy settings.
- Workspace: user menu.
- Workspace: left and right panels.
- Workspace: vertical tabs.
- Search: command palette.
- Search: command search.
- Search: slash command.
- Settings: Account, Appearance, Features, Privacy, AI, Code, MCP, Billing, and Environments.
- Modals/toasts: update toast, destructive dialog, theme modal, tab config modal, terminal share modal.

Record every failed item with the exact command output or manual path, then either update `resources/localization/zh-Hans-overrides.toml` or document why the item is outside the current local-fork scope.

## Upstream sync workflow

```bash
git switch drew/zh-Hans-localization
git fetch origin
git merge origin/master
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

For larger upstream changes, use `git rebase origin/master` instead of merge if you want a linear local history.

## Translation scope

The first pass focuses on high-visibility UI:

- onboarding screens
- login / AI opt-out screens
- vertical tabs labels
- search placeholders and top-level navigation labels
- settings core and advanced pages
- command palette, command search, and slash commands
- common modals, toasts, themes, tab configs, Warp Drive, terminal sharing, and Agent management surfaces

Remaining work should prioritize candidate strings surfaced by the inventory script, especially low-signal broad presets where internal protocol, test, and diagnostic literals are still intentionally filtered manually.

## Build notes

Official local run path:

```bash
./script/bootstrap --skip-common-skills
./script/run
```

`script/bootstrap` may install development dependencies and can request `gcloud` authentication. For localization-only iteration, prefer starting with `cargo check` on the touched crates before running the full app build.
