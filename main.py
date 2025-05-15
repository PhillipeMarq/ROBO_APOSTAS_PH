from flask import Flask, request
import json
from analise import analisar_jogos_hoje, analisar_jogo_especifico

app = Flask(__name__)

@app.route('/<token>', methods=['POST'])
def webhook(token):
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "").lower()

        if texto.startswith("/analise "):
            jogo = texto.replace("/analise ", "").strip()
            resposta = analisar_jogo_especifico(jogo)
        elif texto.startswith("/analise"):
            resposta = analisar_jogos_hoje()
        else:
            resposta = "Comando não reconhecido."

        enviar_mensagem(token, chat_id, resposta)
    return "OK"

def enviar_mensagem(token, chat_id, texto):
    import requests
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto
    }
    requests.post(url, json=payload)