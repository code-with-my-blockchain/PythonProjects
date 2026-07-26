from langsmith_setup import client, DATASET_NAME

# Dataset already exists?
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
    print("✅ Dataset Created")
else:
    print("✅ Dataset Already Exists")

print(dataset.id)