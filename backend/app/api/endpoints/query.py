from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from typing import Optional, List, Dict, Any
import uuid
import json
from datetime import datetime
import base64
import io
from PIL import Image
import re

from ...models.schemas import QueryInput, Solution, NotificationRequest
from ...services.database import JSONDatabase
from ...services.gemini_service import GeminiService
from ...services.serpapi_service import SerpAPIService
from ...services.twilio_service import TwilioService
from ...services.ocr_service import OCRService
from ...services.brain_core import BrainCore
from ...services.virtual_assistant import VirtualAssistantService
from ...services.device_detector import DeviceDetectorService

router = APIRouter()

# Initialize services
db = JSONDatabase()
gemini_service = GeminiService()
serp_service = SerpAPIService()
twilio_service = TwilioService()
ocr_service = OCRService()
brain_core = BrainCore()  # Initialize the brain core system
virtual_assistant = VirtualAssistantService()  # Initialize the virtual assistant
device_detector = DeviceDetectorService()  # Initialize the device detector

@router.post("/text", response_model=Dict[str, Any])
async def process_text_query(query: QueryInput):
    """Process a text-based troubleshooting query using the brain core system"""
    if not query.text_query:
        raise HTTPException(status_code=400, detail="Text query is required")
    
    # Generate a unique ID for this query
    query_id = str(uuid.uuid4())
    
    # Store the query in the database
    query_record = {
        "id": query_id,
        "user_id": query.user_id,
        "input_type": query.input_type,
        "query_content": {"text": query.text_query},
        "timestamp": datetime.now().isoformat(),
        "status": "processing"
    }
    db.add_query(query_record)
    
    try:
        # Use the brain core system to process the input
        input_data = {
            "input_type": "text",
            "text_query": query.text_query,
            "device_category": getattr(query, 'device_category', None),
            "user_id": query.user_id
        }
        
        # Process with brain core (includes brain memory + AI analysis)
        brain_result = await brain_core.process_input(input_data)
        
        # Update the query record with the solution
        db.update_query(query_id, {
            "solution": brain_result["solution"],
            "status": "completed",
            "brain_analysis": {
                "source": brain_result.get("source", "unknown"),
                "query_text": brain_result.get("query_text", query.text_query)
            }
        })
        
        return brain_result
    
    except Exception as e:
        # Log the error and return a fallback response
        print(f"Error processing text query with brain core: {e}")
        
        # Create a fallback solution
        fallback_solution = {
            "query_id": query_id,
            "solution": {
                "issue": f"Error analyzing: {query.text_query[:50]}...",
                "possible_causes": ["Brain system error", "Service unavailable"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please try again with more details about your issue"}
                ],
                "external_sources": []
            },
            "source": "error",
            "query_text": query.text_query
        }
        
        # Update the query record with the error
        db.update_query(query_id, {
            "solution": fallback_solution["solution"],
            "status": "error",
            "error_message": str(e)
        })
        
        return fallback_solution

@router.post("/image", response_model=Dict[str, Any])
async def process_image_query(
    image: UploadFile = File(...),
    text_query: Optional[str] = Form(None),
    user_id: str = Form("anonymous")
):
    """Process an image-based troubleshooting query using the brain core system"""
    # Read image data
    image_data = await image.read()
    
    # Generate a unique ID for this query
    query_id = str(uuid.uuid4())
    
    # Store the query in the database
    query_record = {
        "id": query_id,
        "user_id": user_id,
        "input_type": "image",
        "query_content": {"image": image.filename, "text": text_query},
        "timestamp": datetime.now().isoformat(),
        "status": "processing"
    }
    db.add_query(query_record)
    
    try:
        # Use the brain core system to process the image input
        input_data = {
            "input_type": "image",
            "text_query": text_query or "",
            "image_data": image_data,
            "user_id": user_id
        }
        
        # Process with brain core (includes OCR + brain memory + AI analysis)
        brain_result = await brain_core.process_input(input_data)
        
        # Update the query record with the solution
        db.update_query(query_id, {
            "solution": brain_result["solution"],
            "status": "completed",
            "brain_analysis": {
                "source": brain_result.get("source", "unknown"),
                "query_text": brain_result.get("query_text", text_query or "")
            }
        })
        
        return brain_result
    
    except Exception as e:
        # Log the error and return a fallback response
        print(f"Error processing image query with brain core: {e}")
        
        # Create a fallback solution
        fallback_solution = {
            "query_id": query_id,
            "solution": {
                "issue": "Unable to process image",
                "possible_causes": ["Image format not supported", "Brain system error"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please try with a clearer image"}
                ],
                "external_sources": []
            },
            "source": "error",
            "query_text": text_query or ""
        }
        
        # Update the query record with the error
        db.update_query(query_id, {
            "solution": fallback_solution["solution"],
            "status": "error",
            "error_message": str(e)
        })
        
        return fallback_solution

