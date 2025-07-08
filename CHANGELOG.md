# ProxyMan Windows - Changelog

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
- Configuration files stored in `%USERPROFILE%\.proxyman\`
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

*Based on the original ProxyMan project for Linux by Himanshu Shekhar*
