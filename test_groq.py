# test_groq.py
try:
    from groq import Groq
    print("✅ Groq module installed!")
except ImportError:
    print("❌ Groq module NOT installed!")
    print("Run: pip install groq")