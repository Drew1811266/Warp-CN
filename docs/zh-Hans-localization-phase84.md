# zh-Hans Localization Phase 84

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 84 prepares a reversible asset-only execution plan for the `50`
onboarding PNGs that still contain embedded English UI. It does not generate,
open, upload, replace, or modify images.

## Files Created

- `docs/zh-Hans-onboarding-visual-asset-regeneration-plan-rc16.md`

## Scope

The plan uses `docs/zh-Hans-onboarding-visual-script-package.md` as the source
of Chinese replacement scripts and keeps the four accepted decorative/brand
assets unchanged:

```text
app/assets/async/png/onboarding/hoa_welcome_banner.png
app/assets/async/png/onboarding/onboarding_bg.png
app/assets/async/png/onboarding/openwarp_launch_banner.png
app/assets/async/png/onboarding/orchestration_launch_banner.png
```

## Required Workflow

The RC16 asset plan requires:

```text
separate asset-only branch
before contact sheet
exact Chinese script per deferred PNG
after contact sheet
per-image visual review checklist
binary diff limited to approved deferred PNGs
no source/document/script changes in the asset branch
explicit design/product approval before merge or ship
```

## Acceptance Criteria

The plan checks for:

```text
legible Chinese text
no overlap or cropping
no English UI residue
faithful current product state
matching dimensions and file formats unless approved
acceptable PNG quality
before/after contact sheet evidence
```

## Safety Review

Phase 84 did not modify:

```text
PNG files
other binary assets
Rust source
TOML manifests
GUI state
account/backend/billing/cloud/team state
```

## Acceptance Checks

```text
rg -n 'onboarding|PNG|contact sheet|asset-only|approval' docs/zh-Hans-onboarding-visual-asset-regeneration-plan-rc16.md
passed

git diff --check
passed
```

## Qualification Result

Qualified.

Phase 84 passed because the plan is executable, reversible, explicitly
asset-only, and no PNG or other binary asset was modified.
