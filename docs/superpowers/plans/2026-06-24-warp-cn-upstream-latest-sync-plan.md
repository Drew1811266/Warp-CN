# Warp CN Upstream Latest Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sync Warp CN from the current `0.20.6` fork state to the latest official Warp development source available on 2026-06-24, while preserving the zh-Hans localization overlay and avoiding an unsafe direct update to `main`.

**Architecture:** Work in an isolated sync branch created from current `main`, merge the latest upstream `origin/master`, repair localization drift through `resources/localization/zh-Hans-overrides.toml`, then validate with the existing low-load zh-Hans gates before any packaging or publication. Treat official product version, GitHub stable release, and upstream source commit as separate facts.

**Tech Stack:** Git, Rust/Cargo, Python localization tooling, Warp macOS packaging scripts, zh-Hans manifest overlay.

---

## Current Facts

- Repo: `/Users/drew/Project/Warp CN`.
- Current fork branch: `main`.
- Current fork commit: `3229258e3cb055b40daf563e0cabb36bfc3a65f9`.
- Current fork tag: `0.20.6`.
- Publication remote: `github https://github.com/Drew1811266/Warp-CN.git`.
- Upstream remote: `origin https://github.com/warpdotdev/warp.git`.
- Official changelog latest product entry checked on 2026-06-24: `2026.06.17 (v0.2026.06.17.09.49)`.
- GitHub latest stable release checked on 2026-06-24: `v0.2026.06.03.09.49.stable_00`.
- GitHub latest dev release checked on 2026-06-24: `v0.2026.06.09.19.54.dev_00`.
- Latest fetched upstream source commit checked on 2026-06-24 after implementation-start refresh: `origin/master` at `6691e1e0e0408be8bdcb1891e3a795564cedd897`.
- `origin/master` subject: `Make the New API key modal's Agent picker searchable (#12972)`.
- Current divergence: `git rev-list --left-right --count HEAD...origin/master` returned `894 305`.
- Current diff scale: `git diff --shortstat HEAD..origin/master` returned `1914 files changed, 101928 insertions(+), 803509 deletions(-)`.

## Non-Goals

- Do not update `main` directly.
- Do not force-fetch, delete, or overwrite local `v0.2026.*` tags.
- Do not claim the result is based on a newer official stable tag unless upstream publishes one and it is explicitly selected.
- Do not package or publish a release before static gates and at least the minimum GUI smoke path are recorded.

## Files And Responsibilities

- `resources/localization/zh-Hans-overrides.toml`: canonical zh-Hans overlay manifest. Most translation drift fixes belong here.
- `script/zh_apply_localization.py`: overlay application and manifest validation. Modify only if upstream structure exposes a real tooling bug.
- `script/zh_localization_inventory.py`: coverage and candidate reporting. Modify only if upstream structure exposes a real tooling bug.
- `script/zh_mojibake_scan.py`: mojibake guard. Modify only if current scanner produces false blockers that cannot be resolved through manifest/content fixes.
- `docs/zh-Hans-upstream-sync.md`: append the new 2026-06-24 sync record with exact upstream base, validation results, and decision.
- `docs/zh-Hans-gui-smoke-matrix.md`: record GUI smoke status after a build exists.
- `docs/zh-Hans-localization-functional-test-plan.md`: update only if upstream adds or changes user-visible workflows that require new localization regression coverage.
- `README.md`: update current version/download/status only after the sync candidate has passed release gates.
- `script/macos/package_oss_free`: packaging path to use only after sync validation passes.

## Acceptance Criteria

