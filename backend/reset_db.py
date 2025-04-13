"""
Reset Database Script

This script drops all tables and recreates them with the new schema.
Run this script after making changes to the database models.
"""

from app.db.init_db import init_db

if __name__ == "__main__":
    print("Resetting database...")
    init_db()
    print("Database reset complete!")
