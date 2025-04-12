from datetime import datetime, timedelta
from typing import Any, Union, Optional, Dict
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token blacklist (in-memory for simplicity)
# In a production environment, this should be stored in Redis or a database
token_blacklist: Dict[str, datetime] = {}

# Clean expired tokens from blacklist periodically
def clean_expired_tokens():
    """Remove expired tokens from the blacklist"""
    now = datetime.utcnow()
    expired_tokens = [token for token, expiry in token_blacklist.items() if expiry < now]
    for token in expired_tokens:
        token_blacklist.pop(token, None)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Hash password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Create access token
def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Blacklist a token
def blacklist_token(token: str):
    """Add a token to the blacklist"""
    try:
        # Get token expiry time
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        exp = datetime.fromtimestamp(payload.get("exp"))

        # Add to blacklist
        token_blacklist[token] = exp

        # Clean expired tokens
        clean_expired_tokens()

        return True
    except Exception:
        return False

# Check if token is blacklisted
def is_token_blacklisted(token: str) -> bool:
    """Check if a token is in the blacklist"""
    # Clean expired tokens first
    clean_expired_tokens()
    return token in token_blacklist
