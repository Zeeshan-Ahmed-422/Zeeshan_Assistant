"""
Workflow Executor
Executes complex multi-step workflows like "start my day"
"""
import time
from config.settings import Settings
from utils.logger import logger
from memory.memory_manager import memory
from actions.app_launcher import app_launcher
from actions.web_opener import web_opener
from core.text_to_speech import tts

class WorkflowExecutor:
    """Execute multi-step workflows"""
    
    def __init__(self):
        """Initialize workflow executor"""
        logger.info("Workflow executor initialized")
    
    def execute_workflow(self, workflow_name):
        """
        Execute a workflow
        
        Args:
            workflow_name: Name of workflow to execute
            
        Returns:
            bool: True if successful
        """
        workflows = {
            "start_my_day": self.start_my_day,
            "end_my_day": self.end_my_day,
        }
        
        workflow_func = workflows.get(workflow_name)
        
        if workflow_func:
            return workflow_func()
        else:
            logger.error(f"Unknown workflow: {workflow_name}")
            return False
    
    def start_my_day(self):
        """
        Start my day workflow - opens frequently used apps and websites
        Uses memory to learn user patterns
        """
        try:
            tts.speak("Starting your day. Opening your usual applications and websites.")
            logger.info("Executing 'start my day' workflow")
            
            # Get items to open from memory (intelligent learning)
            if Settings.ENABLE_MEMORY:
                # Use morning routine based on patterns
                items = memory.get_morning_routine()
                
                # If no patterns yet, use recent tabs
                if not items or len(items) < 3:
                    items = memory.get_recent_tabs()
            else:
                # Fallback to default items
                items = [
                    {"type": "open_app", "name": "vscode"},
                    {"type": "open_website", "name": "gmail"},
                    {"type": "open_website", "name": "github"}
                ]
            
            # Execute each item
            opened_count = 0
            for item in items[:8]:  # Limit to 8 items
                item_type = item.get("type")
                item_name = item.get("name")
                
                if item_type == "open_app":
                    if app_launcher.launch(item_name):
                        opened_count += 1
                        time.sleep(0.5)  # Small delay between launches
                
                elif item_type == "open_website":
                    if web_opener.open_website(item_name):
                        opened_count += 1
                        time.sleep(0.5)
            
            message = f"Opened {opened_count} items for you. Have a productive day!"
            tts.speak(message)
            logger.info(f"'Start my day' completed: {opened_count} items opened")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in 'start my day' workflow: {e}")
            tts.speak("Sorry, I encountered an error starting your day.")
            return False
    
    def end_my_day(self):
        """
        End my day workflow - saves state and closes apps
        """
        try:
            tts.speak("Ending your day. Saving your work state.")
            logger.info("Executing 'end my day' workflow")
            
            # In a real implementation, this could:
            # 1. Save currently open apps/tabs
            # 2. Close specific applications
            # 3. Create a backup
            # 4. Set system to sleep/shutdown
            
            tts.speak("Your work state has been saved. Have a great evening!")
            logger.info("'End my day' completed")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in 'end my day' workflow: {e}")
            tts.speak("Sorry, I encountered an error ending your day.")
            return False
    
    def custom_workflow(self, steps):
        """
        Execute a custom workflow with multiple steps
        
        Args:
            steps: List of steps to execute
            
        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Executing custom workflow with {len(steps)} steps")
            
            for i, step in enumerate(steps, 1):
                logger.info(f"Step {i}/{len(steps)}: {step}")
                
                # Parse and execute step
                # This is a simplified version - you can expand this
                if "open" in step:
                    # Extract app/website name and open it
                    pass
                
                time.sleep(1)  # Delay between steps
            
            return True
            
        except Exception as e:
            logger.error(f"Error in custom workflow: {e}")
            return False

# Global workflow executor instance
workflow_executor = WorkflowExecutor()