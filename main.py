import os
import requests
import datetime
from telegram import Update
from telegram.ext import CommandHandler, Updater, CallbackContext

TELEGRAM_TOKEN = "7645585466:AAFDbh4PbveXDId_bVynqElHWlQ5Ndts1a4"
API_FOOTBALL_KEY = "b9b1dfef6bmsh94b835c2f9dc5eep1cb7dajsn1e85556f5e5b"
API_FOOTBALL_HOST = "v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-key": API_FOOTBALL_KEY,
    "x-rapidapi-host": API_FOOTBALL_HOST
}

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

    message = f"📊 Estatísticas: {team1_name} x {team2_name}\n"
    for stat1, stat2 in zip(team1_stats, team2_stats):
        stat_name = stat1["type"]
        value1 = stat1["value"] if stat1["value"] is not None else 0
        value2 = stat2["value"] if stat2["value"] is not None else 0
        message += f"- {stat_name}: {value1} x {value2}\n"
    return message

def handle_analise(update: Update, context: CallbackContext):
    args = context.args
    today = datetime.datetime.now()
    dias = [today + datetime.timedelta(days=i) for i in range(4)]

    jogo_input = " ".join(args).lower() if args else None

    for dia in dias:
        data_str = dia.strftime("%Y-%m-%d")
        jogos = get_games(data_str)

        for jogo in jogos:
            try:
                time1 = jogo["teams"]["home"]["name"]
                time2 = jogo["teams"]["away"]["name"]
                partida = f"{time1.lower()} x {time2.lower()}"
                if not jogo_input or jogo_input in partida:
                    liga = jogo["league"]["name"]
                    fixture_id = jogo["fixture"]["id"]
                    horario = jogo["fixture"]["date"][11:16]
                    stats = get_statistics(fixture_id)
                    estatisticas = format_statistics(stats)
                    mensagem = (
                        f"🏆 {liga}\n"
                        f"📅 {data_str} ⏰ {horario}\n"
                        f"⚽ {time1} x {time2}\n"
                        f"{estatisticas}"
                    )
                    update.message.reply_text(mensagem)
            except Exception as e:
                print(f"Erro ao processar jogo: {e}")
                continue

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    # remove o webhook antigo antes de configurar o novo
    updater.bot.delete_webhook()

    dp.add_handler(CommandHandler("analise", handle_analise))

    PORT = int(os.environ.get("PORT", 10000))
    HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

    print("✅ Bot iniciado com webhook.")
    print(f"🌐 Webhook URL: https://{HOSTNAME}/{TELEGRAM_TOKEN}")

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://{HOSTNAME}/{TELEGRAM_TOKEN}"
    )

    updater.idle()

if __name__ == "__main__":
    main()
