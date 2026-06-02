# zh-Hans Localization Phase 45

Date: 2026-06-02

## Goal

Resolve or formally defer embedded English in static onboarding preview PNGs.

## Method

Phase 45 used source inspection and local contact sheets only. No binary asset was edited.

Temporary contact sheets reviewed:

- `.omx/onboarding-contact-sheets/root.jpg`
- `.omx/onboarding-contact-sheets/agent_intention.jpg`
- `.omx/onboarding-contact-sheets/agent_theme.jpg`
- `.omx/onboarding-contact-sheets/terminal_intention.jpg`
- `.omx/onboarding-contact-sheets/terminal_theme.jpg`

Inventory:

```text
total onboarding PNGs: 54
root-level onboarding PNGs: 12
agent_intention customize PNGs: 16
terminal_intention customize PNGs: 10
agent_intention theme PNGs: 8
terminal_intention theme PNGs: 8
static visual-residue assets: 50
accepted decorative / brand assets: 4
```

## Source Usage Map

| Asset group | Source usage |
| --- | --- |
| `welcome_agent.png`, `welcome_terminal.png` | `crates/onboarding/src/slides/intention_slide.rs`, `crates/onboarding/src/slides/customize_slide.rs` |
| `agent_intention/customize_*.png` | `crates/onboarding/src/slides/agent_slide.rs`, `crates/onboarding/src/slides/customize_slide.rs` |
| `terminal_intention/terminal_*.png` | `crates/onboarding/src/slides/customize_slide.rs` |
| `thirdparty_*.png` | `crates/onboarding/src/slides/third_party_slide.rs` |
| `agent_intention/theme/*.png`, `terminal_intention/theme/*.png` | `crates/onboarding/src/slides/theme_picker_slide.rs`, `app/src/auth/login_slide.rs` |
| `onboarding_bg.png` | `crates/onboarding/src/slides/layout.rs` |
| `hoa_welcome_banner.png` | `app/src/workspace/hoa_onboarding/welcome_banner.rs` |
| `openwarp_launch_banner.png` | `app/src/workspace/view/openwarp_launch_modal/view.rs` |
| `orchestration_launch_banner.png` | `app/src/workspace/view/orchestration_launch_modal/view.rs` |

## Policy Decisions

### Accepted Decorative / Brand Assets

Policy: `accepted-decorative-or-brand-art`.

These assets did not show readable localizable product UI text in the Phase 45 contact-sheet review, so they are not blocking RC11 source localization:

```text
app/assets/async/png/onboarding/hoa_welcome_banner.png
app/assets/async/png/onboarding/onboarding_bg.png
app/assets/async/png/onboarding/openwarp_launch_banner.png
app/assets/async/png/onboarding/orchestration_launch_banner.png
```

### Deferred Visual-Residue Assets

Policy: `defer-to-design-regeneration`.

These PNGs contain embedded English UI, English terminal/code/editor previews, English notification or toolbar copy, or English sidebar labels. They are screenshot/static-art residue rather than manifest drift, so editing Rust strings or manifest entries cannot fix them. They should be regenerated from the current localized UI or replaced with design-approved Chinese-localized static art in a reversible asset branch.

Default intention previews:

```text
app/assets/async/png/onboarding/welcome_agent.png
app/assets/async/png/onboarding/welcome_terminal.png
```

Third-party Agent previews:

```text
app/assets/async/png/onboarding/thirdparty_notifications_disabled.png
app/assets/async/png/onboarding/thirdparty_notifications_enabled.png
app/assets/async/png/onboarding/thirdparty_toolbar_disabled_horizontal.png
app/assets/async/png/onboarding/thirdparty_toolbar_disabled_vertical.png
app/assets/async/png/onboarding/thirdparty_toolbar_enabled_horizontal.png
app/assets/async/png/onboarding/thirdparty_toolbar_enabled_vertical.png
```

Agent customization previews:

