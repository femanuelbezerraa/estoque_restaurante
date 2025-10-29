
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorador import login_required
from app.models.produto import Produto
from app.models.movimentacao import Movimentacao

rota_estoque = Blueprint('estoque', __name__)

@rota_estoque.route('/entrada/<int:produto_id>', methods=['POST'])
@login_required
def entrada_produto(produto_id):
    if request.method == 'POST':
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
        
        flash('Entrada de estoque registrada com sucesso!', 'success')
        return redirect(url_for('produto.lista'))

@rota_estoque.route('/saida/<int:produto_id>', methods=['POST'])
@login_required
def saida_produto(produto_id):
    if request.method == 'POST':
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
        
        flash('Saída de estoque registrada com sucesso!', 'success')
        return redirect(url_for('produto.lista'))

@rota_estoque.route('/historico')
@login_required
def historico_estoque():
    movimentacoes = Movimentacao.listar_todas()
    return render_template('estoque.html', movimentacoes=movimentacoes)