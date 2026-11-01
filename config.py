import os



class Config:

    # Chave utilizada pelo Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "chave-temporaria-Game-Library"

    # Caminho da pasta instance
    PASTA_INSTANCE = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "instance"

    )

    # Caminho do banco de dados
    DATABASE = os.path.join(
        PASTA_INSTANCE,
        "game_library.db"
    )