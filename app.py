from flask import Flask, render_template, request, jsonify
import webbrowser
import subprocess
import threading
from datetime import datetime
from bytez import Bytez
import os

# ---------------- CONFIG -----------------
BYTEZ_KEY = ""
sdk = Bytez(BYTEZ_KEY)

chat_model = sdk.model("openai/gpt-4o")
img_model = sdk.model("google/imagen-4.0-ultra-generate-001")
tts_model = sdk.model("openai/tts-1-hd")  # Bytez TTS

apps = {}
websites = {}
img_history = []

app = Flask(__name__)

# ---------------- TTS FUNCTION -----------------
def speak_text(text):
    if not text:
        return
    output, error = tts_model.run(text)
    if error:
        print("TTS Error:", error)
        return
    audio_bytes = output[0]
    with open("output.mp3", "wb") as f:
        f.write(audio_bytes)
    # Play audio cross-platform
    if os.name == "nt":  # Windows
        os.startfile("output.mp3")
    else:
        os.system("mpg123 output.mp3")  # Linux/Mac

# ---------------- ROUTES -----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_prompt", methods=["POST"])
def send_prompt():
    data = request.json
    prompt = data.get("prompt", "")

    response_text = ""
    lprompt = prompt.lower()

    # Handle open apps/websites or YouTube
    if lprompt.startswith("open "):
        name = prompt[5:]
        if name in websites:
            webbrowser.open(websites[name])
            response_text = f"Opening website {name}"
        elif name in apps:
            try:
                subprocess.Popen(apps[name])
                response_text = f"Opening app {name}"
            except Exception as e:
                response_text = f"Cannot open app: {e}"
        else:
            response_text = f"No app or website named {name} found."
    elif lprompt.startswith("play youtube"):
        query = prompt[13:]
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        response_text = f"Playing {query} on YouTube"
    else:
        # GPT-4o response via Bytez
        output, error = chat_model.run([{"role": "user", "content": prompt}])
        if error:
            response_text = "Error generating response."
        else:
            response_text = output[0]["content"]

    # Speak response in background using Bytez TTS
    threading.Thread(target=lambda: speak_text(response_text)).start()

    return jsonify({"response": response_text})

@app.route("/generate_image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "")
    
    output, error = img_model.run(prompt)
    if error:
        return jsonify({"success": False, "error": str(error)})

    image_url = output[0].get("image_url", "https://via.placeholder.com/512?text=AI+Image")

    entry = {
        "prompt": prompt,
        "image_url": image_url,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    img_history.append(entry)
    return jsonify({"success": True, "entry": entry})

@app.route("/history")
def get_history():
    return jsonify(img_history)

@app.route("/add_web", methods=["POST"])
def add_web():
    data = request.json
    name = data.get("name")
    url = data.get("url")
    websites[name] = url
    return jsonify({"success": True})

@app.route("/add_app", methods=["POST"])
def add_app():
    data = request.json
    name = data.get("name")
    path = data.get("path")
    apps[name] = path
    return jsonify({"success": True})

# ---------------- RUN -------------------
if __name__ == "__main__":
    app.run(debug=True)
