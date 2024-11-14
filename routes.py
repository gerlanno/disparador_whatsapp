import csv
import os
from sqlalchemy.exc import IntegrityError
from flask import flash, redirect, request, render_template, jsonify, url_for
from models import *
from services import (
    disparador,
    intervalo_aleatorio,
    random_instance,
    get_qrcode,
    get_status,
    get_client,
    create_instance,
    terminate_session,
)


def setup_routes(app, db):

    @app.route("/")
    def home_page():

        return render_template("index.html")


    @app.route("/instancias", methods=["GET", "POST"])
    def instancias():

        # Listar instâncias
        if request.method == "GET":
            resultado = []
            instances = Instances.query.all()

           

            for instance in instances:
                session_info = get_client(instance.name)
                resultado.append(
                    {
                        "id": instance.id,
                        "name": instance.name,
                        "status": session_info.get("status"),
                        "client": session_info.get("client"),
                        "phone_number": session_info.get("phone_number"),
                    }
                )

            # return jsonify({"resultado": resultado})
            return render_template("instancias.html", instancias=resultado)


    @app.route("/disparos", methods=["POST", "GET"])
    def disparos():
        if request.method == "POST":
            contacts_list = []
            disparos_config = {}
            if not "disparoAleatorio" in request.form.keys():
                disparos_config["modo_disparo"] = "normal"
            else:
                disparos_config["modo_disparo"] = "randomico"

            if "contactsCSV" not in request.files:

                return "Nenhum arquivo enviado", 400

            file = request.files["contactsCSV"]

            if file.filename == "":
                return "Nenhum arquivo selecionado", 400
            # Abre o arquivo CSV diretamente
            try:
                # Como o arquivo está em memória, usamos `StringIO` se o conteúdo é texto
                # ou `BytesIO` para binários, mas no caso de CSV geralmente é texto.
                file_contacts = file.stream.read().decode("utf-8").splitlines()
                csv_reader = csv.reader(file_contacts, delimiter=";")

                # Tratativa do arquivo CSV, exemplo de leitura das linhas
                for row in csv_reader:
                    contacts_list.append(row)  # Aqui você faz a tratativa desejada

            except Exception as e:
                return f"Erro ao processar o arquivo: {str(e)}", 500

            for key in request.form.keys():
                value = request.form.get(key)
                disparos_config[key] = value
            # Receber o status das mensagens enviadas.    
            status_disparo = disparador(disparos_config, contacts_list)
            print(status_disparo)
            if status_disparo:
                flash(f"Disparos concluídos, Sucessos: {status_disparo.get("Sucesso")} - Erros: {status_disparo.get("Erros")}", "success")
                return redirect(url_for("disparos"), 302)
            else: 
                flash(f"Ocorreu um erro", "danger")
                return redirect(url_for("disparos"), 302)
            
        elif request.method == "GET":

            resultado = []
            instances = Instances.query.all()
            for instance in instances:
                if get_status(instance.name) == "Conectado":
                    resultado.append(instance.name)

            
            return render_template("disparar.html", instances=resultado)
        

    @app.route("/criar-instancias", methods=["POST", "GET"])
    def criar_instancias():
        if request.method == "POST":
            instance_name = request.form.get("addInstancia").lower()
            new_instance = Instances(name=instance_name)
            try:
                db.session.add(new_instance)
                
                try:
                    create_instance(instance_name)
                    db.session.commit()
                    flash("Instância cadastrada com sucesso!", "success")
                except Exception as e:
                    flash(e, "danger")                
                return render_template(template_name_or_list="criar-instancia.html")
            except IntegrityError:
                db.session.rollback()
                flash("Já existe uma instância com esse nome!", "danger")
                return render_template(template_name_or_list="criar-instancia.html")

        return render_template(template_name_or_list="criar-instancia.html")
    

    @app.route("/deletar/<id>", methods=["GET"])
    def delete(id):
        if request.method == "GET":
            try:
                Instances.query.filter(Instances.id == id).delete()
                db.session.commit()
                return redirect(url_for("instancias"), 302)
            except Exception as e:
                print(f"Erro excluindo registro: {e}")
                return redirect(url_for("instancias"), 302)
        else:
            return redirect(url_for("index"), 302)


    @app.route("/qrcode")
    def qrcode():
        try:
            # Checando se a instância existe.
            check_instance = db.session.execute(db.select(Instances.name).filter_by(name=request.args.get("instancia"))).scalar_one()
            print(check_instance)
            if check_instance:
                qrcode = get_qrcode(check_instance)
            else:
                return {"Erro Gerando QR CODE": "Nenhuma instância localizada"}
            return qrcode, 200
        except Exception as e:
            print(f"Erro gerando QR CODE - {e}")
            return {"Erro Gerando QR CODE": {e}}


    @app.route("/terminate/<instance>", methods=["GET"])
    def terminate(instance):
        if request.method == "GET":
            terminate_session(instance)
            # return jsonify({"resultado": resultado})
        return redirect("/instancias", 302)


    @app.route("/webhook", methods=["POST", "GET"])
    def webhook():
        if request.method == "GET":
            return "<h1>Bad Request</h1>", 400  # Para o caso de dados inválidos no POST
        elif request.method == "POST":
            data = request.get_json()
            print(data)
            return "OK", 200   
        return "<h1>Bad Request</h1>", 400  # Para o caso de dados inválidos no POST
