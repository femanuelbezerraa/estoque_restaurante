from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario

controle_usuario = Blueprint('usuario', __name__)

@controle_usuario.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.buscar_por_email(email)
        if not usuario:
            return render_template('autenticacao.html', erro=True)

        if check_password_hash(usuario['senha'], senha):
            session['usuario'] = usuario['id_usuario']
            session['usuario_nome'] = usuario.get('nome')
            return redirect(url_for('tela_principal'))
        else:
            flash('Usuário ou senha incorretos', 'error')
            return render_template('autenticacao.html', erro=True)
    
    return render_template('autenticacao.html')


def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if Usuario.buscar_por_email(email):
            return render_template('cadastro_usuario.html', erro='E-mail já cadastrado')

        senha_hash = generate_password_hash(senha)
        Usuario.criar(nome, email, senha_hash)
    return redirect(url_for('usuario.login'))

    return render_template('cadastro_usuario.html')


def logout():
    session.pop('usuario', None)
    session.pop('usuario_nome', None)
    return redirect(url_for('usuario.login'))