import streamlit as st
from gemini_backend import stream_response

st.set_page_config(
    page_title="My Chatbot",
    page_icon="🤖"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        for token in stream_response(user_input):

            full_response += token

            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":full_response
        }
    )