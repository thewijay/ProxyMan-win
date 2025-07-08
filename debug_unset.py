#!/usr/bin/env python3
"""
Debug script to test the unset command and identify hang issues.
This script will help diagnose where exactly the hang is occurring.
"""

import sys
import os
import platform
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from proxyman import ProxyManager
    from utils import print_colored, get_colors, setup_signal_handlers
    
    def debug_unset():
        """Debug the unset command step by step."""
        colors = get_colors()
        
        print_colored("=" * 60, colors['cyan'])
        print_colored("PROXYMAN DEBUG - UNSET COMMAND", colors['bold'] + colors['cyan'])
        print_colored("=" * 60, colors['cyan'])
        
        print_colored(f"Platform: {platform.system()}", colors['white'])
        print_colored(f"Python: {sys.version}", colors['white'])
        print_colored(f"Script location: {__file__}", colors['white'])
        print_colored(f"Working directory: {os.getcwd()}", colors['white'])
        
        print_colored("\n1. Setting up signal handlers...", colors['yellow'])
        setup_signal_handlers()
        print_colored("   Signal handlers set up successfully", colors['green'])
        
        print_colored("\n2. Creating ProxyManager...", colors['yellow'])
        manager = ProxyManager()
        print_colored("   ProxyManager created successfully", colors['green'])
        
        print_colored("\n3. Checking available targets...", colors['yellow'])
        for target_name, target in manager.available_targets.items():
            is_available = target.is_available()
            status = "AVAILABLE" if is_available else "NOT AVAILABLE"
            print_colored(f"   {target_name}: {status}", colors['white'])
        
        print_colored("\n4. Starting unset process...", colors['yellow'])
        print_colored("   This is where the hang might occur...", colors['yellow'])
        
        # Add a timeout mechanism
        import signal
        
        def timeout_handler(signum, frame):
            print_colored("\n\nTIMEOUT: Operation took too long (>30 seconds)", colors['red'])
            print_colored("This indicates the hang is happening in the unset process", colors['red'])
            sys.exit(1)
        
        # Set a 30-second timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        try:
            print_colored("\n   Calling manager.unset_proxy()...", colors['yellow'])
            manager.unset_proxy()
            print_colored("\n   Unset completed successfully!", colors['green'])
        except KeyboardInterrupt:
            print_colored("\n   KeyboardInterrupt caught properly", colors['yellow'])
        except Exception as e:
            print_colored(f"\n   Exception occurred: {e}", colors['red'])
        finally:
            signal.alarm(0)  # Cancel the timeout
        
        print_colored("\n5. Debug completed", colors['green'])
    
    if __name__ == "__main__":
        debug_unset()
        
except ImportError as e:
    print(f"Failed to import modules: {e}")
    print("Make sure you're running this from the ProxyMan root directory")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
