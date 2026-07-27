from dotenv import load_dotenv
import os

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "PDF-RAG-LANGSMITH"

from langsmith import traceable

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough,
)

from prompts import prompt
from vector_store import load_vector_store

vectorstore = load_vector_store()

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

@traceable(name="Format Documents")
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

parallel = RunnableParallel(
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    }
)

chain = (
    parallel
    | prompt
    | llm
    | StrOutputParser()
)

@traceable(name="Question Answering")
def ask_question(question: str):

    response = chain.invoke(question)

    docs = retriever.invoke(question)

    print("\n==============================")
    print("Retrieved Documents")
    print("==============================")

    for i, doc in enumerate(docs, start=1):

        print(f"\n----- Document {i} -----\n")

        print(doc.page_content[:500])

        print("\n------------------------")

    return response


def main():

    print("=" * 50)
    print(" PDF RAG with Gemini + LangSmith ")
    print("=" * 50)

    print("\nType 'exit' to quit.\n")

    while True:

        try:

            question = input("Question : ").strip()

            if question.lower() in ["exit", "quit", "q"]:

                print("\nGood Bye ")

                break

            if not question:

                continue

            answer = ask_question(question)

            print("\nAnswer\n")

            print(answer)

            print("\n" + "=" * 60 + "\n")

        except KeyboardInterrupt:

            print("\nStopped by user.")

            break

        except Exception as e:

            print("\nError : ", e)


if __name__ == "__main__":

    main()

    from dotenv import load_dotenv
import os

from langsmith import Client

load_dotenv()

client = Client(
    api_key=os.getenv("LANGCHAIN_API_KEY")
)

PROJECT_NAME = "PDF-RAG-LANGSMITH"
DATASET_NAME = "PDF-RAG-Dataset"

from langsmith_setup import client, DATASET_NAME


datasets = list(client.list_datasets())

dataset = None

for ds in datasets:
    if ds.name == DATASET_NAME:
        dataset = ds
        break

if dataset is None:
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Questions and answers for PDF RAG"
    )
    print(" Dataset Created")
else:
    print(" Dataset Already Exists")

print(dataset.id)

from langsmith_setup import client, DATASET_NAME

dataset = client.read_dataset(
    dataset_name=DATASET_NAME
)

examples = [

    {
        "question": "What is machine learning?",
        "answer": "Machine learning is..."
    },

    {
        "question": "What is regression?",
        "answer": "Regression is..."
    },

    {
        "question": "Explain classification.",
        "answer": "Classification predicts categories."
    }

]

for ex in examples:

    client.create_example(

        inputs={
            "question": ex["question"]
        },

        outputs={
            "answer": ex["answer"]
        },

        dataset_id=dataset.id

    )

print("Examples Added")

from langsmith import Client
from langsmith.evaluation import evaluate

from rag import chain

client = Client()


def prediction(inputs: dict):

    question = inputs["question"]

    answer = chain.invoke(question)

    return {
        "answer": answer
    }


results = evaluate(
    prediction,
    data="PDF-RAG-Dataset",
    experiment_prefix="gemini-rag-evaluation",
)

print(results)

def exact_match(outputs, reference_outputs):

    prediction = outputs["answer"].strip().lower()

    expected = reference_outputs["answer"].strip().lower()

    return {
        "score": prediction == expected
    }

results = evaluate(
    prediction,
    data="PDF-RAG-Dataset",
    evaluators=[exact_match],
    experiment_prefix="exact-match",
)

from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    metadata={
        "llm": "gemini-2.5-flash",
        "retriever": "faiss",
        "application": "pdf-rag",
    }
)
while True:

    question = input("Question: ").strip()

    if not question:
        print("Please enter a question.")
        continue

    if question.lower() in ["exit", "quit", "q"]:
        print("Good Bye!")
        break

    try:
        answer = chain.invoke(question)

        print("\nAnswer:\n")
        print(answer)

    except Exception as e:
        print(f"\nError: {e}")
        

docs = retriever.invoke(question)

print("\nRetrieved Sources:\n")

for i, doc in enumerate(docs, start=1):
    print(f"Source {i}:")
    print(doc.page_content[:300])
    print("-" * 50)

    
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    metadata={
        "project": "PDF-RAG-LANGSMITH",
        "model": "gemini-1.5-flash"
    }
)

answer = chain.invoke(question, config=config)
