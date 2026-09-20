import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openrouter import ChatOpenRouter





file_path = r"C:\Users\user\Desktop\Python Projects\test.txt"



loader = TextLoader(
    r"C:\Users\user\OneDrive\Desktop\python Practice\test.txt"
)

documents = loader.load()

# print(documents)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="CHAT-BOT",
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    openrouter_api_key="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",
    app_url="http://localhost:6311",
    app_title = "CHAT-BOT",

)




print("\nReady to chat!")
print("Type 'exit' to stop.\n")

while True:

    question = input("Ask a query: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    relevant_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in relevant_docs
    )

 prompt = f"""
Answer the question using ONLY the context below.

If the answer is not available in the context, say:
"I could not find this information in the document."

Do not make up information.

PDF CONTEXT:
{context}

QUESTION:
{question}
"""

    response = llm.invoke(prompt)

    print("\nAns:", response.content)
    print()