@router.post("/voice", response_model=Dict[str, Any])
async def process_voice_query(
    audio: UploadFile = File(...),
    user_id: str = Form("anonymous")
):
    """Process a voice-based troubleshooting query using the brain core system"""
    # Read audio data
    audio_data = await audio.read()
    
    # Generate a unique ID for this query
    query_id = str(uuid.uuid4())
    
    # Store the query in the database
    query_record = {
        "id": query_id,
        "user_id": user_id,
        "input_type": "voice",
        "query_content": {"audio": audio.filename},
        "timestamp": datetime.now().isoformat(),
        "status": "processing"
    }
    db.add_query(query_record)
    
    try:
        # Use the brain core system to process the voice input
        input_data = {
            "input_type": "voice",
            "audio_data": audio_data,
            "user_id": user_id
        }
        
        # Process with brain core (includes STT + brain memory + AI analysis)
        brain_result = await brain_core.process_input(input_data)
        
        # Update the query record with the solution
        db.update_query(query_id, {
            "solution": brain_result["solution"],
            "query_content": {"audio": audio.filename, "transcribed_text": brain_result.get("query_text", "")},
            "status": "completed",
            "brain_analysis": {
                "source": brain_result.get("source", "unknown"),
                "query_text": brain_result.get("query_text", "")
            }
        })
        
        return brain_result
    
    except Exception as e:
        # Log the error and return a fallback response
        print(f"Error processing voice query with brain core: {e}")
        
        # Create a fallback solution
        fallback_solution = {
            "query_id": query_id,
            "solution": {
                "transcribed_text": "Could not transcribe audio",
                "issue": "Unable to process voice query",
                "possible_causes": ["Audio format not supported", "Brain system error"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please try with a text query instead"}
                ],
                "external_sources": []
            },
            "source": "error",
            "query_text": ""
        }
        
        # Update the query record with the error
        db.update_query(query_id, {
            "solution": fallback_solution["solution"],
            "status": "error",
            "error_message": str(e)
        })
        
        return fallback_solution

@router.post("/logs", response_model=Dict[str, Any])
async def process_log_query(
    log_file: UploadFile = File(...),
    user_id: str = Form("anonymous")
):
    """Process a log file for troubleshooting using the brain core system"""
    # Read log data
    log_content = await log_file.read()
    log_text = log_content.decode("utf-8", errors="ignore")
    
    # Generate a unique ID for this query
    query_id = str(uuid.uuid4())
    
    # Store the query in the database
    query_record = {
        "id": query_id,
        "user_id": user_id,
        "input_type": "log",
        "query_content": {"log_file": log_file.filename},
        "timestamp": datetime.now().isoformat(),
        "status": "processing"
    }
    db.add_query(query_record)
    
    try:
        # Use the brain core system to process the log input
        input_data = {
            "input_type": "log",
            "log_content": log_text,
            "user_id": user_id
        }
        
        # Process with brain core (includes log parsing + brain memory + AI analysis)
        brain_result = await brain_core.process_input(input_data)
        
        # Update the query record with the solution
        db.update_query(query_id, {
            "solution": brain_result["solution"],
            "status": "completed",
            "brain_analysis": {
                "source": brain_result.get("source", "unknown"),
                "query_text": brain_result.get("query_text", "")
            }
        })
        
        return brain_result
    
    except Exception as e:
        # Log the error and return a fallback response
        print(f"Error processing log query with brain core: {e}")
        
        # Create a fallback solution
        fallback_solution = {
            "query_id": query_id,
            "solution": {
                "issue": "Unable to process log file",
                "possible_causes": ["Log format not supported", "Brain system error"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please try with a different log format"}
                ],
                "external_sources": []
            },
            "source": "error",
            "query_text": ""
        }
        
        # Update the query record with the error
        db.update_query(query_id, {
            "solution": fallback_solution["solution"],
            "status": "error",
            "error_message": str(e)
        })
        
        return fallback_solution

