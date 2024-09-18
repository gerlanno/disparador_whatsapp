import json
from flask import jsonify
import requests
import random

from sqlalchemy import null
from models import *
from time import sleep


def disparador(tipo_disparo, linha, tipo_intervalo, intervalo):

    leads = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]

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


def get_client(id_linha):

    url = f"http://localhost:3000/client/getClassInfo/{id_linha}"

    payload = {}
    headers = {"accept": "*/*", "x-api-key": "disparadordogerlas"}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    if data.get("success") == True:
        session = data.get("sessionInfo")
        client = session.get("pushname")
        phone_number = session["wid"]["user"]
    else:
        client = "-"
        phone_number = "-"
    return {"client": client, "phone_number": phone_number}


def get_status(id_linha):

    url = f"http://localhost:3000/session/status/{id_linha}"

    payload = {}
    headers = {"accept": "*/*", "x-api-key": "disparadordogerlas"}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    if data.get("success") == True:
        status = "Conectado"
    else:
        status = "Desconectado"
    return status


def start_session(id_linha):
    url = f"http://localhost:3000/session/start/{id_linha}"

    payload = {}
    headers = {"accept": "*/*", "x-api-key": "disparadordogerlas"}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    print(data)
    if data.get("success") == True or "Session already exists" in data.get("error"):
 
        return {"session": "ok"}
    else:
        return {"session": "fail"}


def get_qrcode(id_linha):
    session_status = start_session(id_linha)
    if session_status.get("session") == "ok":
        url = f"http://localhost:3000/session/qr/{id_linha}"

        payload = {}
        headers = {"accept": "*/*", "x-api-key": "disparadordogerlas"}

        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        print(data)
        return data
    else:
        return jsonify({"error": "erro gerando QR Code"})


def terminate_session(id_linha):
    url = f"http://localhost:3000/session/terminate/{id_linha}"

    payload = {}
    headers = {"accept": "*/*", "x-api-key": "disparadordogerlas"}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    print(data)
    if data.get("success") == True:
        status = "Desconectado"
    else:
        if "state" in data.keys():
           if data.get("state") == None:
               status = "Desconectado"
    return status
