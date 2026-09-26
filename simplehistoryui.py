# install dependies
import os
import streamlit as st
import sqlite3
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv


# LOAD ENVIRONMENT VARIABLES


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# CHECK API KEY


if not OPENROUTER_API_KEY:

    st.error("OPENROUTER_API_KEY is not found in .env file.")

    st.stop()



# DATABASE

DB_NAME = "chat_history.db"


def get_connection():

    return sqlite3.connect(DB_NAME)



# CREATE TABLE

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()



# SAVE MESSAGE


def save_message(user_id, role, message):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (user_id, role, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        role,
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.close()



# LOAD CHAT HISTORY


def load_history(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, message
        FROM chat_history
        WHERE user_id = ?
        ORDER BY id ASC
    """, (user_id,))

    history = cursor.fetchall()

    conn.close()

    return history



# DELETE USER HISTORY

def delete_history(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM chat_history
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()

    conn.close()



# CREATE DATABASE TABLE


create_table()



# STREAMLIT PAGE


st.set_page_config(
    page_title="Simple Ui",
    page_icon="",
    layout="centered"
)



# OPENROUTER CLIENT


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)



# MODEL


MODEL = "openai/gpt-5.4-mini"



# SESSION STATE


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "user_id" not in st.session_state:

    st.session_state.user_id = None



# LOGIN PAGE


if not st.session_state.logged_in:

    st.title("Chat")

    st.subheader("Login")

    user_id = st.text_input(
        "Enter your User ID",
        placeholder="ALI 11"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if user_id.strip() == "":

            st.warning(
                "PLEASE ENTER YOUR USER ID"
            )

        else:

            st.session_state.logged_in = True

            st.session_state.user_id = user_id.strip()

            st.rerun()

   
    st.stop()



# CURRENT USER

user_id = st.session_state.user_id


# SIDEBAR


with st.sidebar:

    st.title("Current User")

    st.write(
        f"User ID: `{user_id}`"
    )

    st.divider()



    # CLEAR HISTORY


    if st.button(
        "Clear History",
        use_container_width=True
    ):

        delete_history(user_id)

        st.success(
            "Chat history deleted."
        )

        st.rerun()


    # LOGOUT


    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.rerun()



# MAIN CHAT


st.title("My Chatbox")



# LOAD HISTORY


history = load_history(user_id)



# DISPLAY HISTORY


for role, message in history:

    with st.chat_message(role):

        st.write(message)


# NEW USER MESSAGE


user_message = st.chat_input(
    "Type your message..."
)


if user_message:


    # 1. SAVE USER MESSAGE


    save_message(
        user_id,
        "user",
        user_message
    )



    # 2. LOAD COMPLETE HISTORY


    history = load_history(user_id)



    # 3. CONVERT DATABASE HISTORY
    #    INTO OPENROUTER FORMAT


    messages = []

    for role, message in history:

        messages.append({
            "role": role,
            "content": message
        })



    # 4. ASK OPENROUTER


    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            temperature=0.7,

            max_tokens=1000
        )

        assistant_response = (
            response.choices[0].message.content
        )


    except Exception as e:

        assistant_response = (
            f"Sorry, an error occurred:\n\n{str(e)}"
        )



    # 5. SAVE AI RESPONSE


    save_message(
        user_id,
        "assistant",
        assistant_response
    )


    st.rerun()








