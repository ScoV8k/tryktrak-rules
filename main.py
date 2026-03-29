import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

klucz_api = os.environ.get("GOOGLE_API") or os.environ.get("GEMINI_API")
genai.configure(api_key=klucz_api)

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    print("Skonfigurowano model. Wysyłam zapytanie do API...")

    prompt = "Cześć! Wygeneruj jedno krótkie zdanie, które potwierdzi, że działasz i wiesz, czym jest gra Tryktrak."
    
    response = model.generate_content(prompt)
    
    print("\n--- Odpowiedź od Gemini ---")
    print(response.text)
    print("---------------------------\n")
    print("Sukces! API działa poprawnie.")

except Exception as e:
    print(f"\n[BŁĄD] Wystąpił problem z połączeniem lub kluczem API:\n{e}")