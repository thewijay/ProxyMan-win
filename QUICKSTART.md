# ProxyMan Windows - Quick Start Guide

## Installation

### Option 1: Simple Installation (Recommended)

```powershell
# Download or clone the repository
git clone https://github.com/your-username/proxyman-windows.git
cd proxyman-windows

# Run the Python installer
python install.py
```

### Option 2: PowerShell Installation

```powershell
# Simple PowerShell installer (recommended):
.\install-simple.ps1

# Or the full PowerShell installer:
.\install.ps1
```

### Option 3: Manual Installation

```powershell
# Install dependencies
pip install -r requirements.txt

# Use the batch file to run the tool
.\proxyman.bat help
```

## Uninstallation

To remove ProxyMan Windows from your system:

### Python Uninstaller

```powershell
python uninstall.py
```

### PowerShell Uninstaller

```powershell
# Interactive uninstall
.\uninstall.ps1

# Silent uninstall (no prompts)
.\uninstall.ps1 -Force

# Keep configuration files
.\uninstall.ps1 -KeepConfig
```

The uninstaller will remove:

- ProxyMan from system PATH
- Configuration files (unless -KeepConfig is used)
- Desktop shortcuts
- Batch files
- Optionally clear all proxy settings

## Basic Usage

### Set Proxy Settings

```powershell
# If proxyman is in PATH (after admin installation):
proxyman set

# If not in PATH, use one of these:
.\proxyman.bat set
python proxyman.py set
```

This will start an interactive setup where you can:

- Enter proxy host and port
- Configure authentication
- Select which applications to configure
- Save the configuration for later use

### List Current Settings

```powershell
# If proxyman is in PATH:
proxyman list

# If not in PATH, use one of these:
.\proxyman.bat list
python proxyman.py list
```

Shows current proxy settings for all supported applications.

### Remove Proxy Settings

```powershell
# If proxyman is in PATH:
proxyman unset

# If not in PATH, use one of these:
.\proxyman.bat unset
python proxyman.py unset
```

Removes proxy settings from selected applications.

### Work with Saved Configurations

```powershell
# List saved configurations
proxyman configs
# or: .\proxyman.bat configs

# Save current settings
proxyman save office_proxy
# or: .\proxyman.bat save office_proxy

# Load saved configuration
proxyman load office_proxy
# or: .\proxyman.bat load office_proxy

# Delete saved configuration
proxyman delete office_proxy
# or: .\proxyman.bat delete office_proxy
```

## Supported Applications

- **Windows System Proxy**: Internet Explorer, Edge, and many other applications
- **Environment Variables**: HTTP_PROXY, HTTPS_PROXY for console applications
- **Git**: Version control proxy settings
- **NPM/Yarn**: Package manager proxy settings
- **PowerShell**: PowerShell profile proxy settings

## Common Use Cases

### Corporate Environment

```powershell
# Set up corporate proxy with authentication
.\proxyman.bat set
# Follow prompts to enter corporate proxy details
# Save as 'corporate' for easy reuse
```

### Home Network

```powershell
# Load home proxy settings
.\proxyman.bat load home
```

### Development

```powershell
# Quickly disable proxy for development
.\proxyman.bat unset
```

## Tips

1. **Run as Administrator** for full functionality
2. **Save configurations** for easy switching between environments
3. **Use selective targeting** to only configure specific applications
4. **Check current settings** with `.\proxyman.bat list` before making changes
5. **If not in PATH**: Use `.\proxyman.bat` or `python proxyman.py` instead of just `proxyman`

## Troubleshooting

### Installation Issues

**Error: "SyntaxError: unterminated string literal" when running install.ps1**

- You're running a PowerShell script with Python
- Use PowerShell: `.\install.ps1` or `.\install-simple.ps1` (not `python install.ps1`)
- Or use the Python installer: `python install.py`

**Error: "ImportError: attempted relative import with no known parent package"**

- This was a module import issue that has been fixed
- Update to the latest version or re-download the project
- The issue was caused by relative imports in Python modules

**Error: "ModuleNotFoundError: No module named 'colorama'"**

- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the correct directory

**Error: "proxyman is not recognized"**

- The tool is not in your system PATH
- Use `.\proxyman.bat` or `python proxyman.py` instead
- Or run `python install.py` as Administrator to add to PATH

### Common Issues

- Run Command Prompt or PowerShell as Administrator
- Some operations (like system proxy) require elevated privileges

**Error: "Python not found"**

- Install Python 3.7+ from python.org
- Make sure Python is added to PATH

**Error: "Git not found"**

- Git proxy configuration will be skipped if Git is not installed
- Install Git if you need Git proxy support

**Settings not taking effect**

- Some applications may need to be restarted
- System proxy changes are usually immediate
- Environment variables affect new processes only

### Getting Help

```powershell
# If proxyman is in PATH:
proxyman help

# If not in PATH, use one of these:
.\proxyman.bat help
python proxyman.py help
```

For more detailed help, check the README.md file or visit the project repository.

## Security Notes

- Configuration files may contain passwords
- Don't share configuration files with credentials
- Use authentication only when necessary
- Consider using environment variables for sensitive data

## Next Steps

- Explore the examples directory for sample configurations
- Check the source code for advanced usage
- Contribute to the project on GitHub
- Report bugs or request features
- Use `python uninstall.py` or `.\uninstall.ps1` to remove ProxyMan when no longer needed
