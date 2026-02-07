import requests
import json

API_KEY = "mu_NvuKO_RzIPGJ_cNM1CZxPwuSZpeZkruT9Tp7L9NpfIPL76AVcJgm-jrJp3HWNJzy0gcYRdUKod_OgDXHZtY9QB8hbwemIM9Xb_7R2Q"
BASE_URL = "https://api.memu.so"

def get_categories(user_id, agent_id):
    print(f"Fetching categories for User: {user_id}, Agent: {agent_id}...")
    
    url = f"{BASE_URL}/api/v3/memory/categories"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_id": user_id,
        "agent_id": agent_id
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            categories = result.get("categories", [])
            
            print(f"\nFound {len(categories)} categories:\n")
            
            for category in categories:
                print(f"=== Category: {category['name']} ===")
                print(f"Description: {category.get('description', 'N/A')}")
                print("--- Summary ---")
                print(category.get('summary', 'No summary available'))
                print("=====================================\n")
                
            return categories
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Using the same user/agent IDs as in the existing sample code
    user_id = "user_B"
    agent_id = "agent_USD/JPY"
    
    get_categories(user_id, agent_id)
