"""
ProxyMan Windows - Proxy Target Handlers
Individual handlers for different proxy targets (System, Git, NPM, etc.)
"""

import os
import subprocess
import platform
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path
from utils import *

# Windows-specific imports
if platform.system() == "Windows":
    import winreg
else:
    # Mock winreg for non-Windows systems (for development/testing)
    class MockWinreg:
        HKEY_CURRENT_USER = None
        KEY_SET_VALUE = None
        KEY_READ = None
        REG_DWORD = None
        REG_SZ = None
        
        @staticmethod
        def OpenKey(*args, **kwargs):
            raise OSError("winreg not available on non-Windows systems")
        
        @staticmethod
        def SetValueEx(*args, **kwargs):
            raise OSError("winreg not available on non-Windows systems")
        
        @staticmethod
        def QueryValueEx(*args, **kwargs):
            raise OSError("winreg not available on non-Windows systems")
        
        @staticmethod
        def CloseKey(*args, **kwargs):
            pass
    
    winreg = MockWinreg()


class ProxyTarget(ABC):
    """Abstract base class for proxy targets."""
    
    @abstractmethod
    def set_proxy(self, config: Dict[str, Any]) -> bool:
        """Set proxy configuration for this target."""
        pass
    
    @abstractmethod
    def unset_proxy(self) -> bool:
        """Unset proxy configuration for this target."""
        pass
    
    @abstractmethod
    def list_proxy(self) -> Optional[Dict[str, Any]]:
        """List current proxy configuration for this target."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this target is available on the system."""
        pass


