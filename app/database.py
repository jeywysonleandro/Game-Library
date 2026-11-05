import sqlite3

from flask import current_app, g


# ABRIR A CONEXÃO COM O BANCO

def obter_banco():

    if "banco" not in g:

        g.banco = sqlite3.connect(
            current_app.config["DATABASE"]
        )

        g.banco.row_factory = sqlite3.Row

        g.banco.execute("PRAGMA foreign_keys = ON")

    return g.banco


# FECHAR A CONEXÃO COM O BANCO

def fechar_banco(e=None):

    banco = g.pop("banco", None)

    if banco is not None:
        banco.close()


# INICIALIZAR BANCO

def inicializar_banco():

    banco = obter_banco()

    with current_app.open_resource("schema.sql") as arquivo:

        banco.executescript(
            arquivo.read().decode("utf-8")
        )

    # VERIFICAR SE A COLUNA DE PRIVACIDADE EXISTE

    colunas = banco.execute(
        "PRAGMA table_info(usuarios)"
    ).fetchall()

    nomes_colunas = [coluna["name"] for coluna in colunas]

    if "perfil_publico" not in nomes_colunas:

        banco.execute(
            """
            ALTER TABLE usuarios
            ADD COLUMN perfil_publico INTEGER NOT NULL DEFAULT 0
            """
        )

    banco.commit()