import streamlit as st
import random

from pages.utils import show_all_messages, response_generator
from openai import OpenAI

## CONFIGURATION
st.session_state.key = st.secrets["OPENAI_API_KEY"]

# Initial greeting message
greeting_message = """Hallo, ich bin der Chatbot von "Kennst du mein Buch?", und du kannst mir einen Buchtitel nennen und wir werden uns darüber unterhalten."""

# System prompt for book stats
book_stats_prompt = """
Du bist ein Buch-Experte mit einer kreativen Ader. Wenn der Nutzer einen Buchtitel nennt, analysiere das Buch und erstelle eine unterhaltsame und visuell ansprechende Präsentation mit folgenden Statistiken:


1. ℹ️ BUCH-INFO:
   - Zeige die Bücherinformationen in einem kleinen Abschnitt an
   - Formatiere dies als nummerierte Liste mit passenden Emojis
   - Zusammenfassung des Buches
2. 📚 BUCH-TRIVIA:
   - Zeige 3-5 überraschende oder witzige Fakten über das Buch und den Autor
   - Formatiere dies als nummerierte Liste mit passenden Emojis
   - Füge eine interessante Anekdote über die Entstehung des Buches hinzu

3. 📅 VERÖFFENTLICHUNG:
   - Zeige das Veröffentlichungsjahr in einem historischen Kontext
   - Vergleiche das Erscheinungsdatum mit anderen bekannten Ereignissen aus dem Jahr

3. 📖 BUCHEMPFEHLUNGEN:
   - Liste 3-4 thematisch ähnliche Bücher auf
   - Gib für jedes Buch einen witzigen Grund an, warum es empfehlenswert ist
   - Formatiere als Liste mit passenden Emojis und einer kreativen Überschrift

Nach deiner Antwort erinnere den Nutzer freundlich daran, dass er noch DREI weitere Fragen zu diesem Buch stellen kann. Formatiere diese Erinnerung in einer auffälligen Weise.

WICHTIG: Jeder Abschnitt soll visuell klar abgegrenzt sein, mit kreativen Trennzeichen, Emojis oder ASCII-Art.
"""

# Initialize OpenAI client
client = OpenAI(api_key=st.session_state.key)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "questions_remaining" not in st.session_state:
    st.session_state.questions_remaining = 3

if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

if "has_asked_about_book" not in st.session_state:
    st.session_state.has_asked_about_book = False

# Functions
def reset_chat():
    st.session_state.messages = []
    st.session_state.questions_remaining = 3
    st.session_state.first_message_sent = False
    st.session_state.has_asked_about_book = False

# Reset button
st.button("Neustart", on_click=reset_chat, type="secondary")

# Display remaining questions
if st.session_state.has_asked_about_book:
    if st.session_state.questions_remaining > 0:
        st.info(f"Du hast noch {st.session_state.questions_remaining} Fragen übrig.")
    else:
        st.warning("Du hast bereits alle Fragen gestellt. Starte neu, um ein anderes Buch zu erkunden.")

# Display chat history
show_all_messages()

# Chat input
chat_input_disabled = st.session_state.has_asked_about_book and st.session_state.questions_remaining <= 0

# Handle user input
if prompt := st.chat_input("Deine Nachricht", disabled=chat_input_disabled):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        # Prepare messages for API
        api_messages = []
        
        # First time user mentions a book
        if not st.session_state.has_asked_about_book:
            api_messages.append({"role": "system", "content": book_stats_prompt})
            st.session_state.has_asked_about_book = True
        else:
            # Not the first message, decrement question counter
            if st.session_state.questions_remaining > 0:
                st.session_state.questions_remaining -= 1
            
            # Add note about remaining questions
            if st.session_state.questions_remaining > 0:
                api_messages.append({
                    "role": "system", 
                    "content": f"Der Nutzer hat noch {st.session_state.questions_remaining} Fragen übrig. Erwähne dies am Ende deiner Antwort auf kreative Weise."
                })
            else:
                api_messages.append({
                    "role": "system", 
                    "content": "Dies war die letzte Frage des Nutzers. Verabschiede dich auf herzliche und kreative Weise und bedanke dich für das Gespräch."
                })
        
        # Add conversation history
        for message in st.session_state.messages:
            api_messages.append({"role": message["role"], "content": message["content"]})
        
        # Get response from OpenAI
        stream = client.chat.completions.create(
            model=st.session_state.model,
            stream=True,
            messages=api_messages,
        )
        
        # Stream and capture response
        response = st.write_stream(stream)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Update first message sent flag
        st.session_state.first_message_sent = True
        
# Show initial greeting if no messages yet
elif not st.session_state.first_message_sent:
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(greeting_message))
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.first_message_sent = True
