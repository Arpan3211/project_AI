from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import the routers
try:
    from app.api.routes import auth, chat
except ImportError:
    # Handle relative imports when running directly
    from backend.app.api.routes import auth, chat
# Import settings
try:
    from app.core.config import settings
except ImportError:
    # Handle relative imports when running directly
    from backend.app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Chat API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
