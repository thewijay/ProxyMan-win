#!/usr/bin/env python3
"""
ProxyManX Windows - Uninstaller Script
Remove ProxyManX Windows from the system
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def print_colored(text, color=None):
    """Print colored text (simple version without colorama)"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    
    if color and color in colors:
        print(f"{colors[color]}{text}{colors['reset']}")
    else:
        print(text)


def is_admin():
    """Check if running as administrator"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def remove_from_path():
    """Remove ProxyManX directory from PATH"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        import winreg
        
        # Remove from user PATH
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
        
        try:
            current_path = winreg.QueryValueEx(key, "PATH")[0]
            
            # Remove current directory from PATH
            path_entries = current_path.split(';')
            new_path_entries = [entry for entry in path_entries if entry != current_dir]
            new_path = ';'.join(new_path_entries)
            
            if new_path != current_path:
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                print_colored("Removed from user PATH", 'green')
            else:
                print_colored("Not found in user PATH", 'blue')
            
        except FileNotFoundError:
            print_colored("PATH variable not found", 'blue')
        
        winreg.CloseKey(key)
        
        # Notify system of PATH change
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        user32.SendMessageW(0xFFFF, 0x1A, 0, "Environment")
        
        return True
        
    except Exception as e:
        print_colored(f"Could not remove from PATH: {e}", 'yellow')
        return False


def remove_config_files():
    """Remove configuration files"""
    config_dir = Path.home() / '.proxymanx'
    
    if config_dir.exists():
        try:
            shutil.rmtree(config_dir)
            print_colored(f"Removed configuration directory: {config_dir}", 'green')
            return True
        except Exception as e:
            print_colored(f"Failed to remove config directory: {e}", 'red')
            return False
    else:
        print_colored("No configuration directory found", 'blue')
        return True


def remove_desktop_shortcut():
    """Remove desktop shortcut if it exists"""
    desktop_shortcut = Path.home() / "Desktop" / "ProxyManX.lnk"
    
    if desktop_shortcut.exists():
        try:
            desktop_shortcut.unlink()
            print_colored("Removed desktop shortcut", 'green')
            return True
        except Exception as e:
            print_colored(f"Could not remove desktop shortcut: {e}", 'yellow')
            return False
    else:
        print_colored("No desktop shortcut found", 'blue')
        return True


def remove_batch_file():
    """Remove the batch file"""
    batch_file = Path("proxymanx.bat")
    
    if batch_file.exists():
        try:
            batch_file.unlink()
            print_colored("Removed proxymanx.bat", 'green')
            return True
        except Exception as e:
            print_colored(f"Failed to remove batch file: {e}", 'red')
            return False
    else:
        print_colored("No batch file found", 'blue')
        return True


def clear_proxy_settings():
    """Clear all proxy settings non-interactively"""
    print_colored("\nProxy Settings Cleanup", 'cyan')
    
    try:
        # Try to run ProxyManX unset command with 'all' parameter to bypass interactive mode
        if Path("proxymanx.py").exists():
            print_colored("Clearing proxy settings...", 'blue')
            result = subprocess.run([sys.executable, "proxymanx.py", "unset", "all"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print_colored("Proxy settings cleared", 'green')
            else:
                print_colored("Some proxy settings may not have been cleared", 'yellow')
                if result.stderr:
                    print_colored(f"Error: {result.stderr.strip()}", 'yellow')
        else:
            print_colored("ProxyManX not found, cannot clear proxy settings", 'yellow')
            print_colored("You may need to manually clear proxy settings", 'yellow')
    except subprocess.TimeoutExpired:
        print_colored("Timeout while clearing proxy settings", 'yellow')
    except Exception as e:
        print_colored(f"Error clearing proxy settings: {e}", 'yellow')


def main():
    """Main uninstallation function"""
    print_colored("ProxyManX Windows Uninstaller", 'cyan')
    print_colored("=" * 40, 'cyan')
    
    # Confirm uninstallation
    print_colored("\nThis will remove ProxyManX Windows from your system.", 'yellow')
    print_colored("The following will be removed:", 'white')
    print_colored("  • ProxyManX executable and files", 'white')
    print_colored("  • Configuration files and saved profiles", 'white')
    print_colored("  • PATH environment variable entries", 'white')
    print_colored("  • Desktop shortcuts", 'white')
    
    try:
        response = input("\nDo you want to continue? (y/N): ").strip().lower()
    except KeyboardInterrupt:
        print_colored("\n\nOperation cancelled by user", 'yellow')
        return
    except EOFError:
        print_colored("\n\nInput terminated", 'yellow')
        return
    
    if response not in ['y', 'yes']:
        print_colored("Uninstallation cancelled.", 'yellow')
        return
    
    print_colored("\nStarting uninstallation...", 'blue')
    
    # Clear proxy settings first (optional)
    clear_proxy_settings()
    
    # Remove from PATH
    print_colored("\nRemoving from PATH...", 'blue')
    remove_from_path()
    
    # Remove configuration files
    print_colored("\nRemoving configuration files...", 'blue')
    remove_config_files()
    
    # Remove desktop shortcut
    print_colored("\nRemoving shortcuts...", 'blue')
    remove_desktop_shortcut()
    
    # Remove batch file
    print_colored("\nRemoving batch file...", 'blue')
    remove_batch_file()
    
    print_colored("\nUninstallation completed!", 'green')
    print_colored("ProxyManX Windows has been removed from your system.", 'green')
    
    print_colored("\n📋 Manual cleanup (if needed):", 'cyan')
    print_colored("  • Check Windows proxy settings in Internet Options", 'white')
    print_colored("  • Verify git proxy settings: git config --global -l", 'white')
    print_colored("  • Check npm proxy settings: npm config list", 'white')
    print_colored("  • Review PowerShell profile for proxy settings", 'white')
    
    if not is_admin():
        print_colored("\nNote: Some PATH changes may require administrator privileges", 'yellow')
    
    print_colored("\nThank you for using ProxyManX Windows!", 'green')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\nUninstallation cancelled by user", 'yellow')
        sys.exit(1)
    except Exception as e:
        print_colored(f"\nUninstallation failed: {e}", 'red')
        sys.exit(1)
