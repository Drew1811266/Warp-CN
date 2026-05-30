# zh-Hans localization branch

This branch is a local Chinese localization branch for Warp's open-source client.

## Current approach

Warp does not currently expose a first-party application language setting or a complete UI localization framework. Most product strings are still inline Rust string literals.

For a maintainable local fork, this branch keeps translations in:

- `resources/localization/zh-Hans-overrides.toml`
- `script/zh_apply_localization.py`

The script applies exact replacements inside Rust string literals, including raw strings used for static pane content. It is idempotent: already translated strings are accepted, while missing source/target pairs report upstream drift.

## Status

Last verified release audit: 2026-05-30.

- Manifest entries: 2556.
- Covered areas: onboarding/auth, workspace shell, Warp on Web home, HOA onboarding, search and command entry points, settings core pages, AI settings deep paths, BYO API keys, AWS Bedrock credentials and user-facing credential errors, Appearance command-palette actions, conversation list actions, cloud agent capacity messaging, environment deletion confirmation, launch modals, credit and plan modals, Agent tips, Agent status/error residue, conversation details panel, CLI admin prompts, destructive confirmation dialogs, advanced settings pages, common modals/toasts, Warp Drive surfaces, tab configs, themes, terminal sharing surfaces, rewind labels, auth-secret confirmation dialogs, environment modal fallbacks, and Agent management/input panels.
- Dry-run summary: `entries: 2556`, `files: 186`, `already_applied: 2541`, `would_change: 0`, `missing: 0`.
- Coverage snapshot:
  - `onboarding`: 266 covered, 55 candidates, 82.9%.
  - `workspace`: 584 covered, 391 candidates, 59.9%.
  - `search`: 267 covered, 26 candidates, 91.1%.
  - `settings`: 1172 covered, 856 candidates, 57.8%.
  - `modals`: 635 covered, 5371 candidates, 10.6%.
  - `release`: 2802 covered, 6678 candidates, 29.6%.
