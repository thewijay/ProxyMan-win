# ProxyManX Windows - Changelog

## v2.0.0 - ProxyManX Release (Professional Version)

### Major Changes

- 🎯 **Rebranded to ProxyManX** - Professional version with enhanced branding
- 📁 **Updated file structure** - All executables renamed to `proxymanx.*`
- 🔧 **Updated commands** - All CLI commands now use `proxymanx` instead of `proxyman`
- 📂 **New config directory** - Configuration files now stored in `%USERPROFILE%\.proxymanx\`
- 🔗 **Updated repository** - New repository structure for ProxyManX branding

### Breaking Changes

- Command name changed from `proxyman` to `proxymanx`
- Batch file renamed from `proxyman.bat` to `proxymanx.bat`
- Main executable renamed from `proxyman.py` to `proxymanx.py`
- Configuration directory moved from `.proxyman` to `.proxymanx`

### Migration Guide

- Existing installations should be uninstalled before upgrading
- Configuration files will need to be recreated or migrated manually
- Update any scripts or shortcuts to use the new `proxymanx` command

## v1.0.0 - Initial Release

### Features

- ✅ **System-wide proxy configuration** for Windows
- ✅ **Interactive CLI** with colorized output
- ✅ **Profile management** - save, load, and delete configurations
- ✅ **Multiple target support**:
  - Windows system proxy settings (Registry)
  - Environment variables
  - Git configuration
  - NPM/Yarn configuration
  - PowerShell profile
- ✅ **Authentication support** for proxy servers
- ✅ **Batch operations** on multiple targets
- ✅ **Cross-platform compatibility** (Windows 10/11)

### Supported Targets

1. **System Proxy** - Windows system proxy settings via Registry
2. **Environment Variables** - User environment variables (HTTP_PROXY, HTTPS_PROXY)
3. **Git** - Global git proxy configuration
4. **NPM** - NPM/Yarn proxy settings
5. **PowerShell** - PowerShell profile proxy settings

### Technical Details

- Built with Python 3.7+
- Uses Windows Registry for system proxy settings
- Colorized terminal output with colorama
- Configuration files stored in `%USERPROFILE%\.proxymanx\`
- Automatic detection of available tools (git, npm, etc.)

### Installation

- Simple installation script (`install.py`)
- Automatic dependency installation
- Optional PATH configuration
- Batch file for easy execution

### Known Limitations

- Some operations require administrator privileges
- Registry changes may require system restart for some applications
- PowerShell profile changes require restarting PowerShell

### Future Enhancements

- Support for additional targets (Docker, Chrome, Firefox)
- GUI interface
- Automatic proxy detection
- Import/export configurations
- Proxy testing and validation

---

_Based on the original ProxyMan project for Linux by Himanshu Shekhar_
