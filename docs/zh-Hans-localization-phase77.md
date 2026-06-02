# zh-Hans Localization Phase 77

Date: 2026-06-02 Asia/Shanghai

## Goal

Prepare Chinese replacement scripts for the `50` deferred onboarding PNGs
without generating, opening, uploading, or replacing binary images.

## Inventory

Ran file-name inventory only:

```text
find app/assets/async/png/onboarding -name '*.png' -print | wc -l
54
```

Accepted decorative/brand assets remain unchanged:

```text
app/assets/async/png/onboarding/hoa_welcome_banner.png
app/assets/async/png/onboarding/onboarding_bg.png
app/assets/async/png/onboarding/openwarp_launch_banner.png
app/assets/async/png/onboarding/orchestration_launch_banner.png
```

Deferred assets remain `50`.

## Created Script Package

Created:

- `docs/zh-Hans-onboarding-visual-script-package.md`

The script package maps every deferred image to:

```text
asset path
reason category
Chinese replacement script
layout risk
review note
```

## Updated Regeneration Plan

Updated:

- `docs/zh-Hans-onboarding-visual-regeneration-plan.md`

The regeneration plan now points future asset-regeneration work to the script
package as the Chinese copy source.

## Binary Safety

No binary image changed in Phase 77:

```text
no PNG opened
no PNG generated
no PNG uploaded
no PNG replaced
no asset branch created
no GUI launched
```

Future PNG replacement must happen on a separate reversible asset branch with
before/after contact sheets and `git diff --stat` review.

## Checks

Passed:

```text
git diff --check
```

## Qualification

Phase 77 is accepted as `qualified-onboarding-visual-script-package`.

The phase is qualified because every deferred image has a Chinese script entry,
the four accepted decorative/brand assets remain unchanged, no binary asset was
modified, the future regeneration path is reversible and reviewable, public RC
remains blocked until regenerated assets or design approval exists, and
`git diff --check` passed.
