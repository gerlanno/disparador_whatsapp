from app import db


"""
executar comando <flask db migrate> e <flask db upgrade> 
ao realizar algura alteração no arquivo models
"""

class Linha(db.Model):
    __tablename__ = 'linhas'
    id = db.Column(db.Integer, primary_key=True, )
    numero = db.Column(db.String(20), unique=True, nullable=False)
    id_linha = db.Column(db.String(40), nullable=False)


    def __repr__(self) -> str:
        return f"Linha {self.id} - {self.id_linha} - {self.numero}"

class Mensagem(db.Model):
    __tablename__= 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    conteudo = db.Column(db.String(160), nullable=False)


    def __repr__(self) -> str:
        return f"Mensagem: {self.id} - {self.name} - {self.conteudo}"
    

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)


    def __repr__(self) -> str:
        return f"Lead: {self.id} - {self.nome} - {self.telefone}"
    

    