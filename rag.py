import os
DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")

def build_vectorstore():

    return {"documents": 0, "chunks": 0}


def ask_question(question: str, chat_history: list = None):
   
    return {
        "answer": "Sample answer",
        "sources": []
    }