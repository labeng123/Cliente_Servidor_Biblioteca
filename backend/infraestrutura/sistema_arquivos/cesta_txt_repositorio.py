import os
from typing import List
from dominio.entidades.livro import Livro
from dominio.interface.icesta_repositorio import ICestaRepository
from dominio.interface.icatalogo_repositorio import ICatalogoRepository

class CestaTxtRepository(ICestaRepository):
    def __init__(self, catalogo_repo: ICatalogoRepository):
        # O TXT precisa do catálogo para simular o "JOIN" do SQL
        self.catalogo_repo = catalogo_repo
        self.file_path = "alocacoes_db.txt"
        
        # Garante que o arquivo exista. Se não existir, cria um vazio.
        if not os.path.exists(self.file_path):
            open(self.file_path, 'w').close()

    def buscar_itens_por_usuario(self, usuario: str) -> List[Livro]:
        itens = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    if not linha.strip(): continue
                    user_txt, livro_id_txt = linha.strip().split(',')
                    
                    if user_txt == usuario:
                        # Busca o objeto Livro completo usando o repositório do catálogo
                        livro = self.catalogo_repo.buscar_por_id(int(livro_id_txt))
                        if livro:
                            itens.append(livro)
        except Exception as e:
            print(f"Erro ao ler TXT da cesta: {e}")
        return itens

    def adicionar(self, usuario: str, livro_id: int) -> bool:
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write(f"{usuario},{livro_id}\n")
            return True
        except Exception as e:
            print(f"Erro ao escrever no TXT: {e}")
            return False

    def remover(self, usuario: str, livro_id: int) -> bool:
        try:
            # Lê tudo
            with open(self.file_path, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            # Escreve tudo de volta, pulando a linha que queremos remover
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for linha in linhas:
                    if linha.strip() != f"{usuario},{livro_id}":
                        f.write(linha)
            return True
        except Exception as e:
            print(f"Erro ao remover do TXT: {e}")
            return False