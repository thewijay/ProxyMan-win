"""
ProxyMan Windows - Installation Script
Install ProxyMan Windows to system PATH
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


def install_dependencies():
    """Install Python dependencies"""
    print_colored("📦 Installing dependencies...", 'blue')
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print_colored("✅ Dependencies installed successfully", 'green')
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Failed to install dependencies: {e}", 'red')
        return False


def create_batch_file():
    """Create batch file for easy execution"""
    batch_content = f"""@echo off
cd /d "{os.path.dirname(os.path.abspath(__file__))}"
python proxyman.py %*
"""
    
    try:
        with open('proxyman.bat', 'w') as f:
            f.write(batch_content)
        print_colored("✅ Created proxyman.bat", 'green')
        return True
    except Exception as e:
        print_colored(f"❌ Failed to create batch file: {e}", 'red')
        return False


def add_to_path():
    """Add current directory to PATH"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not is_admin():
        print_colored("⚠️  Administrator privileges required to add to system PATH", 'yellow')
        print_colored("You can still run ProxyMan using:", 'cyan')
        print_colored(f"  python {os.path.join(current_dir, 'proxyman.py')}", 'white')
        print_colored(f"  or {os.path.join(current_dir, 'proxyman.bat')}", 'white')
        return False
    
    try:
        # Add to user PATH
        import winreg
        
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
            print_colored("✅ Added to PATH", 'green')
        else:
            print_colored("✅ Already in PATH", 'green')
        
        winreg.CloseKey(key)
        
        # Notify system of PATH change
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        user32.SendMessageW(0xFFFF, 0x1A, 0, "Environment")
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Failed to add to PATH: {e}", 'red')
        return False


def main():
    """Main installation function"""
    print_colored("🚀 ProxyMan Windows Installer", 'cyan')
    print_colored("=" * 40, 'cyan')
    
    # Check Python version
    if sys.version_info < (3, 7):
        print_colored("❌ Python 3.7 or higher is required", 'red')
        return False
    
    print_colored(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected", 'green')
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create batch file
    if not create_batch_file():
        return False
    
    # Add to PATH
    add_to_path()
    
    print_colored("\n🎉 Installation completed!", 'green')
    print_colored("You can now use ProxyMan with:", 'cyan')
    print_colored("  proxyman help", 'white')
    print_colored("  proxyman set", 'white')
    print_colored("  proxyman list", 'white')
    
    if not is_admin():
        print_colored("\n⚠️  Note: Run as administrator for full functionality", 'yellow')
    
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
        print_colored(f"\n❌ Installation failed: {e}", 'red')
        sys.exit(1)
