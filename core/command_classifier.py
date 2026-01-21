"""
Command Classifier - API-Based (Simple & Easy)
Supports: Groq (Free!), OpenAI, Anthropic
"""
import json
from config.settings import Settings
from utils.logger import logger
from utils.helpers import load_json

# Import API clients
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logger.warning("Groq not available. Install: pip install groq")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available. Install: pip install openai")

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic not available. Install: pip install anthropic")

class CommandClassifier:
    """Classify commands using API-based LLMs"""
    
    def __init__(self):
        """Initialize classifier with API client"""
        self.commands_config = load_json(Settings.COMMANDS_CONFIG_FILE)
        self.llm_client = None
        self.llm_type = None
        
        # Initialize API client
        self._initialize_llm()
        
        logger.info(f"Command classifier initialized with {self.llm_type}")
    
    def _initialize_llm(self):
        """Initialize API client (Groq, OpenAI, or Anthropic)"""
        
        # Try Groq first (FREE & FAST!)
        if Settings.USE_GROQ and Settings.GROQ_API_KEY and GROQ_AVAILABLE:
            try:
                self.llm_client = Groq(api_key=Settings.GROQ_API_KEY)
                self.llm_type = f"Groq ({Settings.GROQ_MODEL})"
                logger.info(f"✅ Using Groq API (FREE!) - Model: {Settings.GROQ_MODEL}")
                return
            except Exception as e:
                logger.error(f"Failed to initialize Groq: {e}")
        
        # Try OpenAI
        if Settings.USE_OPENAI and Settings.OPENAI_API_KEY and OPENAI_AVAILABLE:
            try:
                self.llm_client = OpenAI(api_key=Settings.OPENAI_API_KEY)
                self.llm_type = f"OpenAI ({Settings.OPENAI_MODEL})"
                logger.info(f"✅ Using OpenAI API - Model: {Settings.OPENAI_MODEL}")
                return
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI: {e}")
        
        # Try Anthropic
        if Settings.USE_ANTHROPIC and Settings.ANTHROPIC_API_KEY and ANTHROPIC_AVAILABLE:
            try:
                self.llm_client = Anthropic(api_key=Settings.ANTHROPIC_API_KEY)
                self.llm_type = f"Anthropic ({Settings.ANTHROPIC_MODEL})"
                logger.info(f"✅ Using Anthropic API - Model: {Settings.ANTHROPIC_MODEL}")
                return
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic: {e}")
        
        # Fallback to rule-based
        logger.warning("⚠️ No API configured. Using rule-based classification")
        logger.info("💡 Get free Groq API key: https://console.groq.com")
        self.llm_type = "Rule-based (No API)"
    
    def classify(self, command_text):
        """
        Classify command and extract intent
        
        Args:
            command_text: User's command text
            
        Returns:
            dict: Classification result with intent, action, and parameters
        """
        if self.llm_client:
            if "Groq" in self.llm_type:
                return self._classify_with_groq(command_text)
            elif "OpenAI" in self.llm_type:
                return self._classify_with_openai(command_text)
            elif "Anthropic" in self.llm_type:
                return self._classify_with_anthropic(command_text)
        
        return self._classify_rule_based(command_text)
    
    def _classify_with_groq(self, command_text):
        """Classify using Groq API (FREE & FAST!)"""
        
        system_prompt = f"""You are a command classifier for voice assistant "{Settings.ASSISTANT_NAME}".
Classify commands into these categories:
1. open_app - Opening applications (notepad, word, excel, vscode, browser, calculator)
2. open_website - Opening websites (gmail, youtube, github, google, chatgpt)
3. system_info - System information (time, date, battery)
4. file_operation - File management (create folder, clean downloads)
5. workflow - Complex workflows (start my day, end my day)
6. unknown - Cannot classify

Return ONLY valid JSON:
{{"intent": "category", "action": "specific_action", "confidence": 0.0-1.0, "parameters": {{}}}}

Examples:
"open notepad" → {{"intent": "open_app", "action": "notepad", "confidence": 0.95, "parameters": {{}}}}
"what time" → {{"intent": "system_info", "action": "time", "confidence": 0.9, "parameters": {{}}}}
"start my day" → {{"intent": "workflow", "action": "start_my_day", "confidence": 0.85, "parameters": {{}}}}"""

        try:
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
            
            # Extract JSON
            if "{" in result_text:
                json_start = result_text.index("{")
                json_end = result_text.rindex("}") + 1
                result = json.loads(result_text[json_start:json_end])
                
                logger.info(f"Groq Classification: {result}")
                return result
            else:
                raise ValueError("No JSON in response")
                
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return self._classify_rule_based(command_text)
    
    def _classify_with_openai(self, command_text):
        """Classify using OpenAI API"""
        
        system_prompt = f"""You are a command classifier for voice assistant "{Settings.ASSISTANT_NAME}".
Classify into: open_app, open_website, system_info, file_operation, workflow, unknown.

Return ONLY JSON:
{{"intent": "category", "action": "specific_action", "confidence": 0.0-1.0, "parameters": {{}}}}"""

        try:
            response = self.llm_client.chat.completions.create(
                model=Settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Classify: {command_text}"}
                ],
                temperature=0.2,
                max_tokens=150
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            if "{" in result_text:
                json_start = result_text.index("{")
                json_end = result_text.rindex("}") + 1
                result = json.loads(result_text[json_start:json_end])
                logger.info(f"OpenAI Classification: {result}")
                return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._classify_rule_based(command_text)
    
    def _classify_with_anthropic(self, command_text):
        """Classify using Anthropic API"""
        
        system_prompt = f"""Classify voice commands for assistant "{Settings.ASSISTANT_NAME}".
Categories: open_app, open_website, system_info, file_operation, workflow, unknown.
Return JSON only: {{"intent": "...", "action": "...", "confidence": 0-1, "parameters": {{}}}}"""

        try:
            response = self.llm_client.messages.create(
                model=Settings.ANTHROPIC_MODEL,
                max_tokens=150,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"Classify: {command_text}"}
                ]
            )
            
            result_text = response.content[0].text.strip()
            
            # Parse JSON
            if "{" in result_text:
                json_start = result_text.index("{")
                json_end = result_text.rindex("}") + 1
                result = json.loads(result_text[json_start:json_end])
                logger.info(f"Anthropic Classification: {result}")
                return result
                
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return self._classify_rule_based(command_text)
    
    def _classify_rule_based(self, command_text):
        """Fallback rule-based classification"""
        command_lower = command_text.lower()
        
        # Check for applications
        for app_name, app_data in self.commands_config.get("applications", {}).items():
            for keyword in app_data.get("keywords", []):
                if keyword in command_lower:
                    return {
                        "intent": "open_app",
                        "action": app_name,
                        "parameters": {},
                        "confidence": 0.9
                    }
        
        # Check for websites
        for site_name, site_data in self.commands_config.get("websites", {}).items():
            for keyword in site_data.get("keywords", []):
                if keyword in command_lower:
                    return {
                        "intent": "open_website",
                        "action": site_name,
                        "parameters": {},
                        "confidence": 0.9
                    }
        
        # Check for workflows
        for workflow_name, workflow_data in self.commands_config.get("workflows", {}).items():
            for keyword in workflow_data.get("keywords", []):
                if keyword in command_lower:
                    return {
                        "intent": "workflow",
                        "action": workflow_name,
                        "parameters": {},
                        "confidence": 0.85
                    }
        
        # Check for system commands
        for cmd_name, cmd_data in self.commands_config.get("system_commands", {}).items():
            for keyword in cmd_data.get("keywords", []):
                if keyword in command_lower:
                    return {
                        "intent": "system_info",
                        "action": cmd_name,
                        "parameters": {},
                        "confidence": 0.95
                    }
        
        # Unknown
        return {
            "intent": "unknown",
            "action": None,
            "parameters": {},
            "confidence": 0.0
        }

# Global classifier instance
classifier = CommandClassifier()