- A branch named `codex/zh-Hans-upstream-latest-2026-06-24` exists and contains the sync work.
- Current `main` remains unchanged until an explicit final merge/publish decision.
- Upstream base is recorded as `origin/master` commit `6691e1e0e0408be8bdcb1891e3a795564cedd897`, unless a newer upstream commit is deliberately fetched and recorded before implementation starts.
- `python3 script/zh_apply_localization.py --validate-manifest` passes.
- `python3 script/zh_apply_localization.py --check-glossary` passes.
- `python3 script/zh_apply_localization.py --dry-run --summary` reports `missing: 0` and `would_change: 0` after overlay application.
- `python3 script/zh_localization_inventory.py --preset release --coverage` runs and the result is recorded.
- `python3 script/zh_mojibake_scan.py` runs and any findings are classified as blocker, false positive, or deferred manual review.
- `git diff --check` passes.
- `cargo fmt --check` passes, or formatting changes are applied and committed before further validation.
- `cargo check -p warp` passes before packaging.
- If a DMG is produced, `script/macos/package_oss_free --version 0.21.0` completes and the DMG is verified with `shasum -a 256`, `hdiutil imageinfo`, `plutil`, and `codesign --verify --deep --strict --verbose=2`.
- GUI smoke evidence records at least: macOS menu bar, global search placeholder, `新会话` entry, command palette filter labels, settings view, and one AI block copy path related to upstream #12892.

## Task 1: Create An Isolated Sync Branch

**Files:**
- Modify: none expected.
- Create: branch `codex/zh-Hans-upstream-latest-2026-06-24`.

- [ ] **Step 1: Verify the starting tree**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git describe --tags --always --dirty
git remote -v
```

Expected:

```text
## main...github/main
3229258e3cb055b40daf563e0cabb36bfc3a65f9
0.20.6
origin points to warpdotdev/warp
github points to Drew1811266/Warp-CN
```

Untracked `.omx/` and `docs/gui-smoke-artifacts/` are local artifacts. Do not add them unless a later task explicitly creates a new tracked doc.

- [ ] **Step 2: Create the branch from current fork main**

Run:

```bash
git switch -c codex/zh-Hans-upstream-latest-2026-06-24 main
```

Expected: branch switches without modifying tracked files.

- [ ] **Step 3: Record the branch point**

Run:

```bash
git show -s --format='%H%n%cd%n%s' --date=iso-strict HEAD
```

Expected first line:

```text
3229258e3cb055b40daf563e0cabb36bfc3a65f9
```

- [ ] **Step 4: Commit only if branch setup creates files**

Expected: no commit needed. If a plan/status note is added in this task, commit it separately:

```bash
git add docs/superpowers/plans/2026-06-24-warp-cn-upstream-latest-sync-plan.md
git commit -m "docs: plan latest upstream sync"
```

## Task 2: Refresh Upstream Without Mutating Local Tags

**Files:**
- Modify: none expected.
- Reference: `docs/zh-Hans-upstream-sync.md`.

- [ ] **Step 1: Refresh upstream branch refs only**

Run:

```bash
git fetch origin --prune
```

Expected: `origin/master` refreshes. This command intentionally does not force-update local `v0.2026.*` tags.

- [ ] **Step 2: Capture release and branch facts**

Run:

```bash
gh api repos/warpdotdev/warp/releases/latest --jq '{tag_name, name, published_at, prerelease, draft, html_url}'
gh api 'repos/warpdotdev/warp/releases?per_page=20' --jq '.[] | {tag_name, name, published_at, prerelease, draft, html_url}'
git ls-remote --heads --refs origin master 'stable_release/*' 'preview_release/*' 'dev_release/*' | tail -100
git show -s --format='%H%n%cd%n%s' --date=iso-strict origin/master
```

Expected:

```text
latest stable release remains v0.2026.06.03.09.49.stable_00 unless upstream changes
origin/master is the selected latest-source base for this sync
```

- [ ] **Step 3: Set the sync base**

Run:

```bash
UPSTREAM_BASE=origin/master
git rev-parse "$UPSTREAM_BASE"
git merge-base --is-ancestor "$UPSTREAM_BASE" HEAD; echo "upstream_base_ancestor_of_head=$?"
git merge-base --is-ancestor HEAD "$UPSTREAM_BASE"; echo "head_ancestor_of_upstream_base=$?"
git rev-list --left-right --count HEAD..."$UPSTREAM_BASE"
```

Expected current base SHA unless refreshed deliberately:

```text
6691e1e0e0408be8bdcb1891e3a795564cedd897
894 305
```

## Task 3: Run Pre-Merge zh-Hans Baseline Gates

**Files:**
- Read: `resources/localization/zh-Hans-overrides.toml`.
- Modify: none expected.

- [ ] **Step 1: Validate current manifest**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_mojibake_scan.py
```

