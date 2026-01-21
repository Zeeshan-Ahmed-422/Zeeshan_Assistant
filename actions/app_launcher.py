"""
Application Launcher
Opens desktop applications
"""
import os
import subprocess
import platform
from config.settings import Settings
from utils.logger import logger
from utils.helpers import load_json

class AppLauncher:
    """Launch desktop applications"""
    
    def __init__(self):
        """Initialize app launcher"""
        self.commands_config = load_json(Settings.COMMANDS_CONFIG_FILE)
        self.system = platform.system()
        logger.info(f"App launcher initialized for {self.system}")
    
    def launch(self, app_name):
        """
        Launch an application
        
        Args:
            app_name: Name of application to launch
            
        Returns:
            bool: True if successful
        """
        try:
            # Get app configuration
            app_config = self.commands_config.get("applications", {}).get(app_name)
            
            if not app_config:
                logger.error(f"Unknown application: {app_name}")
                return False
            
            command = app_config.get("command")
            
            # Platform-specific launching
            if self.system == "Windows":
                success = self._launch_windows(command)
            elif self.system == "Linux":
                success = self._launch_linux(command)
            elif self.system == "Darwin":  # macOS
                success = self._launch_macos(command)
            else:
                logger.error(f"Unsupported platform: {self.system}")
                return False
            
            if success:
                logger.info(f"Successfully launched: {app_name}")
            else:
                logger.error(f"Failed to launch: {app_name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error launching app {app_name}: {e}")
            return False
    
    def _launch_windows(self, command):
        """Launch app on Windows"""
        try:
            if command.startswith("start "):
                # Use start command
                subprocess.Popen(command, shell=True)
            else:
                # Direct executable
                subprocess.Popen(command, shell=True)
            return True
        except Exception as e:
            logger.error(f"Windows launch error: {e}")
            return False
    
    def _launch_linux(self, command):
        """Launch app on Linux"""
        try:
            # Remove .exe extension for Linux
            command = command.replace(".exe", "")
            
            # Try to launch
            subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            logger.error(f"Linux launch error: {e}")
            return False
    
    def _launch_macos(self, command):
        """Launch app on macOS"""
        try:
            # Remove .exe extension for macOS
            command = command.replace(".exe", "")
            
            # Use 'open' command for macOS
            if not command.startswith("open "):
                command = f"open -a {command}"
            
            subprocess.Popen(command, shell=True)
            return True
        except Exception as e:
            logger.error(f"macOS launch error: {e}")
            return False
    
    def launch_custom(self, command):
        """
        Launch a custom command
        
        Args:
            command: Custom command to execute
            
        Returns:
            bool: True if successful
        """
        try:
            subprocess.Popen(command, shell=True)
            logger.info(f"Executed custom command: {command}")
            return True
        except Exception as e:
            logger.error(f"Error executing custom command: {e}")
            return False

# Global app launcher instance
app_launcher = AppLauncher()