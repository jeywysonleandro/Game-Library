
from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from werkzeug.security import generate_password_hash, check_password_hash

from app.database import obter_banco


principal_bp = Blueprint("principal", __name__)


# =========================================
# PROTEGER AS PÁGINAS DO SISTEMA
# =========================================

@principal_bp.before_request
def verificar_login():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))


# =========================================
# PÁGINA INICIAL: DASHBOARD
# =========================================

@principal_bp.route("/")
def inicio():
    return render_template("inicio.html")


# =========================================
# PÁGINA DA BIBLIOTECA
# =========================================

@principal_bp.route("/biblioteca")
def biblioteca():
    return render_template("biblioteca.html")


# =========================================
# PÁGINA DE FAVORITOS
# =========================================

@principal_bp.route("/favoritos")
def favoritos():
    return render_template("favoritos.html")


# =========================================
# PÁGINA DE ESTATÍSTICAS
# =========================================

@principal_bp.route("/estatisticas")
def estatisticas():
    return render_template("estatisticas.html")


# =========================================
# PÁGINA DE CONFIGURAÇÕES
# =========================================

@principal_bp.route("/configuracoes")
def configuracoes():
    return render_template("configuracoes.html")


# =========================================
# PÁGINA DO PERFIL
# =========================================

@principal_bp.route("/perfil")
def perfil():

    banco = obter_banco()

    usuario = banco.execute(
        """
        SELECT id, nome, email, perfil_publico
        FROM usuarios
        WHERE id = ?
        """,
        (session["usuario_id"],)
    ).fetchone()

    return render_template("perfil.html", usuario=usuario)


# =========================================
# ALTERAR A PRIVACIDADE DO PERFIL
# =========================================

@principal_bp.route("/perfil/privacidade", methods=["POST"])
def alterar_privacidade():

    banco = obter_banco()

    # RECEBER A PRIVACIDADE DESEJADA

    nova_privacidade = request.form.get("perfil_publico")

    # VALIDAR O VALOR RECEBIDO

    if nova_privacidade not in ("0", "1"):

        flash("Opção de privacidade inválida.", "erro")

        return redirect(url_for("principal.perfil"))

    # CONVERTER O VALOR PARA INTEIRO

    nova_privacidade = int(nova_privacidade)

    # ATUALIZAR A PRIVACIDADE DO USUÁRIO

    banco.execute(
        """
        UPDATE usuarios
        SET perfil_publico = ?
        WHERE id = ?
        """,
        (nova_privacidade, session["usuario_id"])
    )

    banco.commit()

    # INFORMAR O RESULTADO

    if nova_privacidade == 1:
        flash("Seu perfil agora é público!", "sucesso")
    else:
        flash("Seu perfil agora é privado!", "sucesso")

    return redirect(url_for("principal.perfil"))


# =========================================
# PÁGINA DE EDIÇÃO DO PERFIL
# =========================================

@principal_bp.route("/perfil/editar", methods=["GET", "POST"])
def editar_perfil():

    banco = obter_banco()

    usuario = banco.execute(
        """
        SELECT id, nome, email
        FROM usuarios
        WHERE id = ?
        """,
        (session["usuario_id"],)
    ).fetchone()

    # PROCESSAR O FORMULÁRIO

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()

        # VALIDAR OS CAMPOS

        if not nome or not email:

            flash("Preencha todos os campos.", "erro")

            return render_template(
                "editar_perfil.html",
                usuario=usuario
            )

        # VERIFICAR SE O E-MAIL JÁ ESTÁ CADASTRADO

        email_existente = banco.execute(
            """
            SELECT id
            FROM usuarios
            WHERE email = ? AND id != ?
            """,
            (email, session["usuario_id"])
        ).fetchone()

        if email_existente:

            flash("Este e-mail já está sendo utilizado.", "erro")

            return render_template(
                "editar_perfil.html",
                usuario=usuario
            )

        # ATUALIZAR OS DADOS

        banco.execute(
            """
            UPDATE usuarios
            SET nome = ?, email = ?
            WHERE id = ?
            """,
            (nome, email, session["usuario_id"])
        )

        banco.commit()

        # ATUALIZAR O NOME NA SESSÃO

        session["usuario_nome"] = nome

        flash("Perfil atualizado com sucesso!", "sucesso")

        return redirect(url_for("principal.perfil"))

    return render_template(
        "editar_perfil.html",
        usuario=usuario
    )


# =========================================
# PÁGINA DE ALTERAÇÃO DE SENHA
# =========================================

@principal_bp.route("/perfil/alterar-senha", methods=["GET", "POST"])
def alterar_senha():

    banco = obter_banco()

    # BUSCAR A SENHA ATUAL DO USUÁRIO

    usuario = banco.execute(
        """
        SELECT senha
        FROM usuarios
        WHERE id = ?
        """,
        (session["usuario_id"],)
    ).fetchone()

    # PROCESSAR O FORMULÁRIO

    if request.method == "POST":

        senha_atual = request.form.get("senha_atual", "")
        nova_senha = request.form.get("nova_senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        # VALIDAR CAMPOS OBRIGATÓRIOS

        if not senha_atual or not nova_senha or not confirmar_senha:

            flash("Preencha todos os campos.", "erro")

            return render_template("alterar_senha.html")

        # VERIFICAR A SENHA ATUAL

        if not check_password_hash(usuario["senha"], senha_atual):

            flash("A senha atual está incorreta.", "erro")

            return render_template("alterar_senha.html")

        # VALIDAR O TAMANHO DA NOVA SENHA

        if len(nova_senha) < 8:

            flash("A nova senha deve ter pelo menos 8 caracteres.", "erro")

            return render_template("alterar_senha.html")

        # VERIFICAR SE AS SENHAS COINCIDEM

        if nova_senha != confirmar_senha:

            flash("As novas senhas não coincidem.", "erro")

            return render_template("alterar_senha.html")

        # IMPEDIR A REUTILIZAÇÃO DA SENHA ATUAL

        if nova_senha == senha_atual:

            flash("A nova senha deve ser diferente da atual.", "erro")

            return render_template("alterar_senha.html")

        # GERAR HASH DA NOVA SENHA

        nova_senha_hash = generate_password_hash(nova_senha)

        # ATUALIZAR A SENHA NO BANCO

        banco.execute(
            """
            UPDATE usuarios
            SET senha = ?
            WHERE id = ?
            """,
            (nova_senha_hash, session["usuario_id"])
        )

        banco.commit()

        flash("Senha alterada com sucesso!", "sucesso")

        return redirect(url_for("principal.perfil"))

    return render_template("alterar_senha.html")