- Package note: the app crate package is currently named `warp`; the older checklist label `cargo check -p app` fails in this workspace because no package named `app` exists.
- Phase 2 command-line validation passed:
  - `python3 script/zh_apply_localization.py --dry-run --summary`
  - `python3 script/zh_localization_inventory.py --preset onboarding --coverage`
  - `python3 script/zh_localization_inventory.py --preset workspace --coverage`
  - `python3 script/zh_localization_inventory.py --preset search --coverage`
  - `python3 script/zh_localization_inventory.py --preset settings --coverage`
  - `python3 script/zh_localization_inventory.py --preset modals --coverage`
  - `python3 script/zh_localization_inventory.py --preset release --coverage`
  - `cargo fmt --check`
  - `git diff --check`
  - `python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py`
  - `cargo check -p warp`
  - `cargo test -p warp_search_core`
  - `cargo test -p warp command_palette`
  - `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- Recorded failures / manual gates:
  - `cargo check -p app` fails with `error: package ID specification 'app' did not match any packages`; use `cargo check -p warp` for the current app package.
  - Historical GUI smoke with `target/debug/bundle/osx/WarpOss.app` verified the terminal-only workspace and command palette filter chips (`文件`, `操作`, `会话`, `启动配置`).
  - Phase 2 GUI smoke was attempted on 2026-05-29. The `WarpOss` process launched, but Computer Use and AppleScript window reads timed out, `open` returned `-1712`, and the captured screenshot was black. Treat HOA onboarding, AI settings deep paths, rewind, and auth-secret confirmation as manual GUI gates until they are verified in an interactive desktop session.
  - Phase 2 Round 2 GUI smoke was attempted on 2026-05-30. `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` built, bundled, prepared resources, and signed `WarpOss.app`; `open -na target/debug/bundle/osx/WarpOss.app` launched `warp-oss` and `terminal-server` processes, but Computer Use window state reads timed out. Treat Appearance command actions, conversation actions, cloud agent capacity modal, AWS credential errors, and environment deletion confirmation as manual GUI gates until verified in an interactive desktop session.
  - Phase 2 Round 3 GUI smoke was attempted on 2026-05-30. `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` built, bundled, prepared resources, and signed `WarpOss.app`; `open -n target/debug/bundle/osx/WarpOss.app` launched `warp-oss` and `terminal-server` processes, but Computer Use window state reads timed out. Treat launch modals, credit and plan modals, Agent tips, conversation details panel, CLI admin prompts, remove endpoint confirmation, and transfer ownership confirmation as manual GUI gates until verified in an interactive desktop session.
  - Phase 2 Round 4 GUI smoke was attempted on 2026-05-30. `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` built, bundled, prepared resources, and signed `WarpOss.app`; `open -n target/debug/bundle/osx/WarpOss.app` launched `warp-oss` and `terminal-server` processes. Computer Use successfully read the window state and confirmed Chinese menu labels, the global search placeholder, and the `新会话` entry. Treat Warp on Web home, Agent status labels, Agent error residue, and environment modal fallback paths as manual GUI gates until those specific states are triggered in an interactive desktop session.
  - Interactive login/account smoke remains a manual release gate; the non-interactive bundle gate produced `target/debug/bundle/osx/WarpOss.app`.

## Phase 2 Round 2 execution record

Executed on 2026-05-30.

| Task | Result | Evidence |
| --- | --- | --- |
| Round 2 implementation plan | Complete | `05b719f4 docs: plan phase 2 round 2 zh-Hans localization` |
| Appearance command-palette actions | Complete | `81672827 feat: localize appearance command actions` |
| Conversation list actions and delete toasts | Complete | `25d71e8c feat: localize conversation actions` |
| Cloud agent capacity modal | Complete | `4c31e506 feat: localize cloud agent capacity modal` |
| AWS credential errors and environment deletion confirmation | Complete | `43613337 feat: localize credential and environment dialogs` |

Round 2 intentionally skipped these strings:

- Appearance strings `dim inactive panes`, `focus follows mouse`, and `jump to bottom of block button`, because they also appear as settings search keyword strings in `app/src/settings_view/appearance_page.rs`; the current manifest applies exact replacements per file, so translating them would also mutate search metadata.
- Cloud capacity dynamic strings containing `${price}/month`, `2x`, and `5x`, because they combine runtime pricing or multiplier fragments and need UI review before translation.
- Theme names and example values such as `Aurora`, `Classic 1`, `Glow`, `Warp 1`, `{value}%`, and command/example tokens.

Round 2 command-line validation passed:

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
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

## Phase 2 Round 3 execution record

Executed on 2026-05-30.

Round 3 continued the second-stage cleanup by targeting launch modals, plan/credit billing modals, Agent tips, conversation details metadata, CLI administrator prompts, and destructive confirmation dialogs.

| Task | Result | Evidence |
| --- | --- | --- |
| Round 3 implementation plan | Complete | `9fa400ff docs: plan phase 2 round 3 zh-Hans localization` |
| Launch modals | Complete | `524db95b feat: localize launch modals` |
| Credit and plan modals | Complete | `9511f730 feat: localize credit and plan modals` |
| Agent tips | Complete | `d3e7a2c6 feat: localize agent tips` |
| Conversation details panel | Complete | `c551a024 feat: localize conversation details panel` |
| CLI prompts and destructive confirmations | Complete | `b046da1f feat: localize cli and confirmation prompts` |

Round 3 final dry-run:

```text
entries: 2543
files: 184
already_applied: 2528
would_change: 0
missing: 0
```

Round 3 final coverage snapshot:

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| `onboarding` | 266 | 55 | 82.9% |
| `workspace` | 582 | 392 | 59.8% |
| `search` | 267 | 40 | 87.0% |
| `settings` | 1170 | 860 | 57.6% |
| `modals` | 626 | 5813 | 9.7% |
| `release` | 2789 | 7139 | 28.1% |

Round 3 command-line validation passed:

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
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Round 3 notes:

- The AppleScript CLI install/uninstall prompts require escaped inner quotes in Rust string literals. The manifest entry is valid TOML, and the applied Rust code was manually checked so `cargo fmt --check` and `cargo check -p warp` both pass.
- `open -na target/debug/bundle/osx/WarpOss.app` treats the path as an application name and fails. Use `open -n target/debug/bundle/osx/WarpOss.app` for the local bundle path.
- Automatic GUI inspection remains manual-gated because Computer Use timed out while reading the running `WarpOss` window state.

## Phase 2 Round 4 execution record

Executed on 2026-05-30.

Round 4 shifted the next slice from broad translation to release-quality audit work: inventory review modes, conservative denominator cleanup, raw-string manifest support, Warp on Web home copy, Agent status/error residue, and Agent Assisted Environment fallbacks.

| Task | Result | Evidence |
| --- | --- | --- |
| Round 4 implementation plan | Complete | `9e2f93a3 docs: plan phase 2 round 4 zh-Hans localization` |
| Inventory review modes | Complete | `436d526d chore: add zh-Hans inventory review modes` |
| Inventory noise filters | Complete | `1926d03a chore: refine zh-Hans inventory noise filters` |
| Warp on Web home | Complete | `da976cff feat: localize Warp on Web home` |
| Agent status residue | Complete | `a3e004fc feat: localize agent status residue` |
| Environment modal fallbacks | Complete | `67ce0d9f feat: localize environment modal fallbacks` |

Round 4 final dry-run:

```text
entries: 2556
files: 186
already_applied: 2541
would_change: 0
missing: 0
```

Round 4 final coverage snapshot:

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| `onboarding` | 266 | 55 | 82.9% |
| `workspace` | 584 | 391 | 59.9% |
| `search` | 267 | 26 | 91.1% |
| `settings` | 1172 | 856 | 57.8% |
| `modals` | 635 | 5371 | 10.6% |
| `release` | 2802 | 6678 | 29.6% |

Round 4 top remaining candidate paths:

| Preset | Top paths |
| --- | --- |
| `workspace` | `app/src/workspace/view.rs` (119), `app/src/workspace/mod.rs` (66), `app/src/workspace/tab_settings.rs` (54) |
| `settings` | `app/src/settings_view/features_page.rs` (182), `app/src/settings_view/mod.rs` (172), `app/src/settings_view/teams_page.rs` (146) |
| `modals` | `app/src/terminal/view.rs` (334), `app/src/terminal/view/action.rs` (182), `app/src/terminal/input.rs` (159) |

Round 4 notes:

- `script/zh_localization_inventory.py` now supports `--status` and `--top-paths` for candidate review.
- `script/zh_apply_localization.py` now supports escaped `\n` in manifest values and raw string replacement, used by `app/src/workspace/home.rs`.
- The low `modals` coverage remains dominated by terminal and Agent internals; Round 4 documents exact non-UI exclusions instead of translating protocol/schema strings for coverage.
- GUI automation successfully read the app window in Round 4 and confirmed the base workspace chrome is Chinese. The deeper Round 4 states remain manual GUI gates because they were not triggered in this smoke pass.

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

Use focused review modes before editing broad presets:

```bash
python3 script/zh_localization_inventory.py --preset workspace --status candidate
python3 script/zh_localization_inventory.py --preset settings --status covered-target
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

