use std::path::PathBuf;
use std::str::FromStr;

use serde::{Deserialize, Serialize};
use settings::Setting;

/// The source for a newly-created session.
#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum NewSessionSource {
    /// The user split a pane to create a new session.
    SplitPane,
    /// The user created a new tab, and this is its initial session.
    Tab,
    /// The user created a new window, and this is its initial session.
    Window,
}

#[derive(
    Debug,
    Copy,
    Clone,
    Default,
    Serialize,
    Deserialize,
    PartialEq,
    Eq,
    schemars::JsonSchema,
    settings_value::SettingsValue,
)]
#[schemars(description = "新会话的启动位置。", rename_all = "snake_case")]
pub enum WorkingDirectoryMode {
    /// Start a new session in the user's home directory.
    HomeDir,
    /// Start a new session in the same directory as the previous session.
    #[default]
    PreviousDir,
    /// Start a new session in a specific directory.
    CustomDir,
}

impl WorkingDirectoryMode {
    /// Returns the label that should be used for this mode when configuring
    /// values in the settings view.
    pub fn dropdown_item_label(&self) -> &'static str {
        match self {
            WorkingDirectoryMode::HomeDir => "主目录",
            WorkingDirectoryMode::PreviousDir => "上一会话的目录",
            WorkingDirectoryMode::CustomDir => "自定义目录",
        }
    }
}

#[derive(
    Debug,
    Clone,
    Default,
    Serialize,
    Deserialize,
    PartialEq,
    Eq,
    schemars::JsonSchema,
    settings_value::SettingsValue,
)]
#[schemars(description = "特定会话来源的工作目录设置。")]
pub struct WorkingDirectoryPerSourceConfig {
    #[schemars(description = "工作目录的确定方式。")]
    pub mode: WorkingDirectoryMode,
    #[schemars(description = "自定义目录路径，在模式为 CustomDir 时使用。")]
    pub custom_dir: String,
}

impl WorkingDirectoryPerSourceConfig {
    /// Returns the initial session path that should be used for this source.
    fn initial_directory_for_new_session(
        &self,
        initial_directory_from_current_session: Option<PathBuf>,
        ignore_custom_directory: bool,
    ) -> Option<PathBuf> {
        match self.mode {
            WorkingDirectoryMode::HomeDir => None,
            WorkingDirectoryMode::PreviousDir => initial_directory_from_current_session,
            WorkingDirectoryMode::CustomDir => {
                if self.custom_dir.is_empty() || ignore_custom_directory {
                    None
                } else {
                    Some(
                        // Perform tilde expansion on the provided directory
                        // before converting it into a path.
                        PathBuf::from_str(&shellexpand::tilde(self.custom_dir.as_str()))
                            // This will never actually return the default value, as
                            // the error type here is Infallible.
                            .unwrap_or_default(),
                    )
                }
            }
        }
    }
}

#[derive(
    Debug,
    Clone,
    Default,
    Serialize,
    Deserialize,
    PartialEq,
    Eq,
    schemars::JsonSchema,
    settings_value::SettingsValue,
)]
#[schemars(description = "新会话初始工作目录的配置。")]
pub struct WorkingDirectoryConfig {
    #[schemars(description = "是否按会话来源使用单独设置。")]
    pub advanced_mode: bool,
    #[schemars(description = "高级模式关闭时使用的默认工作目录设置。")]
    pub global: WorkingDirectoryPerSourceConfig,
    #[schemars(description = "分屏会话的工作目录设置。")]
    pub split_pane: WorkingDirectoryPerSourceConfig,
    #[schemars(description = "新标签页会话的工作目录设置。")]
    pub new_tab: WorkingDirectoryPerSourceConfig,
    #[schemars(description = "新窗口会话的工作目录设置。")]
    pub new_window: WorkingDirectoryPerSourceConfig,
}

impl WorkingDirectoryConfig {
    /// Returns the per-source config for the given session source,
    /// taking into account whether advanced mode is enabled.
    pub fn config_for_source(&self, source: NewSessionSource) -> &WorkingDirectoryPerSourceConfig {
        if self.advanced_mode {
            match source {
                NewSessionSource::SplitPane => &self.split_pane,
                NewSessionSource::Tab => &self.new_tab,
                NewSessionSource::Window => &self.new_window,
            }
        } else {
            &self.global
        }
    }

    /// Returns the initial session path that should be used for the given
    /// new session source.
    pub fn initial_directory_for_new_session(
        &self,
        source: NewSessionSource,
        initial_directory_from_current_session: Option<PathBuf>,
        ignore_custom_directory: bool,
    ) -> Option<PathBuf> {
        self.config_for_source(source)
            .initial_directory_for_new_session(
                initial_directory_from_current_session,
                ignore_custom_directory,
            )
    }

    /// Invokes the provided function with a mutable reference to the setting's
    /// internal value then persists it to storage.
    pub fn update_and_save_value<F>(
        &mut self,
        update_fn: F,
        ctx: &mut warpui::ModelContext<<Self as Setting>::Group>,
    ) -> anyhow::Result<()>
    where
        F: FnOnce(&mut <Self as Setting>::Value),
    {
        update_fn(self);
        self.set_value(self.value().clone(), ctx)
    }
}
