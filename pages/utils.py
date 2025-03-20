import streamlit as st
import time


# read all messages from st.state_session["messages"] und show them in the chat
def show_all_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# stream response with a timed delay of 0.5 seconds
def response_generator(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)

