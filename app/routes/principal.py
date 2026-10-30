from flask import Blueprint, render_template


principal_bp = Blueprint("principal", __name__)


@principal_bp.route("/")
def inicio():
    return render_template("inicio.html")