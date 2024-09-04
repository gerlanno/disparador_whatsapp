from models import *
import random
from time import sleep



def disparador(tipo_disparo, linha, tipo_intervalo, intervalo):
    
    leads = ["a","b","c","d","e","f","g","h","i","j","k"]

    # Definir se será mais um modelo de mensagem ou uma só mensagem.
    mensagem = Mensagem.query.filter(id=1)

    if tipo_disparo == "aleatorio":
        selecionar_linha = linha_aleatoria(linha)
    elif tipo_disparo == "fixo":
        selecionar_linha = linha
    if tipo_intervalo == "aleatorio":
        intervalo_selecionado = intervalo_aleatorio(intervalo)
    elif tipo_intervalo == "fixo":
        intervalo_selecionado = intervalo * 60

    

    for lead in leads:
        # API para enviar as mensagens, adaptar de acordo com a ferramenta que será usada
       # envianozap(lead, mensagem, selecionar_linha)
        sleep(intervalo_selecionado)
        ...


def intervalo_aleatorio(intervalo):
    """
    Função que recebe o intervalo em minutos e retorna um intervalo
    aleatório em segundos.
    """
    tempo_em_segundos = intervalo * 60

    intervalo_em_segundos = random.randint(
        30, tempo_em_segundos
    )  # Primeiro argumento vai se referir ao tempo minimo de intervalo. (ex: minimo 30 segundos)

    return intervalo_em_segundos


def linha_aleatoria(lista_linhas):
    """
    Função seleciona aleatoriamente uma 
    linha dentre uma lista de linhas
    """
    linha = random.choice(lista_linhas)

    return linha[0]







