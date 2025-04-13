from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared properties
class MessageBase(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

# Properties to receive via API on creation
class MessageCreate(MessageBase):
    conversation_id: Optional[str] = None  # UUID string

# Properties to return via API
class Message(MessageBase):
    id: int
    message_id: str
    conversation_id: str
    created_at: datetime

    # Support both Pydantic v1 and v2
    try:
        # Pydantic v2
        model_config = {"from_attributes": True}
    except:
        # Pydantic v1
        class Config:
            orm_mode = True
