from dotenv import load_dotenv
import os

from langsmith import Client

load_dotenv()

client = Client(
    api_key=os.getenv("LANGCHAIN_API_KEY")
)

PROJECT_NAME = "PDF-RAG-LANGSMITH"
DATASET_NAME = "PDF-RAG-Dataset"