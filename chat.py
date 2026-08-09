from typing import Optional, Union
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[Union[int, str]] = 1
