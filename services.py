import json
from flask import jsonify
import requests
import random
from sqlalchemy import null
from models import *
from time import sleep


def disparador(configs, recipients):

    for target in recipients:
        recipient_number = f"55{target[1]}@c.us"
        recipient_name = target[0]
        message_content = configs.get("textAreaMensagem")
        instance = (
            configs.get("selectedInstance")
            if not "disparoAleatorio" in configs.keys()
            else random_instance()
        )
        interval = (
            int(configs.get("delayInterval"))
            if not "intervaloAleatorio" in configs.keys()
            else intervalo_aleatorio(int(configs.get("delayInterval")))
        )

        url = f"http://localhost:3000/client/sendMessage/{instance}"
        payload = json.dumps(
            {
                "chatId": recipient_number,
                "contentType": "string",
                "content": f"{message_content} \n Esta mensagem esperou {interval} segs para ser enviada!",
            }
        )
        headers = {
            "accept": "*/*",
            "x-api-key": "disparadordogerlas",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            print("Mensagem enviada!")
        else:
            print("Erro enviando a mensagem!", response.text)


        sleep(float(interval))
    return jsonify({"OK": "Tarefa finalizada"})   


def intervalo_aleatorio(intervalo: int) -> int:
    """
    Função que recebe o intervalo em minutos
    e retorna um intervalo
    aleatório em segundos.
    """
    intervalo_randomico = random.randint(
        5, intervalo
    )  # Primeiro argumento vai se referir ao tempo minimo de intervalo. (ex: minimo 30 segundos)

    return intervalo_randomico


def random_instance():
    """
    Função seleciona aleatoriamente uma
    linha dentre uma lista de linhas
    """
    instances = Instances.query.with_entities(Instances.name).all()

    list_instances = [
        instance
        for tuples in instances
        for instance in tuples
        if get_status(instance) == "Conectado"
    ]

    if list_instances:
        return random.choice(list_instances)
    else:
        return "Nenhuma instância conectada!"


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
    waiting_qr = 0
    if session_status.get("session") == "ok":

        while waiting_qr <= 3:

            url = f"http://localhost:3000/session/qr/{id_linha}"
            payload = {}
            headers = {"accept": "*/*", "x-api-key": "disparadordogerlas"}
            response = requests.request("GET", url, headers=headers, data=payload)
            data = json.loads(response.text)
            if "qr" in data.keys():

                return data
                break
            else:
                sleep(3)
                waiting_qr += 1
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
