# ProxyMan Windows - PowerShell Installation Script
# Alternative installation method using PowerShell

param(
    [switch]$SystemWide,
    [switch]$UserOnly,
    [switch]$SkipPath,
    [string]$InstallPath = $null
)

# Colors for output
$colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    Cyan = "Cyan"
    White = "White"
}

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $colors[$Color]
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

function Create-BatchFile {
    Write-ColoredOutput "📄 Creating batch file..." "Blue"
    
    $batchContent = @'
@echo off
cd /d "%~dp0"
python proxyman.py %*
if %ERRORLEVEL% neq 0 (
    py proxyman.py %*
)
'@
    
    try {
        $batchContent | Out-File -FilePath "proxyman.bat" -Encoding ASCII
        Write-ColoredOutput "✅ Created proxyman.bat" "Green"
        return $true
    } catch {
        Write-ColoredOutput "❌ Failed to create batch file: $_" "Red"
        return $false
    }
}

function Add-ToPath {
    param(
        [string]$Path,
        [bool]$SystemWide = $false
    )
    
    if ($SystemWide -and -not (Test-AdminPrivileges)) {
        Write-ColoredOutput "⚠️  Administrator privileges required for system-wide installation" "Yellow"
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
            $newPath = "$currentPath;$Path"
            [Environment]::SetEnvironmentVariable("PATH", $newPath, $target)
            Write-ColoredOutput "✅ Added to $scope PATH" "Green"
        } else {
            Write-ColoredOutput "✅ Already in $scope PATH" "Green"
        }
        
        return $true
    } catch {
        Write-ColoredOutput "❌ Failed to add to PATH: $_" "Red"
        return $false
    }
}

function Install-ProxyMan {
    Write-ColoredOutput "🚀 ProxyMan Windows PowerShell Installer" "Cyan"
    Write-ColoredOutput "=" * 50 "Cyan"
    
    # Check Python version
    try {
        $pythonVersion = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredOutput "✅ Python detected: $pythonVersion" "Green"
        } else {
            Write-ColoredOutput "❌ Python not found. Please install Python 3.7+" "Red"
            return $false
        }
    } catch {
        Write-ColoredOutput "❌ Python not found. Please install Python 3.7+" "Red"
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
        
        if ($SystemWide) {
            Add-ToPath -Path $currentDir -SystemWide $true
        } else {
            Add-ToPath -Path $currentDir -SystemWide $false
        }
    }
    
    # Create desktop shortcut
    if ($SystemWide -or $UserOnly) {
        try {
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\ProxyMan.lnk")
            $Shortcut.TargetPath = "$PWD\proxyman.bat"
            $Shortcut.WorkingDirectory = "$PWD"
            $Shortcut.Description = "ProxyMan Windows - Proxy Configuration Tool"
            $Shortcut.Save()
            Write-ColoredOutput "✅ Created desktop shortcut" "Green"
        } catch {
            Write-ColoredOutput "⚠️  Could not create desktop shortcut: $_" "Yellow"
        }
    }
    
    Write-ColoredOutput "`n🎉 Installation completed!" "Green"
    Write-ColoredOutput "You can now use ProxyMan with:" "Cyan"
    Write-ColoredOutput "  proxyman help" "White"
    Write-ColoredOutput "  proxyman set" "White"
    Write-ColoredOutput "  proxyman list" "White"
    
    if (-not (Test-AdminPrivileges) -and -not $SkipPath) {
        Write-ColoredOutput "`n⚠️  Note: Run as administrator for system-wide installation" "Yellow"
    }
    
    return $true
}

function Show-Help {
    Write-ColoredOutput "ProxyMan Windows PowerShell Installer" "Cyan"
    Write-ColoredOutput ""
    Write-ColoredOutput "Usage:" "White"
    Write-ColoredOutput "  .\install.ps1 [options]" "White"
    Write-ColoredOutput ""
    Write-ColoredOutput "Options:" "White"
    Write-ColoredOutput "  -SystemWide    Install system-wide (requires admin)" "White"
    Write-ColoredOutput "  -UserOnly      Install for current user only" "White"
    Write-ColoredOutput "  -SkipPath      Skip adding to PATH" "White"
    Write-ColoredOutput "  -InstallPath   Custom installation path" "White"
    Write-ColoredOutput ""
    Write-ColoredOutput "Examples:" "White"
    Write-ColoredOutput "  .\install.ps1                    # Standard installation" "White"
    Write-ColoredOutput "  .\install.ps1 -SystemWide        # System-wide installation" "White"
    Write-ColoredOutput "  .\install.ps1 -UserOnly -SkipPath # User-only, no PATH" "White"
}

# Main execution
try {
    if ($args -contains "-help" -or $args -contains "--help" -or $args -contains "-h") {
        Show-Help
        exit 0
    }
    
    $success = Install-ProxyMan
    if (-not $success) {
        exit 1
    }
} catch {
    Write-ColoredOutput "`n❌ Installation failed: $_" "Red"
    exit 1
}

Write-ColoredOutput "`nPress any key to continue..." "Yellow"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
