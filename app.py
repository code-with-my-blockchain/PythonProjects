import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openrouter import ChatOpenRouter
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

OPENROUTER_API_KEY = os.getenv("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")



file_path = r"C:\Users\user\OneDrive\Desktop\python Practice\test.txt"


loader = TextLoader(
    file_path,
    encoding="utf-8"
)

documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)


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
    search_kwargs={"k": 2}
)


llm = ChatOpenRouter(
    model="openai/gpt-4o-mini"
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

    context_parts = []

    for doc in relevant_docs:
        context_parts.append(doc.page_content)

    context = "\n\n".join(context_parts)


    prompt = f"""
You are an extremely concise and precise question-answering assistant.

Answer the user's question using ONLY the information provided
in the CONTEXT.

Rules:

1. Give a direct and short answer.
2. Maximum 1-3 sentences.
3. Do not repeat the question.
4. Do not mention sources.
5. Do not write [Source 1], [Source 2], etc.
6. Do not add citations.
7. Do not add headings.
8. Do not add extra formatting.

If the answer is not present in the context, reply exactly:

I could not find this information in the document.

CONTEXT:

{context}

QUESTION:

{question}

DIRECT ANSWER:
"""

    response = llm.invoke(prompt)

    answer = response.content.strip()

    answer = answer.replace("[Source 1]", "")
    answer = answer.replace("[Source 2]", "")
    answer = answer.replace("[Source 3]", "")
    answer = answer.replace("[Source 4]", "")
    answer = answer.replace("[Source 5]", "")

    print("\n" + answer.strip() + "\n")


