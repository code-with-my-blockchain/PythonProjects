import uuid
import streamlit as st
from langraph_database_backend import (
    chatbot,
    retrieve_all_threads,
    save_thread_title,
    get_thread_title,
)
from langchain_core.messages import HumanMessage, AIMessage

def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if thread_id not in st.session_state.chat_threads:
        st.session_state.chat_threads.append(thread_id)
        st.session_state.thread_titles[thread_id] = get_thread_title(thread_id)

import os
from dotenv import load_dotenv
load_dotenv()

import os
from dotenv import load_dotenv
load_dotenv()
print("Loaded Key:", os.getenv("GEMINI_API_KEY")[:10] if os.getenv("GEMINI_API_KEY") else "None")



def reset_chat():
    new_thread = generate_thread_id()

    st.session_state.thread_id = new_thread
    add_thread(new_thread)
    st.session_state.message_history = []

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


if "message_history" not in st.session_state:
    st.session_state.message_history = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state.chat_threads = retrieve_all_threads()

if "thread_titles" not in st.session_state:
    st.session_state.thread_titles = {}

add_thread(st.session_state.thread_id)


st.sidebar.title(" My Chatbot")

if st.sidebar.button("➕ New Chat", key="new_chat"):
    reset_chat()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Conversations")

for thread in reversed(st.session_state.chat_threads):

    title = get_thread_title(thread)

    if st.sidebar.button(title, key=f"thread_{thread}"):

        st.session_state.thread_id = thread

        messages = load_conversation(thread)

        history = []

        for msg in messages:

            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            history.append(
                {
                    "role": role,
                    "content": msg.content
                }
            )

        st.session_state.message_history = history

        st.rerun()


for message in st.session_state.message_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input(
    "Type your message...",
    key="main_chat_input"
)

if prompt:

    current_thread = st.session_state["thread_id"]

    if get_thread_title(current_thread) == "New Chat":

        title = prompt[:25]

        if len(prompt) > 25:
            title += "..."

        save_thread_title(current_thread, title)

        st.session_state["thread_titles"][current_thread] = title

    with st.chat_message("user"):
        st.markdown(prompt)

    CONFIG = {
        "configurable": {
            "thread_id": current_thread
        }
    }

    with st.chat_message("assistant"):

        def stream():

            for chunk, metadata in chatbot.stream(
                {
                    "messages": [
                        HumanMessage(content=prompt)
                    ]
                },
                config=CONFIG,
                stream_mode="messages"
            ):

                if isinstance(chunk, AIMessage):
                    yield chunk.content

        response = st.write_stream(stream())

    st.session_state.message_history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()
