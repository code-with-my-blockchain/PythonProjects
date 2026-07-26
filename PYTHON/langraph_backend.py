from typing import TypedDict, Annotated

from dotenv import load_dotenv

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
)
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

graph = StateGraph(ChatState)

def chatbot_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph.add_node("chatbot", chatbot_node)

graph.add_edge(START, "chatbot")

memory = InMemorySaver()

chatbot = graph.compile(checkpointer=memory)

def stream_response(user_input: str, history: list[BaseMessage]):

    messages = history + [HumanMessage(content=user_input)]

    full_response = ""

    for chunk in llm.stream(messages):

        if chunk.content:

            full_response += chunk.content

            yield chunk.content

    return AIMessage(content=full_response)