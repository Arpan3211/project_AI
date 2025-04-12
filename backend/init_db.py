# Import the init_db function
try:
    from app.db.init_db import init_db
except ImportError:
    # Handle relative imports when running directly
    from backend.app.db.init_db import init_db

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
