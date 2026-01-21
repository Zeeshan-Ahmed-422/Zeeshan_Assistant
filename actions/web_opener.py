"""
Web Opener
Opens websites in default browser
"""
import webbrowser
from config.settings import Settings
from utils.logger import logger
from utils.helpers import load_json

class WebOpener:
    """Open websites in browser"""
    
    def __init__(self):
        """Initialize web opener"""
        self.commands_config = load_json(Settings.COMMANDS_CONFIG_FILE)
        logger.info("Web opener initialized")
    
    def open_website(self, site_name):
        """
        Open a website
        
        Args:
            site_name: Name of website to open
            
        Returns:
            bool: True if successful
        """
        try:
            # Get website configuration
            site_config = self.commands_config.get("websites", {}).get(site_name)
            
            if not site_config:
                logger.error(f"Unknown website: {site_name}")
                return False
            
            url = site_config.get("url")
            
            # Open in browser
            webbrowser.open(url)
            logger.info(f"Opened website: {site_name} ({url})")
            return True
            
        except Exception as e:
            logger.error(f"Error opening website {site_name}: {e}")
            return False
    
    def open_url(self, url):
        """
        Open a custom URL
        
        Args:
            url: URL to open
            
        Returns:
            bool: True if successful
        """
        try:
            if not url.startswith("http"):
                url = "https://" + url
            
            webbrowser.open(url)
            logger.info(f"Opened URL: {url}")
            return True
            
        except Exception as e:
            logger.error(f"Error opening URL {url}: {e}")
            return False
    
    def search_google(self, query):
        """
        Search on Google
        
        Args:
            query: Search query
            
        Returns:
            bool: True if successful
        """
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            logger.info(f"Searched Google for: {query}")
            return True
            
        except Exception as e:
            logger.error(f"Error searching Google: {e}")
            return False
    
    def play_youtube(self, query):
        """
        Play video on YouTube
        
        Args:
            query: Video search query
            
        Returns:
            bool: True if successful
        """
        try:
            # Try using pywhatkit if available
            try:
                import pywhatkit as kit
                kit.playonyt(query)
                logger.info(f"Playing on YouTube: {query}")
                return True
            except ImportError:
                # Fallback to search
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                logger.info(f"Opened YouTube search for: {query}")
                return True
                
        except Exception as e:
            logger.error(f"Error playing YouTube video: {e}")
            return False

# Global web opener instance
web_opener = WebOpener()