--- utils/telegram_utils.py ---
from telegram import Bot

def enviar_mensagem(bot: Bot, texto: str):
    bot.send_message(chat_id="7178592047", text=texto)  # SEU CHAT ID

def handle_comandos(update: dict, bot: Bot):
    message = update.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if "/analise " in text:
        jogo = text.replace("/analise ", "")
        from utils.analysis import analisar_jogo_individual
        resposta = analisar_jogo_individual(jogo)
        bot.send_message(chat_id=chat_id, text=resposta)
    elif text == "/analise":
        from utils.analysis import analisar_jogos
        respostas = analisar_jogos()
        for r in respostas:
            bot.send_message(chat_id=chat_id, text=r)
    else:
        bot.send_message(chat_id=chat_id, text="Comando não reconhecido.")

from analysis import analisar_jogos, analisar_jogo_individual
--- utils/telegram_utils.py ---
