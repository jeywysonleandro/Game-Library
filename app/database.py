
import sqlite3

from flask import current_app, g


# =========================================
# ABRIR A CONEXÃO COM O BANCO
# =========================================

def obter_banco():

    if "banco" not in g:

        g.banco = sqlite3.connect(
            current_app.config["DATABASE"]
        )

        g.banco.row_factory = sqlite3.Row

        g.banco.execute("PRAGMA foreign_keys = ON")

    return g.banco


# =========================================
# FECHAR A CONEXÃO COM O BANCO
# =========================================

def fechar_banco(e=None):

    banco = g.pop("banco", None)

    if banco is not None:
        banco.close()


# =========================================
# INICIALIZAR BANCO
# =========================================

def inicializar_banco():

    banco = obter_banco()

    with current_app.open_resource("schema.sql") as arquivo:

        banco.executescript(
            arquivo.read().decode("utf-8")
        )

    # =====================================
    # VERIFICAR COLUNAS DA TABELA USUARIOS
    # =====================================

    colunas_usuarios = banco.execute(
        "PRAGMA table_info(usuarios)"
    ).fetchall()

    nomes_usuarios = [
        coluna["name"] for coluna in colunas_usuarios
    ]

    if "perfil_publico" not in nomes_usuarios:

        banco.execute(
            """
            ALTER TABLE usuarios
            ADD COLUMN perfil_publico INTEGER NOT NULL DEFAULT 0
            """
        )

    # =====================================
    # VERIFICAR COLUNAS DA TABELA JOGOS
    # =====================================

    colunas_jogos = banco.execute(
        "PRAGMA table_info(jogos)"
    ).fetchall()

    nomes_jogos = [
        coluna["name"] for coluna in colunas_jogos
    ]

    # NOVAS COLUNAS

    novas_colunas = {
        "identificador_api": "TEXT",
        "data_lancamento": "TEXT",
        "plataforma": "TEXT",
        "genero": "TEXT",
        "data_inicio": "DATE",
        "data_conclusao": "DATE",
        "observacoes": "TEXT"
    }

    # ADICIONAR SOMENTE AS COLUNAS QUE NÃO EXISTEM

    for nome_coluna, tipo_coluna in novas_colunas.items():

        if nome_coluna not in nomes_jogos:

            banco.execute(
                f"""
                ALTER TABLE jogos
                ADD COLUMN {nome_coluna} {tipo_coluna}
                """
            )

    # SALVAR ALTERAÇÕES

    banco.commit()
