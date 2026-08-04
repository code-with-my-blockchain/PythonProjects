from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.session import get_db
from app.models.user import User
from app.models.document import DocumentStatus
from app.schemas.document import DocumentResponse, DocumentListResponse, DocumentUpdate
from app.api.deps import get_current_user, get_current_active_admin
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt", "md", "markdown", "csv", "xlsx", "xls"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    auto_index: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Upload a document (Admin only).
    Supported formats: PDF, DOCX, TXT, Markdown, CSV, Excel
    """
    # Validate extension
    filename = file.filename or "unknown"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 50MB allowed.")

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    # Create document record
    doc = DocumentService.create_document(
        db=db,
        file_content=content,
        original_filename=filename,
        title=title or filename,
        uploaded_by=current_user.id,
        category=category,
        department=department,
        tags=tags,
    )

    # Auto process & index
    if auto_index:
        try:
            doc = DocumentService.process_and_index(db, doc.id)
        except Exception as e:
            # Document is saved but indexing failed
            pass

    return doc


@router.get("/", response_model=DocumentListResponse)
def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all documents with optional filters"""
    documents, total = DocumentService.get_documents(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        department=department,
        status=status,
    )
    return {"total": total, "documents": documents}


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single document by ID"""
    from app.models.document import Document
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/{document_id}/reindex", response_model=DocumentResponse)
def reindex_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """Re-process and re-index a document (Admin only)"""
    from app.models.document import Document
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        doc = DocumentService.reindex_document(db, document_id)
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reindexing failed: {str(e)}")


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """Delete a document and its vectors (Admin only)"""
    success = DocumentService.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return None


@router.get("/stats/index")
def get_index_stats(
    current_user: User = Depends(get_current_active_admin),
):
    """Get FAISS index statistics (Admin only)"""
    from app.services.faiss_service import faiss_service
    return faiss_service.get_stats()
