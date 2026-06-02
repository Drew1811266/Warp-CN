# zh-Hans Localization Phase 92

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 92 prepares onboarding visual asset work without modifying PNG files or
mixing image changes into the current dirty localization branch.

## Branch Decision

Recommended future asset branch:

```text
codex/zh-Hans-onboarding-assets-rc17
```

The asset branch was not created in this phase. The current working tree
contains extensive source, manifest, script, and documentation changes from the
localization effort. Switching or creating an asset branch in this dirty checkout
would risk mixing binary PNG work with unrelated localization changes.

No branch switch was performed.

## Initial Binary Diff

```text
git status --short app/assets/async/png/onboarding: no output
git diff --stat -- app/assets/async/png/onboarding: no output
```

No onboarding PNG is modified in the current working tree.

## Before Contact Sheet

`magick` was unavailable, so the before contact sheet was generated outside the
repository with low-priority Python/Pillow.

```text
path: /tmp/warp-cn-onboarding-assets-rc17/before-contact-sheet.png
size: 1331040 bytes
image count: 54 PNGs
```

Command shape:

```text
nice -n 10 python3 - <<'PY'
...
PY
```

The command only read `app/assets/async/png/onboarding/**/*.png` and wrote the
contact sheet to `/tmp`.

## Asset Scope

Deferred PNGs requiring regeneration:

```text
50
```

Accepted decorative/brand PNGs to keep unchanged:

```text
app/assets/async/png/onboarding/hoa_welcome_banner.png
app/assets/async/png/onboarding/onboarding_bg.png
app/assets/async/png/onboarding/openwarp_launch_banner.png
app/assets/async/png/onboarding/orchestration_launch_banner.png
```

Total onboarding PNGs included in the contact sheet:

```text
54
```

## Safety Review

```text
PNG modified: no
asset branch created: no
branch switch: no
source/TOML/script changes in asset branch: not applicable
contact sheet location: outside repository
machine heat: no long-running image generation performed
```

## Qualification Result

Qualified as preparation-only.

Phase 92 passed because the asset-only branch decision was recorded, the current
onboarding PNG diff is empty, a before contact sheet was generated outside the
repository, the deferred and unchanged asset counts were restated, no PNG was
modified, and the lightweight diff hygiene gate passed.
