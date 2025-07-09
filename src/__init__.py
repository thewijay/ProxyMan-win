"""
ProxyManX Windows - Package initialization
"""

__version__ = "1.0.0"
__author__ = "Pubudu Wijesundara"
__description__ = "Comprehensive Windows proxy configuration tool"

from .proxymanx import ProxyManX, main
from .config import ConfigManager
from .targets import get_available_targets, get_target_descriptions
from .utils import get_colors, print_colored

__all__ = [
    'ProxyManX',
    'ConfigManager',
    'main',
    'get_available_targets',
    'get_target_descriptions',
    'get_colors',
    'print_colored'
]
