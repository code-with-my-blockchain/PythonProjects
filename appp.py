import random
import requests
import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="AI CHATBOT", page_icon="", layout="wide"
)


API_URL = "http://127.0.0.1:8000/api/v1/chat"
SUPABASE_URL = "https://wmlvketrqisdstimpczq.supabase.co"
SUPABASE_KEY = "sb_publishable_j9_mydLlQf2Ft4n3l02Uzg_cM_P2mDY"


@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


db = init_supabase()



def load_history():
    try:
        response = db.table("chat_history").select("*").execute()
        history = {}
        for row in response.data:
            history[str(row["conversation_id"])] = row["messages"]
        return history
    except Exception as e:
        st.error(f"Supabase Load Error: {e}")
        return {}


def save_conversation(conv_id, messages):
    try:
        data = {"conversation_id": str(conv_id), "messages": messages}
        db.table("chat_history").upsert(data).execute()
    except Exception as e:
        st.error(f"Supabase Save Error: {e}")


def delete_all_history():
    try:
        db.table("chat_history").delete().neq(
            "conversation_id", "0"
        ).execute()
    except Exception as e:
        st.error(f"Supabase Clear Error: {e}")


if "conversations" not in st.session_state:
    st.session_state.conversations = load_history()

if "active_conv_id" not in st.session_state:
    new_id = str(random.randint(100000, 999999))
    st.session_state.active_conv_id = new_id
    st.session_state.conversations[new_id] = []

with st.sidebar:
    st.title("CHATs")

    if st.button(" New Chat", use_container_width=True):
        new_id = str(random.randint(100000, 999999))
        st.session_state.active_conv_id = new_id
        st.session_state.conversations[new_id] = []
        st.rerun()

    if st.button( "Clear Chat History", use_container_width=True):
        delete_all_history()
        st.session_state.conversations = {}
        new_id = str(random.randint(100000, 999999))
        st.session_state.active_conv_id = new_id
        st.session_state.conversations[new_id] = []
        st.rerun()

    st.markdown("---")
    st.subheader("Previous Chats")


    for conv_id in reversed(list(st.session_state.conversations.keys())):
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

if user_query := st.chat_input("ASK ANYTHING ABOUT YOUR DOCUMENT..."):
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
                bot_response = f" Connection Error: {str(e)}"

            st.markdown(bot_response)
            messages.append({"role": "assistant", "content": bot_response})

   
    st.session_state.conversations[active_id] = messages
    save_conversation(active_id, messages)
