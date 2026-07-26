import os
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
import os

# 1. Define Tools
@tool
def get_stock_price(ticker: str) -> float:
    """Retrieves the current stock price for a given company ticker."""
    if ticker.lower() in ["apple", "aapl"]:
        return 278.0
    return 150.0

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b

@tool
def purchase_stocks(ticker: str, quantity: int) -> str:
    """Purchases a specified quantity of shares for a given company ticker."""
    decision = interrupt(f"Approve buying {quantity} shares of {ticker}? (yes/no)")
    
    if isinstance(decision, str) and decision.lower() == "yes":
        return f"Status: Success | Successfully placed a purchase order for {quantity} shares of {ticker}."
    else:
        return f"Status: Cancelled | Purchase order for {quantity} shares of {ticker} was declined."
    
from zoneinfo import ZoneInfo
from datetime import datetime 
@tool
def get_current_time(city: str = "Lahore") -> str:
    """Returns the current date, day and time for Lahore, Pakistan."""

    now = datetime.now(ZoneInfo("Asia/Karachi"))

    return (
        f"City: {city}\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d %B %Y')}\n"
        f"Time: {now.strftime('%I:%M:%S %p PKT')}"
    )
    
    
tools = [
    get_stock_price,
    get_current_time,   # <-- abhi function bana hi nahi
    multiply,
    purchase_stocks,
]
@tool
def get_current_time() -> str:
    """Returns the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 2. Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0, 
    api_key="AQ.Ab8RN6KpAyxFD2hwogCwLZ1lWbnGAUq-TRVrY04vcBI0ifX88g"
)

# 🚀 FIX: llm_with_tools aur tool_node ko initialize karna zaroori tha
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

# 3. Define State
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# 4. Define Nodes
def call_model(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Define Routing Logic
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 6. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# 🚀 FIX: Duplicate edges/compiles ko saaf kiya
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

memory = MemorySaver()
chatbot_graph = workflow.compile(checkpointer=memory)

# 7. Main CLI Loop
def run_chatbot():
    config = {"configurable": {"thread_id": "gemini_stock_agent"}}
    print("Gemini Stock Assistant initialized. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
            
        state = chatbot_graph.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
        
        while "__interrupt__" in state:
            interrupt_msg = state["__interrupt__"][0].value
            print(f"\n[HITL Verification Required]: {interrupt_msg}")
            
            user_decision = input("Your Choice (yes/no): ")
            state = chatbot_graph.invoke(Command(resume=user_decision), config=config)
            
        print(f"Assistant: {state['messages'][-1].content}\n")

# Run the chatbot simulation
if __name__ == "__main__":
    run_chatbot()

    ALPHA_API_KEY = "4OTWFPFRKWEQMBYD."

    from datetime import datetime
import requests

@tool
def get_stock_price(ticker: str) -> str:
    """Gets live stock price using Alpha Vantage."""

    ticker = ticker.upper()

    url = (
        f"https://www.alphavantage.co/query?"
        f"function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        quote = data.get("Global Quote", {})

        if not quote:
            return f"No stock data found for {ticker}."

        price = quote.get("05. price")

        return f"Current price of {ticker} is ${float(price):.2f}"

    except Exception as e:
        return str(e)

@tool
def get_current_time() -> str:
    """Returns current UTC time from internet."""

    try:
        data = requests.get(
            "https://worldtimeapi.org/api/timezone/Etc/UTC",
            timeout=10
        ).json()

        return data["datetime"]

    except Exception as e:
        return str(e)


