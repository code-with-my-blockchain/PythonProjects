import os
from typing import TypedDict, Annotated
from google import genai
from google.genai import types
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage

# 1. Setup Gemini Native Client
# अपनी Gemini Key यहाँ डालें या एनवायरनमेंट में सेट करें
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6KpAyxFD2hwogCwLZ1lWbnGAUq-TRVrY04vcBI0ifX88g"
client = genai.Client()

# 2. Define State
class ChatState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# 3. Define the HITL Chat Node
def chat_node(state: ChatState):
    messages = state["messages"]
    last_message = messages[-1].content
    
    # Trigger standard LangGraph interrupt
    decision = interrupt({
        "type": "approval_required",
        "reason": "User confirmation required before calling Gemini",
        "question": last_message,
        "instruction": "Do you want to send this question to Gemini? (yes/no)"
    })
    
    if decision.get("approved").lower() == "no":
        return {"messages": [AIMessage(content="Not Approved by user. Request cancelled.")]}
    
    # 4. Gemini Direct Native API Call (No LangChain LLM Import needed!)
    # LangGraph के मैसेज फॉर्मेट को Gemini फॉर्मेट में बदलें
    gemini_contents = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "model"
        gemini_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg.content)])
        )
        
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=gemini_contents,
    )
    
    return {"messages": [AIMessage(content=response.text)]}

# 5. Build Graph
workflow = StateGraph(ChatState)
workflow.add_node("chat", chat_node)
workflow.add_edge(START, "chat")
workflow.add_edge("chat", END)

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# 6. Execution Flow
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "native_gemini_thread"}}
    initial_input = {"messages": [HumanMessage(content="Explain gradient descent in very simple terms")]}
    
    print("--- First Invocation (Pausing at Interrupt) ---")
    state_output = graph.invoke(initial_input, config=config)
    
    if "__interrupt__" in state_output:
        interrupt_info = state_output["__interrupt__"][0].value
        print(f"\n[Notification]: {interrupt_info['instruction']}")
        user_response = input("Your Decision (yes/no): ")
        
        print("\n--- Resuming Graph ---")
        final_output = graph.invoke(
            Command(resume={"approved": user_response}), 
   
            config=config
        )
        print("\nFinal Output:")
        print(final_output["messages"][-1].content)