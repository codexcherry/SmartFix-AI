from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

class InputType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"
    LOG = "log"
    MULTI = "multi"

class QueryInput(BaseModel):
    user_id: str = Field(default="anonymous")
    input_type: InputType
    text_query: Optional[str] = None
    image_url: Optional[str] = None
    log_content: Optional[str] = None
    voice_url: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "input_type": "text",
                "text_query": "My TV screen is flickering"
            }
        }

class SolutionStep(BaseModel):
    step_number: int
    description: str
    image_url: Optional[str] = None

class Solution(BaseModel):
    issue: str
    possible_causes: List[str]
    confidence_score: float
    recommended_steps: List[SolutionStep]
    external_sources: Optional[List[Dict[str, str]]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "issue": "TV screen flickering",
                "possible_causes": ["Loose HDMI connection", "Outdated firmware"],
                "confidence_score": 0.85,
                "recommended_steps": [
                    {"step_number": 1, "description": "Check HDMI cable connections"},
                    {"step_number": 2, "description": "Update TV firmware"}
                ],
                "external_sources": [
                    {"title": "Fix TV flickering issues", "url": "https://example.com/fix"}
                ]
            }
        }

class NotificationType(str, Enum):
    SMS = "sms"
    WHATSAPP = "whatsapp"
    EMAIL = "email"

class NotificationRequest(BaseModel):
    user_id: str
    notification_type: NotificationType
    message: str
    to_contact: str
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "notification_type": "sms",
                "message": "Your TV issue has been diagnosed: Loose HDMI connection",
                "to_contact": "+1234567890"
            }
        }

class QueryRecord(BaseModel):
    id: str
    user_id: str
    input_type: InputType
    query_content: Dict[str, Any]
    solution: Optional[Solution] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "processed"

class UserProfile(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    devices: Optional[List[Dict[str, str]]] = None
    history: List[str] = Field(default_factory=list)  # List of query IDs
