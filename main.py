import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    generate_response()
    # get_prompt_from_cmdl()

def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return api_key

def generate_response():
    client = genai.Client(api_key=get_api_key())
    user_prompt = get_prompt_from_cmdl()

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt.removesuffix("--verbose"))])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages
    )
    print(response.text)
    if user_prompt.endswith("--verbose"):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    

def get_prompt_from_cmdl():
    cmd_args = sys.argv[1:]
    if not cmd_args:
        print("Usage: uv run main.py \"write_prompt_here\"")
        sys.exit(1)
    prompt_entered = " ".join(cmd_args)
    return prompt_entered

if __name__ == "__main__":
    main()
