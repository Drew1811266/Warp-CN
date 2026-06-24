use serde::{Deserialize, Serialize};
use settings::macros::define_settings_group;
use settings::{RespectUserSyncSetting, SupportedPlatforms, SyncToCloud};
use warp_core::features::FeatureFlag;
use warpui::units::Pixels;
use warpui::{AppContext, SingletonEntity};

use crate::settings::{AISettings, InputSettings, TerminalSpacing};

#[derive(
    Clone,
    Copy,
    Debug,
    Default,
    PartialEq,
    Eq,
    Serialize,
    Deserialize,
    schemars::JsonSchema,
    settings_value::SettingsValue,
)]
#[schemars(
    description = "Controls whether terminal programs can access the system clipboard via OSC 52 escape sequences.",
    rename_all = "snake_case"
)]
pub enum Osc52ClipboardAccess {
    #[default]
    #[schemars(description = "Deny all OSC 52 clipboard access.")]
    Deny,
    #[schemars(description = "Allow terminal programs to write to the clipboard, but not read.")]
    WriteOnly,
    #[schemars(description = "Allow terminal programs to both read and write the clipboard.")]
    ReadWrite,
}

impl Osc52ClipboardAccess {
    pub fn allows_write(self) -> bool {
        matches!(self, Self::WriteOnly | Self::ReadWrite)
    }

    pub fn allows_read(self) -> bool {
        matches!(self, Self::ReadWrite)
    }

    pub fn as_dropdown_label(self) -> &'static str {
        match self {
            Self::Deny => "拒绝",
            Self::WriteOnly => "仅写入",
            Self::ReadWrite => "读取和写入",
        }
    }
}

#[derive(
    Clone,
    Copy,
    Debug,
    Default,
    PartialEq,
    Eq,
    Serialize,
    Deserialize,
    schemars::JsonSchema,
    settings_value::SettingsValue,
)]
#[schemars(description = "终端块间距。", rename_all = "snake_case")]
pub enum SpacingMode {
    #[default]
    #[schemars(description = "普通")]
    Normal,
    #[schemars(description = "紧凑")]
    Compact,
}

impl SpacingMode {
    pub fn other_mode(&self) -> SpacingMode {
        match *self {
            SpacingMode::Normal => SpacingMode::Compact,
            SpacingMode::Compact => SpacingMode::Normal,
        }
    }
}

#[derive(
    Clone,
    Copy,
    Debug,
    PartialEq,
    Serialize,
    Deserialize,
    schemars::JsonSchema,
    settings_value::SettingsValue,
)]
#[schemars(
    description = "全屏终端应用中的内边距应用方式。",
    rename_all = "snake_case"
)]
pub enum AltScreenPaddingMode {
    #[schemars(description = "使用与块列表相同的内边距。")]
    MatchBlocklist,
    #[schemars(description = "使用自定义统一内边距值。")]
    Custom { uniform_padding: Pixels },
}

impl Default for AltScreenPaddingMode {
    fn default() -> Self {
        Self::Custom {
            uniform_padding: Pixels::zero(),
        }
    }
}

impl AltScreenPaddingMode {
    pub fn toggled(&self) -> Self {
        match self {
            Self::MatchBlocklist => Self::Custom {
                uniform_padding: Pixels::zero(),
            },
            Self::Custom { .. } => Self::MatchBlocklist,
        }
    }

    pub fn telemetry_string(&self) -> String {
        match self {
            Self::MatchBlocklist => "MatchBlocklist",
            Self::Custom { .. } => "Custom",
        }
        .to_string()
    }
}

define_settings_group!(TerminalSettings, settings: [
    use_audible_bell: UseAudibleBell {
        type: bool,
        default: false,
        supported_platforms: SupportedPlatforms::DESKTOP, /* Audible bell is not supported on web */
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "terminal.use_audible_bell",
        description: "终端响铃事件发生时是否播放提示音。",
    },
    spacing_mode: Spacing {
        type: SpacingMode,
        default: SpacingMode::default(),
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "appearance.spacing",
        description: "控制终端块之间的间距。",
    }
    maximum_grid_size: MaximumGridSize {
        type: usize,
        default: 50_000,
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "terminal.maximum_grid_size",
        description: "终端网格中的最大行数。",
    },
    alt_screen_padding: AltScreenPadding {
        type: AltScreenPaddingMode,
        default: AltScreenPaddingMode::default(),
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "appearance.full_screen_apps.alt_screen_padding",
        max_table_depth: 0,
        description: "控制全屏终端应用周围的内边距。",
    },
    // This field should not be referenced directly to check zero state block visibility -- use
    // the `should_show_zero_state_block()` getter, which also considers global AI enablement.
    show_terminal_zero_state_block: ShowTerminalZeroStateBlock {
        type: bool,
        default: true,
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "terminal.show_terminal_zero_state_block",
        description: "是否在新的终端会话中显示 AI 空状态块。",
    },
    osc52_clipboard_access: Osc52ClipboardAccessSetting {
        type: Osc52ClipboardAccess,
        default: Osc52ClipboardAccess::default(),
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "terminal.osc52_clipboard_access",
        description: "控制终端程序能否通过 OSC 52 转义序列访问系统剪贴板。选项：deny（默认）、write_only、read_write。",
    },
    // Opt-in toggle for running terminal find on a background thread. Only consulted on
    // channels where `FeatureFlag::AsyncFind` is off; channels with the flag on force the
    // feature on and hide this toggle. See `is_async_find_enabled` for the composite check.
    async_find_enabled: AsyncFindEnabled {
        type: bool,
        default: false,
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "experimental.async_find_enabled",
        description: "使用改进版查找实现，在大型输出中搜索匹配项时保持界面响应。",
    },
]);

impl TerminalSettings {
    /// Spacing for the terminal blocks.
    pub fn terminal_spacing(&self, line_height_ratio: f32, ctx: &AppContext) -> TerminalSpacing {
        match *self.spacing_mode {
            SpacingMode::Normal => TerminalSpacing::normal(line_height_ratio, ctx),
            SpacingMode::Compact => TerminalSpacing::compact(line_height_ratio, ctx),
        }
    }

    /// Whether the terminal zero state block should be shown.
    /// Checks both the user setting and the global AI enablement.
    pub fn should_show_zero_state_block(&self, ctx: &AppContext) -> bool {
        *self.show_terminal_zero_state_block && AISettings::as_ref(ctx).is_any_ai_enabled(ctx)
    }

    /// Whether asynchronous terminal find should be used. On channels where
    /// `FeatureFlag::AsyncFind` is on, the feature is force-enabled (no toggle shown).
    /// On other channels, users opt in via the `async_find_enabled` setting.
    pub fn is_async_find_enabled(&self) -> bool {
        FeatureFlag::AsyncFind.is_enabled() || *self.async_find_enabled
    }

    /// Spacing for the input box.
    pub fn terminal_input_spacing(
        &self,
        line_height_ratio: f32,
        ctx: &AppContext,
    ) -> TerminalSpacing {
        let should_force_normal_spacing =
            InputSettings::as_ref(ctx).is_universal_developer_input_enabled(ctx);
        if should_force_normal_spacing {
            return TerminalSpacing::normal(line_height_ratio, ctx);
        }
        match *self.spacing_mode {
            SpacingMode::Normal => TerminalSpacing::normal(line_height_ratio, ctx),
            SpacingMode::Compact => TerminalSpacing::compact(line_height_ratio, ctx),
        }
    }
}

#[cfg(test)]
#[path = "settings_tests.rs"]
mod tests;
