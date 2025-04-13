import os
import sys

# Add the current directory to the path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Also add the parent directory to handle 'backend' imports
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Initialize the database
try:
    # Try direct import first
    from app.db.init_db import init_db
except ImportError as e:
    print(f"Direct import failed: {e}")
    try:
        # Try relative import
        from backend.app.db.init_db import init_db
    except ImportError as e:
        print(f"Relative import failed: {e}")
        # Last resort: manual import
        sys.path.insert(0, os.path.join(current_dir, 'app', 'db'))
        import init_db
        init_db = init_db.init_db

print("Initializing database...")
init_db()
print("Database initialized successfully!")

# Run the server
print("Starting the server...")
import uvicorn

# Use the proper idiom for multiprocessing
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
