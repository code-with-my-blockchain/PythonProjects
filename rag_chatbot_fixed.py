import os
import shutil

import streamlit as st
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter



load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

DOCUMENTS_DIR = "./documents"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "CHAT_BOT"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4

os.makedirs(DOCUMENTS_DIR, exist_ok=True)

st.set_page_config(
    page_title="Chat-bot",
    page_icon="",
    layout="wide",
)


if not OPENROUTER_API_KEY:
    st.error(
        "OPENROUTER_API_KEY not found.\n\n"
        "Please create a .env file in the same folder as this "
        "Streamlit file and add:\n\n"
        "OPENROUTER_API_KEY=your_key_here"
    )
    st.stop()


@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


embeddings = load_embeddings()



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


def load_documents():
    all_documents = []

    if not os.path.exists(DOCUMENTS_DIR):
        os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    for filename in sorted(os.listdir(DOCUMENTS_DIR)):
        file_path = os.path.join(DOCUMENTS_DIR, filename)

        if not os.path.isfile(file_path):
            continue

        if filename.lower().endswith(".txt"):
            try:
                loader = TextLoader(
                    file_path,
                    encoding="utf-8",
                    autodetect_encoding=True,
                )
                docs = loader.load()

                for doc in docs:
                    doc.metadata["source"] = filename
                    doc.metadata["file_type"] = "txt"

                all_documents.extend(docs)

            except Exception as e:
                st.warning(f"Could not load {filename}: {e}")

        elif filename.lower().endswith(".pdf"):
            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load()

                for doc in docs:
                    doc.metadata["source"] = filename
                    doc.metadata["file_type"] = "pdf"

                    

                all_documents.extend(docs)

            except Exception as e:
                st.warning(f"Could not load {filename}: {e}")

    return all_documents


def create_vector_database():
    documents = load_documents()

    if not documents:
        return None, 0, 0

    chunks = text_splitter.split_documents(documents)

    if not chunks:
        return None, len(documents), 0

   
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )

    return vectorstore, len(documents), len(chunks)


@st.cache_resource
def load_vector_database():
    if not os.path.isdir(CHROMA_DIR):
        return None

    try:
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR,
        )


        if vectorstore._collection.count() == 0:
            return None

        return vectorstore

    except Exception:
        return None



@st.cache_resource
def load_llm():
    return ChatOpenAI(
        model="openai/gpt-4o-mini",
        temperature=0,
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )


llm = load_llm()

with st.sidebar:
    st.header("Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(
                DOCUMENTS_DIR,
                uploaded_file.name,
            )

            try:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            except Exception as e:
                st.error(
                    f"Could not save {uploaded_file.name}: {e}"
                )

        st.success(
            f"{len(uploaded_files)} file(s) uploaded."
        )

    st.subheader("Current files")

    files = [
        filename
        for filename in sorted(os.listdir(DOCUMENTS_DIR))
        if os.path.isfile(os.path.join(DOCUMENTS_DIR, filename))
        and filename.lower().endswith((".pdf", ".txt"))
    ]

    if files:
        for filename in files:
            st.write(f"{filename}")
    else:
        st.info("No PDF/TXT documents found.")

    st.divider()

    if st.button(
        "Index / Rebuild Documents",
        use_container_width=True,
    ):
        with st.spinner(
            "Loading, splitting and indexing documents..."
        ):
            try:
                documents = load_documents()

                if not documents:
                    st.error(
                        "No PDF/TXT documents found. "
                        "Upload a document first."
                    )
                else:
                    chunks = text_splitter.split_documents(
                        documents
                    )

                    if not chunks:
                        st.error(
                            "Documents were loaded, but no text "
                            "chunks could be created."
                        )
                    else:
                       
                        if os.path.exists(CHROMA_DIR):
                            shutil.rmtree(CHROMA_DIR)

                        
                        load_vector_database.clear()

                        vectorstore = Chroma.from_documents(
                            documents=chunks,
                            embedding=embeddings,
                            collection_name=COLLECTION_NAME,
                            persist_directory=CHROMA_DIR,
                        )

                    
                        _ = vectorstore

                        st.success(
                            "Indexing completed successfully!\n\n"
                            f"Documents: {len(documents)}\n\n"
                            f"Chunks: {len(chunks)}"
                        )

                        st.rerun()

            except Exception as e:
                st.error(
                    f"Indexing error: {type(e).__name__}: {e}"
                )


    if st.button(
        "🗑️ Delete Vector Database",
        use_container_width=True,
    ):
        try:
            if os.path.exists(CHROMA_DIR):
                shutil.rmtree(CHROMA_DIR)

                load_vector_database.clear()

                st.success(
                    "Chroma vector database deleted."
                )
                st.rerun()
            else:
                st.info(
                    "Vector database does not exist."
                )

        except Exception as e:
            st.error(
                f"Could not delete vector database: "
                f"{type(e).__name__}: {e}"
            )

