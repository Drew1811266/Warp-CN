# zh-Hans Onboarding Visual Asset Regeneration Plan RC16

Date: 2026-06-02 Asia/Shanghai.

## Purpose

This plan defines a reversible asset-only workflow for regenerating the `50`
onboarding PNGs that still contain embedded English UI. Phase 84 does not open,
generate, upload, replace, or modify any PNG file.

Primary script source:

- `docs/zh-Hans-onboarding-visual-script-package.md`

## Scope

Regenerate only the deferred onboarding PNGs listed in the script package.

Keep these accepted decorative/brand assets unchanged:

```text
app/assets/async/png/onboarding/hoa_welcome_banner.png
app/assets/async/png/onboarding/onboarding_bg.png
app/assets/async/png/onboarding/openwarp_launch_banner.png
app/assets/async/png/onboarding/orchestration_launch_banner.png
```

## Asset Families

| Family | Count | Notes |
| --- | ---: | --- |
| Welcome screens | 2 | `welcome_agent.png`, `welcome_terminal.png`. |
| Third-party notification/toolbar screens | 6 | Notification and CLI Agent toolbar enabled/disabled variants. |
| Agent intention customization screens | 10 | Code review, conversation, file explorer, file search, tabs, tools, Warp Drive. |
| Agent intention theme previews | 8 | Four theme families, horizontal and vertical. |
| Terminal intention customization screens | 8 | Code review, file explorer, file search, tabs, Warp Drive. |
| Terminal intention theme previews | 8 | Four theme families, horizontal and vertical. |
| Remaining script rows | 8 | Additional horizontal/vertical variants recorded in the script package. |

Total deferred PNG count: `50`.

## Required Asset-Only Branch Workflow

1. Create a separate branch for image assets only.

```bash
git switch -c codex/zh-Hans-onboarding-assets-rc16
```

2. Confirm the branch starts from the reviewed localization state.

```bash
git status --short
git diff --stat -- app/assets/async/png/onboarding
```

3. Generate a before contact sheet without modifying source assets.

Suggested command shape:

```bash
mkdir -p /tmp/warp-cn-onboarding-assets-rc16
magick montage app/assets/async/png/onboarding/**/*.png \
  -label '%f' -geometry 320x220+24+36 \
  /tmp/warp-cn-onboarding-assets-rc16/before-contact-sheet.png
```

If `magick` is unavailable, use a lightweight local script or design tool, but
save the contact sheet path and command in the asset branch notes.

4. Regenerate or edit only the `50` deferred PNGs.

Rules:

```text
use the exact Chinese script row for each asset
preserve Agent, Warp Drive, MCP, Diff, Claude Code, Codex, Gemini CLI, and product names
preserve original dimensions and file formats unless design explicitly approves a change
do not change non-deferred PNGs
do not change Rust, TOML, Markdown, or script files in the asset branch
```

5. Generate an after contact sheet.

```bash
magick montage app/assets/async/png/onboarding/**/*.png \
  -label '%f' -geometry 320x220+24+36 \
  /tmp/warp-cn-onboarding-assets-rc16/after-contact-sheet.png
```

6. Verify binary scope.

```bash
git diff --name-only -- app/assets/async/png/onboarding
git diff --stat -- app/assets/async/png/onboarding
```

The output must list only approved deferred PNG paths.

## Per-Image Review Criteria

Each regenerated asset must pass:

```text
Chinese text is legible at intended size
text does not overlap toolbar, sidebar, tab, terminal, or button boundaries
no English UI residue remains in the regenerated image
product state remains faithful to the current UI
layout and visual hierarchy match the original asset family
dimensions and file format match the original asset unless explicitly approved
compressed PNG quality is acceptable
before/after contact sheets show the intended visual delta
```

## Approval Gate

Do not merge or ship regenerated PNGs until:

```text
before contact sheet is reviewed
after contact sheet is reviewed
per-image checklist is complete
binary diff contains only approved deferred PNGs
no unrelated source/document/script files changed in the asset branch
design/product approval is recorded
```

## Stop Conditions

Stop the asset branch if:

```text
an image generator changes product layout beyond text replacement
text is blurry, cropped, or unreadable
English UI residue remains
dimensions or file formats drift without approval
git diff includes non-approved binary files
git diff includes source or documentation files
design approval is unavailable
the machine overheats during contact-sheet or generation work
```

## RC16 Decision

RC16 public-facing polish remains blocked until the asset-only branch is executed
and approved. Phase 84 only prepares the reversible workflow; no PNG or other
binary asset was modified.
