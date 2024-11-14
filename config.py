import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///whatsapp_sender.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.getenv("API_KEY")
    API_ROOT_URL = os.getenv("API_ROOT_URL")


