from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Load OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get("prompt", "")

    try:
        # Make a request to OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

# Dashboard route (serves taravi_dashboard.html from the same folder)
@app.route('/dashboard')
def dashboard():
    try:
        with open("taravi_dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

