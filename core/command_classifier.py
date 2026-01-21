"""
Command Classifier - Groq API Only
Simple & Fast - FREE API!
"""
import json
from config.settings import Settings
from utils.logger import logger
from utils.helpers import load_json

# Import Groq API client
try:
    from groq import Groq
    GROQ_AVAILABLE = True
    print("✅ Groq module imported successfully")
except ImportError:
    GROQ_AVAILABLE = False
    print("❌ Groq module NOT available - Install: pip install groq")
    logger.warning("Groq not available. Install: pip install groq")

class CommandClassifier:
    """Classify commands using Groq API"""
    
    def __init__(self):
        """Initialize classifier with Groq API client"""
        self.commands_config = load_json(Settings.COMMANDS_CONFIG_FILE)
        self.llm_client = None
        self.llm_type = None
        
        # Initialize Groq API client
        self._initialize_groq()
        
        logger.info(f"Command classifier initialized with {self.llm_type}")
        print(f"🤖 Classifier: {self.llm_type}")
    
    def _initialize_groq(self):
        """Initialize Groq API client"""
        
        print(f"\n{'='*60}")
        print(f"🔧 Initializing Groq API Classifier")
        print(f"{'='*60}")
        print(f"✓ USE_GROQ: {Settings.USE_GROQ}")
        print(f"✓ GROQ_API_KEY exists: {bool(Settings.GROQ_API_KEY)}")
        print(f"✓ GROQ_API_KEY length: {len(Settings.GROQ_API_KEY) if Settings.GROQ_API_KEY else 0}")
        print(f"✓ GROQ_MODEL: {Settings.GROQ_MODEL}")
        print(f"✓ GROQ_AVAILABLE: {GROQ_AVAILABLE}")
        print(f"{'='*60}\n")
        
        # Check if Groq is available and configured
        if not GROQ_AVAILABLE:
            print("❌ Groq module not installed!")
            print("   Run: pip install groq")
            logger.warning("Groq module not available. Falling back to rule-based.")
            self.llm_type = "Rule-based (Groq not installed)"
            return
        
        if not Settings.USE_GROQ:
            print("❌ USE_GROQ is False in .env file!")
            logger.warning("USE_GROQ is disabled. Falling back to rule-based.")
            self.llm_type = "Rule-based (USE_GROQ=false)"
            return
        
        if not Settings.GROQ_API_KEY or len(Settings.GROQ_API_KEY) < 20:
            print("❌ GROQ_API_KEY not set or invalid!")
            print("   Get free API key: https://console.groq.com")
            logger.warning("GROQ_API_KEY not configured. Falling back to rule-based.")
            self.llm_type = "Rule-based (No API key)"
            return
        
        # Try to initialize Groq client
        print("🔄 Attempting to initialize Groq client...")
        try:
            self.llm_client = Groq(api_key=Settings.GROQ_API_KEY)
            self.llm_type = f"Groq ({Settings.GROQ_MODEL})"
            
            print(f"✅ SUCCESS! Groq API initialized")
            print(f"   Model: {Settings.GROQ_MODEL}")
            print(f"   API Key: {Settings.GROQ_API_KEY[:20]}...")
            logger.info(f"✅ Using Groq API (FREE!) - Model: {Settings.GROQ_MODEL}")
            
        except Exception as e:
            print(f"❌ Failed to initialize Groq: {e}")
            logger.error(f"Failed to initialize Groq: {e}")
            self.llm_type = "Rule-based (Groq init failed)"
    
    def classify(self, command_text):
        """
        Classify command and extract intent
        
        Args:
            command_text: User's command text
            
        Returns:
            dict: Classification result with intent, action, and parameters
        """
        # Use Groq if available
        if self.llm_client:
            return self._classify_with_groq(command_text)
        
        # Fallback to rule-based
        print(f"⚠️  Using rule-based classification for: {command_text}")
        return self._classify_rule_based(command_text)
    
    def _classify_with_groq(self, command_text):
        """Classify using Groq API (FREE & FAST!)"""
        
        system_prompt = f"""You are a command classifier for voice assistant "{Settings.ASSISTANT_NAME}".


Classify commands into these categories:
1. open_app - Opening applications
   Examples: notepad, word, excel, vscode, calculator, camera, chrome, firefox, edge, spotify, 
   file_explorer, this_pc, downloads, documents, pictures, c_drive, task_manager, control_panel, 
   cmd, powershell, paint, snipping_tool

2. open_website - Opening websites
   Examples: gmail, youtube, github, google, chatgpt, whatsapp, facebook, instagram, twitter, 
   linkedin, netflix, amazon

3. system_info - System information (time, date, battery)

4. file_operation - File management (create folder, clean downloads)

5. workflow - Complex workflows (start my day, end my day)

6. unknown - Cannot classify

IMPORTANT RULES:
- For "play music" or "spotify" → open_app with action "spotify"
- For "open chrome" or "browser" → open_app with action "chrome"
- For "file explorer" or "open folders" → open_app with action "file_explorer"
- For "downloads folder" → open_app with action "downloads"
- For "c drive" → open_app with action "c_drive"
- For any folder/drive request → open_app with appropriate action
- If command is vague like "open music", infer best app (spotify)
- If command is vague like "open browser", infer best app (chrome)

Return ONLY valid JSON with NO markdown formatting:
{{"intent": "category", "action": "specific_action", "confidence": 0.0-1.0, "parameters": {{}}}}

Examples:
"open notepad" → {{"intent": "open_app", "action": "notepad", "confidence": 0.95, "parameters": {{}}}}
"play music" → {{"intent": "open_app", "action": "spotify", "confidence": 0.90, "parameters": {{}}}}
"open chrome" → {{"intent": "open_app", "action": "chrome", "confidence": 0.95, "parameters": {{}}}}
"open downloads folder" → {{"intent": "open_app", "action": "downloads", "confidence": 0.95, "parameters": {{}}}}
"open c drive" → {{"intent": "open_app", "action": "c_drive", "confidence": 0.95, "parameters": {{}}}}
"what time" → {{"intent": "system_info", "action": "time", "confidence": 0.9, "parameters": {{}}}}"""

        try:
            print(f"\n🔍 Classifying with Groq: '{command_text}'")
            
            response = self.llm_client.chat.completions.create(
                model=Settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Classify: {command_text}"}
                ],
                temperature=0.2,
                max_tokens=150
            )
            
            result_text = response.choices[0].message.content.strip()
            print(f"📥 Groq response: {result_text}")
            
            # Extract JSON (remove markdown code blocks if present)
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            # Extract JSON
            if "{" in result_text:
                json_start = result_text.index("{")
                json_end = result_text.rindex("}") + 1
                result = json.loads(result_text[json_start:json_end])
                
                print(f"✅ Classification: {result['intent']} → {result['action']} (confidence: {result['confidence']})")
                logger.info(f"Groq Classification: {result}")
                return result
            else:
                raise ValueError("No JSON in response")
                
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            logger.error(f"Groq API error: {e}")
            print(f"⚠️  Falling back to rule-based classification")
            return self._classify_rule_based(command_text)
    
    def _classify_rule_based(self, command_text):
        """Fallback rule-based classification"""
        command_lower = command_text.lower()
        
        print(f"🔍 Rule-based classification for: '{command_text}'")
        
        # Check for applications
        for app_name, app_data in self.commands_config.get("applications", {}).items():
            for keyword in app_data.get("keywords", []):
                if keyword in command_lower:
                    result = {
                        "intent": "open_app",
                        "action": app_name,
                        "parameters": {},
                        "confidence": 0.9
                    }
                    print(f"✅ Matched: {result}")
                    return result
        
        # Check for websites
        for site_name, site_data in self.commands_config.get("websites", {}).items():
            for keyword in site_data.get("keywords", []):
                if keyword in command_lower:
                    result = {
                        "intent": "open_website",
                        "action": site_name,
                        "parameters": {},
                        "confidence": 0.9
                    }
                    print(f"✅ Matched: {result}")
                    return result
        
        # Check for workflows
        for workflow_name, workflow_data in self.commands_config.get("workflows", {}).items():
            for keyword in workflow_data.get("keywords", []):
                if keyword in command_lower:
                    result = {
                        "intent": "workflow",
                        "action": workflow_name,
                        "parameters": {},
                        "confidence": 0.85
                    }
                    print(f"✅ Matched: {result}")
                    return result
        
        # Check for system commands
        for cmd_name, cmd_data in self.commands_config.get("system_commands", {}).items():
            for keyword in cmd_data.get("keywords", []):
                if keyword in command_lower:
                    result = {
                        "intent": "system_info",
                        "action": cmd_name,
                        "parameters": {},
                        "confidence": 0.95
                    }
                    print(f"✅ Matched: {result}")
                    return result
        
        # Unknown
        print(f"❌ No match found - returning unknown")
        return {
            "intent": "unknown",
            "action": None,
            "parameters": {},
            "confidence": 0.0
        }

# Global classifier instance
classifier = CommandClassifier()