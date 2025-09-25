import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import system_prompt
from functions.function_schemas import schema_get_files_content, schema_get_files_info, schema_run_python_file, schema_write_file

def main():
    generate_response()

def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return api_key

def generate_response():
    client = genai.Client(api_key=get_api_key())
    user_prompt = get_prompt_from_cmdl()
    verbose = "--verbose" in sys.argv

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt.removesuffix("--verbose"))])
    ]
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )    

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
