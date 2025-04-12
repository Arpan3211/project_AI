# This file makes the models directory a Python package
try:
    from app.models.user import User
    from app.models.conversation import Conversation
    from app.models.message import Message
except ImportError:
    from backend.app.models.user import User
    from backend.app.models.conversation import Conversation
    from backend.app.models.message import Message
