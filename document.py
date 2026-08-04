from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


class DocumentBase(BaseModel):
    title: str
    category: Optional[str] = None
    department: Optional[str] = None
    tags: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    tags: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: Optional[int] = None
    page_count: Optional[int] = None
    chunk_count: int = 0
    status: DocumentStatus
    error_message: Optional[str] = None
    uploaded_by: int
    created_at: datetime
    indexed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    total: int
    documents: List[DocumentResponse]
