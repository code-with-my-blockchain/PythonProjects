import os
import shutil
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rag import (
    DOCUMENTS_DIR,
    build_vectorstore,
    ask_question,
)

app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(DOCUMENTS_DIR, exist_ok=True)


class ChatRequest(BaseModel):
    question: str
    chat_history: List[Dict[str, Any]] = Field(default_factory=list)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "RAG Chatbot Backend is running."
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or ""

    if not filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed."
        )

    file_path = os.path.join(DOCUMENTS_DIR, filename)

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return {
            "status": "success",
            "message": "File uploaded successfully.",
            "filename": filename,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )


@app.get("/documents")
def list_documents():
    try:
        if not os.path.exists(DOCUMENTS_DIR):
            return {"documents": []}

        files = [
            f for f in os.listdir(DOCUMENTS_DIR)
            if f.lower().endswith((".pdf", ".txt"))
        ]

        return {"documents": files}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch documents: {str(e)}"
        )


@app.post("/index")
def index_documents():
    try:
        result = build_vectorstore()
        return {
            "status": "success",
            "message": "Documents indexed successfully.",
            "documents": result.get("documents", 0),
            "chunks": result.get("chunks", 0),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Indexing failed: {str(e)}"
        )


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = ask_question(
            question=question,
            chat_history=request.chat_history,
        )
        return result
    

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


@app.delete("/documents")
def delete_documents():
    try:
        if os.path.exists(DOCUMENTS_DIR):
            for filename in os.listdir(DOCUMENTS_DIR):
                file_path = os.path.join(DOCUMENTS_DIR, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)

        chroma_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "chroma_db"
        )

        if os.path.exists(chroma_dir):
            shutil.rmtree(chroma_dir, ignore_errors=True)

        return {
            "status": "success",
            "message": "Documents and vector database deleted successfully."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reset store: {str(e)}"
        )


