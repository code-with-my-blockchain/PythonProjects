import os
from typing import Annotated, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6KV_MH2tta-rX7VCN23mCisjztzaEJdpqbok6yNRqVCRQ"

class State(TypedDict):

    messages: Annotated[list, lambda x, y: x + y]

def chatbot_node(state: State):

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()

app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "session_gemini_1"}}

print("--- First Turn ---")
initial_input = {"messages": [{"role": "user", "content": "Hi, my name is ALI HAIDER."}]}
events = app.stream(initial_input, config)
for event in events:
    for value in event.values():
        print("Gemini:", value["messages"][-1].content)

print("\n--- Second Turn (Testing Short-Term Memory) ---")
follow_up_input = {"messages": [{"role": "user", "content": "What is my name?"}]}
events = app.stream(follow_up_input, config)
for event in events:
    for value in event.values():
        print("Gemini:", value["messages"][-1].content)

print("\n--- Inspecting State History (Time Travel Setup) ---")

states = list(app.get_state_history(config))

for state in states:
    print(f"Checkpoint ID: {state.config['configurable']['checkpoint_id']}")
    print(f"Values at this step: {state.values}\n" + "-"*40)
