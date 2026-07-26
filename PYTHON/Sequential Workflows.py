from typing import TypedDict
from langgraph.graph import StateGraph, START, END # type: ignore

class BMIState(TypedDict):
    weight: float
    height: float
    bmi: float
    category: str

def calculate_bmi(state: BMIState) -> BMIState:
    weight = state['weight']
    height = state['height']

    bmi_value = weight / (height ** 2)

    state['bmi'] = round(bmi_value, 2)
    return state

def label_bmi(state: BMIState) -> BMIState:
    bmi = state['bmi']

    if bmi < 18.5:
        state['category'] = "Underweight"
    elif 18.5 <= bmi < 25:
        state['category'] = "Normal"
    elif 25 <= bmi < 30:
        state['category'] = "Overweight"
    else:
        state['category'] = "Obese"

    return state

graph = StateGraph(BMIState)

graph.add_node("calculate_bmi", calculate_bmi)
graph.add_node("label_bmi", label_bmi)

graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", "label_bmi")
graph.add_edge("label_bmi", END)

workflow = graph.compile()

initial_state = {
    "weight": 80.0,
    "height": 1.73
}

final_state = workflow.invoke(initial_state)
print(final_state)

from IPython.display import Image  # type: ignore
from langchain_core.runnables.graph import MermaidDrawMethod  # type: ignore
Image(workflow.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API))

from typing import TypedDict
import os
from langchain_groq import ChatGroq  # type: ignore
os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model_name="llama-3.1-8b-instant"
)

print("Success: Updated Groq Model is ready!")
class LLMState(TypedDict):
    question: str
    answer: str

def llm_qa(state: LLMState) -> LLMState:
    question = state['question']
    prompt = f"Answer the following question:\n{question}"

    response = model.invoke(prompt)
    state['answer'] = response.content
    return state

graph = StateGraph(LLMState)

graph.add_node("llm_qa", llm_qa)

graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)

workflow = graph.compile()

initial_state = {
    "question": "How far is moon from the earth?"
}

final_state = workflow.invoke(initial_state)
print(final_state['answer'])

import os
from typing import TypedDict
from langchain_groq import ChatGroq    # type: ignore
from langgraph.graph import StateGraph, START, END    # type: ignore
os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"], 
    model_name="llama-3.1-8b-instant" 
)

class BlogState(TypedDict):
    title: str
    outline: str
    answer: str

def create_outline(state: BlogState) -> dict:
    title = state['title']
    prompt = f"Create a short bullet-point outline for a blog titled: {title}"
    response = model.invoke(prompt) 
    return {"outline": response.content}

def create_blog(state: BlogState) -> dict:
    title = state['title']
    outline = state.get('outline', 'No outline provided') 
    prompt = f"Write a brief, engaging blog post on the title: {title}\nUsing this outline:\n{outline}"
    response = model.invoke(prompt)
    return {"answer": response.content}

graph = StateGraph(BlogState)

graph.add_node("create_outline", create_outline)
graph.add_node("create_blog", create_blog)

graph.add_edge(START, "create_outline")     
graph.add_edge("create_outline", "create_blog") 
graph.add_edge("create_blog", END)             

workflow = graph.compile()

print("Success: Graph compiled with no errors!")

initial_state = {
    "title": "The Future of Artificial Intelligence in 2026"
}

final_state = workflow.invoke(initial_state)
print("\n--- GENERATED OUTLINE ---")
print(final_state.get('outline'))

print("\n--- FINAL BLOG POST ---")
print(final_state.get('answer'))