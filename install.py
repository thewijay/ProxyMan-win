"""
ProxyManX Windows - Installation Script
Install ProxyManX Windows to system PATH
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


def print_header():
    """Print professional installation header"""
    print()
    print_colored("╔" + "═" * 50 + "╗", 'cyan')
    print_colored("║" + " " * 12 + "ProxyManX Windows Installer" + " " * 11 + "║", 'cyan')
    print_colored("║" + " " * 12 + "Professional Proxy Management" + " " * 9 + "║", 'cyan')
    print_colored("╚" + "═" * 50 + "╝", 'cyan')
    print()


def print_section(title):
    """Print section header"""
    print()
    print_colored(f"▶ {title}", 'blue')
    print_colored("─" * (len(title) + 2), 'blue')


def print_success(message):
    """Print success message with checkmark"""
    print_colored(f"  ✓ {message}", 'green')


def print_error(message):
    """Print error message with X mark"""
    print_colored(f"  ✗ {message}", 'red')


def print_info(message):
    """Print info message with bullet"""
    print_colored(f"  • {message}", 'white')


def install_dependencies():
    """Install Python dependencies"""
    print_section("Installing Dependencies")
    
    try:
        print_info("Checking and installing required packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print_success("All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False


def create_batch_file():
    """Create batch file for easy execution"""
    print_section("Creating Launcher")
    
    batch_content = f"""@echo off
cd /d "%~dp0"
python proxymanx.py %*
"""
    
    try:
        with open('proxymanx.bat', 'w') as f:
            f.write(batch_content)
        print_success("Created proxymanx.bat launcher")
        return True
    except Exception as e:
        print_error(f"Failed to create batch file: {e}")
        return False


def add_to_path():
    """Add current directory to PATH"""
    print_section("Configuring System PATH")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if we're on Windows
    if os.name != 'nt':
        print_error("PATH modification only supported on Windows")
        print_info("You can still run ProxyManX using:")
        print_info(f"python {os.path.join(current_dir, 'proxymanx.py')}")
        print_info(f"{os.path.join(current_dir, 'proxymanx.bat')}")
        return False
    
    try:
        # Try to add to user PATH first (no admin required)
        import winreg
        
        print_info(f"Adding directory to PATH: {current_dir}")
        
        # Open the registry key for user environment variables
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
        
        # Get current PATH
        try:
            current_path = winreg.QueryValueEx(key, "PATH")[0]
        except FileNotFoundError:
            current_path = ""
        
        # Add current directory to PATH if not already present
        if current_dir not in current_path:
            new_path = f"{current_path};{current_dir}" if current_path else current_dir
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
            print_success("Added to user PATH")
        else:
            print_success("Already in user PATH")
        
        winreg.CloseKey(key)
        
        # Notify system of PATH change (with timeout to prevent hanging)
        try:
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32
            # Use a timeout to prevent hanging
            import threading
            
            def notify_system():
                try:
                    user32.SendMessageW(0xFFFF, 0x1A, 0, "Environment")
                except:
                    pass  # Ignore any errors from the notification
            
            # Run notification in a separate thread with timeout
            thread = threading.Thread(target=notify_system)
            thread.daemon = True
            thread.start()
            thread.join(timeout=2.0)  # 2 second timeout
        except:
            pass  # Ignore any errors with the notification system
        
        return True
        
    except ImportError:
        print_colored("winreg module not available (Windows only)", 'red')
        print_colored("You can still run ProxyManX using:", 'cyan')
        print_colored(f"  python {os.path.join(current_dir, 'proxymanx.py')}", 'white')
        print_colored(f"  or {os.path.join(current_dir, 'proxymanx.bat')}", 'white')
        return False
        
    except Exception as e:
        print_colored(f"Failed to add to user PATH: {e}", 'red')
        
        # If we have admin privileges, try system PATH as fallback
        if is_admin():
            try:
                print_colored("Trying system PATH...", 'blue')
                # Add to system PATH
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                   "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", 
                                   0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
                
                try:
                    current_path = winreg.QueryValueEx(key, "PATH")[0]
                except FileNotFoundError:
                    current_path = ""
                
                if current_dir not in current_path:
                    new_path = f"{current_path};{current_dir}" if current_path else current_dir
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    print_colored("Added to system PATH", 'green')
                else:
                    print_colored("Already in system PATH", 'green')
                
                winreg.CloseKey(key)
                
                # Notify system of PATH change (with timeout to prevent hanging)
                try:
                    def notify_system():
                        try:
                            user32.SendMessageW(0xFFFF, 0x1A, 0, "Environment")
                        except:
                            pass
                    
                    thread = threading.Thread(target=notify_system)
                    thread.daemon = True
                    thread.start()
                    thread.join(timeout=2.0)
                except:
                    pass
                
                return True
                
            except Exception as e2:
                print_colored(f"Failed to add to system PATH: {e2}", 'red')
        
        # If all fails, provide manual instructions
        print_colored("Could not automatically add to PATH", 'yellow')
        print_colored("You can still run ProxyManX using:", 'cyan')
        print_colored(f"  python {os.path.join(current_dir, 'proxymanx.py')}", 'white')
        print_colored(f"  or {os.path.join(current_dir, 'proxymanx.bat')}", 'white')
        return False


def main():
    """Main installation function"""
    print_header()
    
    # Check Python version
    print_section("System Requirements Check")
    if sys.version_info < (3, 7):
        print_error("Python 3.7 or higher is required")
        print_info(f"Current version: {sys.version_info.major}.{sys.version_info.minor}")
        return False
    
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create batch file
    if not create_batch_file():
        return False
    
    # Add to PATH
    path_success = add_to_path()
    
    # Final success message
    print()
    print_colored("╔" + "═" * 50 + "╗", 'green')
    print_colored("║" + " " * 15 + "Installation Completed!" + " " * 14 + "║", 'green')
    print_colored("╚" + "═" * 50 + "╝", 'green')
    print()
    
    if path_success:
        print_colored("ProxyManX is ready to use!", 'cyan')
        print()
        print_colored("Available commands:", 'white')
        print_info("proxymanx help     - Show all available commands")
        print_info("proxymanx set      - Configure proxy settings")
        print_info("proxymanx list     - Show current proxy status")
        print_info("proxymanx save     - Save current configuration")
        print()
        print_colored("If 'proxymanx' command is not recognized:", 'yellow')
        print_info("Close and reopen your terminal/PowerShell")
        print_info("Or run: .\\refresh_path.bat to refresh PATH")
        print_info("Or use: .\\proxymanx.bat as a temporary workaround")
    else:
        print_colored("Manual Usage Instructions:", 'cyan')
        print()
        print_info("python proxymanx.py help")
        print_info(".\\proxymanx.bat help")
        print()
        print_colored("To add to PATH manually:", 'yellow')
        print_info("1. Open Environment Variables in System Properties")
        print_info(f"2. Add this path to your user PATH:")
        print_colored(f"   {os.path.dirname(os.path.abspath(__file__))}", 'white')
    
    print()
    if not is_admin():
        print_colored("Tip: Run as administrator for enhanced functionality", 'yellow')
    
    print_colored("Thank you for installing ProxyManX!", 'cyan')
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print_colored("\n\nInstallation cancelled by user", 'yellow')
        sys.exit(1)
    except Exception as e:
        print_colored(f"\nInstallation failed: {e}", 'red')
        sys.exit(1)
