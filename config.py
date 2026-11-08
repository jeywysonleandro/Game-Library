
import os


class Config:

    # =========================================
    # CONFIGURAÇÕES DO FLASK
    # =========================================

    SECRET_KEY = os.environ.get("SECRET_KEY") or "chave-temporaria-Game-Library"

    # =========================================
    # CREDENCIAIS DA TWITCH / IGDB
    # =========================================

    TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")

    TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")

    # =========================================
    # CAMINHO DA PASTA INSTANCE
    # =========================================

    PASTA_INSTANCE = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "instance"
    )

    # =========================================
    # CAMINHO DO BANCO DE DADOS
    # =========================================

    DATABASE = os.path.join(
        PASTA_INSTANCE,
        "game_library.db"
    )
