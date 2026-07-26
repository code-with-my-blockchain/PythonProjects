import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

load_dotenv()


from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY:", os.getenv("GOOGLE_API_KEY")[:10])

PDF_PATH = "ISLR.pdf"
FAISS_PATH = "faiss_index"


def create_vector_store():
    print("Loading PDF...")

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300
    )

    splits = splitter.split_documents(docs)

    print(f"Pages  : {len(docs)}")
    print(f"Chunks : {len(splits)}")

    embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)

    vectorstore = FAISS.from_documents(
        splits,
        embeddings
    )

    vectorstore.save_local(FAISS_PATH)

    print("✅ FAISS Index Saved")

    return vectorstore


def load_vector_store():

    embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)

    if os.path.exists(FAISS_PATH):

        print("Loading Existing FAISS Index...")

        vectorstore = FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    else:

        vectorstore = create_vector_store()

    return vectorstore