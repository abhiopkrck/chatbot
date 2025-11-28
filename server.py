from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import json
from datetime import datetime

from bytez import Bytez

BYTEZ_API_KEY = "ea0e20284203b535479c427e0d609c77"
sdk = Bytez(BYTEZ_API_KEY)
GPT5_MODEL = sdk.model("openai/gpt-5")

app = Flask(__name__)
CORS(app)

# ------- GPT-5 Request -------
def ask_gpt(prompt):
    chat_history = [
        {"role": "system", "content": "You are Jarvis, a smart helpful AI."},
        {"role": "user", "content": prompt}
    ]
    try:
        result = GPT5_MODEL.run(chat_history)
        return result.output
    except Exception as e:
        return f"GPT-5 Error: {e}"


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt", "")

    reply = ask_gpt(prompt)
    return jsonify({"reply": reply})


@app.route("/api/image", methods=["POST"])
def image_gen():
    data = request.json
    text = data.get("prompt")

    IMAGE_MODEL = sdk.model("google/imagen-4.0-ultra-generate-001")

    try:
        result = IMAGE_MODEL.run(text)
        return jsonify({"image": result.output})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
