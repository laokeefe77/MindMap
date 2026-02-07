import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load your API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_learning_map(topic):
    # System instructions move from the Client to the Config
    sys_instruct = """
    You are a structural data architect. 
    Your only job is to produce deeply nested JSON learning maps. 
    You have a 'Zero-List-in-Description' policy: descriptions must be prose only. 
    All components must be represented as child nodes.
    """

    prompt = f"""
        Create a comprehensive hierarchical learning roadmap for: '{topic}'.

        STRICT HIERARCHY RULES:
        1. Every specific concept, sub-tool, or sub-topic MUST be its own node in the 'children' list.
        2. The 'description' field must ONLY explain the "What" and "Why" of the current node. 
        3. NEVER list sub-topics, bullet points, or comma-separated lists inside a 'description'. 
        4. If you find yourself writing a list in a description, stop and move those items into the 'children' array instead.
        5. Aim for at least 3 levels of depth where appropriate (e.g., Math -> Linear Algebra -> Matrices).

        JSON STRUCTURE:
        Each node must be an object: {{"name": "...", "description": "...", "children": []}}.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct,
            response_mime_type="application/json",
            temperature=1.0, # Higher temperature for more detailed branching
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.MINIMAL
            )
        )
    )
    
    return json.loads(response.text)

# Example Usage
if __name__ == "__main__":
    topic = "Machine Learning" 
    mind_map = generate_learning_map(topic)
    
    print(json.dumps(mind_map, indent=2))

    print(f"\nMain branches for {topic}:")
    for branch in mind_map.get('children', []):
        print(f"- {branch['name']}")