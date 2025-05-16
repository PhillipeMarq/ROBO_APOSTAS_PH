import random

def analisar_jogos(data):
    # Simulação de análise com base na data
    jogos_com_times_brasileiros = [
        {
            "data": data.strftime('%d/%m/%Y'),
            "hora": "16:00",
            "competicao": "Brasileirão Série A",
            "time_casa": "Flamengo",
            "time_fora": "Grêmio",
            "estatisticas": {
                "media_gols_casa": 2.1,
                "media_gols_fora": 1.8,
                "btts_frequente": True,
                "forma_casa": "VVVEV",
                "forma_fora": "DVEVD",
            }
        },
    ]

    # Adiciona sugestão de aposta com base nas estatísticas
    for jogo in jogos_com_times_brasileiros:
        est = jogo["estatisticas"]
        sugestoes = []
        if est["media_gols_casa"] + est["media_gols_fora"] > 2.5:
            sugestoes.append("👉 Mais de 2.5 gols")
        if est["btts_frequente"]:
            sugestoes.append("👉 Ambas Marcam (BTTS)")
        if "VV" in est["forma_casa"]:
            sugestoes.append("👉 Vitória do " + jogo["time_casa"])
        jogo["sugestoes"] = sugestoes
    return jogos_com_times_brasileiros