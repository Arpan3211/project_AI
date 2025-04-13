"""
Generate Demo HR Data

This script generates demo HR data and populates the HR database for testing.
"""

import os
import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd

# Create the databases directory if it doesn't exist
os.makedirs("app/db", exist_ok=True)

# Database path
db_path = "app/db/hrattri_new.db"

# Check if database already exists
if not os.path.exists(db_path):
    print(f"HR database does not exist. Creating it at {db_path}")
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

    # Commit changes
    conn.commit()
else:
    # Connect to existing database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table already has data
    cursor.execute("SELECT COUNT(*) FROM hr_data")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"HR database already contains {count} records.")
        user_input = input("Do you want to clear existing data and regenerate? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting without changes.")
            conn.close()
            exit()

        # Clear existing data
        cursor.execute("DELETE FROM hr_data")
        conn.commit()
        print("Existing data cleared.")

# Generate demo data
print("Generating demo HR data...")

# Define sample data
departments = ["IT", "HR", "Finance", "Marketing", "Sales", "Operations", "Customer Support", "R&D"]
locations = ["New York", "San Francisco", "Chicago", "Austin", "Seattle", "Boston", "Atlanta", "Denver"]
bands = ["Entry", "Junior", "Mid", "Senior", "Lead", "Manager", "Director", "VP"]
processes = ["Development", "Testing", "Design", "Analysis", "Support", "Management", "Administration"]
genders = ["Male", "Female"]
reasons = ["Better opportunity", "Relocation", "Personal reasons", "Work environment", "Compensation", "Career growth", "Health issues", "Family reasons"]
voluntary_types = ["Voluntary", "Involuntary"]
age_groups = ["20-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51+"]
tenure_buckets = ["<1 year", "1-2 years", "3-5 years", "6-10 years", "10+ years"]

