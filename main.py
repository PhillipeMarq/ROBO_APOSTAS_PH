from flask import Flask, request
import telegram
import os

# Configurações
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text.lower()

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="🤖 Olá! Robô de sinais ativo.")
        
        elif text == "/analise":
            bot.send_message(chat_id=chat_id, text="📊 Enviando análises dos jogos brasileiros de hoje...")

        elif text.startswith("/analise "):
            jogo = text.replace("/analise ", "")
            bot.send_message(chat_id=chat_id, text=f"🔍 Analisando o jogo: {jogo}...")

    return 'ok'

@app.route('/', methods=['GET'])
def index():
    return 'Robô de sinais ativo'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
