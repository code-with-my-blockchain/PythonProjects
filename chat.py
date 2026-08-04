from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class ChatMessage(BaseModel):
    role: str 
    content: str


class SourceCitation(BaseModel):
    document_id: int
    document_title: str
    filename: str
    chunk_index: int
    text: str
    score: float


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[int] = None  
    top_k: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceCitation] = []
    conversation_id: int
    message_id: int
    response_time_ms: Optional[int] = None


class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    message_count: int = 0

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[Any] = None
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    messages: List[MessageResponse]


class FeedbackRequest(BaseModel):
    feedback: str = Field(..., pattern="^(helpful|not_helpful)$")
