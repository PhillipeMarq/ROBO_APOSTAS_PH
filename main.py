from flask import Flask, request
import telegram
import os

TOKEN = '7645585466:AAFDbh4PbveXDId_bVynqElHWlQ5Ndts1a4'
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    # Responde automaticamente ao receber mensagem
    resposta = f"Sinal recebido: {text}"
    bot.send_message(chat_id=chat_id, text=resposta)
    return 'ok'

@app.route('/')
def home():
    return "Bot de Sinais Rodando!"

if __name__ == '__main__':
    chat_id_inicial = '7645585466'  # Seu ID de chat
    bot.send_message(chat_id=chat_id_inicial, text="✅ Robô de sinais iniciado com sucesso!")
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)