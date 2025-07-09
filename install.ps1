# ProxyManX Windows - PowerShell Installation Script
# Unified installer with both simple and advanced options

param(
    [switch]$SystemWide,
    [switch]$UserOnly,
    [switch]$SkipPath,
    [switch]$Simple,
    [switch]$Help,
    [string]$InstallPath = $null
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

function Install-Dependencies {
    Write-ColoredOutput "Installing Python dependencies..." "Blue"
    
    try {
        $result = & python -m pip install -r requirements.txt 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredOutput "Dependencies installed successfully" "Green"
            return $true
        } else {
            Write-ColoredOutput "Failed to install dependencies: $result" "Red"
            return $false
        }
    } catch {
        Write-ColoredOutput "Error installing dependencies: $_" "Red"
        return $false
    }
}
}

function Create-BatchFile {
    Write-ColoredOutput "Creating batch file..." "Blue"
    
    $batchContent = @'
@echo off
cd /d "%~dp0"
python proxymanx.py %*
if %ERRORLEVEL% neq 0 (
    py proxymanx.py %*
)
'@
    
    try {
        $batchContent | Out-File -FilePath "proxymanx.bat" -Encoding ASCII
        Write-ColoredOutput "Created proxymanx.bat" "Green"
        return $true
    } catch {
        Write-ColoredOutput "Failed to create batch file: $_" "Red"
        return $false
    }
}

function Add-ToPath {
    param(
        [string]$Path,
        [bool]$SystemWide = $false
    )
    
    if ($SystemWide -and -not (Test-AdminPrivileges)) {
        Write-ColoredOutput "Administrator privileges required for system-wide installation" "Yellow"
        return $false
    }
    
    try {
        if ($SystemWide) {
            $target = "Machine"
            $scope = "system"
        } else {
            $target = "User"
            $scope = "user"
        }
        
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", $target)
        
        if ($currentPath -notlike "*$Path*") {
            $newPath = if ($currentPath) { "$currentPath;$Path" } else { $Path }
            [Environment]::SetEnvironmentVariable("PATH", $newPath, $target)
            Write-ColoredOutput "Added to $scope PATH" "Green"
        } else {
            Write-ColoredOutput "Already in $scope PATH" "Green"
        }
        
        return $true
    } catch {
        Write-ColoredOutput "Failed to add to PATH: $_" "Red"
        return $false
    }
}

function Create-DesktopShortcut {
    try {
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\ProxyManX.lnk")
        $Shortcut.TargetPath = "$PWD\proxymanx.bat"
        $Shortcut.WorkingDirectory = "$PWD"
        $Shortcut.Description = "ProxyManX Windows - Proxy Configuration Tool"
        $Shortcut.Save()
        Write-ColoredOutput "Created desktop shortcut" "Green"
        return $true
    } catch {
        Write-ColoredOutput "Could not create desktop shortcut: $_" "Yellow"
        return $false
    }
}

function Install-ProxyManX {
    param([bool]$SimpleMode = $false)
    
    Write-ColoredOutput "ProxyManX Windows PowerShell Installer" "Cyan"
    if ($SimpleMode) {
        Write-ColoredOutput "Running in simple mode..." "Yellow"
    }
    Write-ColoredOutput "=" * 50 "Cyan"
    
    # Check Python version
    try {
        $pythonVersion = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredOutput "Python detected: $pythonVersion" "Green"
        } else {
            Write-ColoredOutput "Python not found. Please install Python 3.7+" "Red"
            return $false
        }
    } catch {
        Write-ColoredOutput "Python not found. Please install Python 3.7+" "Red"
        return $false
    }
    
    # Install dependencies
    if (-not (Install-Dependencies)) {
        return $false
    }
    
    # Create batch file
    if (-not (Create-BatchFile)) {
        return $false
    }
    
    # Add to PATH
    if (-not $SkipPath) {
        $currentDir = Get-Location
        
        if ($SimpleMode) {
            # Simple mode: just add to user PATH
            Add-ToPath -Path $currentDir.Path -SystemWide $false
        } else {
            # Advanced mode: respect SystemWide parameter
            if ($SystemWide) {
                Add-ToPath -Path $currentDir.Path -SystemWide $true
            } else {
                Add-ToPath -Path $currentDir.Path -SystemWide $false
            }
        }
    }
    
    # Create desktop shortcut (only in advanced mode unless specifically requested)
    if ((-not $SimpleMode) -and ($SystemWide -or $UserOnly)) {
        Create-DesktopShortcut
    }
    
    Write-ColoredOutput "`nInstallation completed!" "Green"
    Write-ColoredOutput "You can now use ProxyManX with:" "Cyan"
    
    if ($SkipPath) {
        Write-ColoredOutput "  .\proxymanx.bat help" "White"
        Write-ColoredOutput "  .\proxymanx.bat set" "White"
        Write-ColoredOutput "  .\proxymanx.bat list" "White"
    } else {
        Write-ColoredOutput "  proxymanx help" "White"
        Write-ColoredOutput "  proxymanx set" "White"
        Write-ColoredOutput "  proxymanx list" "White"
    }
    
    if (-not (Test-AdminPrivileges) -and (-not $SkipPath) -and (-not $SimpleMode)) {
        Write-ColoredOutput "`nNote: Run as administrator for system-wide installation" "Yellow"
    }
    
    return $true
}

function Show-Help {
    Write-ColoredOutput "ProxyManX Windows PowerShell Installer" "Cyan"
    Write-ColoredOutput ""
    Write-ColoredOutput "Usage:" "White"
    Write-ColoredOutput "  .\install.ps1 [options]" "White"
    Write-ColoredOutput ""
    Write-ColoredOutput "Options:" "White"
    Write-ColoredOutput "  -Simple        Quick installation (user PATH only)" "White"
    Write-ColoredOutput "  -SystemWide    Install system-wide (requires admin)" "White"
    Write-ColoredOutput "  -UserOnly      Install for current user only" "White"
    Write-ColoredOutput "  -SkipPath      Skip adding to PATH" "White"
    Write-ColoredOutput "  -Help          Show this help message" "White"
    Write-ColoredOutput ""
    Write-ColoredOutput "Examples:" "White"
    Write-ColoredOutput "  .\install.ps1                    # Standard installation" "White"
    Write-ColoredOutput "  .\install.ps1 -Simple            # Quick installation" "White"
    Write-ColoredOutput "  .\install.ps1 -SystemWide        # System-wide installation" "White"
    Write-ColoredOutput "  .\install.ps1 -UserOnly -SkipPath # User-only, no PATH" "White"
}

# Main execution
try {
    if ($Help -or $args -contains "-help" -or $args -contains "--help" -or $args -contains "-h") {
        Show-Help
        exit 0
    }
    
    $success = Install-ProxyManX -SimpleMode $Simple
    if (-not $success) {
        exit 1
    }
} catch {
    Write-ColoredOutput "`nInstallation failed: $_" "Red"
    exit 1
}

Write-ColoredOutput "`nPress any key to continue..." "Yellow"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
