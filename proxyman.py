#!/usr/bin/env python3
"""
ProxyMan Windows - Main executable entry point
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main function
from proxyman import main

if __name__ == "__main__":
    main()
