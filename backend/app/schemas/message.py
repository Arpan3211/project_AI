from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared properties
class MessageBase(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

# Properties to receive via API on creation
class MessageCreate(MessageBase):
    conversation_id: Optional[int] = None
    conversation_uuid: Optional[str] = None

# Properties to return via API
class Message(MessageBase):
    id: int
    uuid: str
    conversation_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
