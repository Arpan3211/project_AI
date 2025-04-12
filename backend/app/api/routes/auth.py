from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Handle imports for both direct and package execution
try:
    from app.core.config import settings
    from app.core.security import create_access_token, blacklist_token
    from app.db.database import get_db
    from app.schemas.user import User, UserCreate, Token
    from app.services.auth import authenticate_user, create_user, get_current_user
except ImportError:
    from backend.app.core.config import settings
    from backend.app.core.security import create_access_token, blacklist_token
    from backend.app.db.database import get_db
    from backend.app.schemas.user import User, UserCreate, Token
    from backend.app.services.auth import authenticate_user, create_user, get_current_user

router = APIRouter()

@router.post("/auth/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Register a new user.
    """
    try:
        user = create_user(db, user_in)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/auth/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/auth/me", response_model=User)
def read_users_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.post("/auth/logout")
def logout(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")),
) -> Any:
    """
    Logout user by blacklisting the token.
    """
    blacklist_token(token)
    return {"message": "Successfully logged out"}
