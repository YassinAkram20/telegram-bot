from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/healthz")
def health():
    return "ok"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"status": "no data"}), 400

    message = data.get("message")
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        if text.startswith("/start"):
            send_message(chat_id, "أهلاً! أنا بوت بايثون يعمل عبر Render 🤖")
        else:
            send_message(chat_id, f"استلمت: {text}")
    return jsonify({"ok": True})