```text
app/assets/async/png/onboarding/agent_intention/customize_codereview_disabled_horizontal.png
app/assets/async/png/onboarding/agent_intention/customize_codereview_disabled_vertical.png
app/assets/async/png/onboarding/agent_intention/customize_codereview_enabled_horizontal.png
app/assets/async/png/onboarding/agent_intention/customize_codereview_enabled_vertical.png
app/assets/async/png/onboarding/agent_intention/customize_conversation_horizontal.png
app/assets/async/png/onboarding/agent_intention/customize_conversation_vertical.png
app/assets/async/png/onboarding/agent_intention/customize_fileexplorer_horizontal.png
app/assets/async/png/onboarding/agent_intention/customize_fileexplorer_vertical.png
app/assets/async/png/onboarding/agent_intention/customize_filesearch_horizontal.png
app/assets/async/png/onboarding/agent_intention/customize_filesearch_vertical.png
app/assets/async/png/onboarding/agent_intention/customize_horizontal_tabs.png
app/assets/async/png/onboarding/agent_intention/customize_tools_disabled_horizontal.png
app/assets/async/png/onboarding/agent_intention/customize_tools_disabled_vertical.png
app/assets/async/png/onboarding/agent_intention/customize_vertical_tabs.png
app/assets/async/png/onboarding/agent_intention/customize_warpdrive_horizontal.png
app/assets/async/png/onboarding/agent_intention/customize_warpdrive_vertical.png
```

Terminal customization previews:

```text
app/assets/async/png/onboarding/terminal_intention/terminal_codereview_disabled.png
app/assets/async/png/onboarding/terminal_intention/terminal_codereview_enabled.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_fileexplorer_horizontal.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_fileexplorer_vertical.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_filesearch_horizontal.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_filesearch_vertical.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_horizontal_tabs.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_vertical_tabs.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_warpdrive_horizontal.png
app/assets/async/png/onboarding/terminal_intention/terminal_customize_warpdrive_vertical.png
```

Agent theme and login previews:

```text
app/assets/async/png/onboarding/agent_intention/theme/theme_adeberry_horizontal.png
app/assets/async/png/onboarding/agent_intention/theme/theme_adeberry_vertical.png
app/assets/async/png/onboarding/agent_intention/theme/theme_dark_horizontal.png
app/assets/async/png/onboarding/agent_intention/theme/theme_dark_vertical.png
app/assets/async/png/onboarding/agent_intention/theme/theme_light_horizontal.png
app/assets/async/png/onboarding/agent_intention/theme/theme_light_vertical.png
app/assets/async/png/onboarding/agent_intention/theme/theme_phenomenon_horizontal.png
app/assets/async/png/onboarding/agent_intention/theme/theme_phenomenon_vertical.png
```

Terminal theme and login previews:

```text
app/assets/async/png/onboarding/terminal_intention/theme/theme_adeberry_horizontal.png
app/assets/async/png/onboarding/terminal_intention/theme/theme_adeberry_vertical.png
app/assets/async/png/onboarding/terminal_intention/theme/theme_dark_horizontal.png
app/assets/async/png/onboarding/terminal_intention/theme/theme_dark_vertical.png
app/assets/async/png/onboarding/terminal_intention/theme/theme_light_horizontal.png
app/assets/async/png/onboarding/terminal_intention/theme/theme_light_vertical.png
app/assets/async/png/onboarding/terminal_intention/theme/theme_phenomenon_horizontal.png
app/assets/async/png/onboarding/terminal_intention/theme/theme_phenomenon_vertical.png
```

## Release Impact

RC11 remains honest as `visual-residue`: source strings and manifest entries can be clean while onboarding and login preview imagery still show embedded English in static PNG content.

No row is promoted to public-RC readiness by this phase. The asset decision only classifies the residue and prevents it from being mistaken for unresolved source localization.

Recommended follow-up asset work:

1. Create a reversible asset branch.
2. Regenerate the 50 deferred PNGs from current localized UI, or replace them with design-approved Chinese-localized static art.
3. Capture before/after onboarding screenshots.
4. Verify no unrelated binary assets changed.

## Validation

No build was required because Phase 45 changed no binary assets and no runtime code.

Passed:

```text
git diff --check
```

## Qualification

Phase 45 is accepted as `qualified-static-onboarding-visual-residue-deferred`.
