import os
import sys
import sqlite3

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Get the database path
try:
    from app.core.config import settings
except ImportError:
    from backend.app.core.config import settings

# Get the database path from settings
db_path = settings.DATABASE_URL.replace('sqlite:///', '')

# Delete the database file if it exists
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"Deleted existing database: {db_path}")
    except Exception as e:
        print(f"Error deleting database: {e}")
        # If we can't delete the file, try to recreate the tables
        pass

# Initialize the database
try:
    from app.db.init_db import init_db
except ImportError:
    from backend.app.db.init_db import init_db

print("Initializing database...")
init_db()
print("Database initialized successfully!")

# Verify the database schema
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    
    print("\nTable schema for 'users':")
    for column in columns:
        print(f"  {column[1]} ({column[2]})")
    
    conn.close()
    print("\nDatabase verification complete.")
except Exception as e:
    print(f"Error verifying database: {e}")

print("\nDatabase setup complete. You can now start the server.")
