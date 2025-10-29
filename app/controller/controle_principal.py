from flask import Blueprint, render_template

controle_principal = Blueprint('principal', __name__)

@controle_principal.route('/principal')
def tela_principal():
    return render_template('principal.html')