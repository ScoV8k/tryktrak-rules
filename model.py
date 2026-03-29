import os
from google import genai
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

api_key = os.environ.get("GEMINI_API")
if not api_key:
    print("Błąd: Brak klucza API w pliku .env!")
    exit()

client = genai.Client(api_key=api_key)

def prepare_text_chunks(file_path: str):
    try:
        loader = TextLoader(file_path, encoding="utf-8")
        document = loader.load()
    except Exception as e:
        print(f"Błąd podczas ładowania pliku: {e}")
        return None
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    text_chunks = text_splitter.split_documents(document)
    
    print(f"Sukces! Plik wczytany i podzielony na {len(text_chunks)} kawałków.")
    return text_chunks


def create_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", 
        google_api_key=api_key
    )
    vector_store = Chroma.from_documents(text_chunks, embeddings)
    
    print("Sukces! Kawałki tekstu zamienione na wektory i zapisane w bazie FAISS.")
    return vector_store


def get_gemini_response(prompt: str, vector_store) -> str:
    """
    Wyszukuje kontekst w bazie wektorowej, buduje poszerzony prompt
    i wysyła zapytanie do modelu Gemini.
    """
    try:
        if vector_store is None:
            return "Błąd: Baza wektorowa nie jest zainicjalizowana!"
        
        relevant_documents = vector_store.similarity_search(prompt, k=3)
        
        context = "\n\n".join([doc.page_content for doc in relevant_documents])

        augmented_prompt = f"""
Jesteś asystentem odpowiadającym na pytania WYŁĄCZNIE na podstawie poniższego tekstu.
Jeśli nie znajdziesz odpowiedzi w tekście, powiedz: "Niestety, nie znajduję tej informacji w instrukcji."
Nie używaj wiedzy zewnętrznej.

KONTEKST:
{context}

PYTANIE:
{prompt}
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=augmented_prompt
        )
        return response.text
        
    except Exception as e:
        return f"Wystąpił błąd podczas komunikacji z API: {e}"
