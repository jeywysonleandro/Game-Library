
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import generate_password_hash, check_password_hash

from app.database import obter_banco


# BLUEPRINT DE AUTENTICAÇÃO

autenticacao_bp = Blueprint(
    "autenticacao",
    __name__,
    url_prefix="/auth"
)


# ROTA DE CADASTRO

@autenticacao_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    # Impedir acesso ao cadastro se já estiver conectado
    if "usuario_id" in session:
        return redirect(url_for("principal.inicio"))

    # Verificar se o formulário foi enviado
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "erro")
            return redirect(url_for("autenticacao.cadastro"))

        banco = obter_banco()
        usuario_existente = banco.execute(
            "SELECT id FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

        if usuario_existente:
            flash("Este e-mail já está cadastrado.", "erro")
            return redirect(url_for("autenticacao.cadastro"))

        senha_hash = generate_password_hash(senha)

        banco.execute(
            """
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
            """,
            (nome, email, senha_hash)
        )
        banco.commit()

        flash("Cadastro realizado com sucesso!", "sucesso")
        return redirect(url_for("autenticacao.login"))

    return render_template("autenticacao/cadastro.html")


# ROTA DE LOGIN

@autenticacao_bp.route("/login", methods=["GET", "POST"])
def login():

    # Impedir acesso ao login se já estiver conectado
    if "usuario_id" in session:
        return redirect(url_for("principal.inicio"))

    # Verificar se o formulário foi enviado
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not email or not senha:
            flash("Preencha todos os campos.", "erro")
            return redirect(url_for("autenticacao.login"))

        banco = obter_banco()
        usuario = banco.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

        if usuario is None or not check_password_hash(usuario["senha"], senha):
            flash("E-mail ou senha incorretos.", "erro")
            return redirect(url_for("autenticacao.login"))

        # CRIAR A SESSÃO DO USUÁRIO

        session.clear()
        session["usuario_id"] = usuario["id"]
        session["usuario_nome"] = usuario["nome"]

        flash("Login realizado com sucesso!", "sucesso")
        return redirect(url_for("principal.inicio"))

    return render_template("autenticacao/login.html")


# ROTA DE LOGOUT

@autenticacao_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for("autenticacao.login"))