Expected:

```text
manifest validation passed
glossary check passed
missing: 0
would_change: 0
release coverage printed
mojibake findings absent or classified
```

- [ ] **Step 2: Save pre-merge measurements**

Append the exact outputs to a local note or to the eventual section in `docs/zh-Hans-upstream-sync.md`. Do not edit release-facing README text yet.

- [ ] **Step 3: Commit only if documentation is updated**

Run only if a tracked baseline note is added:

```bash
git add docs/zh-Hans-upstream-sync.md
git commit -m "docs: record pre-sync zh-Hans baseline"
```

## Task 4: Merge Latest Upstream Source Into The Sync Branch

**Files:**
- Modify: broad upstream source tree through merge.
- Likely conflict areas: `README.md`, `docs/`, `resources/localization/zh-Hans-overrides.toml`, app UI files under `app/src/`, build scripts under `script/`.

- [ ] **Step 1: Merge the selected upstream base**

Run:

```bash
git merge --no-ff origin/master
```

Expected: either clean merge or conflicts. If conflicts occur, stop and list them:

```bash
git status --short
git diff --name-only --diff-filter=U
```

- [ ] **Step 2: Resolve conflicts with upstream structure first**

For source conflicts in `app/src`, `crates`, `script`, `.github`, and generated upstream files, create the source-conflict list and prefer upstream structure:

```bash
git diff --name-only --diff-filter=U -- app/src crates script .github > /tmp/warp-cn-source-conflicts.txt
while IFS= read -r conflict_path; do
  git checkout --theirs -- "$conflict_path"
done < /tmp/warp-cn-source-conflicts.txt
```

Then reapply zh-Hans through manifest rather than manually preserving old translated source.

For fork-owned docs and packaging files, inspect both sides one path at a time from the unresolved list:

```bash
git diff --name-only --diff-filter=U -- README.md docs resources/localization script/macos > /tmp/warp-cn-fork-doc-conflicts.txt
while IFS= read -r conflict_path; do
  printf '\n===== OURS %s =====\n' "$conflict_path"
  git diff --ours -- "$conflict_path"
  printf '\n===== THEIRS %s =====\n' "$conflict_path"
  git diff --theirs -- "$conflict_path"
done < /tmp/warp-cn-fork-doc-conflicts.txt
```

Keep fork release docs only when still accurate; otherwise preserve upstream source and update fork docs in later tasks.

- [ ] **Step 3: Finish the merge**

After resolving all conflicts:

```bash
git status --short
git add -u
git commit
```

Expected commit message from Git merge is acceptable if it clearly states upstream merge. If editing message manually, use:

```text
Merge upstream origin/master into Warp CN latest sync
```

## Task 5: Reapply And Repair zh-Hans Overlay

**Files:**
- Modify: `resources/localization/zh-Hans-overrides.toml`.
- Modify as needed: affected upstream UI source files under `app/src/`.
- Modify only if needed: `script/zh_apply_localization.py`.

- [ ] **Step 1: Run manifest validation after merge**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
```

Expected: failures are allowed at this step, but every failure must be classified as moved source, changed English string, removed feature, new UI text, or tooling bug.

- [ ] **Step 2: Apply overlay if needed**

If dry-run reports `would_change > 0`, run:

```bash
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: translated source updates are applied deterministically.

