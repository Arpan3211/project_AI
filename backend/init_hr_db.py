"""
Initialize HR Analytics Database

This script creates the HR Analytics database and tables.
"""

import os
import sqlite3
from pathlib import Path

# Create the databases directory if it doesn't exist
os.makedirs("app/db", exist_ok=True)

# Database path
db_path = "app/db/hrattri_new.db"

# Check if database already exists
if os.path.exists(db_path):
    print(f"HR database already exists at {db_path}")
    print("To recreate the database, delete the file first.")
else:
    # Create the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the HR data table
    cursor.execute('''
    CREATE TABLE hr_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT,
        date TEXT,
        month_year TEXT,
        year INTEGER,
        count INTEGER,
        emp_id TEXT,
        employee_name TEXT,
        date_of_birth TEXT,
        age INTEGER,
        gender TEXT,
        date_of_joining TEXT,
        band TEXT,
        designation TEXT,
        process TEXT,
        voice_non_voice TEXT,
        account_name TEXT,
        domain TEXT,
        department TEXT,
        manager TEXT,
        functional_head TEXT,
        location TEXT,
        sub_location TEXT,
        country TEXT,
        date_of_resignation TEXT,
        last_working_day TEXT,
        date_of_intimation_of_attrition TEXT,
        reason TEXT,
        voluntary_involuntary TEXT,
        nascom_attrition_analysis TEXT,
        new_country TEXT,
        active_count INTEGER,
        new_hire INTEGER,
        opening_hc INTEGER,
        overall_inactive_count INTEGER,
        inactive_count INTEGER,
        age_group TEXT,
        tenure_bucket TEXT
    )
    ''')
    
    # Create indexes for frequently queried columns
    cursor.execute('CREATE INDEX idx_month ON hr_data (month)')
    cursor.execute('CREATE INDEX idx_year ON hr_data (year)')
    cursor.execute('CREATE INDEX idx_department ON hr_data (department)')
    cursor.execute('CREATE INDEX idx_location ON hr_data (location)')
    cursor.execute('CREATE INDEX idx_band ON hr_data (band)')
    cursor.execute('CREATE INDEX idx_process ON hr_data (process)')
    cursor.execute('CREATE INDEX idx_gender ON hr_data (gender)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"HR database created successfully at {db_path}")
    print("You can now import your HR data into this database.")

print("\nTo import data, you can use a script or a tool like DB Browser for SQLite.")
print("Sample import command:")
print("  python import_hr_data.py --file your_hr_data.csv")
