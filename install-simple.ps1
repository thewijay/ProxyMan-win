# ProxyMan Windows - Simple PowerShell Installation Script

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
    Write-ColoredOutput "📦 Installing Python dependencies..." "Blue"
    
    try {
        $result = & python -m pip install -r requirements.txt 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredOutput "✅ Dependencies installed successfully" "Green"
            return $true
        } else {
            Write-ColoredOutput "❌ Failed to install dependencies" "Red"
            return $false
        }
    } catch {
        Write-ColoredOutput "❌ Error installing dependencies: $_" "Red"
        return $false
    }
}

function Create-BatchFile {
    Write-ColoredOutput "📄 Creating batch file..." "Blue"
    
    $batchContent = '@echo off
cd /d "%~dp0"
python proxyman.py %*
if %ERRORLEVEL% neq 0 (
    py proxyman.py %*
)'
    
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
    param([string]$Path)
    
    if (-not (Test-AdminPrivileges)) {
        Write-ColoredOutput "⚠️  Administrator privileges required to add to system PATH" "Yellow"
        return $false
    }
    
    try {
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        
        if ($currentPath -notlike "*$Path*") {
            $newPath = if ($currentPath) { "$currentPath;$Path" } else { $Path }
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            Write-ColoredOutput "✅ Added to user PATH" "Green"
        } else {
            Write-ColoredOutput "✅ Already in user PATH" "Green"
        }
        
        return $true
    } catch {
        Write-ColoredOutput "❌ Failed to add to PATH: $_" "Red"
        return $false
    }
}

# Main installation function
Write-ColoredOutput "🚀 ProxyMan Windows PowerShell Installer" "Cyan"
Write-ColoredOutput "=" * 50 "Cyan"

# Check Python version
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-ColoredOutput "✅ Python detected: $pythonVersion" "Green"
    } else {
        Write-ColoredOutput "❌ Python not found. Please install Python 3.7+" "Red"
        exit 1
    }
} catch {
    Write-ColoredOutput "❌ Python not found. Please install Python 3.7+" "Red"
    exit 1
}

# Install dependencies
if (-not (Install-Dependencies)) {
    exit 1
}

# Create batch file
if (-not (Create-BatchFile)) {
    exit 1
}

# Add to PATH
$currentDir = Get-Location
Add-ToPath -Path $currentDir.Path

Write-ColoredOutput "`n🎉 Installation completed!" "Green"
Write-ColoredOutput "You can now use ProxyMan with:" "Cyan"
Write-ColoredOutput "  .\proxyman.bat help" "White"
Write-ColoredOutput "  .\proxyman.bat set" "White"
Write-ColoredOutput "  .\proxyman.bat list" "White"

if (-not (Test-AdminPrivileges)) {
    Write-ColoredOutput "`n⚠️  Note: Run as administrator to add to system PATH" "Yellow"
}

Write-ColoredOutput "`nPress any key to continue..." "Yellow"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
