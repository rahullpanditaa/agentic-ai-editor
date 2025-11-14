import os
from google import genai
from dotenv import load_dotenv

SYSTEM_PROMPT = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

MODEL = "gemini-2.0-flash-001"

def gemini_client_setup() -> genai.Client:
    load_dotenv()
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except Exception as e:
        print("Unable to load GEMINI_API_KEY from .env file:")
        print(e)
    client = genai.Client(api_key=api_key)
    return client