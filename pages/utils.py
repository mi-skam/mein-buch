import streamlit as st


# read all messages from st.state_session["messaages"] und show them in the chat
def show_all_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
