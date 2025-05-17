from flask import Flask, request
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import requests
import logging
from utils.analysis import analisar_jogos, analisar_jogo_individual
from utils.telegram_utils import enviar_mensagem, handle_comandos

TOKEN = "7645585466:AAFDbh4PbveXDId_bVynqElHWlQ5Ndts1a4"  # SEU TOKEN DO BOT
bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    handle_comandos(update, bot)
    return "OK"

@app.route("/")
def index():
    return "Bot de apostas esportivas ativo."

def analise_diaria():
    jogos = analisar_jogos()
    for jogo in jogos:
        enviar_mensagem(bot, jogo)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scheduler = BackgroundScheduler(timezone=pytz.utc)  # <- CORREÇÃO AQUI
    scheduler.add_job(analise_diaria, 'cron', hour=9)
    scheduler.start()
    app.run(host="0.0.0.0", port=10000)
