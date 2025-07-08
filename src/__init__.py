"""
ProxyMan Windows - Package initialization
"""

__version__ = "1.0.0"
__author__ = "ProxyMan Windows Team"
__description__ = "Windows proxy configuration tool"

from .proxyman import ProxyManager, main
from .config import ConfigManager
from .targets import get_available_targets, get_target_descriptions
from .utils import get_colors, print_colored

__all__ = [
    'ProxyManager',
    'ConfigManager',
    'main',
    'get_available_targets',
    'get_target_descriptions',
    'get_colors',
    'print_colored'
]
