from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, List
import os

from app.models.document import Document, DocumentStatus
from app.models.user import User
from app.services.document_processor import (
    extract_text, clean_text, split_text, save_uploaded_file, get_file_extension
)
from app.services.faiss_service import faiss_service
from app.core.config import settings


class DocumentService:

    @staticmethod
    def create_document(
        db: Session,
        file_content: bytes,
        original_filename: str,
        title: str,
        uploaded_by: int,
        category: Optional[str] = None,
        department: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> Document:
       
        saved_filename, file_path = save_uploaded_file(file_content, original_filename)
        file_type = get_file_extension(original_filename)
        file_size = len(file_content)

        
        doc = Document(
            title=title or original_filename,
            filename=saved_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            category=category,
            department=department,
            tags=tags,
            status=DocumentStatus.PENDING,
            uploaded_by=uploaded_by,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def process_and_index(db: Session, document_id: int) -> Document:
        """Extract text, chunk, embed and store in FAISS"""
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError("Document not found")

        try:
            doc.status = DocumentStatus.PROCESSING
            db.commit()

            
            text, page_count = extract_text(doc.file_path, doc.file_type)
            text = clean_text(text)

            if not text.strip():
                raise ValueError("No text could be extracted from the document")

            
            chunks = split_text(text)

            
            chunk_count = faiss_service.add_documents(
                chunks=chunks,
                document_id=doc.id,
                document_title=doc.title,
                filename=doc.original_filename,
            )

            
            doc.page_count = page_count
            doc.chunk_count = chunk_count
            doc.status = DocumentStatus.INDEXED
            doc.indexed_at = datetime.now(timezone.utc)
            doc.error_message = None
            db.commit()
            db.refresh(doc)

            return doc

        except Exception as e:
            doc.status = DocumentStatus.FAILED
            doc.error_message = str(e)
            db.commit()
            db.refresh(doc)
            raise

    @staticmethod
    def delete_document(db: Session, document_id: int) -> bool:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return False

        
        faiss_service.delete_document(document_id)

       
        if os.path.exists(doc.file_path):
            try:
                os.remove(doc.file_path)
            except Exception:
                pass

        
        db.delete(doc)
        db.commit()
        return True

    @staticmethod
    def get_documents(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        category: Optional[str] = None,
        department: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[List[Document], int]:
        query = db.query(Document)

        if category:
            query = query.filter(Document.category == category)
        if department:
            query = query.filter(Document.department == department)
        if status:
            query = query.filter(Document.status == status)

        total = query.count()
        documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
        return documents, total

    @staticmethod
    def reindex_document(db: Session, document_id: int) -> Document:
        """Delete old vectors and re-process"""
       
        faiss_service.delete_document(document_id)
       
        return DocumentService.process_and_index(db, document_id)
