import requests
import time

API_KEY = "mu_NvuKO_RzIPGJ_cNM1CZxPwuSZpeZkruT9Tp7L9NpfIPL76AVcJgm-jrJp3HWNJzy0gcYRdUKod_OgDXHZtY9QB8hbwemIM9Xb_7R2Q"
BASE_URL = "https://api.memu.so"

def wait_for_task(task_id):
    print(f"Waiting for task {task_id} to complete...")
    while True:
        try:
            response = requests.get(
                f"{BASE_URL}/api/v3/memory/memorize/status/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            
            if response.status_code != 200:
                print(f"Error checking status: {response.status_code} - {response.text}")
                return False

            result = response.json()
            status = result.get("status")
            print(f"Status: {status}")
            
            if status == "SUCCESS":
                print("✅ Memorization complete!")
                return True
            elif status == "FAILED":
                print(f"❌ Memorization failed: {result}")
                return False
            
            time.sleep(5)  # Wait 5 seconds before checking again
            
        except Exception as e:
            print(f"An error occurred while polling: {e}")
            return False

def main():
    # Prepare the conversation (minimum 3 messages required)
    payload = {
        "conversation": [
            {"role": "user", "content": "最近の米ドル円の動向について教えてください。"},
            {"role": "assistant", "content": "現在、米ドル円は約150円前後で推移しており、米国の利上げ継続観測と日銀の金融政策が注目されています。"},
            {"role": "user", "content": "今後の見通しはどうですか？"},
            {"role": "assistant", "content": "今後も米国の経済指標や日銀の政策修正のタイミングによって、為替相場は大きく変動する可能性があります。"},
            {"role": "user", "content": "投資に関するアドバイスはありますか？"},
            {"role": "assistant", "content": "為替変動リスクを考慮し、分散投資や適切なヘッジ戦略を取ることが重要です。専門家の意見も参考にしてください。"}
        ],
        "user_id": "user_876",
        "agent_id": "agent_456"
    }

    print("Submitting memorization task...")
    # Submit the memorization task
    try:
        response = requests.post(
            f"{BASE_URL}/api/v3/memory/memorize",
            json=payload,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
        )

        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("task_id")
            print(f"Task submitted: {task_id}")
            
            # Start polling for status
            if task_id:
                wait_for_task(task_id)
        else:
            print(f"Error submitting task: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
