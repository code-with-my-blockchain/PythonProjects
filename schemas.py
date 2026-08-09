from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    file_path: str
    file_type: str
    file_size: int
    status: str
    chunk_count: Optional[int] = 0
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentStatsResponse(BaseModel):
    total_documents: int
    indexed_documents: int
    processing_documents: int
    failed_documents: int
    pending_documents: int

    class Config:
        from_attributes = True