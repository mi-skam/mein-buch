import streamlit as st

st.set_page_config(
    page_title="Kennst du mein Buch?",
    page_icon=":books:",
    initial_sidebar_state="collapsed",
)


## CONFIGURATION
st.session_state.key = st.secrets["OPENAI_API_KEY"]

## STATE
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []


content = """
# Kennst du mein Buch?

Ich bin ein Chatbot, der dir helfen kann, mehr über ein Buch heraus zu finden.
"""

st.write(content)

start = st.button("Start", icon="🚀", use_container_width=True, type="primary")

if start:
    st.session_state.messages = []
    st.switch_page("pages/chat.py")
