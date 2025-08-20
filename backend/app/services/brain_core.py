# brain_core.py (enhanced)
import logging
from typing import Dict, List, Any, Optional, Tuple
import json
import asyncio
from .brain_memory import BrainMemory
from .huggingface_service import HuggingFaceService
from .gemini_service import GeminiService
from .serpapi_service import SerpAPIService
from .ocr_service import OCRService

logger = logging.getLogger(__name__)

class BrainCore:
    """
    Enhanced Intelligent Brain Core System for SmartFix-AI
    Processes all inputs and makes intelligent decisions using multiple AI models
    """
    
    def __init__(self):
        self.brain_memory = BrainMemory()
        self.hf_service = HuggingFaceService()
        self.gemini_service = GeminiService()
        self.serp_service = SerpAPIService()
        self.ocr_service = OCRService()
        
        logger.info("Brain Core initialized successfully")
    
    async def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing function that handles all input types
        """
        input_type = input_data.get("input_type", "text")
        query_text = input_data.get("text_query", "")
        device_category = input_data.get("device_category", None)
        
        logger.info(f"Processing {input_type} input: {query_text[:100]}...")
        
        try:
            # Step 1: Convert all inputs to text
            processed_text = await self._convert_to_text(input_data)
            
            # Step 2: Analyze with brain memory first
            brain_solution = self.brain_memory.get_best_solution(processed_text, device_category)
            
            if brain_solution and brain_solution.get("confidence_score", 0) > 0.8:
                logger.info(f"Found high-confidence solution in brain memory: {brain_solution['confidence_score']}")
                return self._format_brain_solution(brain_solution, processed_text)
            
            # Step 3: If no good match in brain, use AI analysis
            logger.info("No high-confidence match in brain memory, using AI analysis")
            ai_solution = await self._analyze_with_ai(processed_text, input_data)
            
            # Step 4: Combine brain memory and AI results
            final_solution = await self._combine_solutions(brain_solution, ai_solution, processed_text)
            
            # Step 5: Learn from this interaction
            await self._learn_from_interaction(processed_text, final_solution)
            
            return final_solution
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return self._create_error_response(processed_text, str(e))
    
    async def _convert_to_text(self, input_data: Dict[str, Any]) -> str:
        """
        Convert all input types to text for processing
        """
        input_type = input_data.get("input_type", "text")
        base_text = input_data.get("text_query", "")
        
        if input_type == "voice":
            # Convert voice to text using Hugging Face
            audio_data = input_data.get("audio_data")
            if audio_data:
                try:
                    transcribed_text = await self.hf_service.transcribe_audio(audio_data)
                    return transcribed_text if transcribed_text else base_text
                except Exception as e:
                    logger.warning(f"Voice transcription failed: {e}")
                    return base_text
            return base_text
        
        elif input_type == "image":
            # Extract text from image using OCR
            image_data = input_data.get("image_data")
            if image_data:
                try:
                    ocr_result = self.ocr_service.process_image(image_data)
                    extracted_text = ocr_result.get("extracted_text", "")
                    error_codes = ocr_result.get("error_codes", [])
                    
                    # Combine extracted text with user query
                    combined_text = f"{base_text} {extracted_text}".strip()
                    if error_codes:
                        combined_text += f" Error codes detected: {', '.join(error_codes)}"
                    
                    return combined_text
                except Exception as e:
                    logger.warning(f"OCR processing failed: {e}")
                    return base_text
        
        elif input_type == "log":
            # Log files are already text
            log_content = input_data.get("log_content", "")
            return f"{base_text} {log_content}".strip()
        
        # Default to text input
        return base_text
    
    async def _analyze_with_ai(self, processed_text: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the problem using AI models
        """
        try:
            # Use both Gemini and web search concurrently
            gemini_task = self._analyze_with_gemini(processed_text, input_data)
            search_task = self._search_web_solutions(processed_text)
            
            gemini_result, web_results = await asyncio.gather(
                gemini_task, search_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(gemini_result, Exception):
                logger.error(f"Gemini analysis failed: {gemini_result}")
                gemini_result = {}
            
            if isinstance(web_results, Exception):
                logger.error(f"Web search failed: {web_results}")
                web_results = []
            
            return {
                "issue": gemini_result.get("issue", "Unknown issue"),
                "possible_causes": gemini_result.get("possible_causes", []),
                "recommended_steps": gemini_result.get("recommended_steps", []),
                "confidence_score": gemini_result.get("confidence_score", 0.5),
                "additional_info": gemini_result.get("additional_info", ""),
                "external_sources": web_results,
                "source": "ai_analysis"
            }
        
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            return {
                "issue": "AI analysis failed",
                "possible_causes": ["Technical error", "Service unavailable"],
                "recommended_steps": [{"step_number": 1, "description": "Please try again later"}],
                "confidence_score": 0.1,
                "source": "error"
            }
    
    async def _analyze_with_gemini(self, processed_text: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using Gemini AI"""
        try:
            gemini_prompt = f"""
            Analyze this technical problem and provide a detailed solution:
            
            Problem: {processed_text}
            Device Type: {input_data.get('device_category', 'unknown')}
            
            Provide a structured response with:
            1. Issue identification
            2. Possible causes
            3. Step-by-step solution
            4. Confidence level
            5. Additional recommendations
            
            Format as JSON with fields: issue, possible_causes, recommended_steps, confidence_score, additional_info
            """
            
            return await self.gemini_service.analyze_text(gemini_prompt)
            
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            raise
    
    async def _search_web_solutions(self, query_text: str) -> List[Dict[str, Any]]:
        """Search for web solutions"""
        try:
            search_query = f"{query_text} troubleshooting solution"
            return await self.serp_service.search_solutions(search_query)
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return []
    
    def _format_brain_solution(self, brain_solution: Dict[str, Any], query_text: str) -> Dict[str, Any]:
        """
        Format brain memory solution for response
        """
        return {
            "query_id": f"brain_{brain_solution['id']}",
            "solution": {
                "issue": brain_solution["problem_text"],
                "possible_causes": [brain_solution["symptoms"]],
                "confidence_score": brain_solution["confidence_score"],
                "recommended_steps": [
                    {"step_number": i+1, "description": step}
                    for i, step in enumerate(brain_solution["solution_steps"])
                ],
                "external_sources": [],
                "brain_memory": {
                    "success_rate": brain_solution["success_rate"],
                    "usage_count": brain_solution["usage_count"],
                    "problem_type": brain_solution["problem_type"],
                    "device_category": brain_solution["device_category"],
                    "error_codes": brain_solution["error_codes"]
                }
            },
            "source": "brain_memory",
            "query_text": query_text
        }
    
    async def _combine_solutions(self, brain_solution: Optional[Dict], ai_solution: Dict, query_text: str) -> Dict[str, Any]:
        """
        Combine brain memory and AI solutions intelligently
        """
        if brain_solution and brain_solution.get("confidence_score", 0) > 0.6:
            # Use brain solution as primary, enhance with AI
            combined_solution = self._format_brain_solution(brain_solution, query_text)
            
            # Add AI insights if available
            if ai_solution.get("external_sources"):
                combined_solution["solution"]["external_sources"] = ai_solution["external_sources"]
            
            if ai_solution.get("additional_info"):
                combined_solution["solution"]["additional_info"] = ai_solution["additional_info"]
            
            return combined_solution
        
        else:
            # Use AI solution as primary
            return {
                "query_id": f"ai_{hash(query_text) % 10000}",
                "solution": {
                    "issue": ai_solution["issue"],
                    "possible_causes": ai_solution["possible_causes"],
                    "confidence_score": ai_solution["confidence_score"],
                    "recommended_steps": ai_solution["recommended_steps"],
                    "external_sources": ai_solution.get("external_sources", []),
                    "additional_info": ai_solution.get("additional_info", "")
                },
                "source": "ai_analysis",
                "query_text": query_text
            }
    
    async def _learn_from_interaction(self, query_text: str, solution: Dict[str, Any]):
        """
        Learn from the interaction to improve future responses
        """
        try:
            # Extract solution text for learning
            solution_text = solution.get("solution", {}).get("issue", "")
            
            # Record learning interaction
            self.brain_memory.learn_from_interaction(
                query_text=query_text,
                solution_used=solution_text,
                success=True,  # Assume success for now
                user_feedback=None
            )
            
            # If this was an AI solution, consider adding to brain memory
            if solution.get("source") == "ai_analysis":
                ai_solution = solution.get("solution", {})
                if ai_solution.get("confidence_score", 0) > 0.7:
                    # Add to brain memory for future use
                    new_problem = {
                        "problem_text": ai_solution["issue"],
                        "problem_type": "ai_generated",
                        "device_category": "unknown",
                        "error_codes": [],
                        "symptoms": query_text,
                        "solution_steps": [
                            step["description"] for step in ai_solution.get("recommended_steps", [])
                        ],
                        "confidence_score": ai_solution.get("confidence_score", 0.5),
                        "success_rate": 0.5  # Will be updated based on user feedback
                    }
                    self.brain_memory.add_new_problem(new_problem)
            
            logger.info(f"Learned from interaction: {query_text[:50]}...")
        
        except Exception as e:
            logger.error(f"Error in learning from interaction: {e}")
    
    def _create_error_response(self, query_text: str, error_message: str) -> Dict[str, Any]:
        """Create error response when processing fails"""
        return {
            "query_id": f"error_{hash(query_text) % 10000}",
            "solution": {
                "issue": "System Error",
                "possible_causes": ["Technical issue in processing", "Service unavailable"],
                "confidence_score": 0.1,
                "recommended_steps": [
                    {"step_number": 1, "description": "Please try again later"},
                    {"step_number": 2, "description": "Contact support if the issue persists"}
                ],
                "error": error_message
            },
            "source": "error",
            "query_text": query_text
        }
    
    async def get_brain_stats(self) -> Dict[str, Any]:
        """
        Get brain system statistics
        """
        return self.brain_memory.get_brain_stats()
    
    async def search_brain_memory(self, query: str, device_category: str = None) -> List[Dict[str, Any]]:
        """
        Search brain memory for similar problems
        """
        return self.brain_memory.find_similar_problems(query, device_category)
    
    async def add_custom_solution(self, problem_data: Dict[str, Any]):
        """
        Add a custom solution to brain memory
        """
        self.brain_memory.add_new_problem(problem_data)
    
    async def process_feedback(self, query_id: str, success: bool, feedback_score: int = None):
        """
        Process user feedback to improve the system
        """
        try:
            # Extract query text from query_id
            if query_id.startswith("brain_"):
                # This was a brain memory solution
                pass
            elif query_id.startswith("ai_"):
                # This was an AI solution
                pass
            
            # Record feedback for learning
            # Implementation depends on how we store query history
            
            logger.info(f"Processed feedback for {query_id}: success={success}, score={feedback_score}")
        
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")