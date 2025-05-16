import requests
from datetime import datetime, timedelta

# ✅ Sua chave API da API-Futebol
API_KEY = "live_cb9d3c2a0c2f4e3e9b5d67b94f3d82"

# ✅ Todas as ligas e torneios com times brasileiros
LIGAS_SUPORTADAS = [
    "Campeonato Brasileiro - Série A",
    "Campeonato Brasileiro - Série B",
    "Campeonato Brasileiro - Série C",
    "Campeonato Brasileiro - Série D",
    "Copa do Brasil",
    "Copa do Nordeste",
    "Supercopa do Brasil",
    "Recopa Sul-Americana",
    "Copa Libertadores da América",
    "Copa Sul-Americana",
    "Campeonato Carioca",
    "Campeonato Paulista",
    "Campeonato Mineiro",
    "Campeonato Gaúcho",
    "Campeonato Paranaense",
    "Campeonato Pernambucano",
    "Campeonato Baiano",
    "Campeonato Goiano",
    "Campeonato Cearense",
    "Campeonato Catarinense"
]

def obter_jogos(dias=4):
    url = f"https://api.api-futebol.com.br/v1/partidas"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    hoje = datetime.now()
    datas = [(hoje + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(dias)]

    jogos_encontrados = []
    for data in datas:
        try:
            response = requests.get(f"{url}/data/{data}", headers=headers)
            if response.status_code == 200:
                data_json = response.json()
                for jogo in data_json:
                    nome_liga = jogo["campeonato"]["nome"]
                    if nome_liga in LIGAS_SUPORTADAS:
                        jogos_encontrados.append(jogo)
        except Exception as e:
            print(f"Erro ao buscar jogos do dia {data}: {e}")
    return jogos_encontrados

def gerar_sinal(jogo):
    casa = jogo["time_mandante"]["nome_popular"]
    fora = jogo["time_visitante"]["nome_popular"]
    campeonato = jogo["campeonato"]["nome"]

    # 🔹 Simulação de estatísticas até conectarmos IA ou estatísticas reais
    media_gols_mandante = 1.8
    media_gols_visitante = 1.6
    ambas_marcam_prob = 0.7

    recomendacoes = []
    if media_gols_mandante + media_gols_visitante > 2.5:
        recomendacoes.append("🔼 Over 2.5 gols")

    if ambas_marcam_prob > 0.6:
        recomendacoes.append("✅ Ambas Marcam (BTTS)")

    if not recomendacoes:
        recomendacoes.append("⚠️ Sem aposta recomendada")

    mensagem = f"""📊 *{casa} x {fora}* ({campeonato})
📅 Data: {jogo['data_realizacao']} - {jogo['hora_realizacao']}
🎯 Sinais:
{chr(10).join(recomendacoes)}
"""
    return mensagem

def analisar_jogos_proximos_dias():
    mensagens = []
    jogos = obter_jogos()
    for jogo in jogos:
        try:
            mensagem = gerar_sinal(jogo)
            mensagens.append(mensagem)
        except Exception as e:
            mensagens.append(f"Erro ao analisar jogo: {e}")
    return mensagens
