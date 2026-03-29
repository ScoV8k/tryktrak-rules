import streamlit as st
import os
from model import get_gemini_response, prepare_text_chunks, create_vector_store

st.set_page_config(page_title="Sędzia Tryktraka", page_icon="🎲")
st.title("🎲 Asystent: Tryktrak")

@st.cache_resource
def load_vector_store():
    file_path = "zasady.txt"
    if not os.path.exists(file_path):
        return None
        
    chunks = prepare_text_chunks(file_path)
    if chunks:
        vector_store = create_vector_store(chunks)
        return vector_store
    return None

db = load_vector_store()

if db is None:
    st.error("Błąd: Nie znaleziono pliku 'zasady.txt' lub jest on pusty. Utwórz plik, aby rozpocząć czat.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if db is not None:
    if user_question := st.chat_input("Zadaj pytanie (np. 'Czym jest Tryktrak?')..."):
        
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Myślę..."):
                
                answer = get_gemini_response(user_question, db)
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})