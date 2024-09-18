from flask import redirect, request, render_template, jsonify, url_for
from models import *
from services import (disparador, 
                      intervalo_aleatorio, 
                      linha_aleatoria, 
                      get_qrcode,
                      get_status,
                      get_client,
                      terminate_session)



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
                        "status": get_status(instance.name),
                        "client": session_info.get("client"),
                        "phone_number": session_info.get("phone_number"),
                    }
                )
           
            #return jsonify({"resultado": resultado})
            return render_template("instancias.html", instancias=resultado)

 

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

    @app.route("/leads", methods=["GET", "POST"])
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

    @app.route("/disparos", methods=["POST", "GET"])
    def disparos():

        """
        1 - Tipo de disparo - linha fixa ou aleatória
        2 - Tipo de intervalo - Intervalo fixo ou aleatório
        
        data = request.args
        tipo_disparo = data.get("tipo_disparo")
        tipo_intervalo = data.get("tipo_intervalo")
        intervalo = data.get("intervalo")

        if tipo_disparo == "fixo":
            linha = data.get("linha")

        elif tipo_disparo == "aleatorio":
            linha = request.form.getlist("linhas")
            """
        return render_template("disparar.html")


    @app.route("/criar-instancias", methods=["POST", "GET"])
    def criar_instancias():
        if request.method == "POST":
            name = request.form.get("addInstancia")
            new_instance = Instances(name=name)
            try:
                db.session.add(new_instance)
                db.session.commit()
                return jsonify({"status": "sucess"})
            except Exception as error:
                return jsonify({"Erro": error})

        return render_template("criar-instancia.html")
    

    @app.route("/deletar/<id>", methods=["GET"])
    def delete(id):
        if request.method == "GET":            
            Instances.query.filter(Instances.id == id).delete()
            db.session.commit()
            
            resultado = []
            instances = Instances.query.all()
            for instance in instances:
                resultado.append(
                    {
                        "id": instance.id,
                        "name": instance.name,

                    }
                )
            #return jsonify({"resultado": resultado})
            return render_template("instancias.html", numberlist=resultado)
        
    @app.route("/qrcode")
    def qrcode():
        instance = request.args.get("instancia")
        print(instance)
        qrcode = get_qrcode(instance)

        return qrcode, 200
    

    @app.route("/terminate/<instance>", methods=["GET"])
    def terminate(instance):
        if request.method == "GET":            
            terminate_session(instance)
            #return jsonify({"resultado": resultado})
        return redirect("/instancias", 302)
    
    @app.route("/webhook", methods=["POST", "GET"])
    def webhook():
        if request.method == "GET":          
            return "<h1>Bad Request</h1>", 400  # Para o caso de dados inválidos no POST
        elif request.method == "POST":
            data = request.get_json()
            if data:
                print(data)                
        return "<h1>Bad Request</h1>", 400  # Para o caso de dados inválidos no POST
    
    @app.route("/teste-form", methods=["POST", "GET"])
    def test_form():
        if not "disparoAleatorio" in request.form.keys():
            modoDisparo = "normal"
        else:
            modoDisparo = "randomico"
        for key in request.form.keys():
            value = request.form.get(key)
            print(f"{key} : {value} - Modo de disparo: {modoDisparo}")
        return redirect(url_for("home_page")), 200
