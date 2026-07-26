import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import os


load_dotenv()  
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader 

SCRIPT_DIR = Path(__file__).parent 

PDF_PATH = r"C:\Users\user\PythonProjects\An Introduction to Statistical Learning - Gareth James.pdf"

loader = PyPDFLoader(PDF_PATH)

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
splits = splitter.split_documents(docs)
emb = OpenAIEmbeddings(model="text-embedding-3-small")
vs = FAISS.from_documents(splits, emb)
retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 4})
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If not found, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
def format_docs(docs): return "\n\n".join(d.page_content for d in docs)
parallel = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

chain = parallel | prompt | llm | StrOutputParser()
print("PDF RAG ready. Ask a question (or Ctrl+C to exit).")
q = input("\nQ: ")
ans = chain.invoke(q.strip())
print("\nA:", ans)

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenAIEmbeddings, ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"]= "AQ.Ab8RN6KV_MH2tta-rX7VCN23mCisjztzaEJdpqbok6yNRqVCRQ"

PDF_PATH = "C:/Users/user/PythonProjects/PYTHON/merged-pdf.pdf"
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

embeddings = GoogleGenAIEmbeddings(model="models/text-embedding-004")

vectorstore = FAISS.from_documents(splits, embeddings)
print("successfully ")