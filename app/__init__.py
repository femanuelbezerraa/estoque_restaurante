from flask import Flask
import os

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'views', 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'views', 'static')

    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    app.secret_key = 'sua_chave_secreta_aqui'
    
    from . import routes
    routes.init_app(app)
    
    return app