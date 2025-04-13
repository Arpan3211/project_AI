from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

# Shared properties
class ConversationBase(BaseModel):
    title: Optional[str] = "New Conversation"

# Properties to receive via API on creation
class ConversationCreate(ConversationBase):
    pass

# Properties to return via API
class Conversation(ConversationBase):
    id: int
    conversation_id: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Properties to return via API with messages
class ConversationWithMessages(Conversation):
    messages: List[Any] = []

    class Config:
        orm_mode = True
