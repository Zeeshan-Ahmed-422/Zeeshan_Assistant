"""
Helper Functions for Voice Assistant
"""
import os
import json
from datetime import datetime

def load_json(filepath, default=None):
    """Load JSON file safely"""
    if default is None:
        default = {}
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return default

def save_json(filepath, data):
    """Save data to JSON file safely"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date_str():
    """Get current date as string"""
    return datetime.now().strftime("%Y-%m-%d")

def get_time_str():
    """Get current time as string"""
    return datetime.now().strftime("%H:%M:%S")

def normalize_text(text):
    """Normalize text for comparison"""
    return text.lower().strip()

def extract_keywords(text, keywords_list):
    """Check if any keyword exists in text"""
    normalized_text = normalize_text(text)
    for keyword in keywords_list:
        if normalize_text(keyword) in normalized_text:
            return True
    return False