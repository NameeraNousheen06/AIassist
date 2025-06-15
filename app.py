# streamlit_app.py
import streamlit as st
import google.generativeai as genai
import time

# Direct API Key
API_KEY = "AIzaSyAQJ3zz-Qr9A2p0ZNjy6AETpndobFnFEGo"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-8b-latest")

st.set_page_config(page_title="Fin Assistant 💸", page_icon="💬")
st.title("💬 Fin Assistant - Your AI Finance Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
prompt = st.chat_input("Ask a financial question...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retry if quota exceeded
    retry_attempts = 3
    reply = ""
    for attempt in range(retry_attempts):
        try:
            response = model.generate_content(prompt)
            reply = response.text
            break
        except Exception as e:
            if "429" in str(e) and attempt < retry_attempts - 1:
                time.sleep(5)
            else:
                reply = f"⚠ Error: {e}\n\nPlease wait or check [Gemini API quota](https://ai.google.dev/gemini-api/docs/rate-limits)"
                break

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)