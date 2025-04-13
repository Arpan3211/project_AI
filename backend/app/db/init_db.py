from sqlalchemy.orm import Session

# Handle imports for both direct and package execution
try:
    from app.db.database import Base, engine
    from app.models import User, Conversation, Message
    from app.schemas.user import UserCreate
    from app.services.auth import create_user
except ImportError:
    from backend.app.db.database import Base, engine
    from backend.app.models import User, Conversation, Message
    from backend.app.schemas.user import UserCreate
    from backend.app.services.auth import create_user

# Create tables
def init_db():
    # Drop all tables first to ensure clean schema
    Base.metadata.drop_all(bind=engine)
    # Create all tables with new schema
    Base.metadata.create_all(bind=engine)

    # You can add initial data here if needed
    # For example, a default admin user:
    # with Session(engine) as db:
    #     admin = UserCreate(
    #         email="admin@example.com",
    #         password="adminpassword",
    #         name="Admin User"
    #     )
    #     create_user(db, admin)

if __name__ == "__main__":
    init_db()
