import asyncio
import json
from app.nlp.pipeline import NLPPipeline

async def test_pipeline():
    """Test the NLP pipeline with a sample query"""
    print("Initializing NLP pipeline...")
    pipeline = NLPPipeline()
    
    # Test queries
    queries = [
        "My WiFi keeps disconnecting every few minutes",
        "My laptop screen is flickering and showing lines",
        "My phone battery drains too quickly",
        "Windows keeps showing blue screen error 0x0000007B"
    ]
    
    for query in queries:
        print(f"\n\nProcessing query: {query}")
        result = await pipeline.process(query)
        
        # Print pipeline stages timing
        print("\nPipeline timing:")
        for stage, data in result.items():
            if isinstance(data, dict) and "time_ms" in data:
                print(f"  {stage}: {data['time_ms']} ms")
        print(f"  Total: {result['total_time_ms']} ms")
        
        # Print intent classification
        if "intent" in result and "intents" in result["intent"]:
            intents = result["intent"]["intents"]
            if intents:
                print(f"\nDetected intent: {intents[0]['intent']} ({intents[0]['confidence']:.2f})")
        
        # Print entity extraction
        if "entities" in result and "extracted" in result["entities"]:
            entities = result["entities"]["extracted"]
            print("\nExtracted entities:")
            for entity_type, values in entities.items():
                if values and entity_type != "spacy_entities":
                    print(f"  {entity_type}: {values}")
        
        # Print search results
        if "search" in result and "results" in result["search"]:
            search_results = result["search"]["results"]
            if search_results:
                print(f"\nTop search result: {search_results[0]['title']} ({search_results[0]['similarity']:.2f})")
        
        # Print reasoning result
        if "reasoning" in result and "result" in result["reasoning"]:
            reasoning = result["reasoning"]["result"]
            print(f"\nReasoning result:")
            print(f"  Issue: {reasoning.get('issue')}")
            print(f"  Confidence: {reasoning.get('confidence_score', 0):.2f}")
            print(f"  Possible causes: {', '.join(reasoning.get('possible_causes', []))}")
            print("\n  Recommended steps:")
            for step in reasoning.get("recommended_steps", []):
                print(f"    {step.get('step_number')}. {step.get('description')}")
        
        # Print final response
        if "response" in result and "generated" in result["response"]:
            response = result["response"]["generated"]
            print(f"\nFinal response summary: {response.get('summary')}")

if __name__ == "__main__":
    asyncio.run(test_pipeline())