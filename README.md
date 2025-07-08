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

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the installer:
   ```bash
   python install.py
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
