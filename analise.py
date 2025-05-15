import requests
from datetime import datetime, timedelta

API_KEY = "INSIRA_SUA_API_KEY_AQUI"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

def obter_jogos_brasileiros(dias=4):
    hoje = datetime.now()
    jogos = []
    times_brasileiros = ["Flamengo", "Palmeiras", "São Paulo", "Corinthians", "Grêmio", "Botafogo", "Internacional", "Cruzeiro", "Athletico-PR", "Atlético-MG", "Fortaleza", "Bahia", "Vasco", "Bragantino", "Cuiabá", "Juventude"]

    for i in range(dias + 1):
        data = (hoje + timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"{BASE_URL}/fixtures?date={data}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            resultados = response.json()["response"]
            for jogo in resultados:
                time1 = jogo["teams"]["home"]["name"]
                time2 = jogo["teams"]["away"]["name"]
                if any(t in time1 for t in times_brasileiros) or any(t in time2 for t in times_brasileiros):
                    jogos.append(jogo)
    return jogos

def analisar_jogos_hoje():
    jogos = obter_jogos_brasileiros()
    respostas = []

    for jogo in jogos:
        time1 = jogo["teams"]["home"]["name"]
        time2 = jogo["teams"]["away"]["name"]
        liga = jogo["league"]["name"]
        resposta = f"Jogo: {time1} x {time2} ({liga})
"

        estatisticas = obter_estatisticas(time1, jogo["league"]["id"])
        if estatisticas:
            resposta += f"📊 Estatísticas de {time1} disponíveis.
"
        else:
            resposta += f"❌ Não foi possível obter estatísticas para este time nesta competição.
"
        respostas.append(resposta)
    return "\n\n".join(respostas) or "Nenhum jogo encontrado."

def analisar_jogo_especifico(nome_jogo):
    jogos = obter_jogos_brasileiros()
    for jogo in jogos:
        time1 = jogo["teams"]["home"]["name"].lower()
        time2 = jogo["teams"]["away"]["name"].lower()
        if time1 in nome_jogo.lower() and time2 in nome_jogo.lower():
            return analisar_jogos_hoje()
    return "⚠️ Jogo não encontrado nos próximos dias."

def obter_estatisticas(nome_time, league_id):
    url = f"{BASE_URL}/teams/statistics?team={nome_time}&league={league_id}&season=2024"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None