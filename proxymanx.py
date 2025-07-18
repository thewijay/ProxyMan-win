#!/usr/bin/env python3
"""
ProxyManX Windows - Main executable entry point
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main function
from proxymanx import main

if __name__ == "__main__":
    main()
