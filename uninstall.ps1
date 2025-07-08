# ProxyMan Windows - Uninstaller PowerShell Script
# Remove ProxyMan Windows from the system

param(
    [switch]$Force,
    [switch]$KeepConfig,
    [switch]$KeepProxy
)

# Colors for output
function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    switch ($Color) {
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Blue" { Write-Host $Message -ForegroundColor Blue }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        default { Write-Host $Message }
    }
}

function Test-AdminPrivileges {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Remove-FromPath {
    param([string]$Path)
    
    try {
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        
        if ($currentPath -like "*$Path*") {
            $pathEntries = $currentPath -split ";"
            $newPathEntries = $pathEntries | Where-Object { $_ -ne $Path }
            $newPath = $newPathEntries -join ";"
            
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            Write-ColoredOutput "✅ Removed from user PATH" "Green"
        } else {
            Write-ColoredOutput "ℹ️  Not found in user PATH" "Blue"
        }
        
        return $true
    } catch {
        Write-ColoredOutput "⚠️  Could not remove from PATH: $_" "Yellow"
        return $false
    }
}

function Remove-ConfigFiles {
    if ($KeepConfig) {
        Write-ColoredOutput "ℹ️  Keeping configuration files as requested" "Blue"
        return $true
    }
    
    $configDir = "$env:USERPROFILE\.proxyman"
    
    if (Test-Path $configDir) {
        try {
            Remove-Item $configDir -Recurse -Force
            Write-ColoredOutput "✅ Removed configuration directory: $configDir" "Green"
            return $true
        } catch {
            Write-ColoredOutput "❌ Failed to remove config directory: $_" "Red"
            return $false
        }
    } else {
        Write-ColoredOutput "ℹ️  No configuration directory found" "Blue"
        return $true
    }
}

function Remove-DesktopShortcut {
    $shortcut = "$env:USERPROFILE\Desktop\ProxyMan.lnk"
    
    if (Test-Path $shortcut) {
        try {
            Remove-Item $shortcut -Force
            Write-ColoredOutput "✅ Removed desktop shortcut" "Green"
            return $true
        } catch {
            Write-ColoredOutput "⚠️  Could not remove desktop shortcut: $_" "Yellow"
            return $false
        }
    } else {
        Write-ColoredOutput "ℹ️  No desktop shortcut found" "Blue"
        return $true
    }
}

function Remove-BatchFile {
    if (Test-Path "proxyman.bat") {
        try {
            Remove-Item "proxyman.bat" -Force
            Write-ColoredOutput "✅ Removed proxyman.bat" "Green"
            return $true
        } catch {
            Write-ColoredOutput "❌ Failed to remove batch file: $_" "Red"
            return $false
        }
    } else {
        Write-ColoredOutput "ℹ️  No batch file found" "Blue"
        return $true
    }
}

function Clear-ProxySettings {
    if ($KeepProxy) {
        Write-ColoredOutput "ℹ️  Keeping proxy settings as requested" "Blue"
        return
    }
    
    Write-ColoredOutput "`n🔧 Proxy Settings Cleanup" "Cyan"
    
    if (-not $Force) {
        $response = Read-Host "Do you want to clear all proxy settings set by ProxyMan? (y/N)"
        if ($response -notmatch "^[Yy]") {
            Write-ColoredOutput "ℹ️  Proxy settings left unchanged" "Blue"
            return
        }
    }
    
    try {
        if (Test-Path "proxyman.py") {
            Write-ColoredOutput "Clearing proxy settings..." "Blue"
            $result = & python proxyman.py unset 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-ColoredOutput "✅ Proxy settings cleared" "Green"
            } else {
                Write-ColoredOutput "⚠️  Some proxy settings may not have been cleared" "Yellow"
            }
        } else {
            Write-ColoredOutput "⚠️  ProxyMan not found, cannot clear proxy settings" "Yellow"
            Write-ColoredOutput "You may need to manually clear proxy settings" "Yellow"
        }
    } catch {
        Write-ColoredOutput "⚠️  Error clearing proxy settings: $_" "Yellow"
    }
}

