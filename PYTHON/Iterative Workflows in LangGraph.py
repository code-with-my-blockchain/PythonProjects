import os
import time
import operator
from typing import TypedDict, Literal, Annotated
from pydantic import BaseModel, Field 
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI  

os.environ["GOOGLE_API_KEY"] = "AQ.Ab8RN6KV_MH2tta-rX7VCN23mCisjztzaEJdpqbok6yNRqVCRQ"

generator_llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.7)
optimizer_llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.7)
base_evaluator = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.2)


class TweetEvaluation(BaseModel):
    evaluation: Literal['approved', 'needs_improvement'] = Field(
        description="Select 'approved' if the tweet is clear, funny, and viral. Otherwise select 'needs_improvement'."
    )
    feedback: str = Field(description="Constructive punch-up feedback to improve the tweet content.")

structured_evaluator_llm = base_evaluator.with_structured_output(TweetEvaluation)


class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation: str
    feedback: str
    iteration: int
    max_iteration: int
    tweet_history: Annotated[list, operator.add]


def generate_tweet(state: TweetState):
    """Initial tweet generation"""
    print("🤖 Generating draft...")
    time.sleep(4)  
    
    messages = [
        SystemMessage(content="You are a viral Twitter ghostwriter specializing in tech humor."),
        HumanMessage(content=f"Write a short, viral tweet about: {state['topic']}. Do NOT use a Q&A structure.")
    ]
    response = generator_llm.invoke(messages).content
    return {
        'tweet': response, 
        'iteration': state.get('iteration', 1), 
        'tweet_history': [response]
    }

def evaluate_tweet(state: TweetState):
    """Tweet evaluation using structured Gemini output"""
    print("🧐 Evaluating draft quality...")
    time.sleep(4)  
    
    messages = [
        SystemMessage(content="You are a critical social media manager. Check if the tweet is punchy, under 280 characters, and viral material."),
        HumanMessage(content=f"Evaluate this tweet: {state['tweet']}")
    ]
    response = structured_evaluator_llm.invoke(messages)
    print(f"   └> Judge Verdict: {response.evaluation.upper()}")
    return {
        'evaluation': response.evaluation, 
        'feedback': response.feedback
    }

def optimize_tweet(state: TweetState):
    """Tweet optimization based on feedback"""
    print("🛠️ Polishing draft up based on feedback loop...")
    time.sleep(4) 
    
    messages = [
        SystemMessage(content="You punch up tweets for virality and humor based on given feedback."),   
        HumanMessage(content=f"""
Improve the tweet based on this feedback:
"{state['feedback']}"

Topic: "{state['topic']}"
Original Tweet:
"{state['tweet']}"

Re-write it as a short, viral-worthy tweet. Avoid Q&A style and stay under 280 characters.
""")
    ]
    response = optimizer_llm.invoke(messages).content
    iteration = state['iteration'] + 1
    return {
        'tweet': response, 
        'iteration': iteration, 
        'tweet_history': [response]
    }
def route_evaluation(state: TweetState):
    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return 'approved'
    else:
        return 'needs_improvement'

graph = StateGraph(TweetState)

graph.add_node('generate', generate_tweet)
graph.add_node('evaluate', evaluate_tweet)
graph.add_node('optimize', optimize_tweet)

graph.add_edge(START, 'generate')
graph.add_edge('generate', 'evaluate')

graph.add_conditional_edges(
    'evaluate', 
    route_evaluation, 
    {
        'approved': END, 
        'needs_improvement': 'optimize'
    }
)
graph.add_edge('optimize', 'evaluate')

workflow = graph.compile()

if __name__ == "__main__":
    initial_state = {
        "topic": "Why coding directly outside of OneDrive folders saves human lives",
        "iteration": 1,
        "max_iteration": 3,
        "tweet_history": []  # CRITICAL: Must be initialized as an empty list for the reducer function
    }

    print("--- Running LangGraph Workflow with Gemini 2.0 ---")
    result = workflow.invoke(initial_state)

    print("\n================ FINAL REFINED OUTPUT ================")
    print(f"Final Approved Tweet:\n{result['tweet']}")
    print(f"Total Iterations Taken: {result['iteration']}\n")

    print("--- History of Drafts ---")
    for idx, old_tweet in enumerate(result['tweet_history'], 1):
        print(f"Draft {idx}: {old_tweet}")