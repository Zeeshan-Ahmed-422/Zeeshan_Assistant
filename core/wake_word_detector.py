"""
Wake Word Detector
Listens for "Hey Zeeshan" activation phrase
"""
from core.voice_listener import listener
from core.text_to_speech import tts
from config.settings import Settings
from utils.logger import logger

class WakeWordDetector:
    """Detect wake word to activate assistant"""
    
    def __init__(self):
        """Initialize wake word detector"""
        self.wake_word = Settings.WAKE_WORD
        self.is_active = False
        logger.info(f"Wake word detector initialized with: '{self.wake_word}'")
    
    def listen_for_activation(self):
        """
        Continuously listen for wake word
        
        Returns:
            bool: True if wake word detected
        """
        logger.info(f"Listening for wake word: '{self.wake_word}'")
        print(f"\n🎤 Say '{self.wake_word}' to activate the assistant...")
        
        while True:
            try:
                text = listener.listen(timeout=10, phrase_time_limit=5)
                
                if text:
                    logger.debug(f"Heard: {text}")
                    
                    # Check if wake word is in the text
                    if self.wake_word in text.lower():
                        self.is_active = True
                        logger.info("Wake word detected! Assistant activated.")
                        return True
                
            except KeyboardInterrupt:
                logger.info("Wake word detection interrupted by user")
                return False
            except Exception as e:
                logger.error(f"Error in wake word detection: {e}")
                continue
    
    def activate(self):
        """Activate the assistant"""
        self.is_active = True
        tts.speak("Yes, I'm listening. How can I help you?")
        logger.info("Assistant activated")
    
    def deactivate(self):
        """Deactivate the assistant"""
        self.is_active = False
        logger.info("Assistant deactivated")
    
    def wait_for_command(self):
        """
        Wait for user command after activation
        
        Returns:
            str: User command or None
        """
        if not self.is_active:
            logger.warning("Assistant not activated")
            return None
        
        logger.info("Waiting for user command...")
        command = listener.get_command()
        
        if command:
            logger.info(f"Command received: {command}")
        else:
            logger.warning("No command received")
            tts.speak("I didn't catch that. Could you please repeat?")
        
        return command

# Global wake word detector instance
wake_detector = WakeWordDetector()