from telegram import Bot

def enviar_mensagem(bot: Bot, texto: str):
    chat_id = 7178592047  # Chat ID preenchido
    bot.send_message(chat_id=chat_id, text=texto)

def handle_comandos(update: dict, bot: Bot):
    message = update.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text.startswith("/analise "):
        jogo = text.replace("/analise ", "").strip()
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
