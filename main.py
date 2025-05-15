from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

# Tokens
BOT_TOKEN = "7645585466:AAFDbh4PbveXDId_bVynqElHWlQ5Ndts1a4"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
API_FOOTBALL_KEY = "91f6237443044e37d78513daf112b001"

# Funções básicas
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

# Função de análise pré-jogo
def get_match_analysis():
    headers = {
        "x-apisports-key": API_FOOTBALL_KEY
    }
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={today}&league=71&season=2024"
    res = requests.get(url, headers=headers)
    data = res.json()

    if not data["response"]:
        return "Nenhum jogo encontrado hoje."

    match = data["response"][0]  # primeiro jogo do dia
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]
    fixture_id = match["fixture"]["id"]

    stats_url = f"https://v3.football.api-sports.io/teams/statistics?team={match['teams']['home']['id']}&season=2024&league=71"
    stats_res = requests.get(stats_url, headers=headers).json()

    avg_goals = stats_res["goals"]["for"]["average"]["total"]
    wins = stats_res["fixtures"]["wins"]["total"]
    played = stats_res["fixtures"]["played"]["total"]

    text = f"**Análise Pré-Jogo – {home} x {away}**\n"
    text += f"- Média de gols do {home}: {avg_goals}\n"
    text += f"- Vitórias: {wins}/{played}\n"
    text += f"Sugestão: Over 1.5 ou vitória do {home}"

    return text

active_users = set()

@app.route("/", methods=["GET"])
def home():
    return "Robô de Apostas Esportivas Ativo!"

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
        elif text == "/analise":
            analysis = get_match_analysis()
            send_message(chat_id, analysis)
        else:
            send_message(chat_id, "Comando não reconhecido. Use /analise para ver uma análise pré-jogo.")
    return "OK", 200
