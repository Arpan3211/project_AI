# This file makes the schemas directory a Python package
try:
    from app.schemas.user import User, UserCreate, UserLogin, Token, TokenPayload
except ImportError:
    from backend.app.schemas.user import User, UserCreate, UserLogin, Token, TokenPayload
