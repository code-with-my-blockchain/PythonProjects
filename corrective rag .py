import os
from typing import List
from typing_extensions import TypedDict

from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_tavily import TavilySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph, START


os.environ["USER_AGENT"] = "MyCorrectiveRAGApp/1.0"

GOOGLE_API_KEY = "AQ.Ab8RN6KVCwITRW7ImqTdSTKI1w7HJDAbWURf2pCUZ_a1ZONnqA"
TAVILY_API_KEY = "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"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

class GraphState(TypedDict):
    question: str
    generation: str
    web_search: str
    documents: List[Document]


PERSIST_DIRECTORY = "./chroma_db_crag"
COLLECTION_NAME = "rag-chroma-local"

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
]



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},        
    encode_kwargs={"normalize_embeddings": True}
)

if os.path.exists(PERSIST_DIRECTORY):
    print("Loading existing Chroma DB...")
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )
else:
    print("Creating new Chroma DB (first time only)...")
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250,
        chunk_overlap=0,
    )
    doc_splits = text_splitter.split_documents(docs_list)

    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )
    print("Chroma DB created & saved!")

retriever = vectorstore.as_retriever()


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system_prompt = """You are a grader assessing relevance of a retrieved document to a user question. 
If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. 
Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question."""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)
retrieval_grader = grade_prompt | structured_llm_grader

web_search_tool = TavilySearch(max_results=3)

gen_prompt = ChatPromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.

Question: {question} 
Context: {context} 
Answer:"""
)
rag_chain = gen_prompt | llm


def retrieve(state: GraphState):
    print("---RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}


def grade_documents(state: GraphState):
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search = "No"

    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            web_search = "Yes"

    return {
        "documents": filtered_docs,
        "question": question,
        "web_search": web_search,
    }


def transform_query(state: GraphState):
    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]

    system = """You are a question re-writer that converts an input question to a better version that is optimized 
for web search. Look at the input and try to reason about the underlying semantic intent / meaning."""

    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Formulate an improved question.",
            ),
        ]
    )
    question_rewriter = re_write_prompt | llm
    better_question = question_rewriter.invoke({"question": question}).content

    return {"documents": documents, "question": better_question}


def web_search(state):
    """
    Web search based on the re-phrased question using Tavily.
    """
    print("---WEB SEARCH---")
    question = state["question"]
    documents = state.get("documents", [])


    search_result = web_search_tool.invoke({"query": question})

    if isinstance(search_result, dict) and "results" in search_result:
        web_results = "\n\n".join(
            [d["content"] for d in search_result["results"] if "content" in d]
        )
    else:
       
        web_results = str(search_result)

   
    from langchain_core.documents import Document
    web_results_doc = Document(page_content=web_results)

    
    documents.append(web_results_doc)

    return {"documents": documents, "question": question}


def generate(state: GraphState):
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    if documents:
        context = "\n\n".join([doc.page_content for doc in documents])
    else:
        context = "No relevant documents found."

    generation = rag_chain.invoke({"context": context, "question": question})
    return {
        "documents": documents,
        "question": question,
        "generation": generation.content,
    }


def decide_to_generate(state: GraphState):
    print("---ASSESS GRADED DOCUMENTS---")
    web_search = state["web_search"]

    if web_search == "Yes":
        print("---DECISION: DOCUMENTS NOT RELEVANT → WEB SEARCH---")
        return "transform_query"
    else:
        print("---DECISION: DOCUMENTS RELEVANT → GENERATE---")
        return "generate"



workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("transform_query", transform_query)
workflow.add_node("web_search", web_search)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "web_search")
workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()



if __name__ == "__main__":
    inputs = {"question": "What are the key components of LLM agents?"}

    print("\n" + "=" * 60)
    print("Running Corrective RAG...")
    print("=" * 60 + "\n")

    final_state = None
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Finished Node: '{key}'")
            final_state = value

    print("\n" + "=" * 60)
    print("--- FINAL ANSWER ---")
    print("=" * 60)
    print(final_state.get("generation"))