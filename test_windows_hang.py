#!/usr/bin/env python3
"""
Windows-specific test for the unset command hang issue.
Run this script on Windows to test if the fixes work.
"""

import sys
import os
import platform
import time
import threading

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def timeout_test(func, timeout_seconds=15):
    """Run a function with a timeout to detect hangs."""
    result = [None]
    exception = [None]
    completed = [False]
    
    def target():
        try:
            result[0] = func()
            completed[0] = True
        except Exception as e:
            exception[0] = e
            completed[0] = True
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    
    # Wait for completion or timeout
    thread.join(timeout_seconds)
    
    if not completed[0]:
        print(f"❌ HANG DETECTED: Function took longer than {timeout_seconds} seconds")
        print("   This indicates the infinite loop/hang issue is still present")
        return False
    
    if exception[0]:
        print(f"Exception occurred: {exception[0]}")
        return False
    
    print("✅ Function completed successfully within timeout")
    return True

def test_unset_command():
    """Test the unset command directly."""
    print("Testing proxyman unset command...")
    try:
        from proxyman import ProxyManager
        manager = ProxyManager()
        
        # Test with empty list (should not hang)
        print("Testing unset with empty target list...")
        manager.unset_proxy([])
        
        return True
    except Exception as e:
        print(f"Error in unset test: {e}")
        return False

def test_system_proxy_unset():
    """Test system proxy unset directly."""
    print("Testing system proxy unset directly...")
    try:
        from targets import SystemProxyTarget
        target = SystemProxyTarget()
        
        if target.is_available():
            print("System proxy is available, testing unset...")
            result = target.unset_proxy()
            print(f"Unset result: {result}")
        else:
            print("System proxy not available on this system")
        
        return True
    except Exception as e:
        print(f"Error in system proxy test: {e}")
        return False

def test_input_functions():
    """Test input functions with timeout."""
    print("Testing input functions...")
    print("When prompted, just press Enter to use defaults")
    
    try:
        from utils import get_user_input, get_yes_no_input
        
        # Test get_user_input
        result = get_user_input("Test input", "default_value")
        print(f"Input result: '{result}'")
        
        # Test get_yes_no_input  
        result = get_yes_no_input("Test yes/no", True)
        print(f"Yes/no result: {result}")
        
        return True
    except Exception as e:
        print(f"Error in input test: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("PROXYMAN WINDOWS HANG TEST")
    print("=" * 60)
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print()
    
    if platform.system() != "Windows":
        print("⚠️  This test is designed for Windows. Results may not be relevant.")
        print()
    
    tests = [
        ("Input Functions", test_input_functions),
        ("System Proxy Unset", test_system_proxy_unset),
        ("Unset Command", test_unset_command),
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n🧪 TEST: {test_name}")
        print("-" * 40)
        
        if timeout_test(test_func, 15):
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED (hang detected)")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("The hang issue appears to be resolved.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("The hang issue may still be present.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user (Ctrl+C working correctly!)")
    except Exception as e:
        print(f"\nTest script error: {e}")
