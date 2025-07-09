#!/usr/bin/env python3
"""
ProxyManX Windows Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from src/__init__.py
def get_version():
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from src import __version__
    return __version__

setup(
    name="proxymanx",
    version=get_version(),
    author="Pubudu Wijesundara",
    author_email="",  # Add your email if desired
    description="Comprehensive Windows proxy configuration tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thewijay/ProxyManX-win",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama>=0.4.4",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "proxymanx=src.proxymanx:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="proxy windows configuration network system administration",
    project_urls={
        "Bug Reports": "https://github.com/thewijay/ProxyManX-win/issues",
        "Source": "https://github.com/thewijay/ProxyManX-win",
        "Documentation": "https://github.com/thewijay/ProxyManX-win/blob/main/README.md",
    },
)