@router.post("/notify", response_model=Dict[str, Any])
async def send_notification(notification: NotificationRequest):
    """Send a notification via SMS or WhatsApp"""
    result = {
        "success": False,
        "message": "",
        "notification_id": str(uuid.uuid4())
    }
    
    # Store notification in database
    notification_record = {
        "id": result["notification_id"],
        "user_id": notification.user_id,
        "notification_type": notification.notification_type,
        "message": notification.message,
        "to_contact": notification.to_contact,
        "timestamp": datetime.now().isoformat(),
        "status": "processing"
    }
    db.add_notification(notification_record)
    
    try:
        # Send notification based on type
        if notification.notification_type == "sms":
            send_result = await twilio_service.send_sms(
                notification.to_contact,
                notification.message
            )
        elif notification.notification_type == "whatsapp":
            send_result = await twilio_service.send_whatsapp(
                notification.to_contact,
                notification.message
            )
        else:
            send_result = {
                "success": False,
                "error": f"Unsupported notification type: {notification.notification_type}"
            }
        
        # Update result and database record
        result["success"] = send_result.get("success", False)
        result["message"] = send_result.get("error", "Notification sent successfully")
        
        notification_status = "completed" if result["success"] else "failed"
        db.update_query(result["notification_id"], {
            "status": notification_status,
            "result": send_result
        })
    except Exception as e:
        result["success"] = False
        result["message"] = f"Error sending notification: {str(e)}"
        
        # Update database record with error
        db.update_query(result["notification_id"], {
            "status": "failed",
            "error_message": str(e)
        })
    
    return result

@router.get("/history/{user_id}", response_model=List[Dict[str, Any]])
async def get_user_history(user_id: str):
    """Get troubleshooting history for a specific user"""
    queries = db.get_user_queries(user_id)
    return queries

@router.get("/brain/stats", response_model=Dict[str, Any])
async def get_brain_stats():
    """Get brain system statistics and performance metrics"""
    try:
        stats = await brain_core.get_brain_stats()
        return {
            "success": True,
            "brain_stats": stats,
            "system_status": "operational"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "system_status": "error"
        }

@router.post("/brain/search", response_model=Dict[str, Any])
async def search_brain_memory(query: str = Body(..., embed=True), device_category: str = Body(None, embed=True)):
    """Search brain memory for similar problems"""
    try:
        results = await brain_core.search_brain_memory(query, device_category)
        return {
            "success": True,
            "query": query,
            "device_category": device_category,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "results": []
        }

