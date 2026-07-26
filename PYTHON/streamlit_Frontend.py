import streamlit as st
from langraph_backend import stream_response
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="My Chatbot", page_icon="🤖")

if "message_history" not in st.session_state:
    st.session_state.message_history = []

if "langchain_history" not in st.session_state:
    st.session_state.langchain_history = []

for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type your message...")

if user_input:


    st.session_state.message_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    st.session_state.langchain_history.append(
        HumanMessage(content=user_input)
    )

    with st.chat_message("user"):
        st.markdown(user_input)

   
    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        for token in stream_response(
            user_input,
            st.session_state.langchain_history[:-1]
        ):

            full_response += token

            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

 
    st.session_state.message_history.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    st.session_state.langchain_history.append(
        AIMessage(content=full_response)
    )