# Enterprise AI Knowledge Assistant

**Groq** + **FAISS** + **SQLite** + **Sentence-Transformers**

PostgreSQL اور Ollama کی ضرورت نہیں۔

## Features
- Authentication (JWT + Admin/User)
- Document Upload (PDF, DOCX, TXT, MD, CSV, Excel)
- FAISS Vector Search
- RAG Chat with Source Citations
- Conversation Memory
- Feedback System

## Setup (Windows)

### 1. Groq API Key (مفت)
https://console.groq.com → Sign up → API Key بنائیں

### 2. Backend
```powershell
cd enterprise-ai-knowledge-assistant\backend

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. .env بنائیں
```powershell
copy .env.example .env
```

نوٹ پیڈ سے `.env` کھولیں اور صرف یہ لائن تبدیل کریں:
```env
GROQ_API_KEY=gsk_آپکی_اصل_کلید
```

### 4. Tables + Admin بنائیں
```powershell
python create_tables.py
python ../scripts/init_db.py
```

### 5. سرور چلائیں
```powershell
uvicorn app.main:app --reload --port 8000
```

کھولیں → http://localhost:8000/docs

**Login:** admin / admin123
