"""
Pydantic models for request/response validation
"""

from typing import List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_completion_tokens: Optional[int] = None


class PrefillRequest(BaseModel):
    email_text: str
    model: Optional[str] = None


class PrefillResponse(BaseModel):
    success: bool
    message: str