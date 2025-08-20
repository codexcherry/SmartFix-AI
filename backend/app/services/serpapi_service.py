import requests
from typing import Dict, List, Any, Optional
import json

from ..core.config import settings

class SerpAPIService:
    def __init__(self, api_key: str = settings.SERPAPI_KEY):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
    
    async def search_solutions(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search for solutions to a technical issue using SerpAPI"""
        search_query = f"how to fix {query}"
        
        params = {
            "q": search_query,
            "api_key": self.api_key,
            "engine": "google",
            "num": str(num_results),
            "gl": "us",  # Country to search from
            "hl": "en"   # Language
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            results = response.json()
            
            organic_results = results.get("organic_results", [])
            
            formatted_results = []
            for result in organic_results[:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "url": result.get("link", "")
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Error in search_solutions: {e}")
            return []
    
    async def search_product_info(self, product_name: str) -> Dict[str, Any]:
        """Search for product information using SerpAPI"""
        search_query = f"{product_name} technical specifications"
        
        params = {
            "q": search_query,
            "api_key": self.api_key,
            "engine": "google",
            "num": "3",
            "gl": "us",
            "hl": "en"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            results = response.json()
            
            knowledge_graph = results.get("knowledge_graph", {})
            if knowledge_graph:
                return {
                    "title": knowledge_graph.get("title", product_name),
                    "description": knowledge_graph.get("description", ""),
                    "attributes": knowledge_graph.get("attributes", {})
                }
            
            # Fallback to organic results if no knowledge graph
            organic_results = results.get("organic_results", [])
            if organic_results:
                return {
                    "title": product_name,
                    "description": organic_results[0].get("snippet", ""),
                    "url": organic_results[0].get("link", "")
                }
            
            return {
                "title": product_name,
                "description": "No information found",
                "url": ""
            }
        
        except Exception as e:
            print(f"Error in search_product_info: {e}")
            return {
                "title": product_name,
                "description": "Error retrieving product information",
                "url": ""
            }
    
    async def search_error_code(self, error_code: str, device_type: Optional[str] = None) -> List[Dict[str, str]]:
        """Search for information about a specific error code"""
        search_query = f"{error_code} {device_type if device_type else ''} error code fix"
        
        params = {
            "q": search_query,
            "api_key": self.api_key,
            "engine": "google",
            "num": "5",
            "gl": "us",
            "hl": "en"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            results = response.json()
            
            organic_results = results.get("organic_results", [])
            
            formatted_results = []
            for result in organic_results[:5]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "url": result.get("link", "")
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Error in search_error_code: {e}")
            return []
