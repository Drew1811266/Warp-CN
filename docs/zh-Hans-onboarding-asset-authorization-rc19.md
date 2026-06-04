# zh-Hans Onboarding Asset Authorization RC19

Date: 2026-06-02

## Scope

This package defines the authorization requirements for future onboarding PNG
regeneration. It does not approve, generate, or modify images in the current
source/evidence branch.

## Branch And Scope

```text
future branch: codex/zh-Hans-onboarding-assets-rc19
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

## Current Branch Status

```text
current branch: codex/zh-Hans-followup-localization
current PNG status: no output from git status --short -- '*.png'
current PNG diff: no output from git diff --name-only -- '*.png'
PNG generation approved in this phase: no
PNG modified in this phase: no
```

## Acceptance Boundary

Asset changes are acceptable only on the future asset-only branch after design
approval. This source/evidence branch must remain free of PNG changes.

