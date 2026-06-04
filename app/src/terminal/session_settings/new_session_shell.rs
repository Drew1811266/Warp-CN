use std::path::PathBuf;

use serde::{Deserialize, Serialize};
use warp_util::path::ShellFamily;
use warpui::platform::OperatingSystem;

#[derive(
    Debug,
    Default,
    Clone,
    PartialEq,
    Eq,
    Hash,
    Serialize,
    Deserialize,
    schemars::JsonSchema,
    settings_value::SettingsValue,
)]
#[schemars(description = "打开新会话时使用的 shell。", rename_all = "snake_case")]
pub enum NewSessionShell {
    #[default]
    #[schemars(description = "使用操作系统默认 shell。")]
    SystemDefault,
    #[schemars(description = "shell 可执行文件路径。")]
    Executable(String),
    #[schemars(description = "MSYS2 shell 环境。")]
    MSYS2(String),
    #[schemars(description = "Windows Subsystem for Linux 发行版。")]
    WSL(String),
    #[schemars(description = "自定义 shell 命令。")]
    Custom(String),
}

impl NewSessionShell {
    pub fn shell_family(&self) -> ShellFamily {
        let shell = match self {
            NewSessionShell::SystemDefault => return OperatingSystem::get().default_shell_family(),
            NewSessionShell::WSL(_) => return ShellFamily::Posix,
            NewSessionShell::Executable(shell) => shell,
            NewSessionShell::MSYS2(shell) => shell,
            NewSessionShell::Custom(shell) => shell,
        };

        let path = PathBuf::from(shell);
        if let Some(file_stem) = path
            .file_stem()
            .and_then(|s| s.to_str().map(|s| s.to_lowercase()))
        {
            if file_stem.contains("powershell") || file_stem.contains("pwsh") {
                return ShellFamily::PowerShell;
            }
        }
        ShellFamily::Posix
    }
}
