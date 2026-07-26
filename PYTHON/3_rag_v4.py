import json
import os
import hashlib
import warnings
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langsmith import traceable

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

warnings.filterwarnings("ignore", category=DeprecationWarning)

if not os.getenv("GOOGLE_API_KEY"):
    script_dir = Path(__file__).parent
    load_dotenv(dotenv_path=script_dir / ".env")


PDF_PATH = "islr.pdf"
INDEX_ROOT = Path(".indices")


EMBED_MODEL = "embedding-001" 
LLM_MODEL = "gemini-2.5-flash"

GOOGLE_API_KEY = os.getenv("AQ.Ab8RN6LvoF6uBnz3mW6yj-DWi4xqeOE7ind7oUVuDHtL6W3L-w")
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=0,
    google_api_key="AQ.Ab8RN6LvoF6uBnz3mW6yj-DWi4xqeOE7ind7oUVuDHtL6W3L-w")

@traceable
def load_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2")

@traceable
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300,
    )
    return splitter.split_documents(docs)

@traceable
def build_vectorstore(splits):
    return FAISS.from_documents(
        splits,
        embeddings,
    )

def file_hash(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            sha.update(chunk)
    return sha.hexdigest()

def index_path(pdf_path):
    key = file_hash(pdf_path)
    return INDEX_ROOT / key

@traceable
def load_index(folder):
    return FAISS.load_local(
        str(folder),
        embeddings,
        allow_dangerous_deserialization=True,
    )

@traceable
def build_index(pdf_path):
    docs = load_pdf(pdf_path)
    splits = split_documents(docs)
    vectorstore = build_vectorstore(splits)
    
    folder = index_path(pdf_path)
    folder.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(folder))
    return vectorstore

@traceable
def load_or_build(pdf_path):
    folder = index_path(pdf_path)
    if folder.exists():
        try:
            return load_index(folder)
        except Exception:
            print("\nOld Index Conflict Detected. Rebuilding Index...")
            shutil.rmtree(folder)
            
    return build_index(pdf_path)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer ONLY from the provided context. If the answer is not present, reply 'I don't know.'"
        ),
        (
            "human",
            "Question:\n{question}\n\nContext:\n{context}"
        ),
    ]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@traceable
def build_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    parallel = RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
    )
    
    return (
        parallel
        | prompt
        | llm
        | StrOutputParser()
    )

@traceable
def ask(question):
    vectorstore = load_or_build(PDF_PATH)
    chain = build_chain(vectorstore)
    return chain.invoke(question)

if __name__ == "__main__":
    if INDEX_ROOT.exists():
        shutil.rmtree(INDEX_ROOT)
    INDEX_ROOT.mkdir(exist_ok=True)
    
    print("PDF RAG Ready")
    
    while True:
        question = input("\nQuestion : ")
        if question.lower() in ["exit", "quit"]:
            break
            
        if not question.strip():
            continue
            
        answer = ask(question)
        print("\nAnswer:\n")
        print(answer)

