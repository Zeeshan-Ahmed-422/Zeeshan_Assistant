"""
Configuration Settings - API-Based Version
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Central configuration for the voice assistant"""
    
    # Assistant Identity
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Zeeshan")
    WAKE_WORD = os.getenv("WAKE_WORD", "hey zeeshan").lower()
    
    # API Configuration
    # Groq (FREE & FAST - Recommended!)
    USE_GROQ = os.getenv("USE_GROQ", "true").lower() == "true"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    
    # OpenAI (Popular)
    USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Anthropic (High Quality)
    USE_ANTHROPIC = os.getenv("USE_ANTHROPIC", "false").lower() == "true"
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
    
    # Voice Settings
    VOICE_RATE = int(os.getenv("VOICE_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
    
    # Memory Settings
    ENABLE_MEMORY = os.getenv("ENABLE_MEMORY", "true").lower() == "true"
    MEMORY_RETENTION_DAYS = int(os.getenv("MEMORY_RETENTION_DAYS", "30"))
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    CONFIG_DIR = os.path.join(BASE_DIR, "config")
    
    # File Paths
    MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
    DAILY_TABS_FILE = os.path.join(DATA_DIR, "daily_tabs.json")
    COMMAND_HISTORY_FILE = os.path.join(DATA_DIR, "command_history.json")
    COMMANDS_CONFIG_FILE = os.path.join(CONFIG_DIR, "commands_config.json")
    
    # Audio Settings
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    TIMEOUT = 10
    PHRASE_TIME_LIMIT = 15
    
    @classmethod
    def ensure_data_dir(cls):
        """Create data directory if it doesn't exist"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        
        # Create empty JSON files if they don't exist
        for filepath in [cls.MEMORY_FILE, cls.DAILY_TABS_FILE, cls.COMMAND_HISTORY_FILE]:
            if not os.path.exists(filepath):
                import json
                with open(filepath, 'w') as f:
                    json.dump({}, f)
