"""
ProxyManX Windows - Configuration Management Module
Handles saving, loading, and managing proxy configuration profiles.
"""

import os
import json
import configparser
from pathlib import Path
from typing import Dict, List, Optional, Any
from utils import get_colors, print_colored


class ConfigManager:
    """Manages proxy configuration profiles."""
    
    def __init__(self):
        self.colors = get_colors()
        self.config_dir = Path.home() / '.proxymanx'
        self.config_dir.mkdir(exist_ok=True)
        self.default_config = 'default'
    
    def list_configs(self) -> List[str]:
        """List all available configuration profiles."""
        configs = []
        if self.config_dir.exists():
            for file in self.config_dir.glob('*.ini'):
                configs.append(file.stem)
            for file in self.config_dir.glob('*.json'):
                configs.append(file.stem)
        return sorted(configs)
    
    def save_config(self, name: str, config: Dict[str, Any]) -> bool:
        """Save a configuration profile."""
        try:
            config_file = self.config_dir / f'{name}.ini'
            
            # Create ConfigParser instance
            parser = configparser.ConfigParser()
            
            # Add proxy settings section
            parser.add_section('proxy')
            parser.set('proxy', 'http_host', config.get('http_host', ''))
            parser.set('proxy', 'http_port', str(config.get('http_port', '')))
            parser.set('proxy', 'https_host', config.get('https_host', ''))
            parser.set('proxy', 'https_port', str(config.get('https_port', '')))
            parser.set('proxy', 'ftp_host', config.get('ftp_host', ''))
            parser.set('proxy', 'ftp_port', str(config.get('ftp_port', '')))
            parser.set('proxy', 'use_auth', str(config.get('use_auth', False)))
            parser.set('proxy', 'username', config.get('username', ''))
            parser.set('proxy', 'password', config.get('password', ''))
            parser.set('proxy', 'no_proxy', config.get('no_proxy', ''))
            parser.set('proxy', 'use_same', str(config.get('use_same', False)))
            
            # Write to file
            with open(config_file, 'w') as f:
                parser.write(f)
            
            print_colored(f"✅ Configuration saved to {config_file}", self.colors['green'])
            return True
            
        except Exception as e:
            print_colored(f"❌ Error saving configuration: {e}", self.colors['red'])
            return False
    
    def load_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a configuration profile."""
        try:
            # Check for JSON file first (new format)
            json_file = self.config_dir / f'{name}.json'
            if json_file.exists():
                with open(json_file, 'r') as f:
                    config = json.load(f)
                    return config
            
            # Fall back to INI file (old format)
            config_file = self.config_dir / f'{name}.ini'
            
            if not config_file.exists():
                print_colored(f"❌ Configuration '{name}' not found", self.colors['red'])
                return None
            
            parser = configparser.ConfigParser()
            parser.read(config_file)
            
            if not parser.has_section('proxy'):
                print_colored(f"❌ Invalid configuration file: {config_file}", self.colors['red'])
                return None
            
            config = {
                'http_host': parser.get('proxy', 'http_host'),
                'http_port': parser.get('proxy', 'http_port'),
                'https_host': parser.get('proxy', 'https_host'),
                'https_port': parser.get('proxy', 'https_port'),
                'ftp_host': parser.get('proxy', 'ftp_host'),
                'ftp_port': parser.get('proxy', 'ftp_port'),
                'use_auth': parser.getboolean('proxy', 'use_auth'),
                'username': parser.get('proxy', 'username'),
                'password': parser.get('proxy', 'password'),
                'no_proxy': parser.get('proxy', 'no_proxy'),
                'use_same': parser.getboolean('proxy', 'use_same')
            }
            
            # Convert port strings back to integers if not empty
            for port_key in ['http_port', 'https_port', 'ftp_port']:
                if config[port_key]:
                    config[port_key] = int(config[port_key])
                else:
                    config[port_key] = ''
            
            return config
            
        except Exception as e:
            print_colored(f"❌ Error loading configuration: {e}", self.colors['red'])
            return None
    
    def delete_config(self, name: str) -> bool:
        """Delete a configuration profile."""
        try:
            config_file = self.config_dir / f'{name}.ini'
            
            if not config_file.exists():
                print_colored(f"❌ Configuration '{name}' not found", self.colors['red'])
                return False
            
            config_file.unlink()
            print_colored(f"✅ Configuration '{name}' deleted", self.colors['green'])
            return True
            
        except Exception as e:
            print_colored(f"❌ Error deleting configuration: {e}", self.colors['red'])
            return False
    
    def print_configs(self) -> None:
        """Print all available configurations and current target settings."""
        print_colored("Saved Configurations:", self.colors['cyan'])
        
        configs = self.list_configs()
        if not configs:
            print_colored("  No saved configurations found", self.colors['yellow'])
        else:
            for config in configs:
                print_colored(f"  • {config}", self.colors['white'])
        
        print_colored("\nUse 'proxymanx list' to see profiles with active status", self.colors['cyan'])
        print_colored("Use 'proxymanx show-configs' to see current settings for all targets", self.colors['cyan'])
    
    def get_config_info(self, name: str) -> None:
        """Print detailed information about a configuration."""
        config = self.load_config(name)
        
        if not config:
            return
        
        print_colored(f"Configuration: {name}", self.colors['cyan'])
        print_colored(f"  HTTP  : {config['http_host']}:{config['http_port']}", self.colors['white'])
        print_colored(f"  HTTPS : {config['https_host']}:{config['https_port']}", self.colors['white'])
        print_colored(f"  FTP   : {config['ftp_host']}:{config['ftp_port']}", self.colors['white'])
        print_colored(f"  Auth  : {'Yes' if config['use_auth'] else 'No'}", self.colors['white'])
        if config['use_auth']:
            print_colored(f"  User  : {config['username']}", self.colors['white'])
        print_colored(f"  No Proxy: {config['no_proxy']}", self.colors['white'])
    
    def show_current_configs(self) -> None:
        """Show current proxy configurations for all targets."""
        from targets import get_available_targets
        
        print_colored("Current Proxy Configurations for All Targets:", self.colors['cyan'])
        print_colored("=" * 60, self.colors['cyan'])
        
        available_targets = get_available_targets()
        
        for target_name, target in available_targets.items():
            try:
                print_colored(f"\n{target_name.upper()}", self.colors['blue'])
                target.list_proxy()
            except Exception as e:
                print_colored(f"\n{target_name.upper()}", self.colors['blue'])
                print_colored(f"  Error reading settings: {e}", self.colors['red'])
        
        print_colored("\n" + "=" * 60, self.colors['cyan'])
        print_colored("Use 'proxymanx list' to see available profiles", self.colors['cyan'])
    
    def set_active_profile(self, profile_name: str) -> None:
        """Set the currently active profile."""
        try:
            state_file = self.config_dir / '.active_profile'
            with open(state_file, 'w') as f:
                f.write(profile_name)
        except Exception as e:
            print_colored(f"Warning: Could not save active profile state: {e}", self.colors['yellow'])
    
    def get_active_profile(self) -> Optional[str]:
        """Get the currently active profile."""
        try:
            state_file = self.config_dir / '.active_profile'
            if state_file.exists():
                with open(state_file, 'r') as f:
                    profile_name = f.read().strip()
                    # Verify the profile still exists
                    if profile_name in self.list_configs():
                        return profile_name
                    else:
                        # Profile was deleted, clear the state
                        self.clear_active_profile()
            return None
        except Exception:
            return None
    
    def clear_active_profile(self) -> None:
        """Clear the active profile state."""
        try:
            state_file = self.config_dir / '.active_profile'
            if state_file.exists():
                state_file.unlink()
        except Exception:
            pass
