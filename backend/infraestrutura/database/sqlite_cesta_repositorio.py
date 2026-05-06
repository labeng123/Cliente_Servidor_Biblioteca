import sqlite3
import os
from typing import List

from dominio.entidades.livro import Livro
from dominio.interface.icesta_repositorio import ICestaRepository

# Assina o contrato da cesta
class SqliteCestaRepository(ICestaRepository):
    def __init__(self):
        self.db_name = "app_cliente.db"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, '..', '..', self.db_name)

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    # Assinatura idêntica à Interface
    def buscar_itens_por_usuario(self, usuario: str) -> List[Livro]:
        query = '''
            SELECT c.id, c.titulo, c.livraria 
            FROM alocacoes a 
            JOIN catalogo c ON a.livro_id = c.id 
            WHERE a.usuario = ?
        '''
        itens_cesta = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (usuario,))
                linhas = cursor.fetchall()
                for linha in linhas:
                    livro = Livro(id=linha[0], titulo=linha[1], livraria=linha[2])
                    itens_cesta.append(livro)
        except sqlite3.Error as e:
            print(f"Erro ao buscar cesta no banco (SQLite): {e}")
        return itens_cesta

    def adicionar(self, usuario: str, livro_id: int) -> bool:
        query = "INSERT INTO alocacoes (livro_id, usuario) VALUES (?, ?)"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (livro_id, usuario))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao adicionar na cesta (SQLite): {e}")
            return False

    def remover(self, usuario: str, livro_id: int) -> bool:
        query = "DELETE FROM alocacoes WHERE usuario = ? AND livro_id = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (usuario, livro_id))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover da cesta (SQLite): {e}")
            return False