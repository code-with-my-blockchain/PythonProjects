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

