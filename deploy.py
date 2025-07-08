#!/usr/bin/env python3
"""
ProxyMan Windows - Deployment Script
Creates a deployable package for distribution
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_package():
    """Create a deployable package."""
    print("Creating ProxyMan Windows deployment package...")
    
    # Define directories
    source_dir = Path(".")
    package_dir = Path("dist/ProxyMan-Windows")
    
    # Clean previous builds
    if package_dir.parent.exists():
        shutil.rmtree(package_dir.parent)
    
    # Create package directory
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to include in package
    files_to_copy = [
        "src/",
        "proxyman.py",
        "proxyman.bat",
        "requirements.txt",
        "install.py",
        "install.ps1",
        "install-simple.ps1",
        "uninstall.py",
        "uninstall.ps1",
        "README.md",
        "QUICKSTART.md",
        "CHANGELOG.md",
        "LICENSE"
    ]
    
    # Copy files
    for item in files_to_copy:
        source = source_dir / item
        dest = package_dir / item
        
        if source.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            print(f"Copied: {item}")
        elif source.is_dir():
            shutil.copytree(source, dest)
            print(f"Copied directory: {item}")
    
    # Create ZIP package
    zip_path = package_dir.parent / "ProxyMan-Windows.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"\nPackage created successfully:")
    print(f"  Directory: {package_dir}")
    print(f"  Archive: {zip_path}")
    print(f"  Size: {zip_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    create_package()
