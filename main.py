import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import system_prompt
from functions.function_schemas import schema_get_files_content, schema_get_files_info, schema_run_python_file, schema_write_file
from call_function import call_function

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
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt.removesuffix("--verbose"))])
    ]
    try:
        for _ in range(20):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            messages.append(types.Content(role="model", parts=[types.Part(text=part.text)]))
            #     messages.append(types.Content(role="model", parts=[types.Part(text=candidate.content)]))
            
            if response.function_calls:
                function_call_result = call_function(*response.function_calls, verbose=verbose)
                messages.append(
                types.Content(
                    role="user", 
                    parts=[types.Part(function_response=function_call_result.parts[0].function_response)]))
            elif response.text:
                print(response.text)
                break
    except Exception as e:
        print(f"Error: {e}")    

def get_prompt_from_cmdl():
    cmd_args = sys.argv[1:]
    if not cmd_args:
        print("Usage: uv run main.py \"write_prompt_here\"")
        sys.exit(1)
    prompt_entered = " ".join(cmd_args)
    return prompt_entered

if __name__ == "__main__":
    main()
