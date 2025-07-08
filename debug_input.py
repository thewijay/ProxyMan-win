#!/usr/bin/env python3
"""
Debug script to test input handling specifically.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils import get_user_input, get_yes_no_input, print_colored, get_colors
    
    def test_input_handling():
        """Test input handling to see if there are any issues."""
        colors = get_colors()
        
        print_colored("Testing input handling...", colors['cyan'])
        
        # Test 1: Normal input with default
        print_colored("\nTest 1: Normal input with default", colors['yellow'])
        try:
            result = get_user_input("Enter something", "default_value")
            print_colored(f"Result: '{result}'", colors['green'])
        except Exception as e:
            print_colored(f"Error: {e}", colors['red'])
        
        # Test 2: Yes/No input
        print_colored("\nTest 2: Yes/No input", colors['yellow'])
        try:
            result = get_yes_no_input("Continue?", default=True)
            print_colored(f"Result: {result}", colors['green'])
        except Exception as e:
            print_colored(f"Error: {e}", colors['red'])
        
        print_colored("\nInput handling test completed", colors['green'])
    
    if __name__ == "__main__":
        test_input_handling()
        
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
