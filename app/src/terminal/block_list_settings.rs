use settings::macros::define_settings_group;
use settings::{RespectUserSyncSetting, SupportedPlatforms, SyncToCloud};

// Settings for controlling the behavior of the block list.
define_settings_group!(BlockListSettings, settings: [
   show_jump_to_bottom_of_block_button: ShowJumpToBottomOfBlockButton {
       type: bool,
       default: true,
       supported_platforms: SupportedPlatforms::ALL,
       sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
       private: false,
       toml_path: "appearance.blocks.show_jump_to_bottom_of_block_button",
       description: "是否在较长命令输出中显示跳到底部按钮。",
   },
   snackbar_enabled: SnackbarEnabled {
       type: bool,
       default: true,
       supported_platforms: SupportedPlatforms::ALL,
       sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
       private: false,
       toml_path: "general.snackbar_enabled",
       description: "是否显示 snackbar 通知。",
   }
   // When enabled, the input box retains focus when selecting a block in shell mode
   // (useful for quickly attaching context). When disabled, selecting a block focuses
   // the terminal so blocklist navigation with arrow keys continues to work.
   preserve_input_focus_on_block_selection: PreserveInputFocusOnBlockSelection {
       type: bool,
       default: false,
       supported_platforms: SupportedPlatforms::ALL,
       sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
       private: false,
       toml_path: "general.preserve_input_focus_on_block_selection",
       description: "Whether to preserve input box focus when selecting a block.",
   }
   show_block_dividers: ShowBlockDividers {
       type: bool,
       default: true,
       supported_platforms: SupportedPlatforms::ALL,
       sync_to_cloud: SyncToCloud::Globally(RespectUserSyncSetting::Yes),
       private: false,
       toml_path: "appearance.blocks.show_block_dividers",
       description: "是否在终端块之间显示分隔线。",
   }
]);
