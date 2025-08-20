import logging
from typing import Dict, List, Any, Optional
import time
import json

from .preprocessing.text_preprocessor import TextPreprocessor
from .intent.intent_classifier import IntentClassifier
from .entity.entity_extractor import EntityExtractor
from .embedding.semantic_search import SemanticSearch
from .reasoning.llm_reasoner import LLMReasoner
from .generation.response_generator import ResponseGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPPipeline:
    """
    Main NLP pipeline that integrates all stages:
    1. Text Preprocessing
    2. Intent Classification
    3. Entity Extraction
    4. Semantic Search
    5. LLM Reasoning
    6. Response Generation
    """
    
    def __init__(self):
        """Initialize the NLP pipeline with all components"""
        logger.info("Initializing NLP pipeline...")
        
        try:
            self.text_preprocessor = TextPreprocessor()
            logger.info("Text preprocessor initialized")
        except Exception as e:
            logger.error(f"Failed to initialize text preprocessor: {e}")
            raise
        
        try:
            self.intent_classifier = IntentClassifier()
            logger.info("Intent classifier initialized")
        except Exception as e:
            logger.error(f"Failed to initialize intent classifier: {e}")
            raise
        
        try:
            self.entity_extractor = EntityExtractor()
            logger.info("Entity extractor initialized")
        except Exception as e:
            logger.error(f"Failed to initialize entity extractor: {e}")
            raise
        
        try:
            self.semantic_search = SemanticSearch()
            logger.info("Semantic search initialized")
        except Exception as e:
            logger.error(f"Failed to initialize semantic search: {e}")
            raise
        
        try:
            self.llm_reasoner = LLMReasoner()
            logger.info("LLM reasoner initialized")
        except Exception as e:
            logger.error(f"Failed to initialize LLM reasoner: {e}")
            raise
        
        try:
            self.response_generator = ResponseGenerator()
            logger.info("Response generator initialized")
        except Exception as e:
            logger.error(f"Failed to initialize response generator: {e}")
            raise
        
        logger.info("NLP pipeline initialization complete")
    
    async def process(self, text: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """
        Process text through the entire pipeline
        
        Args:
            text (str): Input text query
            user_id (str): User ID for personalization
            
        Returns:
            dict: Processed results with all intermediate outputs
        """
        start_time = time.time()
        results = {"query": text, "user_id": user_id}
        
        try:
            # Stage 1: Text Preprocessing
            stage_start = time.time()
            preprocessed = self.text_preprocessor.preprocess(text)
            results["preprocessing"] = {
                "processed_text": preprocessed["processed"],
                "corrected_text": preprocessed["corrected"],
                "tokens": preprocessed["tokens"],
                "time_ms": round((time.time() - stage_start) * 1000)
            }
            logger.info(f"Preprocessing complete: {preprocessed['processed']}")
            
            # Use corrected text for subsequent stages
            processed_text = preprocessed["corrected"]
            
            # Stage 2: Intent Classification
            stage_start = time.time()
            intents = self.intent_classifier.classify_intent(processed_text, top_n=2)
            results["intent"] = {
                "intents": intents,
                "time_ms": round((time.time() - stage_start) * 1000)
            }
            logger.info(f"Intent classification complete: {intents[0]['intent'] if intents else 'unknown'}")
            
            # Stage 3: Entity Extraction
            stage_start = time.time()
            entities = self.entity_extractor.extract_entities(processed_text)
            results["entities"] = {
                "extracted": entities,
                "time_ms": round((time.time() - stage_start) * 1000)
            }
            logger.info(f"Entity extraction complete: {len(entities.get('devices', [])) + len(entities.get('error_codes', []))} entities found")
            
            # Stage 4: Semantic Search
            stage_start = time.time()
            search_results = self.semantic_search.search(processed_text, top_k=3)
            results["search"] = {
                "results": search_results,
                "time_ms": round((time.time() - stage_start) * 1000)
            }
            logger.info(f"Semantic search complete: {len(search_results)} documents found")
            
            # Stage 5: LLM Reasoning
            stage_start = time.time()
            reasoning = self.llm_reasoner.reason(processed_text, search_results, entities)
            results["reasoning"] = {
                "result": reasoning,
                "time_ms": round((time.time() - stage_start) * 1000)
            }
            logger.info(f"LLM reasoning complete: {reasoning.get('issue', 'Unknown issue')}")
            
            # Stage 6: Response Generation
            stage_start = time.time()
            response = self.response_generator.generate_response(
                reasoning, processed_text, search_results, entities
            )
            results["response"] = {
                "generated": response,
                "time_ms": round((time.time() - stage_start) * 1000)
            }
            logger.info("Response generation complete")
            
            # Generate report if needed
            if user_id != "anonymous":
                report_path = self.response_generator.generate_report(response, user_id)
                if report_path:
                    results["report_path"] = report_path
            
            # Calculate total processing time
            results["total_time_ms"] = round((time.time() - start_time) * 1000)
            
            return results
        
        except Exception as e:
            logger.error(f"Error in NLP pipeline: {e}")
            results["error"] = str(e)
            results["total_time_ms"] = round((time.time() - start_time) * 1000)
            return results
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get the status of all pipeline components
        
        Returns:
            dict: Status information for each component
        """
        return {
            "text_preprocessor": {
                "status": "active",
                "features": ["spell correction", "tokenization", "lemmatization"]
            },
            "intent_classifier": {
                "status": "active",
                "model": "distilbert-base-uncased",
                "intents": list(self.intent_classifier.intents.keys())
            },
            "entity_extractor": {
                "status": "active",
                "model": "en_core_web_sm",
                "entity_types": ["devices", "error_codes", "versions", "os", "brands"]
            },
            "semantic_search": {
                "status": "active",
                "model": "all-MiniLM-L6-v2",
                "document_count": len(self.semantic_search.documents)
            },
            "llm_reasoner": {
                "status": "active",
                "model": "gemini-1.5-pro" if self.llm_reasoner.use_gemini else "flan-t5-small"
            },
            "response_generator": {
                "status": "active",
                "features": ["structured response", "PDF report generation"]
            }
        }
