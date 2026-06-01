use settings::macros::define_settings_group;
use settings::{RespectUserSyncSetting, SupportedPlatforms, SyncToCloud};

define_settings_group!(CommandSearchSettings, settings: [
    show_global_workflows_in_universal_search: ShowGlobalWorkflowsInUniversalSearch {
        type: bool,
        default: false,
        supported_platforms: SupportedPlatforms::ALL,
        sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
        private: false,
        toml_path: "workflows.show_global_workflows_in_universal_search",
        description: "是否在全局搜索结果中显示全局工作流。",
    },
]);
