from app import db


"""
executar comando <flask db migrate> e <flask db upgrade> 
ao realizar algura alteração no arquivo models
"""

class Instances(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(20), unique=True, nullable=False)
    def __repr__(self) -> str:
        return f"Instância {self.id} - {self.name}"

class Message(db.Model):
    __tablename__= 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(160), nullable=False)

    def __repr__(self) -> str:
        return f"Mensagem: {self.id} - {self.name} - {self.content}"
    

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    lead_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Lead: {self.id} - {self.lead_name} - {self.phone_number}"
    

    