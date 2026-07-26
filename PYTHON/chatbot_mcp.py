
import streamlit as st
import asyncio
from chatbot_mcp_backend import build_graph
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Agentic AI Chatbot with MCP", layout="centered")
st.title("🤖 LangGraph MCP Chatbot")

# Initialize chat history & graph session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph" not in st.session_state:
    # Running async graph compilation inside sync Streamlit
    st.session_state.graph = asyncio.run(build_graph())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        st.write(message.content)

# Async function to handle streaming response
async def stream_response(user_input):
    graph = st.session_state.graph
    inputs = {"messages": [HumanMessage(content=user_input)]}
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    # Stream assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Use astream for async graph streaming
        async for event in graph.astream(inputs, stream_mode="values"):
            if "messages" in event:
                last_msg = event["messages"][-1]
                if isinstance(last_msg, AIMessage) and last_msg.content:
                    full_response = last_msg.content
                    response_placeholder.write(full_response)
                    
        st.session_state.messages.append(AIMessage(content=full_response))

# Capture user input
user_query = st.chat_input("Ask something (e.g., calculations or expense tracking)...")

if user_query:
    # Run the async stream handler inside Streamlit's loop
    asyncio.run(stream_response(user_query))