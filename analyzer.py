import requests
from datetime import datetime, timedelta

API_KEY = "a99b6f47c2msh0ff00f621e1eb56p18dbaajsn45cb42a452c0"
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Lista de ligas brasileiras e internacionais que têm clubes do Brasil
LIGAS_BRASILEIRAS = [
    "Brasileirão Série A",
    "Brasileirão Série B",
    "Brasileirão Série C",
    "Brasileirão Série D",
    "Copa do Brasil",
    "Campeonato Paulista",
    "Campeonato Carioca",
    "Campeonato Mineiro",
    "Campeonato Gaúcho",
    "Copa Libertadores",
    "Copa Sul-Americana",
]

# Lista de times brasileiros para filtrar os jogos
TIMES_BRASILEIROS = [
    "Flamengo", "Palmeiras", "Corinthians", "São Paulo", "Grêmio", "Internacional",
    "Athletico-PR", "Atlético-MG", "Botafogo", "Vasco", "Cruzeiro", "Santos",
    "Bahia", "Fortaleza", "Cuiabá", "Goiás", "Coritiba", "Bragantino", "América-MG",
    "Chapecoense", "Ceará", "Vitória", "Juventude", "Paysandu", "Sport", "ABC",
    "CRB", "Avaí", "Ituano", "Tombense", "Londrina", "Novorizontino", "Botafogo-SP",
    "CSA", "Figueirense", "Ypiranga", "Ferroviária", "Remo", "Manaus", "Altos",
    "São Bernardo", "Mirassol", "Botafogo-PB", "Volta Redonda"
]

def analisar_jogos_proximos_dias(dias=4):
    mensagens = []
    hoje = datetime.utcnow()

    for i in range(dias):
        data = (hoje + timedelta(days=i)).strftime("%Y-%m-%d")
        params = {"date": data, "timezone": "America/Sao_Paulo"}
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            mensagens.append(f"⚠️ Erro ao buscar jogos do dia {data}.")
            continue

        jogos = response.json().get("response", [])

        for jogo in jogos:
            time_casa = jogo["teams"]["home"]["name"]
            time_fora = jogo["teams"]["away"]["name"]
            liga = jogo["league"]["name"]
            horario = jogo["fixture"]["date"]
            horario_formatado = datetime.strptime(horario, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m %H:%M")

            # Filtro por ligas brasileiras ou times brasileiros
            if (time_casa in TIMES_BRASILEIROS or time_fora in TIMES_BRASILEIROS) or liga in LIGAS_BRASILEIRAS:
                mensagens.append(
                    f"*🏆 Liga:* {liga}\n"
                    f"*🕒 Horário:* {horario_formatado}\n"
                    f"*⚔️ Jogo:* {time_casa} x {time_fora}\n"
                    f"*🎯 Sinal:* Em breve com IA 🤖"
                )

    if not mensagens:
        mensagens.append("❌ Nenhum jogo brasileiro encontrado nos próximos dias.")

    return mensagens
