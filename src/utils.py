"""
ProxyMan Windows - Utility Functions
Common utilities and helper functions used across the application.
"""

import os
import sys
import subprocess
import ctypes
import signal
from typing import Dict, Any
from colorama import init, Fore, Back, Style

# Initialize colorama for Windows
init(autoreset=True)


def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        print_colored("\n\nOperation interrupted by user", get_colors()['yellow'])
        # Use sys.exit instead of os._exit to allow cleanup
        sys.exit(0)
    
    try:
        # On Windows, be more conservative with signal handling
        # as it can interfere with input() function
        if os.name == 'nt':  # Windows
            # Only handle SIGINT (Ctrl+C) on Windows
            signal.signal(signal.SIGINT, signal_handler)
        else:
            # On non-Windows systems, handle more signals
            signal.signal(signal.SIGINT, signal_handler)
            if hasattr(signal, 'SIGTERM'):
                signal.signal(signal.SIGTERM, signal_handler)
    except Exception:
        # If signal setup fails, continue without it
        pass


def get_colors() -> Dict[str, str]:
    """Get color codes for terminal output."""
    return {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'bold': Style.BRIGHT,
        'reset': Style.RESET_ALL
    }


def print_colored(text: str, color: str = None) -> None:
    """Print colored text to console."""
    if color:
        print(f"{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def is_admin() -> bool:
    """Check if the current process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin(func):
    """Decorator to run a function with administrator privileges."""
    def wrapper(*args, **kwargs):
        if not is_admin():
            print_colored("⚠️  This operation requires administrator privileges", get_colors()['yellow'])
            print_colored("Please run as administrator or some operations may fail", get_colors()['yellow'])
        return func(*args, **kwargs)
    return wrapper


def get_default_no_proxy() -> str:
    """Get default no_proxy list for Windows."""
    return "localhost,127.0.0.1,::1,*.local,10.*,192.168.*,172.16.*,172.17.*,172.18.*,172.19.*,172.20.*,172.21.*,172.22.*,172.23.*,172.24.*,172.25.*,172.26.*,172.27.*,172.28.*,172.29.*,172.30.*,172.31.*"


def validate_proxy_config(config: Dict[str, Any]) -> bool:
    """Validate proxy configuration."""
    required_fields = ['http_host', 'http_port']
    
    for field in required_fields:
        if not config.get(field):
            print_colored(f"❌ Missing required field: {field}", get_colors()['red'])
            return False
    
    # Validate ports
    for port_field in ['http_port', 'https_port', 'ftp_port']:
        port = config.get(port_field)
        if port and not isinstance(port, int):
            try:
                config[port_field] = int(port)
            except ValueError:
                print_colored(f"❌ Invalid port number: {port}", get_colors()['red'])
                return False
        
        if port and (port < 1 or port > 65535):
            print_colored(f"❌ Port number out of range: {port}", get_colors()['red'])
            return False
    
    return True


def format_proxy_url(host: str, port: int, username: str = None, password: str = None, protocol: str = 'http') -> str:
    """Format proxy URL with authentication if provided."""
    if username and password:
        return f"{protocol}://{username}:{password}@{host}:{port}"
    return f"{protocol}://{host}:{port}"


def run_command(cmd: str, shell: bool = True) -> tuple:
    """Run a system command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except KeyboardInterrupt:
        print_colored("\n\nCommand interrupted by user", get_colors()['yellow'])
        raise KeyboardInterrupt
    except Exception as e:
        return False, "", str(e)


def get_user_input(prompt: str, default: str = None, password: bool = False) -> str:
    """Get user input with optional default value."""
    if default:
        display_prompt = f"{prompt} [{default}]: "
    else:
        display_prompt = f"{prompt}: "
    
    try:
        if password:
            import getpass
            result = getpass.getpass(display_prompt)
        else:
            # Flush all output streams
            sys.stdout.flush()
            sys.stderr.flush()
            
            # Use a timeout-based approach on Windows to prevent hanging
            if os.name == 'nt':  # Windows
                # Try using threading with timeout to prevent infinite hang
                import threading
                import queue
                
                input_queue = queue.Queue()
                
                def get_input():
                    try:
                        result = input(display_prompt)
                        input_queue.put(result)
                    except Exception as e:
                        input_queue.put(f"ERROR:{e}")
                
                input_thread = threading.Thread(target=get_input, daemon=True)
                input_thread.start()
                
                try:
                    # Wait for input with a reasonable timeout
                    result = input_queue.get(timeout=30)
                    if result.startswith("ERROR:"):
                        raise Exception(result[6:])
                    result = result.strip()
                except queue.Empty:
                    print_colored("\n\nInput timeout - using default value", get_colors()['yellow'])
                    result = ""
            else:
                # On non-Windows, use normal input
                result = input(display_prompt).strip()
        
        return result if result else (default or '')
    except KeyboardInterrupt:
        print_colored("\n\nOperation cancelled by user", get_colors()['yellow'])
        sys.exit(1)
    except EOFError:
        print_colored("\n\nInput terminated", get_colors()['yellow'])
        return default or ''
    except Exception as e:
        print_colored(f"\n\nInput error: {e}", get_colors()['red'])
        return default or ''


def get_yes_no_input(prompt: str, default: bool = False) -> bool:
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    
    try:
        # Use the same timeout approach as get_user_input
        full_prompt = f"{prompt} [{default_str}]: "
        
        if os.name == 'nt':  # Windows
            import threading
            import queue
            
            input_queue = queue.Queue()
            
            def get_input():
                try:
                    sys.stdout.flush()
                    sys.stderr.flush()
                    result = input(full_prompt)
                    input_queue.put(result)
                except Exception as e:
                    input_queue.put(f"ERROR:{e}")
            
            input_thread = threading.Thread(target=get_input, daemon=True)
            input_thread.start()
            
            try:
                result = input_queue.get(timeout=30)
                if result.startswith("ERROR:"):
                    raise Exception(result[6:])
                response = result.strip().lower()
            except queue.Empty:
                print_colored("\n\nInput timeout - using default value", get_colors()['yellow'])
                response = ""
        else:
            # On non-Windows, use normal input
            sys.stdout.flush()
            sys.stderr.flush()
            response = input(full_prompt).strip().lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes', '1', 'true']
    except KeyboardInterrupt:
        print_colored("\n\nOperation cancelled by user", get_colors()['yellow'])
        sys.exit(1)
    except EOFError:
        print_colored("\n\nInput terminated", get_colors()['yellow'])
        return default
    except Exception as e:
        print_colored(f"\n\nInput error: {e}", get_colors()['red'])
        return default


def print_separator(char: str = '-', length: int = 60) -> None:
    """Print a separator line."""
    print(char * length)


def print_header(title: str) -> None:
    """Print a formatted header."""
    colors = get_colors()
    print_separator('=')
    print_colored(f"  {title}", colors['bold'] + colors['cyan'])
    print_separator('=')


def print_success(message: str) -> None:
    """Print a success message."""
    print_colored(f"✅ {message}", get_colors()['green'])


def print_error(message: str) -> None:
    """Print an error message."""
    print_colored(f"❌ {message}", get_colors()['red'])


def print_warning(message: str) -> None:
    """Print a warning message."""
    print_colored(f"⚠️  {message}", get_colors()['yellow'])


def print_info(message: str) -> None:
    """Print an info message."""
    print_colored(f"ℹ️  {message}", get_colors()['blue'])
