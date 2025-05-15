from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

BOT_TOKEN = "7645585466:AAFDbh4PbveXDId_bVynqElHWlQ5Ndts1a4"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
API_FOOTBALL_KEY = "91f6237443044e37d78513daf112b001"

brazilian_teams = [
    "Flamengo", "Palmeiras", "São Paulo", "Corinthians", "Grêmio",
    "Atlético Mineiro", "Cruzeiro", "Internacional", "Fluminense",
    "Botafogo", "Athletico Paranaense", "Fortaleza", "Bahia", "Cuiabá",
    "Bragantino", "Vasco", "Santos", "Goiás", "América Mineiro"
]

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def gerar_analise(match, headers):
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]
    stats_url = f"https://v3.football.api-sports.io/teams/statistics?team={match['teams']['home']['id']}&season=2024&league={match['league']['id']}"
    stats_res = requests.get(stats_url, headers=headers).json()

    avg_goals = stats_res["goals"]["for"]["average"]["total"]
    wins = stats_res["fixtures"]["wins"]["total"]
    played = stats_res["fixtures"]["played"]["total"]

    text = f"**Análise Pré-Jogo – {home} x {away}**\\n"
    text += f"- Média de gols do {home}: {avg_goals}\\n"
    text += f"- Vitórias: {wins}/{played}\\n"
    text += f"Sugestão: Over 1.5 ou vitória do {home}\\n"
    return text

def get_all_brazilian_matches():
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    res = requests.get(url, headers=headers)
    data = res.json()
    mensagens = []

    for match in data["response"]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        if any(team in home or team in away for team in brazilian_teams):
            analise = gerar_analise(match, headers)
            mensagens.append(analise)

    return mensagens if mensagens else ["Nenhum jogo de time brasileiro encontrado hoje."]

def get_specific_match_analysis(texto):
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    res = requests.get(url, headers=headers)
    data = res.json()

    partes = texto.split(" ", 1)
    if len(partes) < 2:
        return ["Formato inválido. Ex: /analise Flamengo x Grêmio"]

    nome_jogo = partes[1].lower()

    for match in data["response"]:
        home = match["teams"]["home"]["name"].lower()
        away = match["teams"]["away"]["name"].lower()

        if home in nome_jogo and away in nome_jogo:
            return [gerar_analise(match, headers)]

    return ["Jogo não encontrado."]

active_users = set()

@app.route("/", methods=["GET"])
def home():
    return "Robô de Apostas com Análise Completa!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/start"):
            send_message(chat_id, "Bem-vindo ao Robô de Apostas Esportivas!")
        elif text.startswith("/on"):
            active_users.add(chat_id)
            send_message(chat_id, "Sinais ativados.")
        elif text.startswith("/off"):
            active_users.discard(chat_id)
            send_message(chat_id, "Sinais desativados.")
        elif text.startswith("/analise ") and " x " in text.lower():
            respostas = get_specific_match_analysis(text)
            for r in respostas:
                send_message(chat_id, r)
        elif text.startswith("/analise"):
            respostas = get_all_brazilian_matches()
            for r in respostas:
                send_message(chat_id, r)
        else:
            send_message(chat_id, "Comando não reconhecido. Use /analise ou /analise Flamengo x Grêmio.")
    return "OK", 200
