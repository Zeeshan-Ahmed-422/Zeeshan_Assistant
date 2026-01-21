"""
Memory Manager - RAG-based User Pattern Memory
Learns and remembers user habits and preferences
"""
import json
from datetime import datetime, timedelta
from collections import Counter
from config.settings import Settings
from utils.logger import logger
from utils.helpers import load_json, save_json, get_timestamp
from memory.vector_store import vector_store

class MemoryManager:
    """Manage user behavior patterns and preferences"""
    
    def __init__(self):
        """Initialize memory manager"""
        Settings.ensure_data_dir()
        
        self.memory_data = load_json(Settings.MEMORY_FILE, default={
            "daily_patterns": {},
            "frequent_apps": {},
            "frequent_websites": {},
            "command_history": [],
            "preferences": {}
        })
        
        self.daily_tabs = load_json(Settings.DAILY_TABS_FILE, default={
            "tabs": [],
            "last_updated": None
        })
        
        logger.info("Memory manager initialized")
    
    def record_command(self, command, action_type, action_name, success=True):
        """
        Record a command execution
        
        Args:
            command: Original command text
            action_type: Type of action (open_app, open_website, etc.)
            action_name: Name of action performed
            success: Whether action was successful
        """
        try:
            # Add to command history
            history_entry = {
                "timestamp": get_timestamp(),
                "command": command,
                "action_type": action_type,
                "action_name": action_name,
                "success": success,
                "hour": datetime.now().hour,
                "day_of_week": datetime.now().strftime("%A")
            }
            
            self.memory_data["command_history"].append(history_entry)
            
            # Keep only last 1000 commands
            if len(self.memory_data["command_history"]) > 1000:
                self.memory_data["command_history"] = self.memory_data["command_history"][-1000:]
            
            # Update frequency counters
            if action_type == "open_app":
                self._update_frequency("frequent_apps", action_name)
            elif action_type == "open_website":
                self._update_frequency("frequent_websites", action_name)
            
            # Update daily patterns
            self._update_daily_patterns(action_type, action_name)
            
            # Save to disk
            self._save_memory()
            
            # Add to vector store for semantic search
            if Settings.ENABLE_MEMORY:
                context = {
                    "action_type": action_type,
                    "action_name": action_name,
                    "hour": datetime.now().hour,
                    "day": datetime.now().strftime("%A")
                }
                vector_store.add_pattern(command, context)
            
            logger.debug(f"Recorded command: {command} -> {action_type}:{action_name}")
            
        except Exception as e:
            logger.error(f"Error recording command: {e}")
    
    def _update_frequency(self, category, item):
        """Update frequency counter for an item"""
        if category not in self.memory_data:
            self.memory_data[category] = {}
        
        if item not in self.memory_data[category]:
            self.memory_data[category][item] = 0
        
        self.memory_data[category][item] += 1
    
    def _update_daily_patterns(self, action_type, action_name):
        """Update daily usage patterns"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.memory_data["daily_patterns"]:
            self.memory_data["daily_patterns"][today] = {
                "apps": [],
                "websites": [],
                "commands_count": 0
            }
        
        if action_type == "open_app" and action_name not in self.memory_data["daily_patterns"][today]["apps"]:
            self.memory_data["daily_patterns"][today]["apps"].append(action_name)
        
        if action_type == "open_website" and action_name not in self.memory_data["daily_patterns"][today]["websites"]:
            self.memory_data["daily_patterns"][today]["websites"].append(action_name)
        
        self.memory_data["daily_patterns"][today]["commands_count"] += 1
        
        # Update daily tabs for "start my day" workflow
        self._update_daily_tabs(action_type, action_name)
    
    def _update_daily_tabs(self, action_type, action_name):
        """Update frequently used tabs/apps for 'start my day' command"""
        if action_type in ["open_app", "open_website"]:
            item = {"type": action_type, "name": action_name}
            
            # Add if not already in list
            if item not in self.daily_tabs["tabs"]:
                self.daily_tabs["tabs"].append(item)
            
            # Keep only last 20 items
            if len(self.daily_tabs["tabs"]) > 20:
                self.daily_tabs["tabs"] = self.daily_tabs["tabs"][-20:]
            
            self.daily_tabs["last_updated"] = get_timestamp()
            save_json(Settings.DAILY_TABS_FILE, self.daily_tabs)
    
    def get_morning_routine(self):
        """
        Get recommended apps/websites for 'start my day' based on patterns
        
        Returns:
            list: Recommended items to open
        """
        try:
            # Get items used in morning hours (6 AM - 11 AM) from last 7 days
            morning_items = []
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for entry in self.memory_data["command_history"]:
                try:
                    entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if entry_time >= cutoff_date and 6 <= entry["hour"] <= 11:
                        if entry["action_type"] in ["open_app", "open_website"]:
                            morning_items.append({
                                "type": entry["action_type"],
                                "name": entry["action_name"]
                            })
                except:
                    continue
            
            # Count frequency
            item_counter = Counter(json.dumps(item) for item in morning_items)
            
            # Get top 5 most frequent
            top_items = [json.loads(item) for item, count in item_counter.most_common(5)]
            
            # If no morning patterns, use most frequent overall
            if not top_items:
                top_items = self._get_most_frequent_items(5)
            
            logger.info(f"Morning routine recommendation: {top_items}")
            return top_items
            
        except Exception as e:
            logger.error(f"Error getting morning routine: {e}")
            return self._get_most_frequent_items(5)
    
    def _get_most_frequent_items(self, count=5):
        """Get most frequently used apps and websites"""
        items = []
        
        # Get top apps
        top_apps = sorted(
            self.memory_data.get("frequent_apps", {}).items(),
            key=lambda x: x[1],
            reverse=True
        )[:count]
        
        for app, freq in top_apps:
            items.append({"type": "open_app", "name": app})
        
        # Get top websites
        top_websites = sorted(
            self.memory_data.get("frequent_websites", {}).items(),
            key=lambda x: x[1],
            reverse=True
        )[:count]
        
        for site, freq in top_websites:
            items.append({"type": "open_website", "name": site})
        
        return items[:count]
    
    def get_recent_tabs(self):
        """Get recently used tabs for 'start my day'"""
        return self.daily_tabs.get("tabs", [])[:10]  # Last 10 items
    
    def _save_memory(self):
        """Save memory data to disk"""
        try:
            save_json(Settings.MEMORY_FILE, self.memory_data)
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def get_statistics(self):
        """Get usage statistics"""
        return {
            "total_commands": len(self.memory_data["command_history"]),
            "most_used_apps": sorted(
                self.memory_data.get("frequent_apps", {}).items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "most_used_websites": sorted(
                self.memory_data.get("frequent_websites", {}).items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "days_tracked": len(self.memory_data.get("daily_patterns", {}))
        }

# Global memory manager instance
memory = MemoryManager()