import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "your_huggingface_api_key_here")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "your_serpapi_key_here")
    TWILIO_SID: str = os.getenv("TWILIO_SID", "your_twilio_sid_here")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_auth_token_here")
    TWILIO_FROM_PHONE: str = os.getenv("TWILIO_FROM_PHONE", "your_twilio_phone_number_here")
    TWILIO_TO_PHONE: str = os.getenv("TWILIO_TO_PHONE", "your_phone_number_here")
    
    # App Settings
    APP_NAME: str = "SmartFix-AI"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    DB_FILE: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "database", "db.json")
    
    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()