# ProxyMan Windows

A Windows port of the Linux ProxyMan proxy management tool, built with Python.

## Features

- **System-wide proxy configuration** for Windows
- **Profile management** - save, load, and delete proxy configurations
- **Multiple target support**:
  - Windows system proxy settings
  - Environment variables
  - Git configuration
  - NPM/Yarn configuration
  - PowerShell/Command Prompt
  - Windows Registry
- **Interactive CLI** with colorized output
- **Authentication support** for proxy servers
- **Batch operations** on multiple targets

## Requirements

- Python 3.7+
- Windows 10/11
- Administrator privileges (for some operations)

## Installation

### Option 1: Simple Installation (Recommended)

```powershell
# Download or clone the repository
git clone https://github.com/thewijay/ProxyMan-win.git
cd ProxyMan-win

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

To completely remove ProxyMan Windows from your system:

### Option 1: Python Uninstaller

```bash
python uninstall.py
```

### Option 2: PowerShell Uninstaller

```powershell
# Interactive uninstall
.\uninstall.ps1

# Silent uninstall
.\uninstall.ps1 -Force

# Keep configuration files
.\uninstall.ps1 -KeepConfig

# Keep proxy settings
.\uninstall.ps1 -KeepProxy
```

The uninstaller will:

- Remove ProxyMan from PATH
- Delete configuration files and saved profiles
- Remove desktop shortcuts
- Optionally clear all proxy settings set by ProxyMan
- Clean up all installation artifacts

## Usage

### Set Proxy

```bash
proxyman set
```

### Unset Proxy

```bash
proxyman unset
```

### List Current Settings

```bash
proxyman list
```

### Save Configuration

```bash
proxyman save profile_name
```

### Load Configuration

```bash
proxyman load profile_name
```

### List Configurations

```bash
proxyman configs
```

### Delete Configuration

```bash
proxyman delete profile_name
```

### Show Help

```bash
proxyman help
```

## Supported Targets

1. **System Proxy** - Windows system proxy settings via Registry
2. **Environment Variables** - User and system environment variables
3. **Git** - Global git proxy configuration
4. **NPM/Yarn** - Package manager proxy settings
5. **PowerShell** - PowerShell profile proxy settings
6. **Command Prompt** - CMD environment variables
7. **Internet Explorer** - IE proxy settings (affects many apps)

## Configuration Files

Profiles are stored in `%USERPROFILE%\.proxyman\` directory.

## Notes

- Some operations require administrator privileges
- System proxy changes take effect immediately
- Shell proxy settings require restarting the terminal
- Registry changes may require system restart for some applications

## Project Structure

```
ProxyMan-win/
├── src/                    # Core application modules
│   ├── config.py          # Configuration management
│   ├── proxyman.py        # Main application logic
│   ├── targets.py         # Proxy target handlers
│   └── utils.py           # Utility functions
├── install.py             # Python installer
├── install.ps1            # PowerShell installer
├── install-simple.ps1     # Simple PowerShell installer
├── uninstall.py           # Python uninstaller
├── uninstall.ps1          # PowerShell uninstaller
├── proxyman.py            # Main entry point
├── proxyman.bat           # Windows batch launcher
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## License

MIT License - Same as the original ProxyMan project

## Troubleshooting

### Ctrl+C Not Working During Interactive Prompts

**Problem**: When ProxyMan is prompting for input (like proxy host, port, username), pressing Ctrl+C doesn't stop the program immediately.

**Cause**: This was due to input functions not properly handling KeyboardInterrupt signals.

**Solution**: This has been fixed in the latest version. The application now properly handles Ctrl+C during:

- Interactive proxy configuration
- Yes/No prompts
- Password input
- Configuration name input

**If you're still experiencing this issue**:

1. Make sure you're using the latest version
2. Update your installation: `git pull` and `python install.py`
3. As a workaround, you can:
   - Press Ctrl+Z to suspend the process, then `taskkill /f /im python.exe` in another terminal
   - Close the terminal window entirely
   - Use Task Manager to end the Python process

### Common Issues

**Error: "Python not found"**

- Install Python 3.7+ from python.org
- Make sure Python is added to PATH during installation
- Verify with: `python --version`

**Error: "ModuleNotFoundError: No module named 'colorama'"**

- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the correct project directory

**Error: "proxyman is not recognized"**

- The tool is not in your system PATH
- Use `.\proxyman.bat` or `python proxyman.py` instead
- Or run `python install.py` as Administrator to add to PATH

**Error: "Access is denied" or "Permission denied"**

- Run Command Prompt or PowerShell as Administrator
- Some operations (like system proxy, registry changes) require elevated privileges

**Settings not taking effect**

- Some applications may need to be restarted
- System proxy changes are usually immediate
- Environment variables affect new processes only
- Browser settings may require restart

**Git proxy configuration fails**

- Make sure Git is installed and in PATH
- Verify with: `git --version`
- Git proxy configuration will be skipped if Git is not available

### Performance Issues

**Slow startup or operations**

- Check if antivirus is scanning Python processes
- Add ProxyMan directory to antivirus exclusions
- Ensure Python and pip are up to date

**Registry operations taking too long**

- This is normal for first-time registry access
- Subsequent operations should be faster
- Run as Administrator for better performance

### Getting Help

```powershell
# Display help and available commands
proxyman help
# or
.\proxyman.bat help
# or
python proxyman.py help
```

**For additional support**:

- Check the project repository for latest updates
- Report bugs or issues on GitHub
- Review the QUICKSTART.md for detailed usage examples
