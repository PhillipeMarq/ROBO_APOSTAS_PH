import os
import requests
import datetime
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

# === CONFIGURAÇÕES ===
TELEGRAM_TOKEN = "123456:ABC-DEF_fake_token"
API_FOOTBALL_KEY = "fake_api_key_123"
API_FOOTBALL_HOST = "v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-key": API_FOOTBALL_KEY,
    "x-rapidapi-host": API_FOOTBALL_HOST
}

# === FUNÇÕES PRINCIPAIS ===

def get_games(date_str):
    url = f"https://{API_FOOTBALL_HOST}/fixtures"
    params = {"date": date_str, "timezone": "America/Sao_Paulo"}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data.get("response", [])

def get_statistics(fixture_id):
    url = f"https://{API_FOOTBALL_HOST}/fixtures/statistics"
    params = {"fixture": fixture_id}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json().get("response", [])

def format_statistics(stats):
    if not stats or len(stats) < 2:
        return "Estatísticas indisponíveis para este jogo."

    team1_stats = stats[0]["statistics"]
    team2_stats = stats[1]["statistics"]
    team1_name = stats[0]["team"]["name"]
    team2_name = stats[1]["team"]["name"]

    message = f"📊 Estatísticas: {team1_name} x {team2_name}
"
    for stat1, stat2 in zip(team1_stats, team2_stats):
        stat_name = stat1["type"]
        value1 = stat1["value"] if stat1["value"] is not None else 0
        value2 = stat2["value"] if stat2["value"] is not None else 0
        message += f"- {stat_name}: {value1} x {value2}
"
    return message

def handle_analise(update: Update, context: CallbackContext):
    args = context.args
    today = datetime.datetime.now()
    dias = [today + datetime.timedelta(days=i) for i in range(4)]

    if args:
        jogo_input = " ".join(args).lower()

    for dia in dias:
        data_str = dia.strftime("%Y-%m-%d")
        jogos = get_games(data_str)

        for jogo in jogos:
            try:
                time1 = jogo["teams"]["home"]["name"]
                time2 = jogo["teams"]["away"]["name"]
                partida = f"{time1.lower()} x {time2.lower()}"
                if not args or jogo_input in partida:
                    liga = jogo["league"]["name"]
                    fixture_id = jogo["fixture"]["id"]
                    horario = jogo["fixture"]["date"][11:16]
                    stats = get_statistics(fixture_id)
                    estatisticas = format_statistics(stats)
                    mensagem = (
                        f"🏆 {liga}
"
                        f"📅 {data_str} ⏰ {horario}
"
                        f"⚽ {time1} x {time2}
"
                        f"{estatisticas}"
                    )
                    update.message.reply_text(mensagem)
            except Exception as e:
                print(f"Erro ao processar jogo: {e}")
                continue

# === MAIN ===
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("analise", handle_analise))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()