"""
Voice Listener - Speech Recognition
Converts voice input to text
"""
import speech_recognition as sr
from config.settings import Settings
from utils.logger import logger

class VoiceListener:
    """Handle voice input and speech recognition"""
    
    def __init__(self):
        """Initialize speech recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            logger.info("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        logger.info("Voice listener initialized successfully")
    
    def listen(self, timeout=None, phrase_time_limit=None):
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: Time to wait for speech to start
            phrase_time_limit: Maximum time for phrase
            
        Returns:
            str: Recognized text or None if failed
        """
        if timeout is None:
            timeout = Settings.TIMEOUT
        if phrase_time_limit is None:
            phrase_time_limit = Settings.PHRASE_TIME_LIMIT
        
        try:
            with self.microphone as source:
                logger.debug("Listening for voice input...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech using Google Speech Recognition
            logger.debug("Recognizing speech...")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out - no speech detected")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
            return None
    
    def listen_for_wake_word(self):
        """
        Listen specifically for wake word
        
        Returns:
            bool: True if wake word detected
        """
        text = self.listen(timeout=10, phrase_time_limit=5)
        
        if text and Settings.WAKE_WORD in text:
            logger.info(f"Wake word detected: {text}")
            return True
        
        return False
    
    def get_command(self):
        """
        Get command after wake word is detected
        
        Returns:
            str: Command text or None
        """
        logger.info("Waiting for command...")
        text = self.listen(timeout=5, phrase_time_limit=10)
        return text

# Global listener instance
listener = VoiceListener()