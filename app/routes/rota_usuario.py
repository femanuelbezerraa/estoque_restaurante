from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app.decorador import login_required

rota_usuario = Blueprint('usuario', __name__)

@rota_usuario.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.buscar_por_email(email)
        if not usuario:
            flash('Usuário ou senha incorretos', 'error')
            return render_template('autenticacao.html')
            
        if check_password_hash(usuario['senha'], senha):
            session['usuario'] = usuario['id_usuario']
            session['usuario_nome'] = usuario['nome']
            return redirect(url_for('principal.dashboard'))
            
        flash('Usuário ou senha incorretos', 'error')
        return render_template('autenticacao.html')
        
    return render_template('autenticacao.html')

@rota_usuario.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if Usuario.buscar_por_email(email):
            flash('Email já cadastrado', 'error')
            return render_template('cadastro_usuario.html')
            
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        usuario.cadastrar()
        
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('usuario.login'))
        
    return render_template('cadastro_usuario.html')

@rota_usuario.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Você foi desconectado', 'info')
    return redirect(url_for('usuario.login'))