from flask import Flask
from config import Config


def criar_aplicacao():
    aplicacao = Flask(__name__)

    aplicacao.config.from_object(Config)

    from app.routes.principal import principal_bp

    aplicacao.register_blueprint(principal_bp)

    return aplicacao