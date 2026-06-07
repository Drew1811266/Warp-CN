# zh-Hans Onboarding Visual Regeneration Plan

Date: 2026-06-02 Asia/Shanghai

## Purpose

This plan defines a reversible path for replacing the `50` deferred onboarding PNGs that contain embedded English UI, terminal/code/editor text, notification copy, toolbar text, or sidebar labels.

The visual residue is not Rust source-string drift and is not covered by `resources/localization/zh-Hans-overrides.toml`.

## Asset Baseline

Current inventory:

```text
total onboarding PNGs: 54
root-level onboarding PNGs: 12
agent_intention root PNGs: 16
terminal_intention root PNGs: 10
agent_intention/theme PNGs: 8
terminal_intention/theme PNGs: 8
```

Current policy from Phase 45 and Phase 53:

- `4` assets accepted as `accepted-decorative-or-brand-art`.
- `50` assets remain `defer-to-design-regeneration`.

Accepted decorative/brand assets:

- `hoa_welcome_banner.png`
- `onboarding_bg.png`
- `openwarp_launch_banner.png`
- `orchestration_launch_banner.png`

Phase 68 rechecked the file list and created
`docs/zh-Hans-localization-phase68.md` with a per-asset deferred map. The
decision is unchanged: `50` assets remain `defer-to-design-regeneration`.

Phase 77 adds a Chinese script package for every deferred asset:

- `docs/zh-Hans-onboarding-visual-script-package.md`

Use that script package as the copy source for future image regeneration. It is
documentation only; no PNGs were modified in Phase 77.

## Reversible Workflow

1. Create a dedicated asset-only branch.
2. Do not mix source-string, manifest, or unrelated binary changes into that branch.
3. Recreate each deferred PNG from a design/source-of-truth file where possible, not by editing screenshots in place.
4. Replace only the exact deferred onboarding PNGs.
5. Generate before/after contact sheets for all changed PNGs.
6. Verify image dimensions, filenames, and source references are unchanged unless a design owner explicitly approves otherwise.
7. Run `git diff --stat` and confirm no unrelated binary assets changed.
8. Capture at least one current-source onboarding GUI screenshot after asset replacement if the local machine is cool and the GUI prerequisites are safe.
9. Update `docs/zh-Hans-gui-smoke-matrix.md` and the current RC record with either `visual-regenerated`, `design-approved`, or `still-visual-residue`.

## Acceptance Criteria

- Every changed PNG has a before/after comparison.
- Embedded English UI text is removed or explicitly approved by design/product.
- No file outside `app/assets/async/png/onboarding/` changes in the asset-only branch unless documented.
- No account, backend, cloud, billing, secret, endpoint, or team state is touched.
- Public RC remains blocked until the visual result is approved and isolated account/backend evidence exists.

## Current Phase 61 Decision

No PNG was modified in Phase 61.

The status remains `still-visual-residue` because the deferred assets have not yet been regenerated or design-approved.

## 0.19 Self-Defined Complete Release Asset Decision

The `50` deferred source onboarding PNGs remain asset-branch work. They are not
silently considered completed for Warp CN 0.19 self-defined complete release,
and they do not clear public-RC evidence rows.

For the self-defined 0.19 release, onboarding visual residue must be represented
as `pending-replacement` or `known-limitation-documented` until current-cycle
Chinese assets or explicit design approval exist.

These are 0.19-local documentation statuses. They do not replace the broader RC
asset workflow statuses `visual-regenerated`, `design-approved`, or
`still-visual-residue`.

| Screen | Decision | Required Action |
| --- | --- | --- |
| Welcome local fixture onboarding screen | replace | regenerate current-cycle zh-Hans screenshot or keep documented limitation |
| Theme choice onboarding screen | replace | regenerate current-cycle zh-Hans screenshot or keep documented limitation |
| Agent choice onboarding screen | replace | regenerate current-cycle zh-Hans screenshot or keep documented limitation |

No PNG was modified for this 0.19 planning pass.

## 0.19 Static Asset Release Decision

For Warp CN 0.19 self-defined complete release, onboarding static PNG English
residue is treated as `known-limitation-documented`. Source-level UI
localization remains complete, but inherited static onboarding images may still
need future regeneration.

This decision does not modify PNG files, does not clear public-RC evidence rows,
and does not replace the future asset-only branch workflow.
