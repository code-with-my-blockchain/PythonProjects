from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter   # ← Yeh line change ki
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

print("=== PDF RAG with Gemini ===")

PDF_PATH = "islr.pdf"   

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

# Fixed splitter import
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
splits = splitter.split_documents(docs)

print(f"PDF loaded: {len(docs)} pages | Chunks: {len(splits)}")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(splits, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If not found, say 'I don't know'."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

parallel = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

chain = parallel | prompt | llm | StrOutputParser()

print("\n✅ RAG Ready! Questions poochho (exit likh kar band karo)\n")

while True:
    q = input("Q: ").strip()
    if q.lower() in ['exit', 'quit', 'q']:
        break
    if q:
        ans = chain.invoke(q)
        print(f"A: {ans}\n")