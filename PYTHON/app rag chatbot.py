import os
from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0,
)
loader = PyPDFLoader(r"C:\Users\user\PythonProjects\intro-to-ml.pdf")

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=100,
)


chunks = splitter.split_documents(documents)
print("Number of chunks:", len(chunks))


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key,
)
import os

INDEX_PATH = "faiss_index"

if os.path.exists(INDEX_PATH):
    print("Loading existing FAISS index...")

    vector_store = FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

else:
    print("Creating new FAISS index...")

    vector_store = FAISS.from_documents(
        chunks,
        embeddings,
    )

    vector_store.save_local(INDEX_PATH)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
