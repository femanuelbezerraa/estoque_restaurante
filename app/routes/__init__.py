from .rota_usuario import rota_usuario
from .rota_produto import rota_produto
from .rota_principal import rota_principal
from .rota_estoque import rota_estoque

def init_app(app):
    app.register_blueprint(rota_usuario, url_prefix='/usuario')
    app.register_blueprint(rota_produto, url_prefix='/produto')
    app.register_blueprint(rota_principal)
    app.register_blueprint(rota_estoque, url_prefix='/estoque')