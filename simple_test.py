#!/usr/bin/env python3
"""
Simple test to reproduce the Windows hang issue.
Run this with: python simple_test.py
Then try Ctrl+C to see if it works.
"""

import sys
import signal

def signal_handler(signum, frame):
    print("\nCtrl+C detected, exiting...")
    sys.exit(0)

def main():
    print("Setting up signal handler...")
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Testing input with signal handling...")
    print("Try pressing Ctrl+C during input to test if it works.")
    
    try:
        result = input("Enter something (or press Ctrl+C): ")
        print(f"You entered: {result}")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt caught in except block")
    except EOFError:
        print("\nEOFError caught")
    
    print("Test completed")

if __name__ == "__main__":
    main()
