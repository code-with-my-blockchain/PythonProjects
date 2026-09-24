import os
import shutil

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openrouter import ChatOpenRouter
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found in .env"
    )


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOCUMENTS_DIR = os.path.join(
    BASE_DIR,
    "documents"
)

CHROMA_DIR = os.path.join(
    BASE_DIR,
    "chroma_db"
)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4


os.makedirs(
    DOCUMENTS_DIR,
    exist_ok=True
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)




llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    temperature=0,
    api_key=OPENROUTER_API_KEY,
    app_name=("CHAT-BOT"),
    app_url=("https//:localhost6311"),
)



def load_documents():

    all_documents = []

    for filename in os.listdir(DOCUMENTS_DIR):

        file_path = os.path.join(
            DOCUMENTS_DIR,
            filename
        )

    if filename.lower().endswith(".txt"):

            loader = TextLoader(
                file_path,
                encoding="utf-8"
            )

            docs = loader.load()

            for doc in docs:

                doc.metadata["source"] = filename
                doc.metadata["file_type"] = "txt"

            all_documents.extend(docs)


    elif filename.lower().endswith(".pdf"):

            loader = PyPDFLoader(
                file_path
            )

            docs = loader.load() 
            for doc in docs:

                doc.metadata["source"] = filename
                doc.metadata["file_type"] = "pdf"

            all_documents.extend(docs)

    return all_documents

def build_vectorstore():

    documents = load_documents()

    if not documents:

        raise ValueError(
            "No PDF or TXT documents found."
        )

    chunks = text_splitter.split_documents(
        documents
    )

    if os.path.exists(CHROMA_DIR):

        shutil.rmtree(CHROMA_DIR)


  
    COLLECTION_NAME = "my_rag_collection"
    CHROMA_DIR = "./chroma_db"
    vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    persist_directory=CHROMA_DIR,
)
    


    return {
        "documents": len(documents),
        "chunks": len(chunks),
    }


def get_vectorstore():

    if not os.path.exists(CHROMA_DIR):

        raise ValueError(
            "Vector database does not exist. "
            "Please index documents first."
        )


    COLLECTION_NAME = "my_rag_collection"
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def ask_question(
    question: str,
    chat_history: list
):

    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": TOP_K
        }
    )


    relevant_docs = retriever.invoke(
        question
    )


    context_parts = []

    sources = []

    for doc in relevant_docs:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            None
        )

        if page is not None:

            page_number = page + 1

            context_parts.append(
                f"Source: {source}\n"
                f"Page: {page_number}\n"
                f"Content:\n{doc.page_content}"
            )

            sources.append({
                "source": source,
                "page": page_number,
            })

        else:

            context_parts.append(
                f"Source: {source}\n"
                f"Content:\n{doc.page_content}"
            )

            sources.append({
                "source": source,
                "page": None,
            })


    context = "\n\n---\n\n".join(
        context_parts
    )

    history_text = ""

    for item in chat_history:

        history_text += (
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}\n\n"
        )

    prompt = f"""
You are a precise RAG document assistant.

Answer the user's question using ONLY the information
contained in the CONTEXT.

Previous conversation can be used only to understand
follow-up questions.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. Give a direct answer.
4. Keep the answer concise but useful.
5. If the answer is not present in the context,
   reply exactly:

I could not find this information in the documents.

PREVIOUS CONVERSATION:

{history_text}

CONTEXT:

{context}

CURRENT QUESTION:

{question}

ANSWER:
"""

    response = llm.invoke(
        prompt
    )

    answer = response.content.strip()



    return {
        "answer": answer,
        "sources": sources,
    }






      

