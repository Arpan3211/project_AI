# AI Chat Backend

This is the backend API for the AI Chat application, built with FastAPI.

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   └── chat.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── database.py
│   │   └── init_db.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── services/
│   │   └── auth.py
│   └── utils/
├── main.py
├── setup_and_run.py
├── install_dependencies.py
└── requirements.txt
```

## Quick Start

For the easiest setup, use the provided scripts:

1. Install dependencies:
   ```
   python install_dependencies.py
   ```

2. Initialize the database and run the server in one step:
   ```
   python setup_and_run.py
   ```

## Manual Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python init_db.py
   ```

5. Run the server:
   ```
   python run.py
   ```
   or
   ```
   uvicorn main:app --reload
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

The API uses JWT tokens for authentication. To authenticate:

1. Register a new user at `/api/auth/register`
2. Login at `/api/auth/login` to get an access token
3. Use the access token in the Authorization header for protected endpoints:
   ```
   Authorization: Bearer {your_token}
   ```

## Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user info
- `POST /api/chat` - Send a message to the chatbot
- `GET /api/chat/history` - Get chat history

## Troubleshooting

### Import Errors

If you encounter import errors, it might be due to Python's module resolution. Try one of these solutions:

1. Run the server using the provided scripts:
   ```
   python setup_and_run.py
   ```

2. Add the project directory to PYTHONPATH:
   ```
   # Windows
   set PYTHONPATH=%PYTHONPATH%;.

   # Linux/Mac
   export PYTHONPATH=$PYTHONPATH:.
   ```

### Database Errors

If you encounter database errors:

1. Make sure the database is initialized:
   ```
   python init_db.py
   ```

2. Check if the database file exists in the `app/db/` directory

3. If the database file is corrupted, delete it and reinitialize:
   ```
   del app\db\chat.db
   python init_db.py
   ```

### Dependency Errors

If you encounter dependency errors:

1. Make sure all dependencies are installed:
   ```
   python install_dependencies.py
   ```

2. If you're using a virtual environment, make sure it's activated

3. If specific packages are causing issues, try installing them manually:
   ```
   pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib bcrypt python-multipart email-validator
   ```
