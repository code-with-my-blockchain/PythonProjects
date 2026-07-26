import os
import hashlib
import shutil
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

warnings.filterwarnings("ignore", category=DeprecationWarning)

from pathlib import Path
load_dotenv(Path(__file__).parent / "PYTHON" / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

PDF_PATH = "islr.pdf"
INDEX_ROOT = Path(".indices")
EMBED_MODEL = "models/text-embedding-004"
LLM_MODEL = "gemini-2.5-flash"

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBED_MODEL,
    google_api_key=GOOGLE_API_KEY,
)

llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=0,
    google_api_key=GOOGLE_API_KEY,
)

@traceable
def load_pdf(path):
    return PyPDFLoader(path).load()

@traceable
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    return splitter.split_documents(docs)

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024*1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def index_path(pdf):
    return INDEX_ROOT / file_hash(pdf)

@traceable
def load_or_build(pdf):
    folder = index_path(pdf)
    if folder.exists():
        try:
            return FAISS.load_local(str(folder), embeddings, allow_dangerous_deserialization=True)
        except Exception:
            shutil.rmtree(folder)
    docs = split_documents(load_pdf(pdf))
    vs = FAISS.from_documents(docs, embeddings)
    folder.mkdir(parents=True, exist_ok=True)
    vs.save_local(str(folder))
    return vs

prompt = ChatPromptTemplate.from_messages([
("system","Answer ONLY from the provided context. If the answer is not present, reply 'I don't know.'"),
("human","Question:\n{question}\n\nContext:\n{context}")
])

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

def build_chain(vs):
    retriever = vs.as_retriever(search_kwargs={"k":4})
    return (
        RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        })
        | prompt
        | llm
        | StrOutputParser()
    )

def ask(q):
    return build_chain(load_or_build(PDF_PATH)).invoke(q)

if __name__ == "__main__":
    INDEX_ROOT.mkdir(exist_ok=True)
    print("RAG Ready")
    while True:
        q = input("Question: ").strip()
        if q.lower() in ("exit","quit"):
            break
        if not q:
            continue
        print("\nAnswer:\n")
        print(ask(q))
