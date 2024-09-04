from flask import request, render_template, jsonify
from models import *
from services import (
    disparador,
    intervalo_aleatorio,
    linha_aleatoria
)


def setup_routes(app, db):
    @app.route("/linhas", methods=["GET", "POST"])
    def index():

        # Listar linhas
        if request.method == "GET":
            resultado = []
            linhas = Linha.query.all()
            for linha in linhas:
                resultado.append(
                    {
                        "id": linha.id,
                        "id_linha": linha.id_linha,
                        "num_linha": linha.numero,
                    }
                )
            return jsonify({"resultado": resultado})
           

        # Cadastrar Linha
        elif request.method == "POST":
            data = request.args
            id_linha = data.get("id_linha")
            num_linha = data.get("num_linha")
            linha = Linha(id_linha=id_linha, numero=num_linha)
            try:
                db.session.add(linha)
                db.session.commit()
                return jsonify({"status": "sucess"})
            except Exception as e:
                print(e)
                return jsonify({"status": "failed"})

    # Detalhes das linhas cadastradas
    @app.route("/linhas/<id>", methods=["GET"])
    def detalhes_linha(id):
        if request.method == "GET":
            resultado = []
            linhas = Linha.query.filter(Linha.id == id)
            for linha in linhas:
                resultado.append(
                    {
                        "id": linha.id,
                        "id_linha": linha.id_linha,
                        "num_linha": linha.numero,
                    }
                )
            return jsonify({"resultado": resultado})

    @app.route("/mensagens", methods=["GET", "POST"])
    def mensagens():

        # Listar mensagens
        if request.method == "GET":
            resultado = []
            mensagens = Mensagem.query.all()
            for mensagem in mensagens:
                resultado.append(
                    {
                        "id": mensagem.id,
                        "name": mensagem.name,
                        "conteudo": mensagem.conteudo,
                    }
                )
            return jsonify({"resultado": resultado})
            

        # Cadastrar Mensagem
        elif request.method == "POST":
            name = request.args.get("name")
            conteudo = request.args.get("conteudo")
            nova_mensagem = Mensagem(name=name, conteudo=conteudo)
            try:
                db.session.add(nova_mensagem)
                db.session.commit()
                return jsonify({"status": "sucess"})
            except Exception as e:
                print(e)
                return jsonify({"status": "failed"})

    @app.route("/leads", methods=["GET","POST"])
    def leads(): 
               # Listar leads
        if request.method == "GET":
            resultado = []
            leads = Lead.query.all()
            for lead in leads:
                resultado.append(
                    {
                        "id": lead.id,
                        "nome": lead.nome,
                        "telefone": lead.telefone,
                    }
                )
            return jsonify({"resultado": resultado})
            

        # Cadastrar Lead
        elif request.method == "POST":
            nome = request.args.get("nome")
            telefone = request.args.get("telefone")
            novo_lead = Lead(nome=nome, telefone=telefone)
            try:
                db.session.add(novo_lead)
                db.session.commit()
                return jsonify({"status": "sucess"})
            except Exception as e:
                print(e)
                return jsonify({"status": "failed"})

    @app.route("/disparos", methods=["POST"])
    def disparos():
        """
        1 - Tipo de disparo - linha fixa ou aleatória
        2 - Tipo de intervalo - Intervalo fixo ou aleatório                
        """
        data = request.args
        tipo_disparo = data.get("tipo_disparo")
        tipo_intervalo = data.get("tipo_intervalo")
        intervalo = data.get("intervalo")

        if tipo_disparo == "fixo":
            linha = data.get("linha")           

        elif tipo_disparo == "aleatorio":
            linhas = request.form.getlist("linhas")            
            disparador(tipo_disparo, linhas, tipo_intervalo, intervalo)
    

       
            



