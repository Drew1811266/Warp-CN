# zh-Hans localization branch

This branch is a local Chinese localization branch for Warp's open-source client.

## Current approach

Warp does not currently expose a first-party application language setting or a complete UI localization framework. Most product strings are still inline Rust string literals.

For a maintainable local fork, this branch keeps translations in:

- `resources/localization/zh-Hans-overrides.toml`
- `script/zh_apply_localization.py`

The script applies exact replacements inside Rust double-quoted strings. It is idempotent: already translated strings are accepted, while missing source/target pairs report upstream drift.

## Status

Last verified baseline: 2026-05-29.

- Manifest entries: 122.
- Covered areas: onboarding slides, login / AI opt-out, vertical tabs labels, selected search placeholders, selected top-level navigation labels.
- Validation:
  - `python3 script/zh_apply_localization.py --dry-run`
  - `cargo fmt --check`
  - `git diff --check`

## Apply translations after syncing upstream

```bash
python3 script/zh_apply_localization.py --dry-run
python3 script/zh_apply_localization.py
cargo fmt
```

If `--dry-run` fails, inspect the upstream file, update the matching `source` entry, and rerun the script.

## Upstream sync workflow

```bash
git switch drew/zh-Hans-localization
git fetch origin
git merge origin/master
python3 script/zh_apply_localization.py --dry-run
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

Remaining work should prioritize settings pages, command palette entries, modals, and toast messages.

## Build notes

Official local run path:

```bash
./script/bootstrap --skip-common-skills
./script/run
```

`script/bootstrap` may install development dependencies and can request `gcloud` authentication. For localization-only iteration, prefer starting with `cargo check` on the touched crates before running the full app build.
