import streamlit as st

st.set_page_config(page_title="Kennst du mein Buch?", page_icon=":books:", initial_sidebar_state="collapsed")

content = '''
# Kennst du mein Buch?

Ich bin ein Chatbot, der dir helfen kann, mehr über ein Buch heraus zu finden.
'''

st.write(content)

start = st.button("Start", icon="🚀", use_container_width=True, type="primary")

if start:
    st.write("Button was clicked!")
    st.switch_page("pages/chat.py")

