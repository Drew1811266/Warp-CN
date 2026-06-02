# zh-Hans Localization Phase 80

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 80 translates or classifies remaining safe Terminal residue after RC15 and
Phase 79. The phase focuses on visible Terminal UI, inline banners, shared
session notices, inline menu labels, profile/search hints, Warpify surfaces, and
user-facing PTY/bootstrap errors.

## Low-Load Adjustment

The first non-dry-run `zh_apply_localization.py --summary` attempt was stopped
with SIGINT after it spent several minutes in the sequential summary path. The
process was single-core but sustained high CPU, so continuing would violate the
thermal-safety rule.

`script/zh_apply_localization.py` was updated to batch non-dry-run replacement
application by file:

- Count all sources and already-applied targets in one Rust string-literal pass.
- Validate missing and `expected_count` before applying.
- Apply only valid replacements in one second pass per changed file.

The same manifest semantics are preserved, but Phase 80 application time dropped
to roughly 2.5 seconds.

## Translated Terminal String Families

Phase 80 added and applied Terminal translations for:

- CLI Agent wait/status and unsupported schema warning.
- Conversation, history, plans, repo, profile, and query inline-menu labels.
- Loading and empty states.
- Terminal link middle-click label.
- PTY and Windows bootstrap user-facing errors.
- Startup shell configuration description.
- Shared block iframe title.
- Shared-session plan limit notice.
- Warpify banner titles, suppression action, and host suppression option.
- Terminal onboarding actions.
- Bookmark omitted-lines messages.
- Agent-mode setup, alias expansion, anonymous AI signup, AWS CLI, shell exit,
  and Vim-mode inline banners.
- Shared-session reconnect status.
- SSH remote-server extension failure banner.
- Pending user-query role label.
- Terminal ligature setting description.
- Auto-reload credits display.

## Preserved Terminal Contracts

Phase 80 added exact-path or exact-literal ignore rules for reviewed non-UI
Terminal residue:

```text
viewport/debug metadata
type/schema descriptions
renderer/model invariants
terminal-server diagnostics
WSL registry constants
executor debug names
tmux command templates
locale templates
UI/test identifiers
command snippets
file names and bootstrap suffixes
format placeholders
```

Notably preserved:

```text
Cmd +
Ctrl +
Agent
agents.md
warp.md
.ps1
pwsh.ps1
tmux command fragments
PascalCase UI/cache IDs
```

`Agent` remains a visible product/role term intentionally preserved by the
glossary.

## Coverage Before And After

Before Phase 80 after Phase 79:

```text
terminal: 2121 covered, 140 candidates, 93.8%
```

After Phase 80:

```text
entries: 7902
files: 524
already_applied: 5649
would_change: 0
missing: 0

terminal: 2178 covered, 1 candidate, 100.0%
remaining terminal candidate:
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

The remaining `Agent` candidate is a deliberate preserve-term item, not an
untranslated UI defect.

## Acceptance Checks

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7902
files: 524
already_applied: 5649
would_change: 0
missing: 0

nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --coverage
preset: custom
covered: 2178
candidates: 1
coverage: 100.0%

nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --status candidate
candidate: app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent

nice -n 10 cargo fmt --check
passed

git diff --check
passed
```

## Qualification Result

Qualified.

Phase 80 passed because manifest validation, glossary, dry-run, Terminal
coverage, formatting, and diff checks all passed. The only remaining Terminal
candidate is the intentional `Agent` preserve term.
