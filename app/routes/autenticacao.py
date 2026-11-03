
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
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

        flash("Login realizado com sucesso!", "sucesso")
        return redirect(url_for("principal.inicio"))

    return render_template("autenticacao/login.html")
