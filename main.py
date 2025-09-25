import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.function_schemas import schema_get_files_info

def main():
    generate_response()

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
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info
        ]
    )
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if user_prompt.endswith("--verbose"):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

    if response.function_calls:
        for f in response.function_calls:
            print(f"Calling function: {f.name}({f.args})")
    else:
        print(response.text)

    
    

def get_prompt_from_cmdl():
    cmd_args = sys.argv[1:]
    if not cmd_args:
        print("Usage: uv run main.py \"write_prompt_here\"")
        sys.exit(1)
    prompt_entered = " ".join(cmd_args)
    return prompt_entered

if __name__ == "__main__":
    main()
