import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

import sys

client = MultiServerMCPClient(
    {
        "math_server": {
            "command": sys.executable,
            "args": ["math_server.py"],
            "transport": "stdio",
        }
    }
)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def chat_node(state: AgentState):

    response = await model_with_tools.ainvoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


async def build_graph():

    tools = await client.get_tools()

    global model_with_tools
    model_with_tools = model.bind_tools(tools)

    graph = StateGraph(AgentState)

    graph.add_node("agent", chat_node)

    graph.add_node(
        "tools",
        ToolNode(tools)
    )

    graph.add_edge(
        START,
        "agent"
    )

    graph.add_conditional_edges(
        "agent",
        tools_condition
    )

    graph.add_edge(
        "tools",
        "agent"
    )

    return graph.compile()