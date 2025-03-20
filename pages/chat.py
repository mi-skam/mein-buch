import streamlit as st

from pages.utils import show_all_messages
from openai import OpenAI

## CONFIGURATION
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

## STATE
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

show_all_messages()

## LOGIC
if prompt := st.chat_input("Deine Nachricht"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state.model,
            stream=True,
            messages=[
                {"role": messages["role"], "content": messages["content"]}
                for messages in st.session_state.messages
            ],
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
