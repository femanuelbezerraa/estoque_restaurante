from app.database.db import query_db, execute_db

class Produto:
    @staticmethod
    def listar_todos():
        return query_db('SELECT * FROM produto ORDER BY quantidade - quantidade_minima')

    @staticmethod
    def buscar_por_nome(nome):
        return query_db('SELECT * FROM produto WHERE nome=%s', (nome,), one=True)

    @staticmethod
    def buscar_por_id(id_produto):
        return query_db('SELECT * FROM produto WHERE id_produto=%s', (id_produto,), one=True)

    @staticmethod
    def criar(nome, quantidade, quantidade_minima, tipo=None, validade=None,):
        return execute_db('''INSERT INTO produto (nome, quantidade, quantidade_minima, tipo, validade)
                             VALUES (%s,%s,%s,%s,%s) RETURNING id_produto''',
                          (nome, quantidade, quantidade_minima, tipo, validade))

    @staticmethod
    def atualizar_quantidade(produto_id, quantidade, quantidade_minima):
        execute_db('UPDATE produto SET quantidade=%s, quantidade_minima=%s WHERE id_produto=%s', (quantidade, quantidade_minima, produto_id))

    @staticmethod
    def atualizar(id_produto, nome=None, quantidade=None, quantidade_minima=None, tipo=None, validade=None):

        campos = []
        valores = []
        if nome is not None:
            campos.append('nome=%s'); valores.append(nome)
        if quantidade is not None:
            campos.append('quantidade=%s'); valores.append(quantidade)
        if quantidade_minima is not None:
            campos.append('quantidade_minima=%s'); valores.append(quantidade_minima)
        if tipo is not None:
            campos.append('tipo=%s'); valores.append(tipo)
        if validade is not None:
            campos.append('validade=%s'); valores.append(validade)
      

        if not campos:
            return None

        set_clause = ', '.join(campos)
        valores.append(produto_id)
        execute_db(f'UPDATE produto SET {set_clause} WHERE id_produto=%s', tuple(valores))

    @staticmethod
    def remover(id_produto):
        # Verifica se existem movimentações referenciando este produto
        # Na tabela movimentacao a coluna que referencia produto é 'produto_id'
        referencia = query_db('SELECT 1 FROM movimentacao WHERE produto_id=%s LIMIT 1', (id_produto,), one=True)
        if referencia:
            # Não permite exclusão quando há registros de movimentação
            return False
        execute_db('DELETE FROM produto WHERE id_produto=%s', (id_produto,))
        return True 