# zh-Hans GUI Evidence Policy

This policy controls how Warp CN GUI review evidence is captured, stored, and referenced.

## Core Rule

Do not commit raw full-screen screenshots or videos. GUI evidence must be cropped, redacted, or summarized so it does not expose the desktop, browser state, account identifiers, tokens, local paths, private files, or system permission details unrelated to the review.

## Allowed Evidence

| Evidence type | Git policy | Notes |
| --- | --- | --- |
| Accessibility text from Computer Use | Commit in markdown | Preferred evidence for visible Chinese anchors |
| Cropped and redacted UI screenshot | Commit only when necessary | Must show the relevant Warp surface only |
| Full-screen desktop screenshot | Do not commit | Keep local only, or replace with cropped/redacted evidence |
| Screen recording | Do not commit | Use local-only evidence unless explicitly redacted and approved |
| Raw logs | Do not commit by default | Commit only short redacted excerpts needed for reproduction |
| Process command output | Commit in markdown when relevant | Redact usernames, paths, tokens, cookies, and account details |

## Screenshot Requirements

Before a screenshot can be committed:

- The image shows only the target Warp UI region.
- Account email, username, team name, API key, token, local path, and browser state are redacted.
- The file name includes phase and matrix row when possible.
- The related markdown record explains what Chinese anchors were verified.
- The screenshot is not the only proof for destructive, billing, auth, or team flows.

## Existing Artifact Risk

Earlier phases stored raw `docs/gui-smoke-artifacts/**/*.png` screenshots. Those files should not be used as the model for future evidence. If public repository history must be scrubbed, that requires a separate explicit history-cleanup task because deleting files in a later commit does not remove them from existing Git history or existing tags.

## Artifact Storage

Use this pattern for future local-only artifacts:

```text
docs/gui-smoke-artifacts/<phase>/
```

The directory can contain a `.gitkeep` file, but raw image/video/log outputs should stay untracked unless they have been reviewed and redacted.

## Evidence Labels

Use these labels in review notes:

| Label | Meaning |
| --- | --- |
| `source-anchor` | The translated string exists in source or manifest |
| `accessibility-evidence` | Computer Use or accessibility tree saw the Chinese text |
| `cropped-screenshot-evidence` | A reviewed cropped/redacted screenshot supports the claim |
| `fixture-evidence` | A debug-only or local fixture showed the UI; not public-RC proof |
| `real-account-evidence` | An isolated account or test object showed the real product state |
| `blocked-evidence` | The required state cannot be triggered safely yet |

## Promotion Rule

Do not promote a GUI matrix row to `verified` unless the evidence is from a real user-visible app state. Debug fixture evidence can support `fixture-verified` only.

