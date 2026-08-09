from sqlalchemy.orm import Session
from app.models.document import Document
from app.services.faiss_service import faiss_service

class DocumentService:
    @staticmethod
    def process_and_index(db: Session, document_id: int) -> Document:
        
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError("Document not found")
            
       
        faiss_service.add_document(doc)
        
        doc.status = "indexed"
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def reindex_document(db: Session, document_id: int) -> Document:
        """Delete old vectors and re-process"""
        faiss_service.delete_document(document_id)
        return DocumentService.process_and_index(db, document_id)