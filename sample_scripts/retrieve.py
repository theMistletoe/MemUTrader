import requests

API_KEY = "mu_NvuKO_RzIPGJ_cNM1CZxPwuSZpeZkruT9Tp7L9NpfIPL76AVcJgm-jrJp3HWNJzy0gcYRdUKod_OgDXHZtY9QB8hbwemIM9Xb_7R2Q"
BASE_URL = "https://api.memu.so"


# Retrieve memories related to travel
response = requests.post(
    f"{BASE_URL}/api/v3/memory/retrieve",
    json={
        "user_id": "user_B",
        "agent_id": "agent_USD/JPY",
        "query": "ドル円って今買いかを判断する情報を取得したい"
    },
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
)

result = response.json()
print(f"Query: {result['rewritten_query']}")
print("\nMemories:")
for item in result.get("items", []):
    print(f"  [{item['memory_type']}] {item['content']}")