- [ ] **Step 3: Repair missing entries**

For each `missing` entry, save the dry-run log and inspect the exact path and source reported by the tool:

```bash
python3 script/zh_apply_localization.py --dry-run --summary 2>&1 | tee /tmp/warp-cn-zh-dry-run-after-merge.log
rg -n "missing|path|source" /tmp/warp-cn-zh-dry-run-after-merge.log
```

Decision rules:

- If source moved, update `path`.
- If English changed but meaning stayed the same, update `source` and keep `target`.
- If UI meaning changed, update both `source` and `target`.
- If feature was removed upstream, mark the manifest entry deprecated or remove it with a note in `docs/zh-Hans-upstream-sync.md`.

- [ ] **Step 4: Commit overlay repair**

Run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
git diff --check
git add resources/localization/zh-Hans-overrides.toml app/src crates script
git commit -m "fix: reapply zh-Hans overlay after upstream sync"
```

Expected:

```text
missing: 0
would_change: 0
```

## Task 6: Cover New Official User-Visible Changes

**Files:**
- Modify: `resources/localization/zh-Hans-overrides.toml`.
- Modify: source files containing new visible English strings.
- Modify: `docs/zh-Hans-localization-functional-test-plan.md` if new workflows need explicit regression coverage.

- [ ] **Step 1: Search for new visible strings in likely changed areas**

Run:

```bash
git diff --name-only 3229258e3cb055b40daf563e0cabb36bfc3a65f9..HEAD -- app/src crates resources | sed -n '1,200p'
python3 script/zh_localization_inventory.py --preset settings --top-paths 20
python3 script/zh_localization_inventory.py --preset workspace --top-paths 20
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

Expected: candidate hotspots identify any new English UI introduced since `0.20.6`.

- [ ] **Step 2: Prioritize changelog-driven workflows**

Review and translate visible strings related to:

- remote-environment git chips;
- Settings -> Code "Format on save";
- `/rename-conversation`;
- `warp://settings/warp_agent`;
- git dialog tooltips;
- local-to-cloud handoff prompt and success toast;
- SSH warpification notice and settings;
- Mermaid diagram rendering labels if visible;
- SuperGrok/xAI connection fallback copy;
- tab group bugfix surfaces;
- AI block selected-text copy behavior from upstream `#12892`.

- [ ] **Step 3: Add or update manifest entries**

For each accepted candidate, add or update a manifest entry in `resources/localization/zh-Hans-overrides.toml` using the existing schema. Then run:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py
python3 script/zh_apply_localization.py --dry-run --summary
```

Expected:

```text
manifest validation passed
glossary check passed
missing: 0
would_change: 0
```

- [ ] **Step 4: Commit visible string coverage**

Run:

```bash
git diff --check
git add resources/localization/zh-Hans-overrides.toml app/src crates docs/zh-Hans-localization-functional-test-plan.md
git commit -m "feat: cover latest upstream zh-Hans strings"
```

## Task 7: Run Static And Low-Load Validation Gates

**Files:**
- Modify only if failures require fixes.

- [ ] **Step 1: Run the localization stack**

Run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_mojibake_scan.py
```

Expected: all commands complete; any scanner finding is recorded with exact path and classification.

- [ ] **Step 2: Run Python tool tests**

Run:

```bash
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
python3 script/test_zh_apply_localization.py
python3 script/test_zh_localization_inventory.py
python3 script/test_zh_export_locale.py
```

Expected: all pass.

- [ ] **Step 3: Run formatting and Rust checks**

Run:

```bash
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: all pass. If `cargo fmt --check` fails only because upstream merged unformatted conflict output, run `cargo fmt`, inspect the diff, and commit formatting separately.

- [ ] **Step 4: Commit validation fixes**

Run only if fixes were needed:

```bash
git add -u
git commit -m "fix: pass latest upstream sync validation"
```

## Task 8: Build And Smoke The Synced App

**Files:**
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`.
- Create under tracked docs only if needed: a concise artifact index, not raw GUI screenshots unless intentionally selected.

