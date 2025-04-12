import os
import sys

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize the database
try:
    from app.db.init_db import init_db
except ImportError:
    from backend.app.db.init_db import init_db

print("Initializing database...")
init_db()
print("Database initialized successfully!")

# Run the server
print("Starting the server...")
import uvicorn
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
