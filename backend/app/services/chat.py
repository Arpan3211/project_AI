from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import random

# Handle imports for both direct and package execution
try:
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.schemas.conversation import ConversationCreate
    from app.schemas.message import MessageCreate
except ImportError:
    from backend.app.models.conversation import Conversation
    from backend.app.models.message import Message
    from backend.app.schemas.conversation import ConversationCreate
    from backend.app.schemas.message import MessageCreate

# Get conversation by conversation_id
def get_conversation_by_id_str(db: Session, conversation_id: str) -> Optional[Conversation]:
    return db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()

# Get conversation by ID
def get_conversation_by_id(db: Session, conversation_id: int) -> Optional[Conversation]:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

# Get all conversations for a user
def get_user_conversations(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Conversation]:
    return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()

# Create a new conversation
def create_conversation(db: Session, conversation_in: ConversationCreate, user_id: int) -> Conversation:
    db_conversation = Conversation(
        user_id=user_id,
        title=conversation_in.title
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

# Update conversation title
def update_conversation_title(db: Session, conversation_id: int, title: str) -> Conversation:
    db_conversation = get_conversation_by_id(db, conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    db_conversation.title = title
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

# Delete a conversation
def delete_conversation(db: Session, conversation_id: int) -> bool:
    db_conversation = get_conversation_by_id(db, conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    db.delete(db_conversation)
    db.commit()
    return True

# Get all messages for a conversation
def get_conversation_messages(db: Session, conversation_id: int) -> List[Message]:
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()

# Create a new message
def create_message(db: Session, message_in: MessageCreate, conversation_id_str: str = None) -> Message:
    # Get the conversation by UUID
    conversation_uuid = conversation_id_str or message_in.conversation_id

    if not conversation_uuid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Conversation ID is required")

    # Get the conversation to ensure it exists and to get its numeric ID
    conversation = get_conversation_by_id_str(db, conversation_uuid)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    # Use the numeric ID for the database relationship
    db_message = Message(
        conversation_id= conversation_id_str,  # Use the numeric ID for the database relationship
        role=message_in.role,
        content=message_in.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# Generate AI response (demo version)
def generate_ai_response(prompt: str) -> str:
    # This is a simple demo response generator
    # In a real application, this would call an AI model API

    responses = [
        f"I understand you're saying: '{prompt}'. That's an interesting point.",
        f"Thanks for sharing your thoughts on '{prompt}'. I'd like to learn more.",
        f"Regarding '{prompt}', I think there are several perspectives to consider.",
        f"'{prompt}' is a fascinating topic. Let me share some insights.",
        f"I've processed your message about '{prompt}' and here's my response.",
        f"Your question about '{prompt}' is important. Here's what I think.",
        f"I've analyzed your input on '{prompt}' and have some thoughts to share.",
        f"Based on your message about '{prompt}', I can provide the following information."
    ]

    return random.choice(responses)
