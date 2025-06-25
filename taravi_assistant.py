import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "Referer": "https://github.com/EswarSai/online_assistant",
        "X-Title": "Taravi Assistant"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              headers=headers, json=payload, timeout=10)
    except Exception as e:
        return jsonify({"response": f"Request failed: {e}"})

    debug_info = {
        "status_code": resp.status_code,
        "response_text": resp.text[:500]
    }
    if resp.status_code != 200:
        return jsonify({"response": f"Error {resp.status_code}: {resp.reason}", "debug": debug_info}), resp.status_code

    reply = resp.json()["choices"][0]["message"]["content"]
    return jsonify({"response": reply})
