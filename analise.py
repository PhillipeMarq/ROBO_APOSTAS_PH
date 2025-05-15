import requests
from datetime import datetime, timedelta

API_KEY = "INSIRA_SUA_API_KEY_AQUI"
HEADERS = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"

def obter_jogos():
    hoje = datetime.utcnow().date()
    dias = [hoje + timedelta(days=i) for i in range(5)]
    datas = [d.strftime("%Y-%m-%d") for d in dias]
    jogos = []

    for data in datas:
        url = f"{BASE_URL}/fixtures?date={data}"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            for jogo in resp.json().get("response", []):
                home = jogo["teams"]["home"]["name"]
                away = jogo["teams"]["away"]["name"]
                league = jogo["league"]["name"]
                if "Brazil" in jogo["league"]["country"] or "Libertadores" in league or "Sudamericana" in league:
                    jogos.append((home, away, league))
    return jogos

def obter_estatisticas(time, league_name):
    url = f"{BASE_URL}/teams?search={time}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200 or not resp.json()["response"]:
        return None

    team_id = resp.json()["response"][0]["team"]["id"]

    url_stats = f"{BASE_URL}/teams/statistics?team={team_id}&season=2024&league={league_name}"
    stats_resp = requests.get(url_stats, headers=HEADERS)
    if stats_resp.status_code != 200:
        return None

    return stats_resp.json()

def analisar_jogos():
    jogos = obter_jogos()
    respostas = []
    for home, away, league in jogos:
        estatisticas = obter_estatisticas(home, league)
        if estatisticas:
            respostas.append(f"Jogo: {home} x {away} ({league})\nEstatísticas disponíveis para análise.")
        else:
            respostas.append(f"Jogo: {home} x {away} ({league})\nNão foi possível obter estatísticas para este time nesta competição.")
    return respostas

def analisar_jogo_especifico(nome_jogo):
    partes = nome_jogo.split(" x ")
    if len(partes) != 2:
        return ["Formato inválido. Use: /analise TimeA x TimeB"]
    home, away = partes
    estatisticas = obter_estatisticas(home.strip(), "")
    if estatisticas:
        return [f"Jogo: {home.strip()} x {away.strip()}\nEstatísticas disponíveis para análise."]
    else:
        return [f"Jogo: {home.strip()} x {away.strip()}\nNão foi possível obter estatísticas para este time."]