import os
from pypdf import PdfReader
from app.db.database import SessionLocal
from app.models.models import Document, DocumentChunk, DocumentStatus
from app.services.faiss_service import faiss_service

DOCUMENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../documents"))

def auto_load_documents_from_dir():
    """Project ki 'documents/' directory se saari files automatic index karta hai."""
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    db = SessionLocal()
    
    try:
        files = os.listdir(DOCUMENTS_DIR)
        if not files:
            print("ℹ'documents/' folder is empty.")
            return

        for filename in files:
            file_path = os.path.join(DOCUMENTS_DIR, filename)
            
            
            if not os.path.isfile(file_path):
                continue

            
            existing_doc = db.query(Document).filter(Document.filename == filename).first()
            if existing_doc and existing_doc.status == DocumentStatus.INDEXED:
                continue

            print(f"Auto-indexing document: {filename}")

            
            raw_text = ""
            if filename.lower().endswith(".pdf"):
                try:
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        txt = page.extract_text()
                        if txt:
                            raw_text += txt + "\n"
                except Exception as e:
                    print(f"PDF Read Error ({filename}): {e}")
            else:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        raw_text = f.read()
                except Exception as e:
                    print(f" Text Read Error ({filename}): {e}")

            if not raw_text.strip():
                continue

            
            if not existing_doc:
                db_doc = Document(
                    title=filename,
                    filename=filename,
                    original_filename=filename,  
                    file_path=file_path,
                    file_type="application/pdf" if filename.lower().endswith(".pdf") else "text/plain",
                    file_size=os.path.getsize(file_path),
                    status=DocumentStatus.PROCESSING
                )
                db.add(db_doc)
                db.commit()
                db.refresh(db_doc)
            else:
                db_doc = existing_doc
                db_doc.status = DocumentStatus.PROCESSING
                db.commit()

            
            chunk_size = 500
            overlap = 50
            chunks_text = [
                raw_text[i : i + chunk_size]
                for i in range(0, len(raw_text), chunk_size - overlap)
                if raw_text[i : i + chunk_size].strip()
            ]

            
            for idx, text_chunk in enumerate(chunks_text):
                db.add(DocumentChunk(
                    document_id=db_doc.id,
                    chunk_index=idx,
                    content=text_chunk
                ))

            
            if chunks_text and hasattr(faiss_service, "add_texts"):
                try:
                    metadatas = [
                        {"document_id": db_doc.id, "title": db_doc.title, "chunk_index": idx}
                        for idx in range(len(chunks_text))
                    ]
                    faiss_service.add_texts(texts=chunks_text, metadatas=metadatas)
                except Exception as faiss_err:
                    print(f"FAISS Warning: {faiss_err}")

            db_doc.chunk_count = len(chunks_text)
            db_doc.status = DocumentStatus.INDEXED
            db.commit()
            print(f" Auto-Indexed: {filename}")

    except Exception as e:
        db.rollback()
        print(f" Auto-load failed: {e}")
    finally:
        db.close()
