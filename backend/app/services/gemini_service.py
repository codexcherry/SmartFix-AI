import google.generativeai as genai
from typing import Dict, List, Any, Optional
import base64
import json

from ..core.config import settings

class GeminiService:
    def __init__(self, api_key: str = settings.GEMINI_API_KEY):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        # Update model name to the latest version
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.vision_model = genai.GenerativeModel('gemini-1.5-pro-vision')
    
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text input to identify issues and solutions"""
        prompt = f"""
        You are an AI troubleshooting assistant. Analyze the following technical issue description:
        
        "{text}"
        
        Provide a structured analysis in JSON format with the following fields:
        - issue: A concise summary of the problem
        - possible_causes: List of potential causes
        - confidence_score: A number between 0 and 1 indicating confidence in your analysis
        - recommended_steps: List of troubleshooting steps, each with a step_number and description
        
        Return ONLY the JSON object, no additional text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            # Handle case where response might have markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].strip()
            else:
                json_str = response_text.strip()
            
            result = json.loads(json_str)
            
            # Ensure the response has the expected structure
            if not isinstance(result.get("recommended_steps"), list):
                result["recommended_steps"] = []
            
            # Convert recommended_steps to the expected format if it's just a list of strings
            steps = []
            for i, step in enumerate(result["recommended_steps"]):
                if isinstance(step, str):
                    steps.append({"step_number": i+1, "description": step})
                elif isinstance(step, dict) and "description" in step:
                    if "step_number" not in step:
                        step["step_number"] = i+1
                    steps.append(step)
            
            result["recommended_steps"] = steps
            return result
        
        except Exception as e:
            print(f"Error in analyze_text: {e}")
            # Fallback for non-JSON responses
            return {
                "issue": text[:50] + "..." if len(text) > 50 else text,
                "possible_causes": ["Unable to determine causes"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please provide more details about the issue"}
                ]
            }
    
    async def analyze_image(self, image_data: bytes, text_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Analyze image to identify issues and solutions"""
        if not text_prompt:
            text_prompt = "Analyze this image and identify any technical issues or error messages visible."
        
        prompt = f"""
        You are an AI troubleshooting assistant. Analyze the following image showing a technical issue.
        {text_prompt}
        
        Provide a structured analysis in JSON format with the following fields:
        - issue: A concise summary of the problem visible in the image
        - possible_causes: List of potential causes
        - confidence_score: A number between 0 and 1 indicating confidence in your analysis
        - recommended_steps: List of troubleshooting steps, each with a step_number and description
        
        Return ONLY the JSON object, no additional text.
        """
        
        try:
            response = self.vision_model.generate_content([prompt, image_data])
            
            # Extract JSON from response
            response_text = response.text
            # Handle case where response might have markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].strip()
            else:
                json_str = response_text.strip()
            
            result = json.loads(json_str)
            
            # Ensure the response has the expected structure
            if not isinstance(result.get("recommended_steps"), list):
                result["recommended_steps"] = []
            
            # Convert recommended_steps to the expected format if it's just a list of strings
            steps = []
            for i, step in enumerate(result["recommended_steps"]):
                if isinstance(step, str):
                    steps.append({"step_number": i+1, "description": step})
                elif isinstance(step, dict) and "description" in step:
                    if "step_number" not in step:
                        step["step_number"] = i+1
                    steps.append(step)
            
            result["recommended_steps"] = steps
            return result
        
        except Exception as e:
            print(f"Error in analyze_image: {e}")
            # Fallback for non-JSON responses
            return {
                "issue": "Unable to analyze image",
                "possible_causes": ["Image quality issues", "Unrecognized error format"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please provide a clearer image or additional context"}
                ]
            }
    
    async def analyze_logs(self, log_content: str) -> Dict[str, Any]:
        """Analyze log files to identify issues and solutions"""
        prompt = f"""
        You are an AI troubleshooting assistant specializing in log analysis. Analyze the following log content:
        
        ```
        {log_content[:2000]}  # Limit log size for token constraints
        ```
        
        Provide a structured analysis in JSON format with the following fields:
        - issue: A concise summary of any errors or issues found in the logs
        - possible_causes: List of potential causes for the identified issues
        - confidence_score: A number between 0 and 1 indicating confidence in your analysis
        - recommended_steps: List of troubleshooting steps, each with a step_number and description
        
        Return ONLY the JSON object, no additional text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            # Handle case where response might have markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].strip()
            else:
                json_str = response_text.strip()
            
            result = json.loads(json_str)
            
            # Ensure the response has the expected structure
            if not isinstance(result.get("recommended_steps"), list):
                result["recommended_steps"] = []
            
            # Convert recommended_steps to the expected format if it's just a list of strings
            steps = []
            for i, step in enumerate(result["recommended_steps"]):
                if isinstance(step, str):
                    steps.append({"step_number": i+1, "description": step})
                elif isinstance(step, dict) and "description" in step:
                    if "step_number" not in step:
                        step["step_number"] = i+1
                    steps.append(step)
            
            result["recommended_steps"] = steps
            return result
        
        except Exception as e:
            print(f"Error in analyze_logs: {e}")
            # Fallback for non-JSON responses
            return {
                "issue": "Log analysis error",
                "possible_causes": ["Complex log format", "Insufficient context in logs"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please provide more context about the system generating these logs"}
                ]
            }