# zh-Hans Onboarding Asset Authorization RC20

Date: 2026-06-02

## Scope

This package refreshes authorization requirements for future onboarding PNG
regeneration. It does not approve, generate, or modify images in the current
source/evidence branch.

## Branch And Scope

```text
future branch: codex/zh-Hans-onboarding-assets-rc20
deferred asset count: 50
accepted decorative/brand asset count: 4
allowed dirty scope: app/assets/async/png/onboarding/**/*.png
disallowed dirty scope: Rust, TOML, Python, Markdown, unrelated resources,
unapproved binary assets
```

## Required Approval And Evidence

```text
design/product approval: required before generation
before contact sheet: required before generation and stored outside the repo
generation: small serial batches only
after contact sheet: required after generation and stored outside the repo
binary scope proof: required before acceptance
visual QA: required before acceptance
```

## Current Branch Rule

```text
current branch: codex/zh-Hans-followup-localization
current branch PNG changes allowed: no
PNG generation approved in this phase: no
PNG modified in this phase: no
```

Current PNG checks:

```text
git status --short -- '*.png'
result: no output

git diff --name-only -- '*.png'
result: no output
```

## Regeneration Requirements

The 50 deferred onboarding PNGs from
`docs/zh-Hans-onboarding-visual-script-package.md` still require:

```text
asset-only branch
design/product approval
before contact sheet
small serial generation batches
after contact sheet
binary scope proof
visual QA
no unrelated file changes
```

## Batch Order

```text
Batch A: welcome screens
Batch B: notification and CLI Agent toolbar screens
Batch C: Agent intention customization screens
Batch D: Agent intention theme previews
Batch E: Terminal intention customization screens
Batch F: Terminal intention theme previews
Batch G: remaining script rows
```

## Acceptance Boundary

Asset changes are acceptable only on the future asset-only branch after design
approval. This source/evidence branch must remain free of PNG changes.

