from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.decorador import login_required
from app.models.produto import Produto
from app.models.movimentacao import Movimentacao

rota_produto = Blueprint('produto', __name__)

@rota_produto.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        quantidade_minima = int(request.form['quantidade_min'])
        tipo = request.form.get('tipo', '').strip().lower()
        
        produto = Produto(
            nome=nome,
            quantidade=quantidade,
            quantidade_minima=quantidade_minima,
            tipo=tipo
        )
        produto.cadastrar()
        
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produto.lista'))
        
    return render_template('cadastro_produto.html')

@rota_produto.route('/lista')
@login_required
def lista():
    produtos = Produto.listar_todos()
    return render_template('produtos.html', produtos=produtos)

@rota_produto.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    produto = Produto.buscar_por_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'error')
        return redirect(url_for('produto.lista'))
        
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade_minima = int(request.form['quantidade_min'])
        tipo = request.form.get('tipo', '').strip().lower()
        
        Produto.atualizar(produto_id, nome, quantidade_minima, tipo)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produto.lista'))
        
    return render_template('editar_produto.html', produto=produto)

@rota_produto.route('/remover/<int:produto_id>', methods=['POST'])
@login_required
def remover_produto(produto_id):
    produto = Produto.buscar_por_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'error')
        return redirect(url_for('produto.lista'))
        
    Produto.remover(produto_id)
    flash('Produto removido com sucesso!', 'success')
    return redirect(url_for('produto.lista'))

@rota_produto.route('/adicionar_quantidade/<int:produto_id>', methods=['POST'])
@login_required
def adicionar_quantidade(produto_id):
    quantidade = int(request.form['quantidade'])
    if quantidade <= 0:
        flash('A quantidade deve ser maior que zero', 'error')
        return redirect(url_for('produto.lista'))
        
    produto = Produto.buscar_por_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'error')
        return redirect(url_for('produto.lista'))
        
    nova_quantidade = produto['quantidade'] + quantidade
    Produto.atualizar_quantidade(produto_id, nova_quantidade)
    Movimentacao.registrar(produto_id, quantidade, 'entrada')
    
    flash('Quantidade adicionada com sucesso!', 'success')
    return redirect(url_for('produto.lista'))

@rota_produto.route('/retirar_quantidade/<int:produto_id>', methods=['POST'])
@login_required
def retirar_quantidade(produto_id):
    quantidade = int(request.form['quantidade'])
    if quantidade <= 0:
        flash('A quantidade deve ser maior que zero', 'error')
        return redirect(url_for('produto.lista'))
        
    produto = Produto.buscar_por_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'error')
        return redirect(url_for('produto.lista'))
        
    if produto['quantidade'] < quantidade:
        flash('Quantidade insuficiente em estoque', 'error')
        return redirect(url_for('produto.lista'))
        
    nova_quantidade = produto['quantidade'] - quantidade
    Produto.atualizar_quantidade(produto_id, nova_quantidade)
    Movimentacao.registrar(produto_id, quantidade, 'saida')
    
    flash('Quantidade retirada com sucesso!', 'success')
    return redirect(url_for('produto.lista'))
@login_required
def retirar_quantidade(produto_id):
    return controle_produto.retirar_quantidade(produto_id)