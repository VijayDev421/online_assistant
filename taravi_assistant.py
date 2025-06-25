from flask import Flask, request, jsonify
import requests
import os

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

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are Taravi, a helpful assistant. Answer user queries accurately and clearly."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"response": reply})

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"response": f"HTTP error: {http_err}", "details": response.text}), 500
    except Exception as err:
        return jsonify({"response": f"Other error: {err}"}), 500

@app.route('/')
def home():
    return "Taravi Assistant is running. Go to /dashboard"

@app.route('/dashboard')
def dashboard():
    try:
        with open("taravi_dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500
