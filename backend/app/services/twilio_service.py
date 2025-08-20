from twilio.rest import Client
from typing import Dict, Any, Optional

from ..core.config import settings

class TwilioService:
    def __init__(
        self, 
        account_sid: str = settings.TWILIO_SID,
        auth_token: str = settings.TWILIO_AUTH_TOKEN,
        from_phone: str = settings.TWILIO_FROM_PHONE
    ):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_phone = from_phone
        
        # Initialize client if credentials are available
        self.client = None
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
    
    async def send_sms(self, to_phone: str, message: str) -> Dict[str, Any]:
        """Send SMS notification using Twilio"""
        if not self.client or not self.from_phone:
            return {
                "success": False,
                "error": "Twilio credentials not configured",
                "message_id": None
            }
        
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=to_phone
            )
            
            return {
                "success": True,
                "message_id": message.sid,
                "error": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message_id": None
            }
    
    async def send_whatsapp(self, to_phone: str, message: str) -> Dict[str, Any]:
        """Send WhatsApp notification using Twilio"""
        if not self.client or not self.from_phone:
            return {
                "success": False,
                "error": "Twilio credentials not configured",
                "message_id": None
            }
        
        # Format WhatsApp numbers
        from_whatsapp = f"whatsapp:{self.from_phone}"
        to_whatsapp = f"whatsapp:{to_phone}"
        
        try:
            message = self.client.messages.create(
                body=message,
                from_=from_whatsapp,
                to=to_whatsapp
            )
            
            return {
                "success": True,
                "message_id": message.sid,
                "error": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message_id": None
            }
