# This file makes the models directory a Python package
try:
    from app.models.user import User
except ImportError:
    from backend.app.models.user import User
