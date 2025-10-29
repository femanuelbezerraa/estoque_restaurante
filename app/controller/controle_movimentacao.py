from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto

controle_movimentacao = Blueprint('movimentacao', __name__)

@controle_movimentacao.route('/produto/<int:produto_id>/entrada', methods=['GET', 'POST'])
def entrada_produto(produto_id):
    if request.method == 'POST':
        quantidade_entrada = int(request.form['quantidade_entrada'])
        if quantidade_entrada > 0:
            Produto.atualizar_quantidade(
                produto_id,
                Produto.buscar_por_id(produto_id)['quantidade'] + quantidade_entrada,
                Produto.buscar_por_id(produto_id)['quantidade_minima']
            )
            Movimentacao.registrar_entrada(produto_id, quantidade_entrada, session['usuario_id'])
    return redirect(url_for('cadastro_produto'))


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
    return redirect(url_for('cadastro_produto'))


def historico_estoque():
    movimentacoes = Movimentacao.listar_todas()
    return render_template('estoque.html', Movimentacao=movimentacoes, usuario=session.get('usuario_nome'))