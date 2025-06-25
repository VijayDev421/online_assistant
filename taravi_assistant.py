from flask import Flask, request, jsonify
import os
import requests

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
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=payload, timeout=10
        )
    except Exception as e:
        return jsonify({"response": f"Request failed: {e}", "payload": payload, "headers": dict(headers)}), 500

    return jsonify({
        "status_code": resp.status_code,
        "reason": resp.reason,
        "response_text": resp.text[:500],
        "sent_payload": payload,
        "sent_headers": dict(headers)
    }), resp.status_code

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

@app.route('/')
def home():
    return "Taravi Assistant is running. Go to /dashboard to use it."


@app.route('/dashboard')
def dashboard():
    try:
        with open("taravi_dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500
