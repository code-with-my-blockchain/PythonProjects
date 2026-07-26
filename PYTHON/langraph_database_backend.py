from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key="AQ.Ab8RN6K6QQ0uLeTHzewmtUeAkO_ucm_zIGiPrwV4qrlxZMUT7Q",
    streaming=True,
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

conn.execute("""
CREATE TABLE IF NOT EXISTS thread_titles (
    thread_id TEXT PRIMARY KEY,
    title TEXT
)
""")

conn.commit()

def save_thread_title(thread_id, title):
    conn.execute(
        """
        INSERT OR REPLACE INTO thread_titles(thread_id, title)
        VALUES (?, ?)
        """,
        (str(thread_id), title)
    )
    conn.commit()


def get_thread_title(thread_id):
    cursor = conn.execute(
        """
        SELECT title
        FROM thread_titles
        WHERE thread_id=?
        """,
        (str(thread_id),)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return "New Chat"

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
