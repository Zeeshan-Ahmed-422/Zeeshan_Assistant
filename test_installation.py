"""
Test Script for Voice Assistant
Verifies that all dependencies are installed correctly
"""
import sys

print("🧪 Testing Voice Assistant Dependencies...")
print("=" * 60)

# Test 1: Python version
print("\n1. Python Version:")
print(f"   ✓ Python {sys.version}")

# Test 2: Speech Recognition
try:
    import speech_recognition as sr
    print("\n2. Speech Recognition:")
    print("   ✓ speech_recognition installed")
    
    # Test microphone
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("   ✓ Microphone detected")
    except Exception as e:
        print(f"   ⚠ Microphone issue: {e}")
except ImportError:
    print("\n2. Speech Recognition:")
    print("   ✗ speech_recognition NOT installed")
    print("   → pip install SpeechRecognition")

# Test 3: Text-to-Speech
try:
    import pyttsx3
    print("\n3. Text-to-Speech:")
    print("   ✓ pyttsx3 installed")
    
    # Test TTS engine
    try:
        engine = pyttsx3.init()
        print("   ✓ TTS engine initialized")
    except Exception as e:
        print(f"   ⚠ TTS engine issue: {e}")
except ImportError:
    print("\n3. Text-to-Speech:")
    print("   ✗ pyttsx3 NOT installed")
    print("   → pip install pyttsx3")

# Test 4: LLM Libraries
print("\n4. LLM Support:")
try:
    import openai
    print("   ✓ OpenAI library installed")
except ImportError:
    print("   ⚠ OpenAI library not installed (optional)")

try:
    import anthropic
    print("   ✓ Anthropic library installed")
except ImportError:
    print("   ⚠ Anthropic library not installed (optional)")

# Test 5: Memory/RAG Support
print("\n5. Memory System:")
try:
    import chromadb
    print("   ✓ ChromaDB installed")
except ImportError:
    print("   ⚠ ChromaDB not installed (memory features limited)")

try:
    from sentence_transformers import SentenceTransformer
    print("   ✓ Sentence Transformers installed")
except ImportError:
    print("   ⚠ Sentence Transformers not installed (memory features limited)")

# Test 6: Utilities
print("\n6. Utility Libraries:")
try:
    import numpy
    print("   ✓ NumPy installed")
except ImportError:
    print("   ⚠ NumPy not installed")

try:
    import pandas
    print("   ✓ Pandas installed")
except ImportError:
    print("   ⚠ Pandas not installed")

try:
    from dotenv import load_dotenv
    print("   ✓ python-dotenv installed")
except ImportError:
    print("   ⚠ python-dotenv not installed")

# Test 7: Environment Configuration
print("\n7. Configuration:")
import os
if os.path.exists('.env'):
    print("   ✓ .env file found")
    
    # Check for API keys
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.getenv('OPENAI_API_KEY'):
        print("   ✓ OpenAI API key configured")
    elif os.getenv('ANTHROPIC_API_KEY'):
        print("   ✓ Anthropic API key configured")
    else:
        print("   ⚠ No API key configured (will use rule-based classification)")
else:
    print("   ⚠ .env file not found")
    print("   → Copy .env.example to .env and configure")

# Test 8: Project Structure
print("\n8. Project Structure:")
required_dirs = ['config', 'core', 'memory', 'actions', 'utils', 'data']
for directory in required_dirs:
    if os.path.exists(directory):
        print(f"   ✓ {directory}/ found")
    else:
        print(f"   ✗ {directory}/ missing")

# Final Summary
print("\n" + "=" * 60)
print("🎯 Test Summary:")
print("   If you see ✓ for tests 1-3, you're ready to start!")
print("   Other features are optional but recommended.")
print("\n💡 Next Step:")
print("   Run: python main.py")
print("=" * 60)