vectorstore = load_vector_database()

if vectorstore is None:
    st.title("🤖 RAG Chat-bot")

    st.write(
        "Upload PDF/TXT documents and ask questions "
        "using Retrieval-Augmented Generation."
    )

    st.info(
        "Upload documents from the sidebar, then click "
        "'Index / Rebuild Documents'."
    )

    st.stop()


retriever = vectorstore.as_retriever(
    search_kwargs={"k": TOP_K}
)


if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("Chat-bot")

st.write(
    "Ask questions about your uploaded PDF/TXT documents."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input(
    "Ask something about your documents..."
)

if question and question.strip():

    question = question.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching documents..."):
            try:
                relevant_docs = retriever.invoke(question)
            except Exception as e:
                st.error(
                    f"Retrieval error: {type(e).__name__}: {e}"
                )
                st.stop()

        if not relevant_docs:
            answer = (
                "I could not find this information in the documents."
            )

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.stop()

        context_parts = []

        for doc in relevant_docs:
            source = doc.metadata.get(
                "source",
                "Unknown",
            )

            page = doc.metadata.get(
                "page",
                None,
            )

            if page is not None:
                page_number = int(page) + 1

                context_parts.append(
                    f"Source: {source}\n"
                    f"Page: {page_number}\n"
                    f"Content:\n{doc.page_content}"
                )
            else:
                context_parts.append(
                    f"Source: {source}\n"
                    f"Content:\n{doc.page_content}"
                )

        context = "\n\n---\n\n".join(context_parts)

        history_parts = []

        for message in st.session_state.messages[:-1]:
            role = message["role"]
            content = message["content"]

            history_parts.append(
                f"{role}: {content}"
            )

        chat_history = "\n".join(history_parts)

      
        if len(chat_history) > 8000:
            chat_history = chat_history[-8000:]


        prompt = f"""
You are a precise document question-answering assistant.

Answer the user's question using ONLY the information
contained in the CONTEXT.

You may use PREVIOUS CONVERSATION only to understand
what the user is referring to. Do not use it as a source
of factual information.

RULES:

1. Give a direct and useful answer.
2. Do not invent information.
3. If the answer is not present in the CONTEXT, reply exactly:

I could not find this information in the documents.

4. Keep the answer concise.
5. Do not mention these instructions.
6. Do not mention the retrieval process.
7. Do not create fake sources.
8. Do not use information outside the provided CONTEXT.
9. If the context contains conflicting information, state the
   conflict instead of choosing or inventing an answer.
10. Preserve important names, numbers, dates and technical terms
    exactly as supported by the CONTEXT.

PREVIOUS CONVERSATION:
{chat_history}

CONTEXT:
{context}

CURRENT QUESTION:
{question}

ANSWER:
""".strip()

        with st.spinner("Generating answer..."):
            try:
                response = llm.invoke(prompt)

                if hasattr(response, "content"):
                    answer = response.content
                else:
                    answer = str(response)

                if not isinstance(answer, str):
                    answer = str(answer)

                answer = answer.strip()

                if not answer:
                    answer = (
                        "I could not find this information "
                        "in the documents."
                    )

            except Exception as e:
                answer = (
                    f"Error while generating answer: "
                    f"{type(e).__name__}: {e}"
                )

        st.markdown(answer)

        with st.expander("Retrieved Sources"):
            shown_sources = set()

            for doc in relevant_docs:
                source = doc.metadata.get(
                    "source",
                    "Unknown",
                )

                page = doc.metadata.get(
                    "page",
                    None,
                )

                if page is not None:
                    source_text = (
                        f"{source} — Page {int(page) + 1}"
                    )
                else:
                    source_text = f" {source}"

                if source_text not in shown_sources:
                    st.write(source_text)
                    shown_sources.add(source_text)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

