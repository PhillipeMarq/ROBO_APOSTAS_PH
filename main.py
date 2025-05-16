@bot.message_handler(commands=["analise"])
def analise_jogos(message):
    texto = message.text
    chat_id = message.chat.id

    if texto.strip() == "/analise":
        bot.send_message(chat_id, "📊 Enviando análises dos jogos brasileiros de hoje...")
        jogos = obter_jogos_brasileiros()
        if not jogos:
            bot.send_message(chat_id, "❌ Nenhum jogo brasileiro encontrado para hoje.")
            return

        for jogo in jogos:
            try:
                bot.send_message(chat_id, f"🔍 Analisando o jogo: {jogo['homeTeam']} x {jogo['awayTeam']}...")
                analise = gerar_analise_jogo(jogo)
                bot.send_message(chat_id, analise)
            except Exception as e:
                print(f"Erro ao analisar {jogo['homeTeam']} x {jogo['awayTeam']}: {e}")
                bot.send_message(chat_id, f"⚠️ Erro ao analisar {jogo['homeTeam']} x {jogo['awayTeam']}")
    else:
        nome = texto.replace("/analise", "").strip().lower()
        if not nome:
            bot.send_message(chat_id, "⚠️ Escreva o nome do time ou jogo após /analise")
            return

        bot.send_message(chat_id, f"🔍 Analisando o jogo: {nome}...")
        jogo = buscar_jogo_por_nome(nome)
        if not jogo:
            bot.send_message(chat_id, f"❌ Jogo '{nome}' não encontrado.")
            print(f"⚠️ Nenhum jogo encontrado com o nome: {nome}")
            return

        try:
            analise = gerar_analise_jogo(jogo)
            bot.send_message(chat_id, analise)
        except Exception as e:
            print(f"Erro ao analisar o jogo '{nome}': {e}")
            bot.send_message(chat_id, "⚠️ Erro ao gerar a análise. Tente novamente.")
