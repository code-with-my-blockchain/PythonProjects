import os
import re
import time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI CHATBOT")

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


def extract_accurate_block(query: str, raw_text: str) -> str:
    
    clean_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    
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
        "mein",
        "hai",
        "batao",
        "do",
        "bare",
        "data",
        "predictions",
        "tell",
        "me",
        "about",
        "main",
        "key",
        "points",
        "se",
        "par",
        "show",
        "give",
        "karo",
        "mily",
        "detail",
    }

    words = [
        w.lower()
        for w in re.findall(r"\w+", query)
        if len(w) > 1 and w.lower() not in stopwords
    ]

    if not words:
        return  "Please ask a specific keyword query (e.g., BTC, Gold, EUR/USD, CPU, RAM)."

     
    lines = [
        line.strip()
        for line in re.split(r"[\n\.]+", clean_text)
        if len(line.strip()) > 15
    ]

    content_lines = []
    for line in lines:
        if any(
            line.startswith(prefix)
            for prefix in [
                "DOCUMENT METADATA",
                "System Target",
                "Version",
                "File Name",
                "Target Directory",
                "END OF SPECIFICATION",
                "=",
            ]
        ):
            continue
        content_lines.append(line)

   
    matched_results = []
    for line in content_lines:
        line_lower = line.lower()
        score = 0
        for w in words:
            if re.search(r"\b" + re.escape(w) + r"\b", line_lower):
                score += 5
            elif w in line_lower:
                score += 2

        if score > 0:
            matched_results.append((score, line))

   
    trading_keywords = {
        "btc",
        "bitcoin",
        "gold",
        "xau",
        "eur",
        "gbp",
        "forex",
        "trading",
    }
    if any(tk in query.lower() for tk in trading_keywords):
        for line in content_lines:
            line_lower = line.lower()
            if any(
                rk in line_lower
                for rk in ["risk", "drawdown", "win rate", "circuit breaker"]
            ):
                if not any(line == item[1] for item in matched_results):
                    matched_results.append((3, line))

    if not matched_results:
        return (
            "No details found regarding documents."
        )

    
    matched_results.sort(key=lambda x: x[0], reverse=True)

    top_answers = []
    for score, line in matched_results:
        clean_line = line.strip("• ").strip()
        if clean_line not in top_answers:
            top_answers.append(clean_line)
        if len(top_answers) >= 4:  
            break

    return "\n\n".join([f"• {ans}" for ans in top_answers])


def get_latest_document() -> Optional[str]:
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
            answer = " Error: `backend/documents/`"
        else:
            answer = extract_accurate_block(request.question, raw_content)

        return {
            "answer": answer,
            "conversation_id": request.conversation_id,
            "response_time_ms": int((time.time() - start_time) * 1000),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
