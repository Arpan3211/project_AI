"""
HR Database Service

This module provides a simple database connection for HR Analytics
that doesn't rely on LangChain, for use when LangChain is not available.
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
import os

# Handle imports for both direct and package execution
try:
    from app.core.config import settings
except ImportError:
    from backend.app.core.config import settings

class HRDatabase:
    """Simple database connection for HR Analytics"""
    
    def __init__(self, db_path: str = None):
        """Initialize the database connection"""
        if db_path is None:
            # Extract the path from the SQLAlchemy URI
            db_path = settings.HR_DATABASE_URL.replace('sqlite:///', '')
        
        self.db_path = db_path
        self.dialect = "sqlite"
        self._conn = None
    
    def connect(self) -> None:
        """Connect to the database"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
    
    def close(self) -> None:
        """Close the database connection"""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    def get_table_info(self) -> str:
        """Get information about the tables in the database"""
        if not self._conn:
            self.connect()
        
        cursor = self._conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        table_info = []
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            column_info = []
            for col in columns:
                column_info.append(f"{col[1]} ({col[2]})")
            
            table_info.append(f"Table: {table_name}")
            table_info.append("Columns: " + ", ".join(column_info))
            table_info.append("")
        
        return "\n".join(table_info)
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return the results as a list of dictionaries"""
        if not self._conn:
            self.connect()
        
        cursor = self._conn.cursor()
        cursor.execute(query)
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        results = []
        for row in rows:
            result = {}
            for i, column in enumerate(column_names):
                result[column] = row[i]
            results.append(result)
        
        return results
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format query results as a string"""
        if not results:
            return "No results found."
        
        # Get column names from the first result
        columns = list(results[0].keys())
        
        # Calculate column widths
        widths = {column: len(column) for column in columns}
        for result in results:
            for column in columns:
                value = str(result.get(column, ""))
                widths[column] = max(widths[column], len(value))
        
        # Format header
        header = " | ".join(column.ljust(widths[column]) for column in columns)
        separator = "-+-".join("-" * widths[column] for column in columns)
        
        # Format rows
        rows = []
        for result in results:
            row = " | ".join(str(result.get(column, "")).ljust(widths[column]) for column in columns)
            rows.append(row)
        
        # Combine all parts
        return f"{header}\n{separator}\n" + "\n".join(rows)

# Create a singleton instance
hr_db = HRDatabase()