- [ ] **Step 1: Run the low-load app launch gate**

Run:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected: command completes far enough to prove the app target can launch without opening the GUI. If blocked by heat/load, record `defer-heavy-gate` and stop before claiming runtime completeness.

- [ ] **Step 2: Build or package only after static gates pass**

For a local app smoke build:

```bash
cargo build --profile release-lto -p warp
```

For a release candidate package after the user approves a version number:

```bash
NEXT_VERSION=0.21.0
script/macos/package_oss_free --version "$NEXT_VERSION"
```

Expected package output format:

```text
target/Warp-CN-0.21.0-macos-arm64-release.dmg
```

- [ ] **Step 3: Verify package metadata if packaged**

Run:

```bash
NEXT_VERSION=0.21.0
shasum -a 256 "target/Warp-CN-${NEXT_VERSION}-macos-arm64-release.dmg"
hdiutil imageinfo "target/Warp-CN-${NEXT_VERSION}-macos-arm64-release.dmg"
plutil -p target/release-lto/bundle/osx/Warp.app/Contents/Info.plist | rg 'CFBundleShortVersionString|CFBundleVersion|CFBundleName|CFBundleIdentifier'
codesign --verify --deep --strict --verbose=2 target/release-lto/bundle/osx/Warp.app
```

Expected: hash printed, imageinfo succeeds, plist version matches `0.21.0`, codesign verification succeeds for ad-hoc signing.

- [ ] **Step 4: Run minimum GUI smoke**

Open the app candidate and verify:

```bash
open -n target/release-lto/bundle/osx/Warp.app
```

Record in `docs/zh-Hans-gui-smoke-matrix.md`:

- macOS menu bar text;
- global search placeholder;
- `新会话` entry;
- command palette filter labels;
- Settings -> Code format-on-save row;
- conversation rename surface;
- git dialog tooltips;
- AI block selected-text copy behavior.

- [ ] **Step 5: Commit smoke docs**

Run:

```bash
git add docs/zh-Hans-gui-smoke-matrix.md docs/zh-Hans-upstream-sync.md
git commit -m "docs: record latest upstream sync validation"
```

## Task 9: Update Release-Facing Docs After Validation

**Files:**
- Modify: `README.md`.
- Modify: `docs/zh-Hans-upstream-sync.md`.
- Modify as needed: release notes docs.

- [ ] **Step 1: Decide the next fork version**

Use a fork-owned version such as `0.21.0` for the next packaged candidate unless the user requests another label. Do not call it official `v0.2026.06.17.09.49` or official stable.

- [ ] **Step 2: Update README only after gates pass**

Change:

```text
当前版本：`0.20.6`
```

to the approved fork version, and update the status paragraph to say the fork is synced to:

```text
上游开发源 `origin/master` commit `6691e1e0e0408be8bdcb1891e3a795564cedd897`
```

If a package exists, update the download filename to:

```text
Warp-CN-0.21.0-macos-arm64-release.dmg
```

- [ ] **Step 3: Append the sync record**

Append to `docs/zh-Hans-upstream-sync.md`:

```markdown
## zh-Hans latest-source sync 2026-06-24

- Upstream product changelog latest checked: `2026.06.17 (v0.2026.06.17.09.49)`
- GitHub latest stable release checked: `v0.2026.06.03.09.49.stable_00`
- Selected upstream source base: `origin/master`
- Selected upstream source commit: `6691e1e0e0408be8bdcb1891e3a795564cedd897`
- Fork branch: `codex/zh-Hans-upstream-latest-2026-06-24`
- Manifest dry-run: `missing: 0`, `would_change: 0`
- Release coverage: paste the exact output from `python3 script/zh_localization_inventory.py --preset release --coverage`.
- Command-line gate: record each command from Task 7 as passed, failed, or deferred with the exact failing command.
- GUI matrix: record exact counts from `docs/zh-Hans-gui-smoke-matrix.md` after editing it.
- Package: record `none`, `local-only target/Warp-CN-0.21.0-macos-arm64-release.dmg`, or published GitHub asset URL.
- Notes:
  - This is a latest development source sync, not a newer official stable tag adoption.
```

