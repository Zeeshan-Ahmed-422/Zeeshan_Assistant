"""
Voice Assistant - ZEESHAN
Main Entry Point

A modular, intelligent voice-controlled assistant with Groq API
"""
import sys
import signal
from datetime import datetime
from config.settings import Settings
from utils.logger import logger
from core.wake_word_detector import wake_detector
from core.text_to_speech import tts
from core.command_classifier import classifier
from memory.memory_manager import memory
from actions.app_launcher import app_launcher
from actions.web_opener import web_opener
from actions.system_info import system_info
from actions.file_manager import file_manager
from actions.workflow_executor import workflow_executor

class VoiceAssistant:
    """Main Voice Assistant Class"""
    
    def __init__(self):
        """Initialize the voice assistant"""
        logger.info("="*60)
        logger.info(f"Initializing {Settings.ASSISTANT_NAME} Voice Assistant")
        logger.info("="*60)
        
        self.running = False
        self.assistant_name = Settings.ASSISTANT_NAME
        
        # Ensure data directory exists
        Settings.ensure_data_dir()
        
        logger.info("Voice Assistant initialized successfully")
    
    def start(self):
        """Start the voice assistant"""
        self.running = True
        
        # Welcome message
        welcome_msg = f"Hello! I am {self.assistant_name}, your voice assistant. Say 'Hey {self.assistant_name}' to activate me."
        tts.speak(welcome_msg)
        
        logger.info("Voice Assistant started")
        print("\n" + "="*60)
        print(f"🤖 {self.assistant_name} Voice Assistant")
        print("="*60)
        print(f"💡 Say 'Hey {self.assistant_name}' to activate")
        print("💡 Say 'exit' or 'quit' to stop")
        print("="*60 + "\n")
        
        # Main loop
        try:
            while self.running:
                # Listen for wake word
                if wake_detector.listen_for_activation():
                    wake_detector.activate()
                    self.handle_command_session()
        
        except KeyboardInterrupt:
            self.stop()
    
    def handle_command_session(self):
        """Handle a command session after wake word is detected"""
        try:
            # Get command from user
            command = wake_detector.wait_for_command()
            
            if not command:
                wake_detector.deactivate()
                return
            
            # Check for exit commands
            if command in ["exit", "quit", "goodbye", "bye", "stop"]:
                tts.speak("Goodbye! Have a great day!")
                self.stop()
                return
            
            # Classify command using Groq
            logger.info(f"Processing command: {command}")
            print(f"\n{'='*60}")
            print(f"🎯 Processing: {command}")
            print(f"{'='*60}")
            
            classification = classifier.classify(command)
            
            print(f"📋 Intent: {classification.get('intent')}")
            print(f"📋 Action: {classification.get('action')}")
            print(f"📋 Confidence: {classification.get('confidence')}")
            print(f"{'='*60}\n")
            
            # Execute action based on classification
            success = self.execute_action(classification, command)
            
            # Record in memory
            if success and Settings.ENABLE_MEMORY:
                try:
                    memory.record_command(
                        command=command,
                        action_type=classification.get("intent"),
                        action_name=classification.get("action"),
                        success=True
                    )
                except Exception as e:
                    logger.warning(f"Could not record in memory: {e}")
            
            # Deactivate after command
            wake_detector.deactivate()
            
        except Exception as e:
            logger.error(f"Error in command session: {e}")
            print(f"❌ Error: {e}")
            tts.speak("Sorry, I encountered an error.")
            wake_detector.deactivate()
    
    def execute_action(self, classification, original_command):
        """
        Execute action based on classification
        
        Args:
            classification: Classification result from Groq
            original_command: Original command text
            
        Returns:
            bool: True if successful
        """
        intent = classification.get("intent")
        action = classification.get("action")
        confidence = classification.get("confidence", 0.0)
        
        logger.info(f"Intent: {intent}, Action: {action}, Confidence: {confidence}")
        
        # Low confidence - ask for clarification
        if confidence < 0.5:
            tts.speak("I'm not sure what you want me to do. Could you please rephrase?")
            return False
        
        # Execute based on intent
        try:
            if intent == "open_app":
                print(f"🚀 Opening app: {action}")
                return self.handle_open_app(action)
            
            elif intent == "open_website":
                print(f"🌐 Opening website: {action}")
                return self.handle_open_website(action)
            
            elif intent == "system_info":
                print(f"ℹ️  Getting system info: {action}")
                return self.handle_system_info(action)
            
            elif intent == "file_operation":
                print(f"📁 File operation: {action}")
                return self.handle_file_operation(action, original_command)
            
            elif intent == "workflow":
                print(f"⚙️  Executing workflow: {action}")
                return self.handle_workflow(action)
            
            else:
                print(f"❓ Unknown intent: {intent}")
                tts.speak("I don't know how to do that yet.")
                return False
        
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            print(f"❌ Action error: {e}")
            tts.speak("Sorry, I couldn't complete that action.")
            return False
    
    def handle_open_app(self, app_name):
        """Handle opening an application"""
        print(f"  → Launching: {app_name}")
        tts.speak(f"Opening {app_name}")
        
        success = app_launcher.launch(app_name)
        
        if success:
            print(f"  ✅ {app_name} opened successfully")
            tts.speak(f"{app_name} opened successfully")
        else:
            print(f"  ❌ Failed to open {app_name}")
            tts.speak(f"Sorry, I couldn't open {app_name}")
        
        return success
    
    def handle_open_website(self, site_name):
        """Handle opening a website"""
        print(f"  → Opening website: {site_name}")
        tts.speak(f"Opening {site_name}")
        
        success = web_opener.open_website(site_name)
        
        if success:
            print(f"  ✅ {site_name} opened successfully")
            tts.speak(f"{site_name} opened in browser")
        else:
            print(f"  ❌ Failed to open {site_name}")
            tts.speak(f"Sorry, I couldn't open {site_name}")
        
        return success
    
    def handle_system_info(self, info_type):
        """Handle system information requests"""
        print(f"  → Getting {info_type}")
        
        if info_type == "time":
            time_str = system_info.get_time()
            if time_str:
                print(f"  ✅ Current time: {time_str}")
                tts.speak(f"The current time is {time_str}")
                return True
        
        elif info_type == "date":
            date_str = system_info.get_date()
            if date_str:
                print(f"  ✅ Current date: {date_str}")
                tts.speak(f"Today is {date_str}")
                return True
        
        elif info_type == "battery":
            battery_str = system_info.get_battery_status()
            if battery_str:
                print(f"  ✅ Battery: {battery_str}")
                tts.speak(f"Battery is at {battery_str}")
                return True
        
        print(f"  ❌ Could not get {info_type}")
        tts.speak("Sorry, I couldn't get that information")
        return False
    
    def handle_file_operation(self, operation, command):
        """Handle file operations"""
        print(f"  → File operation: {operation}")
        
        if operation == "create_folder":
            # Extract folder name from command (simplified)
            folder_name = f"Folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            print(f"  → Creating folder: {folder_name}")
            tts.speak(f"Creating folder")
            
            success = file_manager.create_folder(folder_name)
            
            if success:
                print(f"  ✅ Folder created: {folder_name}")
                tts.speak("Folder created successfully")
            else:
                print(f"  ❌ Failed to create folder")
                tts.speak("Sorry, I couldn't create the folder")
            
            return success
        
        elif operation == "clean_downloads":
            print(f"  → Cleaning downloads folder")
            tts.speak("Cleaning your downloads folder")
            
            stats = file_manager.clean_downloads()
            
            if stats:
                total = sum(stats.values())
                print(f"  ✅ Organized {total} files")
                print(f"     Images: {stats['images']}")
                print(f"     Documents: {stats['documents']}")
                print(f"     Videos: {stats['videos']}")
                print(f"     Archives: {stats['archives']}")
                print(f"     Others: {stats['others']}")
                tts.speak(f"Organized {total} files in your downloads folder")
                return True
            else:
                print(f"  ❌ Failed to clean downloads")
                tts.speak("Sorry, I couldn't clean the downloads folder")
                return False
        
        print(f"  ❌ Unknown file operation: {operation}")
        return False
    
    def handle_workflow(self, workflow_name):
        """Handle workflow execution"""
        print(f"  → Executing workflow: {workflow_name}")
        tts.speak(f"Executing {workflow_name} workflow")
        
        success = workflow_executor.execute_workflow(workflow_name)
        
        if success:
            print(f"  ✅ Workflow completed: {workflow_name}")
        else:
            print(f"  ❌ Workflow failed: {workflow_name}")
        
        return success
    
    def stop(self):
        """Stop the voice assistant"""
        self.running = False
        logger.info("Voice Assistant stopping...")
        print("\n" + "="*60)
        print("👋 Thank you for using Zeeshan Voice Assistant!")
        print("="*60 + "\n")
        sys.exit(0)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n⚠️  Interrupt received. Shutting down...")
    sys.exit(0)

def main():
    """Main function"""
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start assistant
    assistant = VoiceAssistant()
    assistant.start()

if __name__ == "__main__":
    main()