"""
ProxyManX Windows - Main Application Module
Core application logic for proxy management.
"""

import sys
import os
from typing import Dict, List, Any, Optional
from config import ConfigManager
from targets import get_available_targets, get_target_descriptions, PROXY_TARGETS
from utils import *


class ProxyManX:
    """Main proxy management class."""
    
    def __init__(self):
        self.colors = get_colors()
        self.config_manager = ConfigManager()
        self.available_targets = get_available_targets()
        self.target_descriptions = get_target_descriptions()
    
    def interactive_set_proxy(self) -> None:
        """Interactive proxy configuration."""
        print_header("Set Proxy Configuration")
        
        # Get proxy configuration
        config = self._get_proxy_config()
        if not config:
            return
        
        # Get target selection
        targets = self._get_target_selection()
        if not targets:
            return
        
        # Apply proxy settings
        self._apply_proxy_settings(config, targets)
        
        # Ask to save configuration
        if get_yes_no_input("Save this configuration for later use?"):
            name = get_user_input("Enter configuration name", "default")
            if name:
                self.config_manager.save_config(name, config)
    
    def _get_proxy_config(self) -> Optional[Dict[str, Any]]:
        """Get proxy configuration from user input."""
        config = {}
        
        # HTTP proxy settings
        print_colored("HTTP Proxy Settings", self.colors['cyan'])
        config['http_host'] = get_user_input("HTTP Proxy Host")
        if not config['http_host']:
            print_error("HTTP proxy host is required")
            return None
        
        config['http_port'] = get_user_input("HTTP Proxy Port", "8080")
        try:
            config['http_port'] = int(config['http_port'])
        except ValueError:
            print_error("Invalid port number")
            return None
        
        # Authentication
        config['use_auth'] = get_yes_no_input("Use authentication (username/password)?")
        if config['use_auth']:
            print_warning("Please don't save passwords on shared computers")
            config['username'] = get_user_input("Username")
            config['password'] = get_user_input("Password", password=True)
        else:
            config['username'] = ""
            config['password'] = ""
        
        # Same settings for HTTPS and FTP
        config['use_same'] = get_yes_no_input("Use same settings for HTTPS and FTP?", True)
        if config['use_same']:
            config['https_host'] = config['http_host']
            config['https_port'] = config['http_port']
            config['ftp_host'] = config['http_host']
            config['ftp_port'] = config['http_port']
        else:
            print_colored("HTTPS Proxy Settings", self.colors['cyan'])
            config['https_host'] = get_user_input("HTTPS Proxy Host", config['http_host'])
            https_port = get_user_input("HTTPS Proxy Port", str(config['http_port']))
            try:
                config['https_port'] = int(https_port)
            except ValueError:
                print_error("Invalid HTTPS port number")
                return None
            
            print_colored("FTP Proxy Settings", self.colors['cyan'])
            config['ftp_host'] = get_user_input("FTP Proxy Host", config['http_host'])
            ftp_port = get_user_input("FTP Proxy Port", str(config['http_port']))
            try:
                config['ftp_port'] = int(ftp_port)
            except ValueError:
                print_error("Invalid FTP port number")
                return None
        
        # No proxy list
        default_no_proxy = get_default_no_proxy()
        config['no_proxy'] = get_user_input("No proxy (comma-separated)", default_no_proxy)
        
        # Validate configuration
        if not validate_proxy_config(config):
            return None
        
        return config
    
    def _get_target_selection(self, allow_auto_all=False) -> Optional[List[str]]:
        """Get target selection from user."""
        # Check if we're running non-interactively (e.g., from subprocess)
        if allow_auto_all and not sys.stdin.isatty():
            # Running non-interactively, return all targets
            return list(self.available_targets.keys())
        
        print_header("Select Proxy Targets")
        
        targets = list(self.available_targets.keys())
        
        # Show available targets
        print_colored("Available targets:", self.colors['cyan'])
        print_colored("  0. All targets", self.colors['white'])
        for i, target in enumerate(targets, 1):
            description = self.target_descriptions.get(target, target)
            available = "[OK]" if target in self.available_targets else "[UNAVAILABLE]"
            print_colored(f"  {i}. {available} {target} - {description}", self.colors['white'])
        
        # Get user selection
        selection = get_user_input("Select targets (comma-separated numbers or 0 for all)", "0")
        
        try:
            if selection.strip() == "0":
                return list(self.available_targets.keys())
            
            selected_indices = [int(x.strip()) for x in selection.split(",")]
            selected_targets = []
            
            for index in selected_indices:
                if 1 <= index <= len(targets):
                    target = targets[index - 1]
                    if target in self.available_targets:
                        selected_targets.append(target)
                    else:
                        print_warning(f"Target '{target}' is not available")
                else:
                    print_warning(f"Invalid target number: {index}")
            
            return selected_targets if selected_targets else None
            
        except ValueError:
            print_error("Invalid selection format")
            return None
    
    def _apply_proxy_settings(self, config: Dict[str, Any], targets: List[str]) -> None:
        """Apply proxy settings to selected targets."""
        print_header("Applying Proxy Settings")
        
        for target_name in targets:
            target = self.available_targets[target_name]
            print_colored(f"Setting proxy for {target_name}...", self.colors['blue'])
            
            try:
                success = target.set_proxy(config)
                if success:
                    print_success(f"{target_name} proxy configured")
                else:
                    print_error(f"Failed to configure {target_name} proxy")
            except Exception as e:
                print_error(f"Error configuring {target_name}: {e}")
    
    def unset_proxy(self, targets: List[str] = None) -> None:
        """Unset proxy settings."""
        if targets is None:
            targets = self._get_target_selection(allow_auto_all=True)
            if not targets:
                return
        
        print_header("Unsetting Proxy Settings")
        
        for target_name in targets:
            if target_name not in self.available_targets:
                print_warning(f"Target '{target_name}' is not available")
                continue
            
            target = self.available_targets[target_name]
            print_colored(f"Unsetting proxy for {target_name}...", self.colors['blue'])
            
            try:
                success = target.unset_proxy()
                if success:
                    print_success(f"{target_name} proxy cleared")
                else:
                    print_error(f"Failed to clear {target_name} proxy")
            except Exception as e:
                print_error(f"Error clearing {target_name}: {e}")
    
    def list_proxy_settings(self) -> None:
        """List saved proxy profiles and current active configuration."""
        print_header("Proxy Profiles")
        
        # Get all saved configurations
        configs = self.config_manager.list_configs()
        
        if not configs:
            print_colored("No saved profiles found", self.colors['yellow'])
            print_colored("Use 'proxymanx set' to create a new profile", self.colors['cyan'])
            return
        
        # Detect currently active profile by comparing with system proxy
        active_profile = self._detect_active_profile()
        
        print_colored("Available Profiles:", self.colors['cyan'])
        for config in configs:
            if config == active_profile:
                print_colored(f"  • {config}", self.colors['green'])  # Active profile
            else:
                print_colored(f"  • {config}", self.colors['white'])   # Inactive profile
        
        # Show which profile is currently active
        if active_profile:
            print_colored(f"\nCurrently active: {active_profile}", self.colors['green'])
        else:
            print_colored("\nNo active profile detected", self.colors['yellow'])
        
        print_colored("\nUse 'proxymanx configs' to see detailed configuration for all targets", self.colors['cyan'])
    
    def load_and_apply_config(self, config_name: str) -> None:
        """Load and apply a saved configuration."""
        print_header(f"Loading Configuration: {config_name}")
        
        # Load configuration
        config = self.config_manager.load_config(config_name)
        if not config:
            return
        
        # Show configuration details
        self._show_config_details(config)
        
        # Get target selection
        targets = self._get_target_selection()
        if not targets:
            return
        
        # Apply settings
        self._apply_proxy_settings(config, targets)
    
    def _show_config_details(self, config: Dict[str, Any]) -> None:
        """Show configuration details."""
        print_colored("Configuration Details:", self.colors['cyan'])
        print_colored(f"  HTTP : {config['http_host']}:{config['http_port']}", self.colors['white'])
        print_colored(f"  HTTPS: {config['https_host']}:{config['https_port']}", self.colors['white'])
        print_colored(f"  FTP  : {config['ftp_host']}:{config['ftp_port']}", self.colors['white'])
        print_colored(f"  Auth : {'Yes' if config['use_auth'] else 'No'}", self.colors['white'])
        if config['use_auth']:
            print_colored(f"  User : {config['username']}", self.colors['white'])
        print_colored(f"  No Proxy: {config['no_proxy']}", self.colors['white'])
        print()
    
    def show_current_configs(self) -> None:
        """Show current configuration for all targets."""
        print_header("Current Proxy Configuration")
        
        print_colored("Current Settings for All Targets:", self.colors['cyan'])
        
        # Check each target
        for target_name, target_instance in self.available_targets.items():
            
            try:
                # Get current proxy settings for this target
                current_settings = target_instance.list_proxy()
                
                if current_settings:
                    # Target has proxy settings
                    print_colored(f"\n[ACTIVE] {target_name.title()}", self.colors['green'])
                    if isinstance(current_settings, dict):
                        for key, value in current_settings.items():
                            print_colored(f"  {key}: {value}", self.colors['white'])
                    else:
                        print_colored(f"  {current_settings}", self.colors['white'])
                else:
                    # Target has no proxy settings
                    print_colored(f"\n[INACTIVE] {target_name.title()}", self.colors['yellow'])
                    print_colored(f"  No proxy settings configured", self.colors['white'])
                    
            except Exception as e:
                print_colored(f"\n[ERROR] {target_name.title()}", self.colors['red'])
                print_colored(f"  Error reading settings: {e}", self.colors['white'])
        
        print_colored(f"\nUse 'proxymanx set' to configure proxy settings", self.colors['cyan'])
        print_colored(f"Use 'proxymanx list' to see saved profiles", self.colors['cyan'])
    
    def save_current_config(self, config_name: str) -> None:
        """Save current proxy configuration."""
        print_header(f"Saving Configuration: {config_name}")
        
        # This would need to read current settings from all targets
        # For now, we'll just show an info message
        print_info("Use 'proxymanx set' to create and save a new configuration")
    
    def show_help(self) -> None:
        """Show help information."""
        print_header("ProxyManX Windows - Help")
        
        help_text = f"""
{self.colors['cyan']}ProxyManX Windows{self.colors['reset']} - Proxy configuration made easy

{self.colors['bold']}Usage:{self.colors['reset']}
  proxymanx <command> [options]

{self.colors['bold']}Commands:{self.colors['reset']}
  {self.colors['green']}set{self.colors['reset']}                    Set proxy settings interactively
  {self.colors['green']}unset{self.colors['reset']}                  Unset proxy settings
  {self.colors['green']}unset all{self.colors['reset']}              Unset proxy for all targets
  {self.colors['green']}unset <target>{self.colors['reset']}         Unset proxy for specific target(s)
  {self.colors['green']}list{self.colors['reset']}                   List saved profiles (with active status)
  {self.colors['green']}configs{self.colors['reset']}                Show current settings for all targets
  {self.colors['green']}load <name>{self.colors['reset']}            Load and apply a saved configuration
  {self.colors['green']}save <name>{self.colors['reset']}            Save current configuration
  {self.colors['green']}delete <name>{self.colors['reset']}          Delete a saved configuration
  {self.colors['green']}help{self.colors['reset']}                   Show this help message

{self.colors['bold']}Examples:{self.colors['reset']}
  proxymanx set                   # Interactive proxy setup
  proxymanx load office           # Load 'office' configuration
  proxymanx list                  # Show saved profiles with active status
  proxymanx show-configs          # Show current settings for all targets
  proxymanx unset                 # Remove proxy settings (interactive)
  proxymanx unset all             # Remove proxy for all targets
  proxymanx unset windows npm     # Remove proxy for specific targets

{self.colors['bold']}Supported Targets:{self.colors['reset']}
"""
        
        for name, description in self.target_descriptions.items():
            available = "[OK]" if name in self.available_targets else "[UNAVAILABLE]"
            print_colored(f"  {available} {name:12} - {description}", self.colors['white'])
        
        print(help_text)
        
        print_colored(f"\n{self.colors['bold']}Note:{self.colors['reset']} Some operations require administrator privileges")
        print_colored(f"Repository: https://github.com/thewijay/ProxyManX", self.colors['blue'])
    
    def _detect_active_profile(self) -> Optional[str]:
        """Detect which saved profile matches the current proxy settings."""
        try:
            # Get current proxy settings from environment (most common case)
            current_http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
            
            if not current_http_proxy:
                return None
            
            # Parse the proxy URL to extract host and port
            if current_http_proxy.startswith('http://'):
                proxy_part = current_http_proxy[7:]  # Remove 'http://'
            elif current_http_proxy.startswith('https://'):
                proxy_part = current_http_proxy[8:]  # Remove 'https://'
            else:
                proxy_part = current_http_proxy
            
            # Remove trailing slash if present
            if proxy_part.endswith('/'):
                proxy_part = proxy_part[:-1]
            
            # Parse host:port
            if ':' in proxy_part:
                current_host, current_port = proxy_part.split(':', 1)
                try:
                    current_port = int(current_port)
                except ValueError:
                    return None
            else:
                current_host = proxy_part
                current_port = 8080  # Default port
            
            # Check each saved configuration
            configs = self.config_manager.list_configs()
            for config_name in configs:
                config = self.config_manager.load_config(config_name)
                if config:
                    # Compare host and port
                    if (config.get('http_host') == current_host and 
                        config.get('http_port') == current_port):
                        return config_name
            
            return None
            
        except Exception as e:
            # If any error occurs, just return None
            return None


