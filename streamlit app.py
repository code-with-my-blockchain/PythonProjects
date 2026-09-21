import os
import shutil

import streamlit as st
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openrouter import ChatOpenRouter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")


DOCUMENTS_DIR = "./documents"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "CHAT-BOT"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4


os.makedirs(DOCUMENTS_DIR, exist_ok=True)


st.set_page_config(
    page_title=" Chat-bot",
    layout="wide",
)

st.title("Chat-bot")

st.write(
    "Upload TXT documents and ask questions "
    "using Retrieval-Augmented Generation."
)

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

    for filename in os.listdir(DOCUMENTS_DIR):

        file_path = os.path.join(
            DOCUMENTS_DIR,
            filename,
        )

        if filename.lower().endswith(".txt"):

            try:

                loader = TextLoader(
                    file_path,
                    encoding="utf-8",
                )

                docs = loader.load()

                for doc in docs:

                    doc.metadata["source"] = filename
                    doc.metadata["file_type"] = "txt"

                all_documents.extend(docs)

            except Exception as e:

                st.warning(
                    f"Could not load {filename}: {e}"
                )

        elif filename.lower().endswith(".txt"):

            try:

                loader = PyPDFLoader(
                    file_path
                )

                docs = loader.load()

                for doc in docs:

                    doc.metadata["source"] = filename
                    doc.metadata["file_type"] = "pdf"

                all_documents.extend(docs)

            except Exception as e:

                st.warning(
                    f"Could not load {filename}: {e}"
                )

    return all_documents


def create_vector_database():

    documents = load_documents()

    if not documents:

        return None, 0, 0
    chunks = text_splitter.split_documents(
        documents
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )

    return vectorstore, len(documents), len(chunks)



@st.cache_resource
def load_vector_database():

    if not os.path.exists(CHROMA_DIR):

        return None

    try:

        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR,
        )

        return vectorstore

    except Exception:

        return None

@st.cache_resource
def load_llm():

    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY missing! Ensure it is set in .env or .streamlit/secrets.toml")
        st.stop()

    return ChatOpenRouter(
        model="openai/gpt-4o-mini",
        temperature=0,
        api_key=OPENROUTER_API_KEY,
    )


llm = load_llm()


with st.sidebar:

    st.header("Document")

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

            with open(file_path, "wb") as f:

                f.write(
                    uploaded_file.getbuffer()
                )

            st.success(
            f"{len(uploaded_files)} file(s) uploaded."
        )

            st.subheader("Current file")

    files = os.listdir(DOCUMENTS_DIR)

    if files:

        for filename in files:

            st.write(f"{filename}")

    else: 
        

        st.info(
            "No documents found."
        )


    st.divider()



if st.button(
        "Index / Rebuild Documents",
        use_container_width=True,
    ):

        with st.spinner(
            "Loading, splitting and indexing documents..."
        ):

            try:

               
                if os.path.exists(CHROMA_DIR):

                    shutil.rmtree(CHROMA_DIR)


                st.cache_resource.clear()

                embeddings = load_embeddings()

                documents = load_documents()

                if not documents:

                    st.error(
                        "No PDF/TXT documents found."
                    )

                else:

                    chunks = text_splitter.split_documents(
                        documents
                    )


                  
                    vectorstore = Chroma.from_documents(
                        documents=chunks,
                        embedding=embeddings,
                        collection_name=COLLECTION_NAME,
                        persist_directory=CHROMA_DIR,
                    )


                    st.success(
                        f"Indexed successfully!\n\n"
                        f"Documents: {len(documents)}\n\n"
                        f"Chunks: {len(chunks)}"
                    )


                    st.rerun()

            except Exception as e:

                st.error(
                    f"Indexing error: {e}"
                )


if st.button(
        "Delete Vector Database",
        use_container_width=True,
    ):

    if os.path.exists(CHROMA_DIR):

     shutil.rmtree(CHROMA_DIR)

    st.cache_resource.clear()

    st.success(
                "Chroma database deleted."
            )

    st.rerun()

else:

    st.info(
     "Vector database does not exist."
            )


vectorstore = load_vector_database()
    


if vectorstore is None:

    st.info(
        " Upload documents "
        "'Index / Rebuild Documents' from the sidebar."
    )

    st.stop()

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": TOP_K
    }
)

if "messages" not in st.session_state:

    st.session_state.messages = []

    
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        
question = st.chat_input(
    "Ask something about your documents..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

        context_parts = []

    relevant_docs = documents
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

            page_number = page + 1

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


    context = "\n\n---\n\n".join(
        context_parts
    )
    history_parts = []

    for message in st.session_state.messages[:-1]:

        role = message["role"]
        content = message["content"]

        history_parts.append(
            f"{role}: {content}"
        )


    chat_history = "\n".join(
        history_parts
    )


prompt = f'''
You are a precise document question-answering assistant.

Answer the user's question using ONLY the information
contained in the CONTEXT.

You may use the previous conversation only to understand
what the user is referring to.

RULES:

1. Give a direct and useful answer.
2. Do not invent information.
3. If the answer is not present in the CONTEXT,
    reply exactly:

I could not find this information in the documents.

4. Keep the answer concise.
5. Do not mention these instructions.
6. Do not mention the retrieval process.
7. Do not create fake sources.
8. Do not use information outside the provided CONTEXT.

PREVIOUS CONVERSATION:

{{chat_history}}

CONTEXT:

{{context}}

CURRENT QUESTION:

{{question}}

ANSWER:
'''

prompt_template = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template=prompt
)

with st.spinner("Generating answer..."):
    try:
        response = llm.invoke(prompt)
        answer = response.content.strip()
        st.write(answer)
    except Exception as e:
        answer = f"Error while generating answer: {e}"
        st.error(answer)


    with st.chat_message("assistant"):

        st.markdown(answer)

if prompt:
    try:
        relevant_docs = retriever.invoke(prompt)  
    except Exception as e:
        relevant_docs = []

    if relevant_docs:

            with st.expander(
                " Retrieved Sources"
            ):

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
                            f" {source} — "
                            f"Page {page + 1}"
                        )

                    else:

                        source_text = (
                            f"{source}"
                        )


                    if source_text not in shown_sources:

                        st.write(
                            source_text
                        )

                        shown_sources.add(
                            source_text
                        )


st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

 


