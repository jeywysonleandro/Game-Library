
from flask import Blueprint, render_template

principal_bp = Blueprint("principal", __name__)


# Página inicial: Dashboard
@principal_bp.route("/")
def inicio():
    return render_template("inicio.html")


# Página da biblioteca
@principal_bp.route("/biblioteca")
def biblioteca():
    return render_template("biblioteca.html")


# Página de favoritos
@principal_bp.route("/favoritos")
def favoritos():
    return render_template("favoritos.html")


# Página de estatísticas
@principal_bp.route("/estatisticas")
def estatisticas():
    return render_template("estatisticas.html")


# Página de configurações
@principal_bp.route("/configuracoes")
def configuracoes():
    return render_template("configuracoes.html")
