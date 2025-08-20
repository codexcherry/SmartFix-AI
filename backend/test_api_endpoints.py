import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1/query"

def test_text_query():
    """Test the text query endpoint"""
    print("\n=== Testing Text Query Endpoint ===")
    
    # Test data
    data = {
        "user_id": "test_user",
        "input_type": "text",
        "text_query": "My WiFi keeps disconnecting every few minutes"
    }
    
    # Send request
    start_time = time.time()
    print(f"Sending request: {data['text_query']}")
    
    try:
        response = requests.post(f"{BASE_URL}/text", json=data)
        
        # Print response time
        elapsed = time.time() - start_time
        print(f"Response time: {elapsed:.2f} seconds")
        
        # Check status code
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Print query ID
            print(f"Query ID: {result.get('query_id')}")
            
            # Print solution
            solution = result.get("solution", {})
            print("\nSolution:")
            print(f"  Issue: {solution.get('issue')}")
            print(f"  Confidence: {solution.get('confidence_score', 0):.2f}")
            print(f"  Possible causes: {', '.join(solution.get('possible_causes', []))}")
            print("\n  Recommended steps:")
            for step in solution.get("recommended_steps", []):
                print(f"    {step.get('step_number')}. {step.get('description')}")
            
            # Return query ID for history test
            return result.get("query_id")
        else:
            print(f"Error: {response.text}")
            return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_pipeline_status():
    """Test the pipeline status endpoint"""
    print("\n=== Testing Pipeline Status Endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/pipeline/status")
        
        # Check status code
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Print pipeline status
            print("\nPipeline Status:")
            for component, status in result.items():
                print(f"  {component}: {status.get('status')}")
                if "model" in status:
                    print(f"    Model: {status.get('model')}")
        else:
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"Error: {e}")

def test_user_history(user_id):
    """Test the user history endpoint"""
    print(f"\n=== Testing User History Endpoint for {user_id} ===")
    
    try:
        response = requests.get(f"{BASE_URL}/history/{user_id}")
        
        # Check status code
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Print history
            print(f"\nFound {len(result)} queries in history:")
            for i, query in enumerate(result):
                print(f"  {i+1}. {query.get('query_content', {}).get('text', 'No text')} ({query.get('status')})")
        else:
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    # Test pipeline status
    test_pipeline_status()
    
    # Test text query
    query_id = test_text_query()
    
    # Test user history if text query was successful
    if query_id:
        # Wait a bit for the database to be updated
        time.sleep(2)
        test_user_history("test_user")
