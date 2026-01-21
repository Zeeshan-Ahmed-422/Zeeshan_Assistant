# test_env_simple.py (encoding fix ke sath)
import os
from dotenv import load_dotenv

print("=" * 60)
print("Testing .env File Loading")
print("=" * 60)

# Check if .env exists
if os.path.exists('.env'):
    print("✅ .env file exists")
else:
    print("❌ .env file NOT found!")

print("\n" + "=" * 60)
print("Loading environment variables...")
print("=" * 60)

# Load .env
load_dotenv(override=True)

# Check variables
use_groq = os.getenv("USE_GROQ")
groq_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL")

print(f"\nUSE_GROQ: {use_groq}")
print(f"GROQ_MODEL: {groq_model}")

if groq_key and len(groq_key) > 10:
    print(f"GROQ_API_KEY: {groq_key[:20]}... (length: {len(groq_key)}) ✅")
elif groq_key:
    print(f"GROQ_API_KEY: {groq_key} ❌ (Too short!)")
else:
    print("GROQ_API_KEY: ❌ NOT SET OR EMPTY")

print("\n" + "=" * 60)
print("Testing Settings Class")
print("=" * 60)

from config.settings import Settings

print(f"\nSettings.USE_GROQ: {Settings.USE_GROQ}")
print(f"Settings.GROQ_MODEL: {Settings.GROQ_MODEL}")

if Settings.GROQ_API_KEY and len(Settings.GROQ_API_KEY) > 10:
    print(f"Settings.GROQ_API_KEY: {Settings.GROQ_API_KEY[:20]}... ✅ LOADED!")
elif Settings.GROQ_API_KEY:
    print(f"Settings.GROQ_API_KEY: '{Settings.GROQ_API_KEY}' ❌ (Placeholder!)")
else:
    print("Settings.GROQ_API_KEY: ❌ EMPTY!")

print("\n" + "=" * 60)
print("FINAL STATUS:")
if Settings.USE_GROQ and Settings.GROQ_API_KEY and len(Settings.GROQ_API_KEY) > 20:
    print("✅ Groq API should work!")
else:
    print("❌ Groq API will NOT work!")
    print("\nFix:")
    print("1. Edit .env file")
    print("2. Set GROQ_API_KEY=gsk_your_actual_key")
    print("3. Get key from: https://console.groq.com")
print("=" * 60)