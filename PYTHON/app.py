import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults 
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated, List
from langgraph.checkpoint.memory import MemorySaver

st.title("My Chatbot")

os.environ["GROQ_API_KEY"] = "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" 
os.environ["TAVILY_API_KEY"] = "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"


search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

llm = ChatGroq(model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: List

def chatbot_node(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

if "graph" not in st.session_state:
    graph_builder = StateGraph(State)
    
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_node("tools", ToolNode(tools))
    
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    
    memory = MemorySaver()
    st.session_state.graph = graph_builder.compile(checkpointer=memory)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask a Question (or a live query)..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    inputs = {"messages": [("user", user_input)]}
    config = {"configurable": {"thread_id": "main_chat_session"}}

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        output = st.session_state.graph.invoke(inputs, config)
        
        bot_reply = output["messages"][-1].content
        response_placeholder.markdown(bot_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})