- [ ] **Step 4: Commit release-facing docs**

Run:

```bash
git diff --check
git add README.md docs/zh-Hans-upstream-sync.md
git commit -m "docs: update Warp CN latest sync status"
```

## Task 10: Publish Only After Explicit Approval

**Files:**
- Modify: none unless release notes are updated.
- Release artifact: `target/Warp-CN-0.21.0-macos-arm64-release.dmg`.

- [ ] **Step 1: Verify local branch and tag plan**

Run:

```bash
git status --short --branch
git log --oneline --decorate -5
git diff github/main...HEAD --stat
```

Expected: clean tracked tree except intended local artifacts.

- [ ] **Step 2: Ask for publish approval**

Present:

- branch name;
- final commit SHA;
- package filename and SHA-256;
- validation summary;
- proposed tag, for example `0.21.0`.

Do not publish without explicit approval.

- [ ] **Step 3: Merge/push only after approval**

Recommended non-destructive path:

```bash
git switch main
git merge --no-ff codex/zh-Hans-upstream-latest-2026-06-24
git push github main
git tag -a 0.21.0 -m "Warp CN 0.21.0"
git push github 0.21.0
```

If direct git transport stalls, use the existing GitHub API fallback workflow recorded in memory, but only after confirming the exact ref update.

- [ ] **Step 4: Verify GitHub state**

Run:

```bash
git ls-remote github refs/heads/main refs/tags/0.21.0
gh release view 0.21.0 --repo Drew1811266/Warp-CN
gh api repos/Drew1811266/Warp-CN/releases/latest --jq '{tag_name, name, published_at, html_url, draft, prerelease}'
```

Expected: branch, tag, release asset, and Latest state match the approved version.

## Risks And Mitigations

- **Risk: latest `origin/master` is ahead of official stable release.** Mitigation: label the result as latest-source sync, not official stable adoption.
- **Risk: local upstream tags conflict with remote retargeted tags.** Mitigation: use `git fetch origin --prune` and `git ls-remote` for truth; do not force-update local `v0.2026.*` tags.
- **Risk: merge brings large upstream source churn.** Mitigation: isolate on `codex/zh-Hans-upstream-latest-2026-06-24`, commit merge separately, repair overlay in smaller commits.
- **Risk: manifest drift hides real untranslated UI.** Mitigation: require `missing: 0`, `would_change: 0`, coverage reports, and top-path candidate inspection before package.
- **Risk: GUI automation cannot prove runtime behavior.** Mitigation: mark unresolved GUI rows as `automation-blocked`, `manual-gate`, or `needs-trigger`; do not claim verified.
- **Risk: machine heat/load makes Rust build unsafe.** Mitigation: run low-load gates first and stop on `defer-heavy-gate`.

## Verification Summary Commands

Run before declaring the sync complete:

```bash
git status --short --branch
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_mojibake_scan.py
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
python3 script/test_zh_apply_localization.py
python3 script/test_zh_localization_inventory.py
python3 script/test_zh_export_locale.py
cargo fmt --check
git diff --check
cargo check -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

## Execution Recommendation

Use a parallel team only after Task 4 completes and conflicts are understood:

- Lane A: merge/conflict resolution and upstream source compatibility.
- Lane B: manifest drift repair and new visible string translation.
- Lane C: validation, build, package, and GitHub proof.

Before Task 4, one engineer should own the branch and merge because conflicting Git operations cannot safely run in parallel.
