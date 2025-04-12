from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Handle imports for both direct and package execution
try:
    from app.db.database import get_db
    from app.services.auth import get_current_user
    from app.services.chat import (
        get_user_conversations, create_conversation, get_conversation_by_id,
        get_conversation_messages, create_message, generate_ai_response,
        update_conversation_title, delete_conversation, get_conversation_by_uuid
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
        update_conversation_title, delete_conversation, get_conversation_by_uuid
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
    messages = get_conversation_messages(db, conversation.id)

    # Create a ConversationWithMessages object
    result = ConversationWithMessages(
        id=conversation.id,
        uuid=conversation.uuid,
        user_id=conversation.user_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=messages
    )

    return result

# Get a specific conversation by UUID with messages
@router.get("/conversations/uuid/{conversation_uuid}", response_model=ConversationWithMessages)
def get_conversation_by_uuid_route(
    conversation_uuid: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific conversation by UUID with all messages.
    """
    conversation = get_conversation_by_uuid(db, conversation_uuid)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # Get messages for this conversation
    messages = get_conversation_messages(db, conversation.id)

    # Create a ConversationWithMessages object
    result = ConversationWithMessages(
        id=conversation.id,
        uuid=conversation.uuid,
        user_id=conversation.user_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=messages
    )

    return result

# Update conversation title
@router.put("/conversations/{conversation_id}", response_model=Conversation)
def update_conversation(
    conversation_id: int,
    title: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update conversation title.
    """
    conversation = get_conversation_by_id(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    updated_conversation = update_conversation_title(db, conversation_id, title)
    return updated_conversation

# Delete a conversation
@router.delete("/conversations/{conversation_id}")
def delete_conversation_route(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a conversation.
    """
    conversation = get_conversation_by_id(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    delete_conversation(db, conversation_id)
    return {"status": "success", "message": "Conversation deleted"}

# Send a message and get AI response
@router.post("/chat", response_model=List[Message])
def chat(
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Send a message and get AI response.
    """
    # Determine the conversation
    conversation_id = None
    if message_in.conversation_id:
        conversation = get_conversation_by_id(db, message_in.conversation_id)
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

        if conversation.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        conversation_id = conversation.id
    elif message_in.conversation_uuid:
        conversation = get_conversation_by_uuid(db, message_in.conversation_uuid)
        if not conversation:
            # Create a new conversation if it doesn't exist
            new_conversation = ConversationCreate(title="New Conversation")
            conversation = create_conversation(db, new_conversation, current_user.id)

        if conversation.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        conversation_id = conversation.id
    else:
        # Create a new conversation
        new_conversation = ConversationCreate(title="New Conversation")
        conversation = create_conversation(db, new_conversation, current_user.id)
        conversation_id = conversation.id

    # Ensure the role is 'user'
    message_in.role = "user"

    # Save the user message
    user_message = create_message(db, message_in, conversation_id)

    # Generate AI response
    ai_response_text = generate_ai_response(message_in.content)

    # Create AI response message
    ai_message_in = MessageCreate(
        role="assistant",
        content=ai_response_text,
        conversation_id=conversation_id
    )
    ai_message = create_message(db, ai_message_in, conversation_id)

    # Return both messages
    return [user_message, ai_message]