function Show-Help {
    Write-ColoredOutput "ProxyMan Windows Uninstaller" "Cyan"
    Write-ColoredOutput ""
    Write-ColoredOutput "Usage:" "White"
    Write-ColoredOutput "  .\uninstall.ps1 [options]" "White"
    Write-ColoredOutput ""
    Write-ColoredOutput "Options:" "White"
    Write-ColoredOutput "  -Force        Don't ask for confirmation" "White"
    Write-ColoredOutput "  -KeepConfig   Keep configuration files" "White"
    Write-ColoredOutput "  -KeepProxy    Don't clear proxy settings" "White"
    Write-ColoredOutput ""
    Write-ColoredOutput "Examples:" "White"
    Write-ColoredOutput "  .\uninstall.ps1                    # Interactive uninstall" "White"
    Write-ColoredOutput "  .\uninstall.ps1 -Force             # Silent uninstall" "White"
    Write-ColoredOutput "  .\uninstall.ps1 -KeepConfig        # Keep config files" "White"
}

function Uninstall-ProxyMan {
    Write-ColoredOutput "🗑️  ProxyMan Windows Uninstaller" "Cyan"
    Write-ColoredOutput "=" * 50 "Cyan"
    
    if (-not $Force) {
        Write-ColoredOutput "`nThis will remove ProxyMan Windows from your system." "Yellow"
        Write-ColoredOutput "The following will be removed:" "White"
        Write-ColoredOutput "  • ProxyMan executable and files" "White"
        
        if (-not $KeepConfig) {
            Write-ColoredOutput "  • Configuration files and saved profiles" "White"
        }
        
        Write-ColoredOutput "  • PATH environment variable entries" "White"
        Write-ColoredOutput "  • Desktop shortcuts" "White"
        
        $response = Read-Host "`nDo you want to continue? (y/N)"
        
        if ($response -notmatch "^[Yy]") {
            Write-ColoredOutput "Uninstallation cancelled." "Yellow"
            return
        }
    }
    
    Write-ColoredOutput "`n🚀 Starting uninstallation..." "Blue"
    
    # Clear proxy settings first (optional)
    Clear-ProxySettings
    
    # Remove from PATH
    Write-ColoredOutput "`n📍 Removing from PATH..." "Blue"
    $currentDir = Get-Location
    Remove-FromPath -Path $currentDir.Path
    
    # Remove configuration files
    Write-ColoredOutput "`n📁 Removing configuration files..." "Blue"
    Remove-ConfigFiles
    
    # Remove desktop shortcut
    Write-ColoredOutput "`n🖥️  Removing shortcuts..." "Blue"
    Remove-DesktopShortcut
    
    # Remove batch file
    Write-ColoredOutput "`n📄 Removing batch file..." "Blue"
    Remove-BatchFile
    
    Write-ColoredOutput "`n🎉 Uninstallation completed!" "Green"
    Write-ColoredOutput "ProxyMan Windows has been removed from your system." "Green"
    
    Write-ColoredOutput "`n📋 Manual cleanup (if needed):" "Cyan"
    Write-ColoredOutput "  • Check Windows proxy settings in Internet Options" "White"
    Write-ColoredOutput "  • Verify git proxy settings: git config --global -l" "White"
    Write-ColoredOutput "  • Check npm proxy settings: npm config list" "White"
    Write-ColoredOutput "  • Review PowerShell profile for proxy settings" "White"
    
    if (-not (Test-AdminPrivileges)) {
        Write-ColoredOutput "`n⚠️  Note: Some PATH changes may require administrator privileges" "Yellow"
    }
    
    Write-ColoredOutput "`nThank you for using ProxyMan Windows!" "Green"
}

# Main execution
try {
    if ($args -contains "-help" -or $args -contains "--help" -or $args -contains "-h") {
        Show-Help
        exit 0
    }
    
    Uninstall-ProxyMan
} catch {
    Write-ColoredOutput "`n❌ Uninstallation failed: $_" "Red"
    exit 1
}

Write-ColoredOutput "`nPress any key to continue..." "Yellow"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
