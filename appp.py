import json
import os
import random
import requests
import streamlit as st

st.set_page_config(
    page_title="AI CHATBOT", page_icon="", layout="wide"
)

API_URL = "http://127.0.0.1:8000/api/v1/chat"
HISTORY_FILE = "chat_history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_history(history_data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f)



if "conversations" not in st.session_state:
    st.session_state.conversations = load_history()


if "active_conv_id" not in st.session_state:
    new_id = str(random.randint(100000, 999999))
    st.session_state.active_conv_id = new_id
    st.session_state.conversations[new_id] = []
    save_history(st.session_state.conversations)


with st.sidebar:
    st.title("Chats")

    if st.button("New Chat", use_container_width=True):
        new_id = str(random.randint(100000, 999999))
        st.session_state.active_conv_id = new_id
        st.session_state.conversations[new_id] = []
        save_history(st.session_state.conversations)
        st.rerun()

    if st.button("Clear All History", use_container_width=True):
        st.session_state.conversations = {}
        new_id = str(random.randint(100000, 999999))
        st.session_state.active_conv_id = new_id
        st.session_state.conversations[new_id] = []
        save_history(st.session_state.conversations)
        st.rerun()

    st.markdown("---")
    st.subheader("Previous Chats")

    
    for conv_id in list(st.session_state.conversations.keys()):
        msgs = st.session_state.conversations[conv_id]
        if msgs:  
            label = f" {msgs[0]['content'].split('\n')[0][:20]}..."
            if st.button(
                label, key=f"session_{conv_id}", use_container_width=True
            ):
                st.session_state.active_conv_id = conv_id
                st.rerun()


st.title("AI CHATBOT")

active_id = st.session_state.active_conv_id
messages = st.session_state.conversations.get(active_id, [])

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if user_query := st.chat_input("Ask anything about document..."):
    messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    conv_id_int = (
        int(active_id)
        if str(active_id).isdigit()
        else random.randint(100000, 999999)
    )
    payload = {"question": str(user_query), "conversation_id": conv_id_int}

    with st.chat_message("assistant"):
        with st.spinner("Searching document..."):
            try:
                res = requests.post(API_URL, json=payload, timeout=30)
                bot_response = (
                    res.json().get("answer", "No answer found.")
                    if res.status_code == 200
                    else f" Error: {res.status_code}"
                )
            except Exception as e:
                bot_response = f"Connection Error: {str(e)}"

            st.markdown(bot_response)
            messages.append({"role": "assistant", "content": bot_response})

    st.session_state.conversations[active_id] = messages
    save_history(st.session_state.conversations)
