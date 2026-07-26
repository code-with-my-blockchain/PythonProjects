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

print("✅ Examples Added")