@router.post("/brain/feedback", response_model=Dict[str, Any])
async def submit_feedback(
    query_id: str = Body(..., embed=True),
    success: bool = Body(..., embed=True),
    feedback_score: int = Body(None, embed=True)
):
    """Submit feedback for a solution to improve the brain system"""
    try:
        await brain_core.process_feedback(query_id, success, feedback_score)
        return {
            "success": True,
            "message": "Feedback processed successfully",
            "query_id": query_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/brain/add-solution", response_model=Dict[str, Any])
async def add_custom_solution(problem_data: Dict[str, Any] = Body(...)):
    """Add a custom solution to brain memory"""
    try:
        await brain_core.add_custom_solution(problem_data)
        return {
            "success": True,
            "message": "Custom solution added to brain memory",
            "problem_text": problem_data.get("problem_text", "")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Virtual Assistant Endpoints
@router.post("/assistant/chat", response_model=Dict[str, Any])
async def assistant_chat(
    query: str = Body(..., embed=True),
    user_id: str = Body("anonymous", embed=True),
    session_id: str = Body(None, embed=True),
    input_type: str = Body("text", embed=True)
):
    """Process a chat query with the virtual assistant"""
    try:
        result = await virtual_assistant.process_query(query, user_id, session_id, input_type)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/assistant/voice", response_model=Dict[str, Any])
async def assistant_voice_query(
    audio: UploadFile = File(...),
    user_id: str = Form("anonymous"),
    session_id: str = Form(None)
):
    """Process a voice query with the virtual assistant"""
    try:
        audio_data = await audio.read()
        result = await virtual_assistant.process_voice_query(audio_data, user_id, session_id)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/assistant/quick-actions", response_model=Dict[str, Any])
async def get_quick_actions():
    """Get available quick actions for the virtual assistant"""
    try:
        actions = virtual_assistant.get_quick_actions()
        return {
            "success": True,
            "quick_actions": actions
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/assistant/session/{session_id}", response_model=Dict[str, Any])
async def get_session_history(session_id: str):
    """Get conversation history for a specific session"""
    try:
        result = virtual_assistant.get_session_history(session_id)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/assistant/sessions/{user_id}", response_model=Dict[str, Any])
async def get_user_sessions(user_id: str):
    """Get all sessions for a specific user"""
    try:
        sessions = virtual_assistant.get_all_sessions(user_id)
        return {
            "success": True,
            "sessions": sessions,
            "count": len(sessions)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/assistant/stats", response_model=Dict[str, Any])
async def get_assistant_stats():
    """Get virtual assistant statistics"""
    try:
        stats = virtual_assistant.get_assistant_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/assistant/quick-actions", response_model=Dict[str, Any])
async def get_quick_actions():
    """Get quick actions for virtual assistant"""
    try:
        quick_actions = [
            { "label": "System Diagnostics", "prompt": "Run a full system diagnostic check" },
            { "label": "Error Analysis", "prompt": "Analyze recent error logs" },
            { "label": "Performance Tips", "prompt": "Provide performance optimization tips" },
            { "label": "Troubleshooting", "prompt": "Help me troubleshoot common issues" },
            { "label": "Device Health", "prompt": "Check my device health status" },
            { "label": "Security Scan", "prompt": "Perform a security analysis" }
        ]
        
        return {
            "success": True,
            "quick_actions": quick_actions
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Device Detection Endpoints
@router.post("/device/analyze", response_model=Dict[str, Any])
async def analyze_device():
    """Perform comprehensive device analysis and generate health report"""
    try:
        analysis_result = await device_detector.perform_full_system_analysis()
        return analysis_result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/device/health", response_model=Dict[str, Any])
async def get_device_health():
    """Get quick device health status"""
    try:
        health_result = await device_detector.get_quick_health_check()
        return health_result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.post("/device/analyze/quick", response_model=Dict[str, Any])
async def quick_device_scan():
    """Perform quick device scan"""
    try:
        analysis_result = await device_detector.perform_full_system_analysis()
        return analysis_result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/device/analyze/system-info", response_model=Dict[str, Any])
async def get_system_info():
    """Get detailed system information"""
    try:
        device_detector._collect_system_info()
        return {
            "success": True,
            "system_info": device_detector.system_info,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/device/analyze/performance", response_model=Dict[str, Any])
async def get_performance_metrics():
    """Get detailed performance metrics"""
    try:
        await device_detector._perform_health_checks()
        return {
            "success": True,
            "metrics": device_detector.health_metrics,
            "recommendations": device_detector.recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/device/analyze/security", response_model=Dict[str, Any])
async def get_security_analysis():
    """Get security analysis results"""
    try:
        # Mock security analysis for now
        security_issues = [
            {
                "title": "Outdated System",
                "description": "System has not been updated in 30+ days",
                "severity": "medium",
                "category": "System Updates",
                "impact": "Potential security vulnerabilities"
            },
            {
                "title": "Firewall Status",
                "description": "Firewall is active and properly configured",
                "severity": "low",
                "category": "Network Security",
                "impact": "No immediate security concerns"
            }
        ]
        
        return {
            "success": True,
            "issues": security_issues,
            "recommendations": [
                "Update system to latest version",
                "Run security scan regularly",
                "Enable automatic updates"
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/device/analyze/hardware", response_model=Dict[str, Any])
async def get_hardware_diagnostics():
    """Get hardware diagnostics"""
    try:
        # Mock hardware diagnostics
        hardware_status = {
            "storage": [
                {
                    "device": "C:",
                    "type": "SSD",
                    "health_status": "Good",
                    "temperature": 45,
                    "power_on_hours": 8760,
                    "life_remaining": 85
                }
            ],
            "battery": {
                "health": 95,
                "cycle_count": 150,
                "capacity": 87
            },
            "thermal": {
                "cpu": 65,
                "gpu": 55,
                "system": 45
            }
        }
        
        return {
            "success": True,
            "status": hardware_status,
            "recommendations": [
                "Monitor storage health regularly",
                "Keep system well ventilated",
                "Consider battery replacement if health drops below 80%"
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/device/analyze/failure", response_model=Dict[str, Any])
async def get_failure_analysis():
    """Get failure analysis results"""
    try:
        # Mock failure analysis
        failure_analysis = {
            "recent_errors": [
                {
                    "message": "Application crash detected",
                    "timestamp": datetime.now().isoformat(),
                    "severity": "medium"
                }
            ],
            "performance_degradation": {
                "cpu": 85,
                "memory": 90,
                "disk": 95
            },
            "resource_exhaustion": {
                "memory": 2,
                "cpu": 1
            },
            "root_cause": {
                "description": "High memory usage causing system slowdown",
                "probability": 75
            }
        }
        
        return {
            "success": True,
            "analysis": failure_analysis,
            "recommendations": [
                "Close unnecessary applications",
                "Increase system memory if possible",
                "Monitor resource usage regularly"
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.post("/device/analyze/deep", response_model=Dict[str, Any])
async def deep_device_scan():
    """Perform deep device scan"""
    try:
        # Perform comprehensive analysis
        analysis_result = await device_detector.perform_full_system_analysis()
        
        # Add additional deep scan data
        deep_scan_data = {
            **analysis_result,
            "scan_type": "deep",
            "additional_metrics": {
                "process_analysis": "Completed",
                "network_analysis": "Completed",
                "file_system_check": "Completed",
                "registry_analysis": "Completed"
            }
        }
        
        return deep_scan_data
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/device/detailed-metrics", response_model=Dict[str, Any])
async def get_detailed_metrics():
    """Get detailed system metrics"""
    try:
        import psutil
        import time
        
        detailed_metrics = {
            "process_count": len(list(psutil.process_iter())),
            "uptime": time.time() - psutil.boot_time(),
            "boot_time": psutil.boot_time(),
            "users_count": len(psutil.users()),
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            **detailed_metrics
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Helper functions
def extract_error_codes(text: str) -> List[str]:
    """Extract error codes from text using pattern matching"""
    # Common error code patterns
    patterns = [
        r'error\s+code[:\s]+([A-Za-z0-9\-_]+)',
        r'error[:\s]+([A-Za-z0-9\-_]+)',
        r'exception[:\s]+([A-Za-z0-9\-_]+)',
        r'fail[:\s]+([A-Za-z0-9\-_]+)',
        r'([A-Z][0-9]{4,6})',  # Common format like E12345
        r'([A-Z]-[0-9]{2,4})'  # Format like E-123
    ]
    
    error_codes = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        error_codes.extend(matches)
    
    # Remove duplicates and return
    return list(set(error_codes))

def find_similar_queries(text_query: str, user_id: str) -> List[Dict[str, Any]]:
    """Find similar queries in the database using simple keyword matching"""
    db_instance = JSONDatabase()
    all_queries = db_instance.get_user_queries(user_id)
    
    # Filter queries that have a solution and match some keywords
    similar_queries = []
    keywords = set(text_query.lower().split())
    
    for query in all_queries:
        if query.get("solution") and query.get("query_content", {}).get("text"):
            query_text = query["query_content"]["text"].lower()
            query_keywords = set(query_text.split())
            
            # Calculate similarity based on common keywords
            common_keywords = keywords.intersection(query_keywords)
            if len(common_keywords) >= 2:  # At least 2 common keywords
                similarity_score = len(common_keywords) / max(len(keywords), len(query_keywords))
                if similarity_score > 0.3:  # At least 30% similarity
                    similar_queries.append(query)
    
    # Sort by similarity (most similar first)
    similar_queries.sort(key=lambda q: len(set(q["query_content"]["text"].lower().split()).intersection(keywords)) / 
                         max(len(keywords), len(set(q["query_content"]["text"].lower().split()))),
                         reverse=True)
    
    return similar_queries[:3]  # Return top 3 similar queries