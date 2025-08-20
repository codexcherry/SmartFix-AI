from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import sys

from .api.api import api_router
from .core.config import settings
from .services.database import JSONDatabase

# Debug prints
print("Current working directory:", os.getcwd())
print("Database file path:", settings.DB_FILE)
print("Database directory exists:", os.path.exists(os.path.dirname(settings.DB_FILE)))
print("Python version:", sys.version)

# Create database directory if it doesn't exist
os.makedirs(os.path.dirname(settings.DB_FILE), exist_ok=True)

try:
    # Initialize database
    db = JSONDatabase()
    print("Database initialized successfully")
except Exception as e:
    print(f"Error initializing database: {e}")
    raise

app = FastAPI(
    title=settings.APP_NAME,
    description="Multimodal troubleshooting assistant API",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)