import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from agentic-ai-editor!")

def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return api_key

def generate_response():
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    print(response.text)

if __name__ == "__main__":
    main()
