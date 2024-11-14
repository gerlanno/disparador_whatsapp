import socket
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///disparador.db"
    app.secret_key = "secret*Key@Flask"
    db.init_app(app)
   
    from routes import setup_routes

    setup_routes(app, db)

    migrate = Migrate(app, db)
    

    return app
