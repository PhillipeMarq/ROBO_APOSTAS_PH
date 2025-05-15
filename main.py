from fastapi import FastAPI, Request
import telegram
import asyncio
from analise import analisar_jogos, analisar_jogo_especifico

app = FastAPI()
bot_token = "SEU_TOKEN_AQUI"
bot = telegram.Bot(token=bot_token)

@app.post(f"/{bot_token}")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id", "")

    if message.startswith("/analise "):
        nome_jogo = message.replace("/analise ", "")
        resposta = analisar_jogo_especifico(nome_jogo)
    elif message == "/analise":
        resposta = analisar_jogos()
    else:
        resposta = "Comando não reconhecido. Use /analise ou /analise [time x time]"

    if resposta:
        for r in resposta:
            asyncio.create_task(bot.send_message(chat_id=chat_id, text=r))
    return {"ok": True}