class SystemProxyTarget(ProxyTarget):
    """Windows system proxy settings via Registry."""
    
    def __init__(self):
        self.colors = get_colors()
        self.reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    
    def is_available(self) -> bool:
        """System proxy is always available on Windows."""
        return True
    
    def set_proxy(self, config: Dict[str, Any]) -> bool:
        """Set system proxy settings."""
        try:
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_SET_VALUE)
            
            # Set proxy enable flag
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            
            # Set proxy server
            proxy_server = f"{config['http_host']}:{config['http_port']}"
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy_server)
            
            # Set proxy override (no_proxy)
            if config.get('no_proxy'):
                winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, config['no_proxy'])
            
            winreg.CloseKey(key)
            
            # Refresh system settings
            self._refresh_system_settings()
            
            print_success("System proxy settings updated")
            return True
            
        except Exception as e:
            print_error(f"Failed to set system proxy: {e}")
            return False
    
    def unset_proxy(self) -> bool:
        """Unset system proxy settings."""
        try:
            # Check if we're on Windows
            if platform.system() != "Windows":
                print_warning("System proxy settings are only available on Windows")
                return True  # Return True to not break the chain
            
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_SET_VALUE)
            
            # Disable proxy
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            
            # Clear proxy server
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "")
            
            # Clear proxy override
            winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "")
            
            winreg.CloseKey(key)
            
            # Refresh system settings
            self._refresh_system_settings()
            
            print_success("System proxy settings cleared")
            return True
            
        except Exception as e:
            print_error(f"Failed to unset system proxy: {e}")
            return False
    
    def list_proxy(self) -> Optional[Dict[str, Any]]:
        """List current system proxy settings."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_READ)
            
            try:
                proxy_enable = winreg.QueryValueEx(key, "ProxyEnable")[0]
                proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
                proxy_override = winreg.QueryValueEx(key, "ProxyOverride")[0]
                
                winreg.CloseKey(key)
                
                if proxy_enable:
                    return {
                        'status': 'Enabled',
                        'server': proxy_server,
                        'override': proxy_override
                    }
                else:
                    return {
                        'status': 'Disabled',
                        'server': proxy_server,
                        'override': proxy_override
                    }
                
            except FileNotFoundError:
                winreg.CloseKey(key)
                return None
            
        except Exception as e:
            print_error(f"Failed to read system proxy settings: {e}")
            return None
    
    def _refresh_system_settings(self) -> None:
        """Refresh system proxy settings."""
        try:
            # Notify system of proxy changes
            import ctypes
            from ctypes import wintypes
            
            user32 = ctypes.windll.user32
            user32.SendMessageW(0xFFFF, 0x1A, 0, "Environment")
            
        except Exception:
            pass  # Ignore errors in refresh


class EnvironmentProxyTarget(ProxyTarget):
    """Environment variables proxy settings."""
    
    def __init__(self):
        self.colors = get_colors()
    
    def is_available(self) -> bool:
        """Environment variables are always available."""
        return True
    
    def set_proxy(self, config: Dict[str, Any]) -> bool:
        """Set environment variable proxy settings."""
        try:
            # Format proxy URLs
            http_proxy = format_proxy_url(
                config['http_host'], config['http_port'],
                config.get('username') if config.get('use_auth') else None,
                config.get('password') if config.get('use_auth') else None
            )
            
            https_proxy = http_proxy  # Use HTTP proxy for HTTPS by default
            if config.get('https_host') and config.get('https_port'):
                https_proxy = format_proxy_url(
                    config['https_host'], config['https_port'],
                    config.get('username') if config.get('use_auth') else None,
                    config.get('password') if config.get('use_auth') else None
                )
            
            # Set environment variables for current process
            env_vars = {
                'HTTP_PROXY': http_proxy,
                'HTTPS_PROXY': https_proxy,
                'http_proxy': http_proxy,
                'https_proxy': https_proxy,
                'NO_PROXY': config.get('no_proxy', ''),
                'no_proxy': config.get('no_proxy', '')
            }
            
            for key, value in env_vars.items():
                os.environ[key] = value
            
            # Set persistent environment variables
            success = self._set_persistent_env_vars(env_vars)
            
            if success:
                print_success("Environment proxy variables set")
                print_info("Note: Restart applications to pick up new environment variables")
            else:
                print_warning("Environment variables set for current session only")
            
            return True
            
        except Exception as e:
            print_error(f"Failed to set environment proxy: {e}")
            return False
    
    def unset_proxy(self) -> bool:
        """Unset environment variable proxy settings."""
        try:
            # Remove from current process
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'no_proxy']
            
            for var in proxy_vars:
                if var in os.environ:
                    del os.environ[var]
            
            # Remove persistent environment variables (Windows only)
            if platform.system() == "Windows":
                success = self._remove_persistent_env_vars(proxy_vars)
                if success:
                    print_success("Environment proxy variables cleared")
                else:
                    print_warning("Environment variables cleared for current session only")
            else:
                print_success("Environment proxy variables cleared (current session)")
            
            return True
            
        except Exception as e:
            print_error(f"Failed to unset environment proxy: {e}")
            return False
    
    def list_proxy(self) -> Optional[Dict[str, Any]]:
        """List current environment proxy settings."""
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY', 'http_proxy', 'https_proxy', 'no_proxy']
        found_vars = {}
        
        for var in proxy_vars:
            value = os.environ.get(var)
            if value:
                found_vars[var] = value
        
        return found_vars if found_vars else None
    
    def _set_persistent_env_vars(self, env_vars: Dict[str, str]) -> bool:
        """Set persistent environment variables via Registry."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
            
            for name, value in env_vars.items():
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
            
            winreg.CloseKey(key)
            return True
            
        except Exception:
            return False
    
    def _remove_persistent_env_vars(self, var_names: List[str]) -> bool:
        """Remove persistent environment variables via Registry."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
            
            for name in var_names:
                try:
                    winreg.DeleteValue(key, name)
                except FileNotFoundError:
                    pass  # Variable doesn't exist
            
            winreg.CloseKey(key)
            return True
            
        except Exception:
            return False


class GitProxyTarget(ProxyTarget):
    """Git proxy settings."""
    
    def __init__(self):
        self.colors = get_colors()
    
    def is_available(self) -> bool:
        """Check if git is available."""
        success, _, _ = run_command("git --version")
        return success
    
    def set_proxy(self, config: Dict[str, Any]) -> bool:
        """Set git proxy settings."""
        try:
            # Format proxy URL
            proxy_url = format_proxy_url(
                config['http_host'], config['http_port'],
                config.get('username') if config.get('use_auth') else None,
                config.get('password') if config.get('use_auth') else None
            )
            
            # Set HTTP proxy
            success1, _, err1 = run_command(f'git config --global http.proxy "{proxy_url}"')
            
            # Set HTTPS proxy
            success2, _, err2 = run_command(f'git config --global https.proxy "{proxy_url}"')
            
            if success1 and success2:
                print_success("Git proxy settings updated")
                return True
            else:
                print_error(f"Failed to set git proxy: {err1} {err2}")
                return False
                
        except Exception as e:
            print_error(f"Failed to set git proxy: {e}")
            return False
    
    def unset_proxy(self) -> bool:
        """Unset git proxy settings."""
        try:
            # Remove HTTP proxy (ignore exit code - config may not exist)
            success1, _, _ = run_command("git config --global --unset http.proxy")
            
            # Remove HTTPS proxy (ignore exit code - config may not exist)
            success2, _, _ = run_command("git config --global --unset https.proxy")
            
            # Git config --unset returns exit code 5 when key doesn't exist, which is normal
            # So we consider it successful regardless of exit code
            print_success("Git proxy settings cleared")
            return True
            
        except Exception as e:
            print_error(f"Failed to unset git proxy: {e}")
            return False
    
    def list_proxy(self) -> Optional[Dict[str, Any]]:
        """List current git proxy settings."""
        settings = {}
        
        # Get HTTP proxy
        success, http_proxy, _ = run_command("git config --global http.proxy")
        if success and http_proxy.strip():
            settings['http'] = http_proxy.strip()
        
        # Get HTTPS proxy
        success, https_proxy, _ = run_command("git config --global https.proxy")
        if success and https_proxy.strip():
            settings['https'] = https_proxy.strip()
        
        return settings if settings else None


class NPMProxyTarget(ProxyTarget):
    """NPM/Yarn proxy settings."""
    
    def __init__(self):
        self.colors = get_colors()
    
    def is_available(self) -> bool:
        """Check if npm is available."""
        success, _, _ = run_command("npm --version")
        return success
    
    def set_proxy(self, config: Dict[str, Any]) -> bool:
        """Set npm proxy settings."""
        try:
            # Format proxy URL
            proxy_url = format_proxy_url(
                config['http_host'], config['http_port'],
                config.get('username') if config.get('use_auth') else None,
                config.get('password') if config.get('use_auth') else None
            )
            
            # Set HTTP proxy
            success1, _, err1 = run_command(f'npm config set proxy "{proxy_url}"')
            
            # Set HTTPS proxy
            success2, _, err2 = run_command(f'npm config set https-proxy "{proxy_url}"')
            
            # Set strict-ssl to false for proxy compatibility
            success3, _, err3 = run_command("npm config set strict-ssl false")
            
            if success1 and success2 and success3:
                print_success("NPM proxy settings updated")
                return True
            else:
                print_error(f"Failed to set npm proxy: {err1} {err2} {err3}")
                return False
                
        except Exception as e:
            print_error(f"Failed to set npm proxy: {e}")
            return False
    
    def unset_proxy(self) -> bool:
        """Unset npm proxy settings."""
        try:
            # Remove proxy settings (ignore exit codes - configs may not exist)
            success1, _, _ = run_command("npm config delete proxy")
            success2, _, _ = run_command("npm config delete https-proxy")
            success3, _, _ = run_command("npm config set strict-ssl true")
            
            # npm config delete returns non-zero when key doesn't exist, which is normal
            # So we consider it successful regardless of individual exit codes
            print_success("NPM proxy settings cleared")
            return True
            
        except Exception as e:
            print_error(f"Failed to unset npm proxy: {e}")
            return False
    
    def list_proxy(self) -> Optional[Dict[str, Any]]:
        """List current npm proxy settings."""
        settings = {}
        
        # Get HTTP proxy
        success, http_proxy, _ = run_command("npm config get proxy")
        if success and http_proxy.strip() and http_proxy.strip() != "null":
            settings['http'] = http_proxy.strip()
        
        # Get HTTPS proxy
        success, https_proxy, _ = run_command("npm config get https-proxy")
        if success and https_proxy.strip() and https_proxy.strip() != "null":
            settings['https'] = https_proxy.strip()
        
        # Get strict-ssl
        success, strict_ssl, _ = run_command("npm config get strict-ssl")
        if success and strict_ssl.strip():
            settings['strict_ssl'] = strict_ssl.strip()
        
        return settings if settings else None


class PowerShellProxyTarget(ProxyTarget):
    """PowerShell proxy settings."""
    
    def __init__(self):
        self.colors = get_colors()
        self.profile_path = self._get_profile_path()
    
    def is_available(self) -> bool:
        """PowerShell is always available on Windows."""
        return True
    
    def _get_profile_path(self) -> Optional[Path]:
        """Get PowerShell profile path."""
        try:
            # Get PowerShell profile path
            success, output, _ = run_command('powershell -Command "$PROFILE"')
            if success and output.strip():
                return Path(output.strip())
        except Exception:
            pass
        
        # Fallback to default location
        return Path.home() / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
    
    def set_proxy(self, config: Dict[str, Any]) -> bool:
        """Set PowerShell proxy settings."""
        try:
            if not self.profile_path:
                print_error("Could not determine PowerShell profile path")
                return False
            
            # Create profile directory if it doesn't exist
            self.profile_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Format proxy URL
            proxy_url = format_proxy_url(
                config['http_host'], config['http_port'],
                config.get('username') if config.get('use_auth') else None,
                config.get('password') if config.get('use_auth') else None
            )
            
            # Remove existing proxy settings
            self._remove_proxy_from_profile()
            
            # Add proxy settings to profile
            proxy_script = f"""
