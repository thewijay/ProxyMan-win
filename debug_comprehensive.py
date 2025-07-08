#!/usr/bin/env python3
"""
Comprehensive debug script to identify the exact cause of the Windows hang.
"""

import sys
import os
import platform
import time
import threading

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_simple_input():
    """Test if basic input() works without hanging."""
    print("Testing basic input()...")
    try:
        result = input("Enter something (basic input): ")
        print(f"Got: {result}")
        return True
    except KeyboardInterrupt:
        print("KeyboardInterrupt in basic input")
        return False
    except Exception as e:
        print(f"Error in basic input: {e}")
        return False

def test_get_user_input():
    """Test our get_user_input function."""
    print("\nTesting get_user_input()...")
    try:
        from utils import get_user_input
        result = get_user_input("Enter something (get_user_input)", "default")
        print(f"Got: {result}")
        return True
    except KeyboardInterrupt:
        print("KeyboardInterrupt in get_user_input")
        return False
    except Exception as e:
        print(f"Error in get_user_input: {e}")
        return False

def test_signal_handling():
    """Test signal handling setup."""
    print("\nTesting signal handling...")
    try:
        from utils import setup_signal_handlers
        setup_signal_handlers()
        print("Signal handlers set up successfully")
        return True
    except Exception as e:
        print(f"Error setting up signal handlers: {e}")
        return False

def test_target_availability():
    """Test target availability."""
    print("\nTesting target availability...")
    try:
        from proxyman import ProxyManager
        manager = ProxyManager()
        
        print("Available targets:")
        for name, target in manager.available_targets.items():
            available = target.is_available()
            print(f"  {name}: {'YES' if available else 'NO'}")
        
        return True
    except Exception as e:
        print(f"Error testing targets: {e}")
        return False

def test_target_selection_step_by_step():
    """Test the target selection process step by step."""
    print("\nTesting target selection step by step...")
    try:
        from proxyman import ProxyManager
        from utils import print_header, print_colored, get_colors, get_user_input
        
        manager = ProxyManager()
        colors = get_colors()
        
        print_header("Select Proxy Targets")
        
        targets = list(manager.available_targets.keys())
        print(f"Targets list: {targets}")
        
        # Show available targets
        print_colored("Available targets:", colors['cyan'])
        print_colored("  0. All targets", colors['white'])
        for i, target in enumerate(targets, 1):
            description = manager.target_descriptions.get(target, target)
            available = "[OK]" if target in manager.available_targets else "[UNAVAILABLE]"
            print_colored(f"  {i}. {available} {target} - {description}", colors['white'])
        
        print("\nAbout to call get_user_input...")
        print("If this hangs, the issue is in get_user_input")
        
        # This is where the hang might occur
        selection = get_user_input("Select targets (comma-separated numbers or 0 for all)", "0")
        print(f"Got selection: '{selection}'")
        
        return True
    except KeyboardInterrupt:
        print("KeyboardInterrupt in target selection")
        return False
    except Exception as e:
        print(f"Error in target selection: {e}")
        return False

def run_with_timeout(func, timeout_seconds=10):
    """Run a function with a timeout."""
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout_seconds)
    
    if thread.is_alive():
        print(f"TIMEOUT: Function took longer than {timeout_seconds} seconds")
        return False
    
    if exception[0]:
        print(f"Exception: {exception[0]}")
        return False
    
    return result[0]

def main():
    """Main debug function."""
    print("=" * 60)
    print("PROXYMAN COMPREHENSIVE DEBUG")
    print("=" * 60)
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print()
    
    # Test 1: Basic input
    print("TEST 1: Basic input() function")
    if not run_with_timeout(test_simple_input, 10):
        print("FAILED: Basic input hangs!")
        return
    
    # Test 2: Signal handling
    print("\nTEST 2: Signal handling setup")
    if not run_with_timeout(test_signal_handling, 5):
        print("FAILED: Signal handling setup hangs!")
        return
    
    # Test 3: get_user_input function
    print("\nTEST 3: get_user_input function")
    if not run_with_timeout(test_get_user_input, 10):
        print("FAILED: get_user_input hangs!")
        return
    
    # Test 4: Target availability
    print("\nTEST 4: Target availability")
    if not run_with_timeout(test_target_availability, 5):
        print("FAILED: Target availability check hangs!")
        return
    
    # Test 5: Target selection
    print("\nTEST 5: Target selection process")
    if not run_with_timeout(test_target_selection_step_by_step, 15):
        print("FAILED: Target selection hangs!")
        return
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDebugging interrupted by user")
    except Exception as e:
        print(f"Debug script error: {e}")
