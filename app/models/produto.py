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
    def criar(nome, quantidade, quantidade_minima, unidade='unidade', validade=None):
        # Use 'unidade' como valor padrão para satisfazer a restrição CHECK do banco
        return execute_db('''INSERT INTO produto (nome, quantidade, quantidade_minima, unidade)
                             VALUES (%s,%s,%s,%s) RETURNING id_produto''',
                          (nome, quantidade, quantidade_minima, unidade))

    @staticmethod
    def atualizar_quantidade(produto_id, quantidade, quantidade_minima):
        execute_db('UPDATE produto SET quantidade=%s, quantidade_minima=%s WHERE id_produto=%s', (quantidade, quantidade_minima, produto_id))

    @staticmethod
    def atualizar(id_produto, nome=None, quantidade=None, quantidade_minima=None, unidade=None, validade=None):
        campos = []
        valores = []
        if nome is not None:
            campos.append('nome=%s'); valores.append(nome)
        if quantidade is not None:
            campos.append('quantidade=%s'); valores.append(quantidade)
        if quantidade_minima is not None:
            campos.append('quantidade_minima=%s'); valores.append(quantidade_minima)
        if unidade is not None:
            campos.append('unidade=%s'); valores.append(unidade)

        if not campos:
            return None

        set_clause = ', '.join(campos)
        valores.append(id_produto)
        execute_db(f'UPDATE produto SET {set_clause} WHERE id_produto=%s', tuple(valores))

    @staticmethod
    def remover(id_produto):
        referencia = query_db('SELECT 1 FROM movimentacao WHERE produto_id=%s LIMIT 1', (id_produto,), one=True)
        if referencia:
            return False
        execute_db('DELETE FROM produto WHERE id_produto=%s', (id_produto,))
        return True 