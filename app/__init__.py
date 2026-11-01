from flask import Flask
from config import Config
from app.database import fechar_banco, inicializar_banco


def criar_aplicacao():
    aplicacao = Flask(__name__)

    aplicacao.config.from_object(Config)

    # Fechar a conexão com o banco ao finalizar o contexto
    aplicacao.teardown_appcontext(fechar_banco)

    # Comando para inicializar o banco
    @aplicacao.cli.command("init-db")
    def comando_inicializar_banco():
        inicializar_banco()
        print("Banco de dados inicializado com sucesso!")
    
    from app.routes.principal import principal_bp
    aplicacao.register_blueprint(principal_bp)

    return aplicacao