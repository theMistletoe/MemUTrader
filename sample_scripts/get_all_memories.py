import requests
import json
import time

API_KEY = "mu_NvuKO_RzIPGJ_cNM1CZxPwuSZpeZkruT9Tp7L9NpfIPL76AVcJgm-jrJp3HWNJzy0gcYRdUKod_OgDXHZtY9QB8hbwemIM9Xb_7R2Q"
BASE_URL = "https://api.memu.so"

def get_all_memories(user_id, agent_id):
    print(f"Attempting to retrieve comprehensive memories for User: {user_id}...\n")
    
    # Queries designed to cast a wide net for memories
    queries = [
        "User's profile, preferences, and habits",
        "Important facts and details about the user",
        "History of conversations and topics discussed",
        "ユーザーのプロフィール、好み、習慣",
        "ユーザーに関する重要な事実と詳細",
    ]
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    collected_memories = []
    seen_contents = set()
    
    for query in queries:
        print(f"Searching with query: '{query}'...")
        
        payload = {
            "user_id": user_id,
            "agent_id": agent_id,
            "query": query
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/v3/memory/retrieve", json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                items = result.get("items", [])
                
                new_items_count = 0
                for item in items:
                    content = item.get("content")
                    if content and content not in seen_contents:
                        seen_contents.add(content)
                        collected_memories.append(item)
                        new_items_count += 1
                
                print(f"  -> Found {len(items)} items ({new_items_count} new)")
            else:
                print(f"  -> Error: {response.status_code}")
                
            # Be nice to the API
            time.sleep(1)
            
        except Exception as e:
            print(f"  -> Exception: {e}")

    print(f"\nTotal unique memories found: {len(collected_memories)}\n")
    
    # Output formatted for potential copy-pasting
    print("--- MEMORY DUMP START ---")
    for i, mem in enumerate(collected_memories, 1):
        m_type = mem.get('memory_type', 'unknown')
        content = mem.get('content', '').strip()
        print(f"{i}. [{m_type}] {content}")
    print("--- MEMORY DUMP END ---")

if __name__ == "__main__":
    user_id = "user_B"
    agent_id = "agent_USD/JPY"
    get_all_memories(user_id, agent_id)
