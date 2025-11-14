import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from .utils import (
    MODEL,
    SYSTEM_PROMPT, 
    gemini_client_setup,
)
from functions.function_schemas import (
    schema_get_files_content, 
    schema_get_files_info, 
    schema_run_python_file, 
    schema_write_file
)
from call_function import call_function

def main():
    generate_response()

# def get_api_key():
#     load_dotenv()
#     api_key = os.environ.get("GEMINI_API_KEY")
#     return api_key

def generate_response():
    client = gemini_client_setup()
    user_prompt = _get_prompt_from_cmdl()

    # check if verbose flag is in command line args
    verbose = "--verbose" in sys.argv    
    
    # Creating a Tool object/ instance of a Tool class
    # tool - a function that LLM is allowed to call
    # while generating a response
    available_functions = types.Tool(
        # list of schemas i.e. function descriptions
        # of the functions LLM can use
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    # chat history
    messages = [
        # Content object - contains the parts of a message
        # role=user, marks as message coming from user in chat history
        # parts = [..] ,list containing the content being sent in message
        # initialize conversation history by sending a 'user' message, --verbose removed from end
        types.Content(role="user", parts=[types.Part(text=user_prompt.removesuffix("--verbose"))])
    ]
    try:
        # Agent loop
        for _ in range(20):
            # send a request to Gemini
            response = client.models.generate_content(
                model=MODEL, 
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)
            )
            # Gemini returns 1 or more candidates (i.e. possible outputs)
            # loop through them all
            for candidate in response.candidates:
                # if candidate contains content, and the content has some parts
                if candidate.content and candidate.content.parts:
                    # loop through each part, 
                    for part in candidate.content.parts:
                        # if part contains text,
                        if part.text:
                            # add the text to messages
                            messages.append(types.Content(role="model", parts=[types.Part(text=part.text)]))
            
            # function_calls - list of function calls in response
            # if this condition is True, model wants to execute 
            # one of the available tools/functions
            if response.function_calls:
                # a list of Contents, where each Content is 
                # the result of calling the tool with its args
                function_call_results = call_function(response.function_calls, verbose=verbose)
                for function_call_result in function_call_results:
                    messages.append(
                        types.Content(
                            role="model",
                            parts=[types.Part(
                                function_response=function_call_result.parts[0].function_response
                            )]
                        )
                    )
            
            #     messages.append(
            #     types.Content(
            #         role="model", 
            #         parts=[types.Part(function_response=function_call_result.parts[0].function_response)]))
            
            # LLM decides to produce text, not call function
            elif response.text:
                print(response.text)
                break
    except Exception as e:
        print(f"Error: {e}")    


# grabs all args after main.py
# if not provided, print error message, exit
# convert into str, return
def _get_prompt_from_cmdl():
    cmd_args = sys.argv[1:]
    if not cmd_args:
        print("Usage: uv run main.py \"write_prompt_here\"")
        sys.exit(1)
    prompt_entered = " ".join(cmd_args)
    return prompt_entered

# def gemini_client_setup():
#     load_dotenv()
#     try:
#         api_key = os.environ.get("GEMINI_API_KEY")
#     except Exception as e:
#         print("Unable to load GEMINI_API_KEY from .env file:")
#         print(e)
#     client = genai.Client(api_key=api_key)
#     return client


if __name__ == "__main__":
    main()
