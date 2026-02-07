# api calls and other gemini related functionality

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents="Say 'System online!'"
    )
    print("--- SUCCESS ---")
    print(response.text)
except Exception as e:
    print("--- FAILURE ---")
    print(f"Error: {e}")