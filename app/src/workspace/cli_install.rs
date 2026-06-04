use std::fs;
use std::os::unix::fs::symlink;
use std::path::{Path, PathBuf};

use anyhow::{anyhow, Context, Result};
use command::blocking::Command;
use warp_core::channel::ChannelState;
use warp_util::path::ShellFamily;

/// Compute the target path where the symlink should be installed, based on channel
fn cli_install_target_path() -> PathBuf {
    PathBuf::from("/usr/local/bin").join(ChannelState::channel().cli_command_name())
}

/// Create a symlink with elevated privileges using osascript
///
/// This function uses macOS's osascript to prompt for administrator privileges
/// and create a symlink
fn create_symlink_with_admin(source: &Path, target: &Path) -> Result<()> {
    let source_str = source
        .to_str()
        .ok_or_else(|| anyhow!("Source path contains invalid UTF-8: {source:?}"))?;
    let target_str = target
        .to_str()
        .ok_or_else(|| anyhow!("Target path contains invalid UTF-8: {target:?}"))?;

    let escaped_source = ShellFamily::Posix.shell_escape(source_str);
    let escaped_target = ShellFamily::Posix.shell_escape(target_str);

    // Use osascript to run the ln command with admin privileges, with a custom prompt
    let script = format!(
        "do shell script \"ln -sf {escaped_source} {escaped_target}\" with prompt \"Warp 需要管理员权限才能将命令安装到 /usr/local/bin。\" with administrator privileges"
    );

    log::debug!("Creating symlink with admin privileges");

    let output = Command::new("osascript")
        .arg("-e")
        .arg(&script)
        .output()
        .context("无法通过 osascript 获取管理员权限")?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        if stderr.contains("User canceled") || stderr.contains("cancelled") {
            return Err(anyhow!("用户已取消安装。"));
        }
        return Err(anyhow!("使用管理员权限创建符号链接失败：{stderr}"));
    }

    Ok(())
}

/// Remove a file with elevated privileges using osascript
///
/// This function uses macOS's osascript to prompt for administrator privileges
/// and remove a file, used for CLI uninstallation.
fn remove_file_with_admin(target: &Path) -> Result<()> {
    let target_str = target
        .to_str()
        .ok_or_else(|| anyhow!("Target path contains invalid UTF-8: {target:?}"))?;

    let escaped_target = ShellFamily::Posix.shell_escape(target_str);

    let script = format!(
        "do shell script \"rm {escaped_target}\" with prompt \"Warp 需要管理员权限才能从 /usr/local/bin 卸载该命令。\" with administrator privileges"
    );

    log::debug!("Removing file with admin privileges");

    let output = Command::new("osascript")
        .arg("-e")
        .arg(&script)
        .output()
        .context("无法通过 osascript 获取管理员权限")?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        if stderr.contains("User canceled") || stderr.contains("cancelled") {
            return Err(anyhow!("用户已取消卸载。"));
        }
        return Err(anyhow!("使用管理员权限移除文件失败：{stderr}"));
    }

    Ok(())
}

/// Install the CLI by creating a symlink (channel-specific target)
///
/// This function:
/// 1. Detects the current Warp channel and finds the appropriate binary
/// 2. Attempts to create a symlink without admin privileges first
/// 3. Falls back to prompting for admin privileges if needed
/// 4. Handles existing installations and edge cases
pub fn install_cli() -> Result<()> {
    let cli_path = cli_install_target_path();
    let current_binary = std::env::current_exe().context("无法获取当前可执行文件路径")?;

    // Check if target file exists and handle conflicts
    if cli_path.exists() && !cli_path.is_symlink() {
        return Err(anyhow!(
            "无法安装：{:?} 已存在但不是符号链接。请先手动移除。",
            cli_path
        ));
    }

    // Try to create symlink without admin privileges first
    let symlink_result = symlink(&current_binary, &cli_path);

    match symlink_result {
        Ok(_) => {
            log::debug!(
                "CLI installed successfully without admin privileges: {:?} -> {}",
                cli_path,
                current_binary.display()
            );
        }
        Err(_) => {
            log::debug!("Symlink creation failed, trying with admin privileges");

            create_symlink_with_admin(&current_binary, &cli_path)
                .context("即使使用管理员权限也无法创建符号链接")?;

            log::debug!("CLI installed successfully with admin privileges");
        }
    }

    Ok(())
}

/// Uninstall the CLI by removing the symlink (channel-specific target)
///
/// This function:
/// 1. Verifies that the target is actually a symlink (safety check)
/// 2. Attempts to remove without admin privileges first
/// 3. Falls back to prompting for admin privileges if needed
pub fn uninstall_cli() -> Result<()> {
    let cli_path = cli_install_target_path();

    if !cli_path.exists() {
        return Err(anyhow!("Oz command is not currently installed."));
    }

    // Safety check: verify it's actually a symlink before removing
    if !cli_path.is_symlink() {
        return Err(anyhow!(
            "无法卸载：{:?} 已存在但不是符号链接。请手动移除。",
            cli_path
        ));
    }

    // Try to remove without admin privileges first
    let remove_result = fs::remove_file(&cli_path);

    match remove_result {
        Ok(_) => {
            log::debug!("CLI uninstalled successfully without admin privileges");
        }
        Err(_) => {
            log::debug!("File removal failed, trying with admin privileges");

            remove_file_with_admin(&cli_path).context("即使使用管理员权限也无法移除符号链接")?;

            log::debug!("CLI uninstalled successfully with admin privileges");
        }
    }

    Ok(())
}
