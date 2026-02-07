import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load your .env file
load_dotenv()

# 2. Initialize the Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_flash(prompt):
    try:
        # Use only the 2026 Gemini 3 Flash model
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                # 'MINIMAL' is perfect for hackathons: fast and low-cost
                thinking_config=types.ThinkingConfig(
                    thinking_level=types.ThinkingLevel.MINIMAL
                )
            )
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "Error: Rate limit reached. Wait 60 seconds."
        return f"Error: {e}"

# 3. Simple Test
if __name__ == "__main__":
    query = "Give me a one-sentence elevator pitch for a hackathon project using AI."
    print("Gemini 3 Flash says:")
    print(ask_flash(query))