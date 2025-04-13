# This file makes the models directory a Python package
try:
    from app.models.user import User
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models.hr_analytics import HRData
except ImportError:
    from backend.app.models.user import User
    from backend.app.models.conversation import Conversation
    from backend.app.models.message import Message
    from backend.app.models.hr_analytics import HRData
