"""
Text-to-Speech Engine
Provides voice feedback to the user
"""
import pyttsx3
from config.settings import Settings
from utils.logger import logger

class TextToSpeech:
    """Handle text-to-speech functionality"""
    
    def __init__(self):
        """Initialize TTS engine"""
        try:
            self.engine = pyttsx3.init()
            self._configure_voice()
            logger.info("Text-to-Speech engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def _configure_voice(self):
        """Configure voice properties"""
        if self.engine:
            # Set rate (speed of speech)
            self.engine.setProperty('rate', Settings.VOICE_RATE)
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', Settings.VOICE_VOLUME)
            
            # Optional: Set voice (male/female)
            voices = self.engine.getProperty('voices')
            if len(voices) > 0:
                # Use first available voice (usually male)
                self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.engine:
            print(f"[TTS Error] Cannot speak: {text}")
            return False
        
        try:
            logger.info(f"Speaking: {text}")
            print(f"🔊 {Settings.ASSISTANT_NAME}: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"[TTS Error] {text}")
            return False
    
    def speak_async(self, text):
        """Speak without blocking (experimental)"""
        if not self.engine:
            print(f"[TTS Error] Cannot speak: {text}")
            return False
        
        try:
            logger.info(f"Speaking (async): {text}")
            print(f"🔊 {Settings.ASSISTANT_NAME}: {text}")
            self.engine.say(text)
            self.engine.startLoop(False)
            self.engine.iterate()
            self.engine.endLoop()
            return True
        except Exception as e:
            logger.error(f"TTS async error: {e}")
            return False
    
    def stop(self):
        """Stop current speech"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

# Global TTS instance
tts = TextToSpeech()