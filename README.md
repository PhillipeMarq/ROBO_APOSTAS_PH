# Robô de Análise Esportiva

Este robô analisa jogos de times brasileiros e envia as análises para um bot do Telegram.

## Comandos disponíveis:

- `/analise` – Envia análise de todos os jogos dos próximos 4 dias.
- `/analise TimeA x TimeB` – Envia análise específica de um jogo.

## Como usar:

1. Crie um bot no Telegram via @BotFather e copie o token.
2. Substitua o valor de `bot_token` em `main.py` pelo seu token do bot.
3. Substitua `"INSIRA_SUA_API_KEY_AQUI"` em `analise.py` pela sua chave da API-Football.
4. Suba o projeto para o GitHub e conecte ao Render.
5. Configure o webhook para:
   ```
   https://SEU_PROJETO_RENDER.onrender.com/SEU_TOKEN_DO_BOT
   ```

Pronto! Seu robô está ativo.