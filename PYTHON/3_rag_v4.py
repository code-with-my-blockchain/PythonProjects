import os
import hashlib
import warnings
import shutil
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings   

warnings.filterwarnings("ignore")


PDF_PATH = "islr.pdf"
INDEX_ROOT = Path(".indices")


GROQ_API_KEY = "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"   
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


llm = ChatGroq(
    model="llama-3.3-70b-versatile",   
    temperature=0,
    api_key=GROQ_API_KEY,
)

# Free local embeddings (no API key needed)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def load_pdf(path):
    return PyPDFLoader(path).load()

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
    return splitter.split_documents(docs)

def build_vectorstore(splits):
    return FAISS.from_documents(splits, embeddings)

def file_hash(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            sha.update(chunk)
    return sha.hexdigest()

def index_path(pdf_path):
    return INDEX_ROOT / file_hash(pdf_path)

def load_index(folder):
    return FAISS.load_local(str(folder), embeddings, allow_dangerous_deserialization=True)

def build_index(pdf_path):
    print("Building new index...")
    docs = load_pdf(pdf_path)
    splits = split_documents(docs)
    vectorstore = build_vectorstore(splits)
    folder = index_path(pdf_path)
    folder.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(folder))
    print(f"Index saved at: {folder}")
    return vectorstore

def load_or_build(pdf_path):
    folder = index_path(pdf_path)
    if folder.exists():
        try:
            print("Loading existing index...")
            return load_index(folder)
        except Exception as e:
            print(f"Index conflict: {e}. Rebuilding...")
            shutil.rmtree(folder)
    return build_index(pdf_path)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If the answer is not present, reply 'I don't know.'"),
    ("human", "Question:\n{question}\n\nContext:\n{context}"),
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    parallel = RunnableParallel({
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    })
    return parallel | prompt | llm | StrOutputParser()

def ask(question):
    vectorstore = load_or_build(PDF_PATH)
    chain = build_chain(vectorstore)
    return chain.invoke(question)


if __name__ == "__main__":
    if not Path(PDF_PATH).exists():
        print(f"Error: '{PDF_PATH}' not found!")
        exit(1)

    INDEX_ROOT.mkdir(exist_ok=True)
    print("PDF RAG Ready (Groq + Local Embeddings)")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("Question : ").strip()
        if question.lower() in ["exit", "quit"]:
            break
        if not question:
            continue

        try:
            answer = ask(question)
            print("\nAnswer:\n")
            print(answer)
            print("\n" + "-" * 50)
        except Exception as e:
            print(f"\nError: {e}\n")
