import streamlit as st
from model import get_gemini_response

st.set_page_config(page_title="Sędzia Tryktraka", page_icon="🎲")
st.title("🎲 Asystent: Tryktrak")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("Zadaj pytanie (np. 'Czym jest Tryktrak?')..."):
    
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Myślę..."):

            answer = get_gemini_response(user_question)
            
            st.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})