Review only `candidate` rows. Add manifest entries in small batches, then rerun:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
```

The inventory script intentionally filters telemetry files, keybindings, filter tokens, placeholder-only strings, and settings search tags. These strings are not treated as untranslated UI unless they are also rendered directly in a visible control.

Coverage counts are available for release tracking:

```bash
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

`search` includes the app search surfaces and the shared `warp_search_core` crate, where common filter chip labels and search placeholders live. `release` is an aggregate preset across the named high-visibility source roots. Keep the per-surface commands in release notes so regressions remain easy to locate.

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
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
./script/run
```

Current workspace notes:

- `cargo check -p app` is not part of the current checklist. Older planning docs used `app` as the app-crate label; in the current workspace the package is named `warp`, so `cargo check -p app` fails with `package ID specification 'app' did not match any packages`.
- Use `TERM=xterm-256color ./script/run --dont-open` for a non-interactive bundle/build check. Without that `TERM`, `cargo-bundle` may panic while printing colored status output with `Error(Term(ColorOutOfRange), ...)`.
- Use `./script/run` or `open -n target/debug/bundle/osx/WarpOss.app` for the interactive app smoke pass after the bundle gate is green.
- Phase 2 local automatic GUI smoke is currently manual-gated on this machine because the app process starts but window automation times out.

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

Prioritize remaining work from candidate strings surfaced by the inventory script, especially low-signal broad presets where internal protocol, test, and diagnostic literals are still intentionally filtered manually.

## Build notes

Official local run path:

```bash
./script/bootstrap --skip-common-skills
./script/run
```

`script/bootstrap` may install development dependencies and can request `gcloud` authentication. For localization-only iteration, prefer starting with `cargo check` on the touched crates before running the full app build.
