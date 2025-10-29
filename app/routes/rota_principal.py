from flask import Blueprint, render_template, session, redirect, url_for
from app.decorador import login_required

rota_principal = Blueprint('principal', __name__)

@rota_principal.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('principal.dashboard'))
    return redirect(url_for('usuario.login'))

@rota_principal.route('/dashboard')
@login_required
def dashboard():
    return render_template('principal.html', nome_usuario=session.get('usuario_nome'))