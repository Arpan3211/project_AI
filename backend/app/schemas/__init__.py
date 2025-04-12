# This file makes the schemas directory a Python package
try:
    from app.schemas.user import User, UserCreate, UserLogin, Token, TokenPayload
    from app.schemas.conversation import Conversation, ConversationCreate, ConversationWithMessages
    from app.schemas.message import Message, MessageCreate
except ImportError:
    from backend.app.schemas.user import User, UserCreate, UserLogin, Token, TokenPayload
    from backend.app.schemas.conversation import Conversation, ConversationCreate, ConversationWithMessages
    from backend.app.schemas.message import Message, MessageCreate
