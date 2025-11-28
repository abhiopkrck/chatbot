from flask import Flask, request, render_template, jsonify
import os, json
from datetime import datetime
from bytez import Bytez

app = Flask(__name__)

BYTEZ_API_KEY = "ea0e20284203b535479c427e0d609c77"
sdk = Bytez(BYTEZ_API_KEY)
GPT5_MODEL = sdk.model("openai/gpt-5")

history_path = "modules/data/chat_history.json"
notepad_path = "modules/data/chat_notepad.txt"
os.makedirs("modules/data", exist_ok=True)

# ---------- Ask GPT-5 ----------
def ask_gpt5(prompt):
    chat = [
        {"role": "system", "content": "You are Jarvis."},
        {"role": "user", "content": prompt}
    ]
    result = GPT5_MODEL.run(chat)
    return result.output[0]["content"] if isinstance(result.output, list) else str(result.output)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user = data["prompt"]

    reply = ask_gpt5(user)

    # save history
    try:
        if os.path.exists(history_path):
            with open(history_path) as f:
                hist = json.load(f)
        else:
            hist = []

        hist.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "user": user,
            "jarvis": reply
        })

        with open(history_path, "w") as f:
            json.dump(hist, f, indent=4)

    except Exception as e:
        print("History error:", e)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
