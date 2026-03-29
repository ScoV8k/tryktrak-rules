import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

klucz_api = os.environ.get("GEMINI_API")

client = genai.Client(api_key=klucz_api)

def get_gemini_response(prompt: str) -> str:
    """
    Wysyła zapytanie do modelu Gemini i zwraca odpowiedź w formie tekstu.
    To tutaj w przyszłości wepniemy logikę RAG (czytanie plików tekstowych).
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Wystąpił błąd podczas komunikacji z API: {e}"