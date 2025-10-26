"""Quick API Test - Verify all APIs are working"""

import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

print("="*70)
print("QUICK API TEST")
print("="*70)

# Test 1: Environment variables loaded
print("\n[1] Checking API Keys...")
openai_key = os.getenv("OPENAI_API_KEY")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

print(f"✓ OpenAI: {openai_key[:20]}..." if openai_key else "❌ OpenAI: Not found")
print(f"✓ DeepSeek: {deepseek_key[:20]}..." if deepseek_key else "❌ DeepSeek: Not found")
print(f"✓ Gemini: {gemini_key[:20]}..." if gemini_key else "❌ Gemini: Not found")

# Test 2: Simple OpenAI call
print("\n[2] Testing OpenAI...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=50
    )
    print(f"✓ OpenAI works! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI error: {e}")

# Test 3: Simple Gemini call
print("\n[3] Testing Gemini...")
try:
    import google.generativeai as genai
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hi")
    print(f"✓ Gemini works! Response: {response.text}")
except Exception as e:
    print(f"❌ Gemini error: {e}")

# Test 4: Simple DeepSeek call
print("\n[4] Testing DeepSeek...")
try:
    import requests
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {deepseek_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 50
        },
        timeout=30
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✓ DeepSeek works! Response: {result['choices'][0]['message']['content']}")
    else:
        print(f"❌ DeepSeek error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ DeepSeek error: {e}")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
