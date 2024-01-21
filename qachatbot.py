from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_res(que):
    res = chat.send_message(que, stream=True)
    return res

st.set_page_config(page_title="QnA chatbot")
st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key="input")
submit = st.button('Get the response')

if submit and input:
    res = get_gemini_res(input)
    st.session_state['chat_history'].append(("user", input))
    st.subheader('The response is')

    for chunk in res:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("bot", chunk.text))

st.subheader("The Chat History is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
