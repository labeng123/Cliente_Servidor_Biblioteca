import sqlite3
import os
from typing import List, Optional

from dominio.entidades.livro import Livro
from dominio.interface.icatalogo_repositorio import ICatalogoRepository

# 3. A classe herda (assina) a interface ICatalogoRepository
class SqliteCatalogoRepository(ICatalogoRepository):
    def __init__(self):
        # A mesma lógica de antes
        self.db_name = "app_cliente.db"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, '..', '..', self.db_name)

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    # 4. A assinatura dos métodos DEVE ser exatamente igual à exigida pela Interface
    def listar_todos(self) -> List[Livro]:
        query = "SELECT id, titulo, livraria FROM catalogo"
        livros = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                linhas = cursor.fetchall()
                for linha in linhas:
                    livro = Livro(id=linha[0], titulo=linha[1], livraria=linha[2])
                    livros.append(livro)
        except sqlite3.Error as e:
            print(f"Erro ao buscar catálogo (SQLite): {e}")
        return livros

    def buscar_por_id(self, livro_id: int) -> Optional[Livro]:
        query = "SELECT id, titulo, livraria FROM catalogo WHERE id = ?"
        livro = None
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (livro_id,))
                linha = cursor.fetchone()
                if linha:
                    livro = Livro(id=linha[0], titulo=linha[1], livraria=linha[2])
        except sqlite3.Error as e:
            print(f"Erro ao buscar livro por ID (SQLite): {e}")
        return livro