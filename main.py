import datetime
from utils.analyzer import analisar_jogos
from utils.telegram import enviar_mensagem

def main():
    hoje = datetime.date.today()
    dias = [hoje + datetime.timedelta(days=i) for i in range(4)]
    for dia in dias:
        jogos = analisar_jogos(dia)
        for jogo in jogos:
            enviar_mensagem(jogo)

if __name__ == "__main__":
    main()