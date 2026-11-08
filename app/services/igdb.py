
import requests

from flask import current_app


# =========================================
# OBTER TOKEN DE ACESSO DA TWITCH
# =========================================

def obter_token():

    url = "https://id.twitch.tv/oauth2/token"

    dados = {
        "client_id": current_app.config["TWITCH_CLIENT_ID"],
        "client_secret": current_app.config["TWITCH_CLIENT_SECRET"],
        "grant_type": "client_credentials"
    }

    try:

        resposta = requests.post(
            url,
            data=dados,
            timeout=15
        )

        resposta.raise_for_status()

        return resposta.json()["access_token"]

    except requests.RequestException as erro:

        current_app.logger.error(
            "Erro ao obter token da Twitch: %s",
            erro
        )

        raise RuntimeError(
            "Não foi possível autenticar com a Twitch."
        ) from erro


# =========================================
# CABEÇALHOS DE AUTENTICAÇÃO DA IGDB
# =========================================

def obter_cabecalhos():

    token = obter_token()

    return {
        "Client-ID": current_app.config["TWITCH_CLIENT_ID"],
        "Authorization": f"Bearer {token}",
        "Content-Type": "text/plain"
    }


# =========================================
# PESQUISAR JOGOS NA IGDB
# =========================================

def buscar_jogos(termo):

    if not termo or not termo.strip():
        return []

    url = "https://api.igdb.com/v4/games"

    # EVITAR QUE ASPAS NO TERMO QUEBREM A CONSULTA

    termo = termo.strip().replace("\\", "\\\\").replace('"', '\\"')

    consulta = f'''
        search "{termo}";
        fields
            id,
            name,
            summary,
            first_release_date,
            cover.url,
            genres.name,
            platforms.name;
        limit 10;
    '''

    cabecalhos = obter_cabecalhos()

    try:

        resposta = requests.post(
            url,
            headers=cabecalhos,
            data=consulta,
            timeout=20
        )

        resposta.raise_for_status()

        return resposta.json()

    except requests.RequestException as erro:

        current_app.logger.error(
            "Erro ao pesquisar jogos na IGDB: %s",
            erro
        )

        raise RuntimeError(
            "Não foi possível pesquisar jogos na IGDB."
        ) from erro


# =========================================
# BUSCAR UM JOGO ESPECÍFICO PELO ID
# =========================================

def obter_jogo_por_id(identificador):

    # VALIDAR O IDENTIFICADOR

    try:
        identificador = int(identificador)

    except (TypeError, ValueError):
        return None

    if identificador <= 0:
        return None

    url = "https://api.igdb.com/v4/games"

    consulta = f'''
        fields
            id,
            name,
            summary,
            first_release_date,
            cover.url,
            genres.name,
            platforms.name;
        where id = {identificador};
        limit 1;
    '''

    cabecalhos = obter_cabecalhos()

    try:

        resposta = requests.post(
            url,
            headers=cabecalhos,
            data=consulta,
            timeout=20
        )

        resposta.raise_for_status()

        resultados = resposta.json()

        if not resultados:
            return None

        return resultados[0]

    except requests.RequestException as erro:

        current_app.logger.error(
            "Erro ao buscar jogo por ID na IGDB: %s",
            erro
        )

        raise RuntimeError(
            "Não foi possível obter os dados do jogo."
        ) from erro