# Generate data for 2023 and 2024
years = [2023, 2024]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Generate 1000 employee records
employees = []
for i in range(1, 1001):
    emp_id = f"EMP{i:04d}"

    # Basic employee info
    gender = random.choice(genders)
    first_names_male = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
    first_names_female = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]

    if gender == "Male":
        first_name = random.choice(first_names_male)
    else:
        first_name = random.choice(first_names_female)

    last_name = random.choice(last_names)
    employee_name = f"{first_name} {last_name}"

    # Generate date of birth (25-55 years old)
    age = random.randint(25, 55)
    dob = datetime.now() - timedelta(days=age*365)
    date_of_birth = dob.strftime("%Y-%m-%d")

    # Generate joining date (0-10 years ago)
    years_employed = random.randint(0, 10)
    joining_date = datetime.now() - timedelta(days=years_employed*365 + random.randint(0, 364))
    date_of_joining = joining_date.strftime("%Y-%m-%d")

    # Assign department, band, etc.
    department = random.choice(departments)
    location = random.choice(locations)
    band = random.choice(bands)
    process = random.choice(processes)

    # Determine if employee has left
    is_inactive = random.random() < 0.15  # 15% attrition rate

    # For inactive employees, generate resignation details
    if is_inactive:
        # Resignation date is after joining but before now
        max_days_after_joining = (datetime.now() - joining_date).days
        # Ensure max_days_after_joining is at least 30 to avoid empty range error
        if max_days_after_joining < 30:
            days_after_joining = max_days_after_joining
        else:
            days_after_joining = random.randint(30, max_days_after_joining)  # At least 30 days after joining
        resignation_date = joining_date + timedelta(days=days_after_joining)
        date_of_resignation = resignation_date.strftime("%Y-%m-%d")

        # Last working day is typically 2-4 weeks after resignation
        notice_period = random.randint(14, 30)
        last_working_day_date = resignation_date + timedelta(days=notice_period)
        last_working_day = last_working_day_date.strftime("%Y-%m-%d")

        # Date of intimation is usually same as resignation date
        date_of_intimation = date_of_resignation

        reason = random.choice(reasons)
        voluntary_involuntary = random.choice(voluntary_types)
    else:
        date_of_resignation = None
        last_working_day = None
        date_of_intimation = None
        reason = None
        voluntary_involuntary = None

    # Determine age group
    if age < 26:
        age_group = "20-25"
    elif age < 31:
        age_group = "26-30"
    elif age < 36:
        age_group = "31-35"
    elif age < 41:
        age_group = "36-40"
    elif age < 46:
        age_group = "41-45"
    elif age < 51:
        age_group = "46-50"
    else:
        age_group = "51+"

    # Determine tenure bucket
    if years_employed < 1:
        tenure_bucket = "<1 year"
    elif years_employed < 3:
        tenure_bucket = "1-2 years"
    elif years_employed < 6:
        tenure_bucket = "3-5 years"
    elif years_employed < 11:
        tenure_bucket = "6-10 years"
    else:
        tenure_bucket = "10+ years"

    # Add employee to list
    employees.append({
        "emp_id": emp_id,
        "employee_name": employee_name,
        "date_of_birth": date_of_birth,
        "age": age,
        "gender": gender,
        "date_of_joining": date_of_joining,
        "band": band,
        "designation": band,  # Using band as designation for simplicity
        "process": process,
        "voice_non_voice": "Non_Voice" if department in ["IT", "Finance", "R&D"] else "Voice",
        "account_name": "Main Account",
        "domain": "Corporate",
        "department": department,
        "manager": random.choice(["Manager1", "Manager2", "Manager3", "Manager4", "Manager5"]),
        "functional_head": random.choice(["Head1", "Head2", "Head3"]),
        "location": location,
        "sub_location": "Main Office",
        "country": "USA",
        "date_of_resignation": date_of_resignation,
        "last_working_day": last_working_day,
        "date_of_intimation_of_attrition": date_of_intimation,
        "reason": reason,
        "voluntary_involuntary": voluntary_involuntary,
        "nascom_attrition_analysis": voluntary_involuntary,
        "new_country": "USA",
        "active_count": 0 if is_inactive else 1,
        "new_hire": 1 if years_employed < 1 else 0,
        "opening_hc": 1,
        "overall_inactive_count": 1 if is_inactive else 0,
        "inactive_count": 1 if is_inactive else 0,
        "age_group": age_group,
        "tenure_bucket": tenure_bucket
    })

# Generate monthly records for each employee
records = []
for year in years:
    for month_idx, month in enumerate(months, 1):
        month_date = datetime(year, month_idx, 1)
        month_year = f"{month} {year}"

        for employee in employees:
            # Skip if employee hasn't joined yet
            joining_date = datetime.strptime(employee["date_of_joining"], "%Y-%m-%d")
            if month_date < joining_date:
                continue

            # Skip if employee has already left
            if employee["date_of_resignation"]:
                resignation_date = datetime.strptime(employee["date_of_resignation"], "%Y-%m-%d")
                if month_date > resignation_date:
                    continue

            # Create record for this employee for this month
            record = {
                "month": month,
                "date": month_date.strftime("%Y-%m-%d"),
                "month_year": month_year,
                "year": year,
                "count": 1
            }

            # Add employee details
            record.update(employee)

            records.append(record)

# Insert records into database
print(f"Inserting {len(records)} records into database...")

# Convert to DataFrame for easier handling
df = pd.DataFrame(records)

# Insert in batches to avoid SQLite limitations
batch_size = 500
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]

    # Convert DataFrame to list of tuples for insertion
    values = []
    for _, row in batch.iterrows():
        values.append(tuple(row))

    # Create placeholders for SQL query
    placeholders = ", ".join(["?" for _ in range(len(df.columns))])

    # Create SQL query
    columns = ", ".join(df.columns)
    sql = f"INSERT INTO hr_data ({columns}) VALUES ({placeholders})"

    # Execute query
    cursor.executemany(sql, values)

    # Commit changes
    conn.commit()

    print(f"Inserted {len(batch)} records...")

# Close connection
conn.close()

print(f"Successfully generated {len(records)} demo HR records!")
print(f"Database is ready at {db_path}")
