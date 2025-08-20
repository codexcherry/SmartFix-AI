import requests
import json

def test_text_query():
    url = "http://127.0.0.1:8000/api/v1/query/text"
    payload = {
        "user_id": "test_user",
        "input_type": "text",
        "text_query": "My TV screen is flickering"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        print("=== Text Query Test ===")
        print("Status Code:", response.status_code)
        print("Response:")
        print(json.dumps(response.json(), indent=4))
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_notify():
    url = "http://127.0.0.1:8000/api/v1/query/notify"
    payload = {
        "user_id": "test_user",
        "notification_type": "sms",
        "message": "Your TV issue has been diagnosed: Loose HDMI connection",
        "to_contact": "+1234567890"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        print("\n=== Notification Test ===")
        print("Status Code:", response.status_code)
        print("Response:")
        print(json.dumps(response.json(), indent=4))
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_user_history():
    url = "http://127.0.0.1:8000/api/v1/query/history/test_user"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        print("\n=== User History Test ===")
        print("Status Code:", response.status_code)
        print("Response:")
        print(json.dumps(response.json(), indent=4))
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_text_query()
    test_notify()
    test_user_history()