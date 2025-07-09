# ProxyManX Windows - Quick Start Guide

## Installation

### Option 1: Python Installation (Cross-platform)

```powershell
# Download or clone the repository
git clone https://github.com/thewijay/ProxyManX.git
cd ProxyManX

# Run the Python installer (automatically adds to user PATH)
python install.py
```

### Option 2: PowerShell Installation (Windows-only)

```powershell
# Quick installation (recommended):
.\install.ps1 -Simple

# Standard installation with options:
.\install.ps1
```

### Option 3: Manual Installation

```powershell
# Install dependencies
pip install -r requirements.txt

# Use the batch file to run the tool
.\proxymanx.bat help
```

## Uninstallation

To remove ProxyManX Windows from your system:

### Python Uninstaller (Recommended)

```powershell
python uninstall.py
```

The uninstaller will automatically:

- Clear all proxy settings (no prompts needed)
- Remove ProxyManX from system PATH
- Remove configuration files and saved profiles
- Remove desktop shortcuts and batch files

### PowerShell Uninstaller

```powershell
# Interactive uninstall
.\uninstall.ps1

# Silent uninstall (no prompts)
.\uninstall.ps1 -Force

# Keep configuration files
.\uninstall.ps1 -KeepConfig
```

**Note**: If the uninstaller hangs or shows interactive prompts, make sure you have the latest version. Use `git pull` to update or re-download the project.

## Basic Usage

### Set Proxy Settings

```powershell
# If proxymanx is in PATH (after admin installation):
proxymanx set

# If not in PATH, use one of these:
.\proxymanx.bat set
python proxymanx.py set
```

This will start an interactive setup where you can:

- Enter proxy host and port
- Configure authentication
- Select which applications to configure
- Save the configuration for later use

### List Current Settings

```powershell
# If proxymanx is in PATH:
proxymanx list

# If not in PATH, use one of these:
.\proxymanx.bat list
python proxymanx.py list
```

Shows current proxy settings for all supported applications.

### Remove Proxy Settings

```powershell
# If proxymanx is in PATH:
proxymanx unset

# Remove all proxy settings (non-interactive):
proxymanx unset all

# Remove proxy for specific targets:
proxymanx unset git npm

# If not in PATH, use one of these:
.\proxymanx.bat unset
python proxymanx.py unset all
```

Removes proxy settings from selected applications.

### Work with Saved Configurations

```powershell
# List saved configurations
proxymanx configs
# or: .\proxymanx.bat configs

# Save current settings
proxymanx save office_proxy
# or: .\proxymanx.bat save office_proxy

# Load saved configuration
proxymanx load office_proxy
# or: .\proxymanx.bat load office_proxy

# Delete saved configuration
proxymanx delete office_proxy
# or: .\proxymanx.bat delete office_proxy
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
.\proxymanx.bat set
# Follow prompts to enter corporate proxy details
# Save as 'corporate' for easy reuse
```

### Home Network

```powershell
# Load home proxy settings
.\proxymanx.bat load home
```

### Development

```powershell
# Quickly disable proxy for development
.\proxymanx.bat unset
```

## Tips

1. **Run as Administrator** for full functionality
2. **Save configurations** for easy switching between environments
3. **Use selective targeting** to only configure specific applications
4. **Check current settings** with `.\proxymanx.bat list` before making changes
5. **If not in PATH**: Use `.\proxymanx.bat` or `python proxymanx.py` instead of just `proxymanx`

## Troubleshooting

### Installation Issues

**Error: "SyntaxError: unterminated string literal" when running install.ps1**

- You're running a PowerShell script with Python
- Use PowerShell: `.\install.ps1` (not `python install.ps1`)
- For quick install: `.\install.ps1 -Simple`
- Or use the Python installer: `python install.py`

**Error: "ImportError: attempted relative import with no known parent package"**

- This was a module import issue that has been fixed
- Update to the latest version or re-download the project
- The issue was caused by relative imports in Python modules

**Error: "ModuleNotFoundError: No module named 'colorama'"**

- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the correct directory

**Error: "proxymanx is not recognized"**

This happens when ProxyManX is not in your system PATH:

```powershell
# First, check if the installer succeeded:
python install.py

# If PATH wasn't added automatically, use these alternatives:
.\proxymanx.bat help
python proxymanx.py help

# Or add to PATH manually:
# 1. Open "Environment Variables" in Windows System Properties
# 2. Edit your user PATH variable
# 3. Add the ProxyManX directory path
# 4. Restart your terminal
```

**Error: "Administrator privileges required to add to system PATH"**

- The Python installer now automatically tries user PATH first (no admin needed)
- Use `.\proxymanx.bat` or `python proxymanx.py` if PATH addition fails
- For system-wide installation, run as Administrator or use PowerShell installer

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

### Uninstaller Issues

**Error: "Uninstaller hangs or prompts for proxy settings cleanup"**

This indicates you're running an older version of the uninstaller:

```powershell
# Update to the latest version:
git pull

# Or clear Python cache and retry:
python -c "import py_compile; py_compile.compile('uninstall.py')"
python uninstall.py

# Or use the manual cleanup approach:
python proxymanx.py unset all
python uninstall.py
```

**Error: "Command 'proxymanx.py unset' timed out after 30 seconds"**

- Update to the latest version which includes non-interactive unset
- The new version uses `proxymanx.py unset all` for automatic cleanup

### Getting Help

```powershell
# If proxymanx is in PATH:
proxymanx help

# If not in PATH, use one of these:
.\proxymanx.bat help
python proxymanx.py help
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
- Use `python uninstall.py` or `.\uninstall.ps1` to remove ProxyManX when no longer needed
