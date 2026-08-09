import os
import re
import time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Enterprise AI Knowledge Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[int] = 1


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")


def extract_accurate_block(query: str, text: str) -> str:
    """Document ko logical sections/blocks mein break karke sab se relevant complete block return karta hai"""

  
    raw_blocks = re.split(r"\n(?=[•\- A-Z0-9]{1,5}[\.\:\-])|\n\n+", text)

    blocks = [b.strip() for b in raw_blocks if b.strip()]

    
    stopwords = {
        "what",
        "is",
        "are",
        "the",
        "and",
        "for",
        "aur",
        "kya",
        "hain",
        "ki",
        "ka",
        "ko",
        "detail",
        "samjha",
        "do",
        "specs",
        "mein",
        "report",
        "exact",
        "kya",
        "hai",
    }
    keywords = [
        w.lower()
        for w in re.findall(r"\w+", query)
        if len(w) > 1 and w.lower() not in stopwords
    ]

    if not keywords:
        keywords = [w.lower() for w in re.findall(r"\w+", query) if len(w) > 1]

    
    best_score = 0
    best_blocks = []

    for block in blocks:
        block_lower = block.lower()
        
        score = sum(2 if kw in block_lower else 0 for kw in keywords)

        
        if any(term in query.lower() for term in ["xau", "gold", "eur/usd", "btc", "workstation"]):
            for term in ["xau", "gold", "eur/usd", "btc", "workstation"]:
                if term in query.lower() and term in block_lower:
                    score += 5

        if score > 0:
            best_blocks.append((score, block))

    
    best_blocks.sort(key=lambda x: x[0], reverse=True)

    if not best_blocks:
        return "no answer found regarding document."

    
    top_matched = [b[1] for b in best_blocks[:2]]
    return "\n\n---\n\n".join(top_matched)


def get_latest_document():
    if not os.path.exists(DOCUMENTS_DIR):
        return None
    files = [
        os.path.join(DOCUMENTS_DIR, f)
        for f in os.listdir(DOCUMENTS_DIR)
        if f.endswith(".txt")
    ]
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/v1/chat")
@app.post("/api/v1/chat/")
async def direct_chat(request: ChatRequest):
    start_time = time.time()
    try:
        raw_content = get_latest_document()
        if not raw_content:
            answer = "Error: `documents/` folder mein koi `.txt` file nahi mili."
        else:
            answer = extract_accurate_block(request.question, raw_content)

        return {
            "answer": answer,
            "conversation_id": request.conversation_id,
            "response_time_ms": int((time.time() - start_time) * 1000),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
