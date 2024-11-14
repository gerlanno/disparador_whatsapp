import json
import os
import requests
import random
from flask import jsonify
from sqlalchemy import null
from models import *
from time import sleep
from config import Config


API_KEY = Config.API_KEY
API_ROOT_URL = Config.API_ROOT_URL


def disparador(configs, recipients):

    """
    Função responsável por processar os disparos de mensagem, de acordo com as 
    configurações informadas pelo usuário.
    """
    
    erros = 0
    sucesso = 0
    
    for target in recipients:
        recipient_number = f"55{target[1]}"
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

        url = f"{API_ROOT_URL}/message/sendText/{instance}"
        payload = json.dumps(
            {
                "number": recipient_number,
                "text": message_content,                
            }
        )
        headers = {
            "apikey": API_KEY,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code == 201:
            print("Mensagem enviada!")
            sucesso += 1
        else:
            erros += 1
            print("Erro enviando a mensagem!", response.text)



        sleep(float(interval))
    return {"Sucesso": sucesso,
                    "Erros": erros}


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


def get_client(instance_name):

    url = f"{API_ROOT_URL}/instance/fetchInstances/"

    payload = {}
    headers = {"accept": "*/*", "apikey": API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)   
    instances = data
    
    for instance in instances:
        print(instance)
        if instance.get("name") == instance_name:
            
            instance_name = instance.get("name")
            status = "Conectado" if instance.get("connectionStatus") ==  "open" else "Desconectado"
            phone_number = instance.get("number")
            profile_name = instance.get("profileName")
      

            return {"client": profile_name, "phone_number": phone_number, "status": status}
        
            
    return {"error": "erro", "error_message": "instância não localizada!"}        


def get_status(instance_name):

    url = f"{API_ROOT_URL}/instance/connectionState/{instance_name}"

    payload = {}
    headers = {"accept": "*/*", "apikey": API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)

    if not response.status_code == 200:
        return {"erro:": "instância não encontrada"}
    
    data = json.loads(response.text)

    instance = data.get("instance")
    if instance.get("state") == "open":
        status = "Conectado"
    else:
        status = "Desconectado"

    return status


def create_instance(instance_name):
    url = f"{API_ROOT_URL}/instance/create"

    payload = {"instanceName": instance_name,
               
               "integration": "WHATSAPP-BAILEYS"
               }
    
    headers = {"accept": "*/*", "apikey": API_KEY}

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)

    
    if response.status_code == 201:
        return {"session": "ok"}
    else:
        raise Exception(f"Erro criando instância! - {data["response"]}")


def get_qrcode(instance_name):
        
    waiting_qr = 0
   
    while waiting_qr <= 3:

        url = f"{API_ROOT_URL}/instance/connect/{instance_name}"
        payload = {}
        headers = {"accept": "*/*", "apikey": API_KEY}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        print(data)
        if "code" in data.keys():
            return data
            break
        else:
            sleep(3)
            waiting_qr += 1
    
    return jsonify({"error": "erro gerando QR Code"})


def terminate_session(instance_name):
    url = f"http://localhost:3000/session/terminate/{instance_name}"

    payload = {}
    headers = {"accept": "*/*", "x-api-key": "disparadordogerlas"}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    
    if data.get("success") == True:
        status = "Desconectado"
    else:
        if "state" in data.keys():
            if data.get("state") == None:
                status = "Desconectado"
    return status


print(get_status("gerlanno"))