def main():
    """Main entry point."""
    # Setup signal handlers for graceful Ctrl+C handling
    from utils import setup_signal_handlers
    setup_signal_handlers()
    
    try:
        manager = ProxyManX()
        
        if len(sys.argv) < 2:
            manager.show_help()
            return
        
        command = sys.argv[1].lower()
        
        if command == 'set':
            manager.interactive_set_proxy()
        
        elif command == 'unset':
            # Check for additional arguments
            targets = None
            if len(sys.argv) > 2:
                if sys.argv[2] == 'all':
                    targets = list(manager.available_targets.keys())
                else:
                    # Parse target names from command line
                    targets = [arg.strip() for arg in sys.argv[2:] if arg.strip() in manager.available_targets]
                    if not targets:
                        print_error(f"Invalid targets specified. Available: {', '.join(manager.available_targets.keys())}")
                        return
            manager.unset_proxy(targets)
        
        elif command == 'list':
            manager.list_proxy_settings()
        
        elif command == 'configs':
            manager.show_current_configs()
        
        elif command == 'show-configs':
            manager.show_current_configs()
        
        elif command == 'load':
            if len(sys.argv) < 3:
                print_error("Usage: proxymanx load <config_name>")
                return
            manager.load_and_apply_config(sys.argv[2])
        
        elif command == 'save':
            if len(sys.argv) < 3:
                print_error("Usage: proxymanx save <config_name>")
                return
            manager.save_current_config(sys.argv[2])
        
        elif command == 'delete':
            if len(sys.argv) < 3:
                print_error("Usage: proxymanx delete <config_name>")
                return
            manager.config_manager.delete_config(sys.argv[2])
        
        elif command in ['help', '-h', '--help']:
            manager.show_help()
        
        else:
            print_error(f"Unknown command: {command}")
            manager.show_help()
    
    except KeyboardInterrupt:
        print_colored("\n\nOperation cancelled by user", get_colors()['yellow'])
    except Exception as e:
        print_error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
