from flask import Flask, request, jsonify, session
import requests
import os

app = Flask(__name__)
app.secret_key = "taravi-secret"  # Needed for session memory
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    user_prompt = request.json.get("prompt", "")

    if "messages" not in session:
        session["messages"] = [
            {"role": "system", "content": "You are Taravi, an intelligent assistant. Give clear, direct, useful answers without repeating introductions."}
        ]

    session["messages"].append({"role": "user", "content": user_prompt})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "Referer": "https://github.com/EswarSai/online_assistant",
        "X-Title": "Taravi Assistant"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": session["messages"]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        session["messages"].append({"role": "assistant", "content": reply})
        return jsonify({"response": reply.strip()})
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"response": f"HTTP error: {http_err}", "details": response.text}), 500
    except Exception as err:
        return jsonify({"response": f"Other error: {err}"}), 500

@app.route('/')
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/dashboard')
def dashboard():
    try:
        with open("taravi_dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/reset', methods=['POST'])
def reset():
    session.pop("messages", None)
    return jsonify({"response": "Memory has been reset."})
