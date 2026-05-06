from flask import Flask
from flask_cors import CORS 

from apresentacao.controladores.controlador import criar_blueprint_biblioteca

def create_app():
    app = Flask(__name__)
    CORS(app) 
    app.secret_key = 'chave_secreta_mvp' 

