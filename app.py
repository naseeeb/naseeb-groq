import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your Groq API endpoint and key
API_KEY = "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"  # Replace with your Groq API key
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"  # Replace with the actual Groq API URL (or another API if different)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_question = data.get('question', '')

    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",  # or "mixtral-8x7b-32768"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_question}
        ]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
