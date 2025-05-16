def enviar_mensagem(jogo):
    msg = f'''
🏆 {jogo["competicao"]}
📅 {jogo["data"]} - {jogo["hora"]}

⚽ {jogo["time_casa"]} x {jogo["time_fora"]}

📊 Estatísticas:
- Média de gols {jogo["time_casa"]}: {jogo["estatisticas"]["media_gols_casa"]}
- Média de gols {jogo["time_fora"]}: {jogo["estatisticas"]["media_gols_fora"]}
- BTTS frequente: {'Sim' if jogo["estatisticas"]["btts_frequente"] else 'Não'}
- Forma {jogo["time_casa"]}: {jogo["estatisticas"]["forma_casa"]}
- Forma {jogo["time_fora"]}: {jogo["estatisticas"]["forma_fora"]}

💡 Sugestão de Aposta:
{chr(10).join(jogo["sugestoes"])}
'''
    print(msg.strip())