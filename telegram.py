from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN_BOT = "6050715735:AAGPqON4N5XdrSu9F8TH7K7OWP02N8N9hmE"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Olá! Eu sou seu robô de apostas. Use /ajuda para ver os comandos disponíveis."
    )

def ajuda(update: Update, context: CallbackContext) -> None:
    comandos = (
        "/start - Iniciar o bot\n"
        "/ajuda - Mostrar comandos\n"
        "/analise - Análise de jogos do Brasileirão\n"
        "/analise_campeonato <nome> - Análise de um campeonato específico"
    )
    update.message.reply_text(comandos)

def iniciar_bot():
    updater = Updater(TOKEN_BOT, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ajuda", ajuda))

    # Aqui você pode adicionar os handlers dos comandos analise e analise_campeonato depois

    comandos = [
        BotCommand("start", "Iniciar o bot"),
        BotCommand("ajuda", "Mostrar comandos"),
        BotCommand("analise", "Análise de jogos do Brasileirão"),
        BotCommand("analise_campeonato", "Análise de um campeonato específico"),
    ]
    updater.bot.set_my_commands(comandos)

    print("Bot iniciado...")
    updater.start_polling()
    updater.idle()
