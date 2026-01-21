"""
System Information
Provides system information like time, date, etc.
"""
from datetime import datetime
import platform
import psutil
from utils.logger import logger

class SystemInfo:
    """Provide system information"""
    
    def __init__(self):
        """Initialize system info"""
        self.system = platform.system()
        logger.info("System info module initialized")
    
    def get_time(self):
        """Get current time"""
        try:
            current_time = datetime.now().strftime("%I:%M %p")
            logger.info(f"Current time: {current_time}")
            return current_time
        except Exception as e:
            logger.error(f"Error getting time: {e}")
            return None
    
    def get_date(self):
        """Get current date"""
        try:
            current_date = datetime.now().strftime("%B %d, %Y")
            day_name = datetime.now().strftime("%A")
            logger.info(f"Current date: {day_name}, {current_date}")
            return f"{day_name}, {current_date}"
        except Exception as e:
            logger.error(f"Error getting date: {e}")
            return None
    
    def get_battery_status(self):
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged
                status = "charging" if plugged else "on battery"
                logger.info(f"Battery: {percent}% ({status})")
                return f"{percent}% {status}"
            else:
                return "Battery information not available"
        except Exception as e:
            logger.error(f"Error getting battery status: {e}")
            return None
    
    def get_system_info(self):
        """Get system information"""
        try:
            info = {
                "os": f"{platform.system()} {platform.release()}",
                "processor": platform.processor(),
                "machine": platform.machine()
            }
            logger.info(f"System info: {info}")
            return info
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return None
    
    def get_cpu_usage(self):
        """Get CPU usage percentage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            logger.info(f"CPU usage: {cpu_percent}%")
            return f"{cpu_percent}%"
        except Exception as e:
            logger.error(f"Error getting CPU usage: {e}")
            return None
    
    def get_memory_usage(self):
        """Get memory usage"""
        try:
            memory = psutil.virtual_memory()
            used_gb = memory.used / (1024 ** 3)
            total_gb = memory.total / (1024 ** 3)
            percent = memory.percent
            logger.info(f"Memory: {used_gb:.1f}/{total_gb:.1f} GB ({percent}%)")
            return f"{used_gb:.1f} GB out of {total_gb:.1f} GB ({percent}%)"
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return None

# Global system info instance
system_info = SystemInfo()