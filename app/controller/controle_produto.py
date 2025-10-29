from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.produto import Produto
from app.models.movimentacao import Movimentacao

controle_produto = Blueprint('produto', __name__)

@controle_produto.route('/produto/cadastro', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        quantidade_minima = int(request.form['quantidade_min'])

        
    existente = Produto.buscar_por_nome(nome)
    if existente:
        Produto.atualizar_quantidade(
             existente['id'], 
            existente['quantidade'] + quantidade, 
            quantidade_minima
            )
        id_produto = existente['id']
    else:
        id_produto = Produto.criar(nome, quantidade, quantidade_minima)

    Movimentacao.registrar_entrada(id_produto, quantidade, session['usuario_id'])
    return redirect(url_for('produto.cadastro_produto'))

    return render_template(
        'cadastro_produto.html', 
        produtos=Produto.listar_todos(),
        usuario=session.get('usuario_nome')
    )


def saida_produto(produto_id):
    if request.method == 'POST':
        quantidade_saida = int(request.form['quantidade_saida'])
        if Produto.buscar_por_id(produto_id) and quantidade_saida > 0 and Produto.buscar_por_id(produto_id)['quantidade'] >= quantidade_saida:
            Produto.atualizar_quantidade(
                produto_id, 
                Produto.buscar_por_id(produto_id)['quantidade'] - quantidade_saida,
                Produto.buscar_por_id(produto_id)['quantidade_minima']
            )
            Movimentacao.registrar_saida(produto_id, quantidade_saida, session['usuario_id'])
        return redirect(url_for('produto.cadastro_produto'))


def editar_produto(id_produto):
    produto = Produto.buscar_por_id(id_produto)
    if request.method == 'POST':
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')
        if quantidade is not None and quantidade != '':
            try:
                quantidade = int(quantidade)
            except ValueError:
                quantidade = None
    quantidade_minima = request.form.get('quantidade_minima')
    if quantidade_minima is not None and quantidade_minima != '':
        try:
                quantidade_minima = int(quantidade_minima)
        except ValueError:
                quantidade_minima = None
    else:
            quantidade_minima = None

        # não atualizamos o campo 'tipo' porque não existe na tabela
    Produto.atualizar(id_produto, nome=nome, quantidade=quantidade, quantidade_minima=quantidade_minima)
    return redirect(url_for('produto.cadastro_produto'))

    return render_template('editar_produto.html', produto=produto, usuario=session.get('usuario_nome'))


def remover_produto(produto_id):
    sucesso = Produto.remover(id_produto=produto_id)
    if not sucesso:
        # Não é possível remover produto referenciado em movimentações
        return render_template('cadastro_produto.html', produtos=Produto.listar_todos(), usuario=session.get('usuario_nome'), error='Não é possível remover produto que possui movimentações registradas.')
    return redirect(url_for('produto.cadastro_produto'))


def adicionar_quantidade(produto_id):
    if request.method == 'POST':
        q = int(request.form.get('quantidade_adicionar', 0))
        produto = Produto.buscar_por_id(produto_id)
        Produto.atualizar_quantidade(produto_id, produto['quantidade'] + q, produto['quantidade_minima'])
        Movimentacao.registrar_entrada(produto_id, q, session['usuario_id'])
        return redirect(url_for('produto.cadastro_produto'))


def retirar_quantidade(id_produto):
    if request.method == 'POST':
        q = int(request.form.get('quantidade_retirar', 0))
        produto = Produto.buscar_por_id(id_produto)
        if produto and produto['quantidade'] >= q:
            Produto.atualizar_quantidade(id_produto, produto['quantidade'] - q, produto['quantidade_minima'])
            Movimentacao.registrar_saida(id_produto, q, session['usuario_id'])
        return redirect(url_for('produto.cadastro_produto'))