use settings::macros::define_settings_group;
use settings::{RespectUserSyncSetting, SupportedPlatforms, SyncToCloud};

define_settings_group!(AltScreenReporting, settings: [
    mouse_reporting_enabled: MouseReportingEnabled {
        type: bool,
        default: true,
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "terminal.mouse_reporting_enabled",
        description: "是否将鼠标事件转发给全屏终端应用。",
    },
    scroll_reporting_enabled: ScrollReportingEnabled {
        type: bool,
        default: true,
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "terminal.scroll_reporting_enabled",
        description: "是否将滚动事件转发给全屏终端应用。",
    },
    focus_reporting_enabled: FocusReportingEnabled {
        type: bool,
        default: true,
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "terminal.focus_reporting_enabled",
        description: "是否将焦点和失焦事件转发给全屏终端应用。",
    },
]);
