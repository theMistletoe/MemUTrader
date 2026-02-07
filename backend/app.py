from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
CORS(app)
app.json.ensure_ascii = False

# Configuration
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.memu.so"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


CURRENCY_PAIRS = [
    "USD/JPY", "EUR/USD", "GBP/USD", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD",
    "EUR/JPY", "GBP/JPY", "CHF/JPY", "CAD/JPY", "NZD/JPY", "ZAR/JPY", "MXN/JPY",
    "TRY/JPY", "EUR/GBP", "EUR/AUD", "GBP/AUD", "AUD/NZD"
]

def infer_agent_id(query):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Identify the relevant currency pair(s) for the user's query from the following list: {', '.join(CURRENCY_PAIRS)}. Return the result as a JSON object with a key 'agents' containing an array of strings. Example: {{'agents': ['USD/JPY']}}"},
                {"role": "user", "content": query}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        agents = data.get("agents", [])
        print(agents)
        return agents
    except Exception as e:
        print(f"Error inferring agent_id: {e}")
        return []

@app.route('/')
def hello():
    return jsonify({"message": "hello"})

@app.route('/memories', methods=['GET'])
def get_memories():
    user_id = request.args.get('user_id')
    agent_id = request.args.get('agent_id')
    query = request.args.get('query')

    if not agent_id and query:
        inferred_agents = infer_agent_id(query)
        if inferred_agents:
            agent_id = f"agent_{inferred_agents[0]}"

    if not user_id or not agent_id or not query:
        return jsonify({"error": "Missing required parameters: user_id, agent_id, query"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "user_id": "user_" + user_id,
        "agent_id": agent_id,
        "query": query
    }
    print(payload)

    def generate():
        try:
            response = requests.post(f"{BASE_URL}/api/v3/memory/retrieve", json=payload, headers=headers)
            memories_data = response.json()
            
            if response.status_code == 200:
                # Send memories data first
                yield f"event: memories\ndata: {json.dumps(memories_data, ensure_ascii=False)}\n\n"

                # Analyze memories to infer buy/sell decision
                try:
                    stream = client.chat.completions.create(
                        model="gpt-5.2",
                        messages=[
                            {"role": "system", "content": "You are a financial trading assistant. Analyze the provided memory content and query to decide whether to 'BUY', 'SELL', or 'HOLD' the currency pair. Also provide a brief reason.\n\nFormat your response exactly as follows:\nACTION: [BUY/SELL/HOLD]\nREASON: [Your detailed reasoning here]"},
                            {"role": "user", "content": f"Query: {query}\nMemories: {json.dumps(memories_data, ensure_ascii=False)}"}
                        ],
                        stream=True
                    )

                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            yield f"event: token\ndata: {json.dumps(content, ensure_ascii=False)}\n\n"
                    
                except Exception as e:
                    print(f"Error analyzing memories: {e}")
                    yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
            else:
                yield f"event: error\ndata: {json.dumps({'error': 'Failed to retrieve memories', 'details': response.text}, ensure_ascii=False)}\n\n"
                
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/memorize', methods=['POST'])
def memorize():
    data = request.json
    
    if not data:
         return jsonify({"error": "Request body is empty"}), 400

    required_fields = ['user_id', 'agent_id', 'user_message']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Prepare the conversation (minimum 3 messages required)
    payload = {
        "conversation": [
            {"role": "user", "content": data[required_fields[2]]},
        ],
        "user_id": "user_" + data[required_fields[0]],
        "agent_id": "agent_" + data[required_fields[1]]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v3/memory/memorize",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
             return jsonify({"error": "Failed to submit memory task", "status_code": response.status_code, "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
