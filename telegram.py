from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from analisador import analisar_jogos_proximos_dias

# 🔐 Token do seu bot do Telegram
TOKEN = "6842676519:AAHDFX5u8W-U27KY_V2nyEMJrP2KkD68L20"  # Token real preenchido

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Olá! Eu sou o Robô de Apostas PH!\n\n"
        "Comandos disponíveis:\n"
        "👉 /analise – Análises de todos os jogos com times brasileiros\n"
        "👉 /analise [time x time] – Análise de um jogo específico\n"
        "👉 /liga [nome da liga] – Ver jogos de uma liga (ex: /liga Brasileirão Série A)"
    )

# ✅ /analise → todos os jogos brasileiros
async def analise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Buscando análises de jogos com times brasileiros...")
    mensagens = analisar_jogos_proximos_dias()
    for msg in mensagens:
        await update.message.reply_text(msg, parse_mode="Markdown")

# ✅ /analise [jogo específico]
async def analise_especifica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Digite o nome do jogo. Ex: /analise Flamengo x Grêmio")
        return

    termo = " ".join(context.args).lower()
    mensagens = analisar_jogos_proximos_dias()
    encontrados = [msg for msg in mensagens if termo in msg.lower()]

    if encontrados:
        for msg in encontrados:
            await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Nenhum jogo encontrado com esse nome.")

# ✅ /liga [nome da liga]
async def liga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Digite o nome da liga. Ex: /liga Brasileirão Série B")
        return

    liga_nome = " ".join(context.args).lower()
    mensagens = analisar_jogos_proximos_dias()
    encontrados = [msg for msg in mensagens if liga_nome in msg.lower()]

    if encontrados:
        for msg in encontrados:
            await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Nenhum jogo encontrado nessa liga.")

# ✅ Iniciar o bot
def iniciar_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analise", analise))
    app.add_handler(CommandHandler("analise", analise_especifica))
    app.add_handler(CommandHandler("liga", liga))

    print("🤖 Bot está funcionando...")
    app.run_polling()
