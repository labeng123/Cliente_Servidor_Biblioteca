from flask import Flask
from flask_cors import CORS # <-- NOVA IMPORTAÇÃO

# ... suas importações de infraestrutura e aplicação ...
from apresentacao.controladores.controlador import criar_blueprint_biblioteca

def create_app():
    app = Flask(__name__)
    CORS(app) # <-- LIBERANDO A COMUNICAÇÃO DE REDE

    # O app.secret_key não é mais tão vital para Flash Messages, 
    # mas pode manter para sessões futuras.
    app.secret_key = 'chave_secreta_mvp' 

    # ... resto da sua injeção de dependência e registro do blueprint ...