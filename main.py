# main.py

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

# === CONFIGURAÇÃO DO BOT ===
TOKEN = '7645585466:AAFDbh4PbveXDId_bVynqElHWlQ5Ndts1a4'
bot = Bot(token=TOKEN)

# === CRIA APLICATIVO FLASK ===
app = Flask(__name__)

# === DISPATCHER (Responsável por lidar com os comandos) ===
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# === COMANDO /analise (exemplo simples) ===
def analise_cmd(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="🔍 Análise ainda em desenvolvimento. Aguarde atualizações.")

# Adiciona o comando /analise
dispatcher.add_handler(CommandHandler('analise', analise_cmd))

# === ROTA DE TESTE (GET /) ===
@app.route('/', methods=['GET'])
def home():
    return '✅ Bot está rodando com webhook!'

# === ROTA DE RECEBIMENTO DO TELEGRAM ===
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# === INICIALIZAÇÃO LOCAL (Render ignora essa parte) ===
if __name__ == '__main__':
    app.run(port=10000, debug=True)