# ProxyMan Windows - Proxy Settings
$env:HTTP_PROXY = "{proxy_url}"
$env:HTTPS_PROXY = "{proxy_url}"
$env:NO_PROXY = "{config.get('no_proxy', '')}"

# Set system proxy for PowerShell web requests
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy("{proxy_url}")
[System.Net.WebRequest]::DefaultWebProxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials
"""
            
            with open(self.profile_path, 'a', encoding='utf-8') as f:
                f.write(proxy_script)
            
            print_success("PowerShell proxy settings updated")
            print_info("Restart PowerShell to apply changes")
            return True
            
        except Exception as e:
            print_error(f"Failed to set PowerShell proxy: {e}")
            return False
    
    def unset_proxy(self) -> bool:
        """Unset PowerShell proxy settings."""
        try:
            self._remove_proxy_from_profile()
            print_success("PowerShell proxy settings cleared")
            return True
            
        except Exception as e:
            print_error(f"Failed to unset PowerShell proxy: {e}")
            return False
    
    def _remove_proxy_from_profile(self) -> None:
        """Remove proxy settings from PowerShell profile."""
        if not self.profile_path.exists():
            return
        
        try:
            # Read current profile
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove proxy settings
            lines = content.split('\n')
            new_lines = []
            skip_lines = False
            
            for line in lines:
                if "# ProxyMan Windows - Proxy Settings" in line:
                    skip_lines = True
                    continue
                elif skip_lines and (line.strip() == "" or line.startswith("#")):
                    continue
                elif skip_lines and not line.startswith(("$env:", "[System.Net.WebRequest]")):
                    skip_lines = False
                    new_lines.append(line)
                elif not skip_lines:
                    new_lines.append(line)
            
            # Write back to profile
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
                
        except Exception as e:
            print_error(f"Failed to clean PowerShell profile: {e}")
    
    def list_proxy(self) -> Optional[Dict[str, Any]]:
        """List current PowerShell proxy settings."""
        if not self.profile_path.exists():
            return None
        
        try:
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "ProxyMan Windows - Proxy Settings" in content:
                return {
                    'status': 'Configured',
                    'profile_path': str(self.profile_path)
                }
            else:
                return None
                
        except Exception as e:
            print_error(f"Failed to read PowerShell profile: {e}")
            return None


# Registry of all available proxy targets
PROXY_TARGETS = {
    'system': SystemProxyTarget,
    'environment': EnvironmentProxyTarget,
    'git': GitProxyTarget,
    'npm': NPMProxyTarget,
    'powershell': PowerShellProxyTarget
}


def get_available_targets() -> Dict[str, ProxyTarget]:
    """Get all available proxy targets on the system."""
    available = {}
    
    for name, target_class in PROXY_TARGETS.items():
        target = target_class()
        if target.is_available():
            available[name] = target
    
    return available


def get_target_descriptions() -> Dict[str, str]:
    """Get descriptions for all proxy targets."""
    return {
        'system': 'Windows system proxy settings (Registry)',
        'environment': 'Environment variables (HTTP_PROXY, HTTPS_PROXY)',
        'git': 'Git global proxy configuration',
        'npm': 'NPM/Yarn proxy settings',
        'powershell': 'PowerShell profile proxy settings'
    }
