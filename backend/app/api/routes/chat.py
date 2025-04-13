from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Handle imports for both direct and package execution
try:
    from app.db.database import get_db
    from app.services.auth import get_current_user
    from app.services.chat import (
        get_user_conversations, create_conversation, get_conversation_by_id,
        get_conversation_messages, create_message, generate_ai_response,
        update_conversation_title, delete_conversation, get_conversation_by_id_str,
        get_conversation_history
    )
    from app.schemas.conversation import Conversation, ConversationCreate, ConversationWithMessages
    from app.schemas.message import Message, MessageCreate
    from app.models.user import User
except ImportError:
    from backend.app.db.database import get_db
    from backend.app.services.auth import get_current_user
    from backend.app.services.chat import (
        get_user_conversations, create_conversation, get_conversation_by_id,
        get_conversation_messages, create_message, generate_ai_response,
        update_conversation_title, delete_conversation, get_conversation_by_id_str,
        get_conversation_history
    )
    from backend.app.schemas.conversation import Conversation, ConversationCreate, ConversationWithMessages
    from backend.app.schemas.message import Message, MessageCreate
    from backend.app.models.user import User

router = APIRouter()

# Get all conversations for the current user
@router.get("/conversations", response_model=List[Conversation])
def get_conversations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get all conversations for the current user.
    """
    conversations = get_user_conversations(db, current_user.id, skip, limit)
    return conversations

# Create a new conversation
@router.post("/conversations", response_model=Conversation, status_code=status.HTTP_201_CREATED)
def create_new_conversation(
    conversation_in: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create a new conversation.
    """
    conversation = create_conversation(db, conversation_in, current_user.id)
    return conversation

# Get a specific conversation with messages
@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific conversation with all messages.
    """
    conversation = get_conversation_by_id(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # Get messages for this conversation
    messages = get_conversation_messages(db, conversation.conversation_id)

    # Convert Message objects to dictionaries
    message_dicts = []
    for msg in messages:
        message_dicts.append({
            "id": msg.id,
            "message_id": msg.message_id,
            "conversation_id": msg.conversation_id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at
        })

    # Create a ConversationWithMessages object
    result = ConversationWithMessages(
        id=conversation.id,
        conversation_id=conversation.conversation_id,
        user_id=conversation.user_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=message_dicts
    )

    return result

# Get a specific conversation by conversation_id with messages
@router.get("/conversations/id/{conversation_id_str}", response_model=ConversationWithMessages)
def get_conversation_by_id_str_route(
    conversation_id_str: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific conversation by conversation_id with all messages.
    """
    conversation = get_conversation_by_id_str(db, conversation_id_str)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # Get messages for this conversation
    messages = get_conversation_messages(db, conversation.conversation_id)

    # Convert Message objects to dictionaries
    message_dicts = []
    for msg in messages:
        message_dicts.append({
            "id": msg.id,
            "message_id": msg.message_id,
            "conversation_id": msg.conversation_id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at
        })

    # Create a ConversationWithMessages object
    result = ConversationWithMessages(
        id=conversation.id,
        conversation_id=conversation.conversation_id,
        user_id=conversation.user_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=message_dicts
    )

    return result

# Update conversation title by ID
@router.put("/conversations/{conversation_id}", response_model=Conversation)
def update_conversation(
    conversation_id: int,
    title: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update conversation title by ID.
    """
    conversation = get_conversation_by_id(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    updated_conversation = update_conversation_title(db, conversation_id, title)
    return updated_conversation

# Update conversation title by conversation_id (UUID)
@router.put("/conversations/id/{conversation_id_str}", response_model=Conversation)
def update_conversation_by_id_str(
    conversation_id_str: str,
    title: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update conversation title by conversation_id (UUID).
    """
    conversation = get_conversation_by_id_str(db, conversation_id_str)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    updated_conversation = update_conversation_title(db, conversation.conversation_id, title)
    return updated_conversation

# Delete a conversation by ID
@router.delete("/conversations/{conversation_id}")
def delete_conversation_route(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a conversation by ID.
    """
    conversation = get_conversation_by_id(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    delete_conversation(db, conversation_id)
    return {"status": "success", "message": "Conversation deleted"}

# Delete a conversation by conversation_id (UUID)
@router.delete("/conversations/id/{conversation_id_str}")
def delete_conversation_by_id_str_route(
    conversation_id_str: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a conversation by conversation_id (UUID).
    """
    conversation = get_conversation_by_id_str(db, conversation_id_str)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    delete_conversation(db, conversation.conversation_id)
    return {"status": "success", "message": "Conversation deleted"}

# Custom response model for chat API
class ChatResponse(BaseModel):
    messages: List[Message]
    conversation: Conversation

# Send a message and get AI response
@router.post("/chat", response_model=ChatResponse)
def chat(
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Send a message and get AI response.
    """
    # Determine the conversation
    conversation = None
    conversation_id_str = message_in.conversation_id

    if conversation_id_str:
        # Try to get existing conversation by UUID
        conversation = get_conversation_by_id_str(db, conversation_id_str)
        if not conversation:
            # If not found, create a new conversation
            # Use the first part of the message as the title (up to 50 chars)
            title = message_in.content[:50] + ("..." if len(message_in.content) > 50 else "")
            new_conversation = ConversationCreate(title=title)
            conversation = create_conversation(db, new_conversation, current_user.id)
            conversation_id_str = conversation.conversation_id
        elif conversation.user_id != current_user.id:
            # Check permissions
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    else:
        # Create a new conversation
        # Use the first part of the message as the title (up to 50 chars)
        title = message_in.content[:50] + ("..." if len(message_in.content) > 50 else "")
        new_conversation = ConversationCreate(title=title)
        conversation = create_conversation(db, new_conversation, current_user.id)
        conversation_id_str = conversation.conversation_id

    # Ensure the role is 'user'
    message_in.role = "user"

    # Save the user message
    user_message = create_message(db, message_in, conversation_id_str)

    # Get conversation history for context
    conversation_history = get_conversation_history(db, conversation_id_str)

    # Generate AI response with conversation history
    ai_response_text = generate_ai_response(message_in.content, conversation_history)

    # Create AI response message
    ai_message_in = MessageCreate(
        role="assistant",
        content=ai_response_text
    )
    ai_message = create_message(db, ai_message_in, conversation_id_str)

    # Return messages and conversation details
    return {
        "messages": [user_message, ai_message],
        "conversation": conversation
    }
