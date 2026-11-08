
from dotenv import load_dotenv

# CARREGAR AS VARIÁVEIS DO ARQUIVO .ENV

load_dotenv()


from flask import Flask
from config import Config
from app.database import fechar_banco, inicializar_banco


def criar_aplicacao():

    aplicacao = Flask(__name__)

    aplicacao.config.from_object(Config)

    # FECHAR A CONEXÃO COM O BANCO AO FINALIZAR O CONTEXTO

    aplicacao.teardown_appcontext(fechar_banco)

    # COMANDO PARA INICIALIZAR O BANCO

    @aplicacao.cli.command("init-db")
    def comando_inicializar_banco():

        inicializar_banco()

        print("Banco de dados inicializado com sucesso!")

    # REGISTRAR ROTAS PRINCIPAIS

    from app.routes.principal import principal_bp

    aplicacao.register_blueprint(principal_bp)

    # REGISTRAR ROTAS DE AUTENTICAÇÃO

    from app.routes.autenticacao import autenticacao_bp

    aplicacao.register_blueprint(autenticacao_bp)

    return aplicacao
