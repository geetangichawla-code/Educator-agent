from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GROQ_API_KEY")

# Check 1: Is the key loading at all?
if not key:
    print("❌ GROQ_API_KEY is None — .env file not found or key name is wrong")
else:
    print(f"✅ Key loaded: {key[:8]}...{key[-4:]}")
    print(f"   Full length: {len(key)} characters")
    print(f"   Starts with 'gsk_': {key.startswith('gsk_')}")

# Check 2: Try the actual API call
client = Groq(api_key=key)

try:
    response = client.chat.completions.create(
       model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": "Say hi"}],
        max_tokens=10
    )
    print("✅ API call succeeded:", response.choices[0].message.content)
except Exception as e:
    print(f"❌ API call failed: {e}")