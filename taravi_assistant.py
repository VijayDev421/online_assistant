from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder=".")
CORS(app)

chat_history = []

@app.route('/dashboard')
def dashboard():
    return render_template('taravi_dashboard.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("question", "")
    response = f"You asked: {user_input} — this is a placeholder response."
    chat_history.append({"user": user_input, "assistant": response})
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)