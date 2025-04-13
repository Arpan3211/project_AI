"""
Test script to check if the database models are working correctly.
"""

from sqlalchemy.orm import Session
from app.db.database import engine, Base
from app.models.user import User
from app.core.security import get_password_hash

# Create a test user
def create_test_user():
    with Session(engine) as db:
        # Check if test user already exists
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if test_user:
            print(f"Test user already exists: {test_user.user_id}")
            return
        
        # Create a new test user
        hashed_password = get_password_hash("testpassword")
        new_user = User(
            name="Test User",
            email="test@example.com",
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"Created test user with ID: {new_user.id}")
        print(f"User UUID: {new_user.user_id}")

if __name__ == "__main__":
    print("Testing database models...")
    create_test_user()
    print("Test complete!")
