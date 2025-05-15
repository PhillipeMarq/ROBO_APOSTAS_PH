from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7645585466:AAFDbh4PbveXDId_bVynqElHWlQ5Ndts1a4"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

active_users = set()

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "Robô de Apostas Esportivas Online!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Bem-vindo ao Robô de Apostas Esportivas!")
        elif text == "/on":
            active_users.add(chat_id)
            send_message(chat_id, "Sinais ativados.")
        elif text == "/off":
            active_users.discard(chat_id)
            send_message(chat_id, "Sinais desativados.")
        else:
            send_message(chat_id, "Comando não reconhecido.")
    return "OK", 200
