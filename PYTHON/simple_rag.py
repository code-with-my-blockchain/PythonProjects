from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

print("=== Simple RAG Test (No PDF) ===")

# Sample text (aap isme apna text daal sakte ho)
text = """
LangSmith is a platform by LangChain for debugging, testing, and monitoring LLM applications.
It helps in tracing, evaluating, and improving AI agents and chains.
Gemini is Google's powerful AI model.
"""

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = splitter.create_documents([text])

print(f"Created {len(splits)} chunks")

# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="embedding-001")
vectorstore = FAISS.from_documents(splits, embeddings)
retriever = vectorstore.as_retriever()

# Prompt & Model
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the question based on the context."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })
    | prompt 
    | llm 
    | StrOutputParser()
)

print("\n✅ Ready! Question poochho:")

while True:
    q = input("\nQ: ").strip()
    if q.lower() in ['exit', 'quit']:
        break
    if q:
        ans = chain.invoke(q)
        print(f"A: {ans}")