import os
from typing import List, Optional
from dominio.entidades.livro import Livro
from dominio.interface.icatalogo_repositorio import ICatalogoRepository

class CatalogoTxtRepository(ICatalogoRepository):
    def __init__(self):
        # Blindagem: Força o caminho ser sempre a raiz do projeto
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.base_dir, '..', '..', 'catalogo_db.txt')
        self._inicializar_dados()

    def _inicializar_dados(self):
        """Se o arquivo não existir, cria e injeta os livros padrão do MVP."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                # Formato: id,titulo,livraria
                f.write("1,O Nome do Vento,Livraria Cultura - Centro\n")
                f.write("2,Engenharia de Software,Biblioteca Universitaria\n")
                f.write("3,Padroes de Projeto,Saraiva Mega Store\n")

    def listar_todos(self) -> List[Livro]:
        livros = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    if not linha.strip(): continue
                    id_str, titulo, livraria = linha.strip().split(',')
                    
                    livros.append(Livro(id=int(id_str), titulo=titulo, livraria=livraria))
        except Exception as e:
            # Em vez de falhar em silêncio, isso vai te mostrar no terminal se algo der errado
            print(f"\n[ERRO CRÍTICO] Falha ao ler TXT do catálogo: {e}\n")
        return livros

    def buscar_por_id(self, livro_id: int) -> Optional[Livro]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    if not linha.strip(): continue
                    id_str, titulo, livraria = linha.strip().split(',')
                    
                    if int(id_str) == livro_id:
                        return Livro(id=int(id_str), titulo=titulo, livraria=livraria)
        except Exception as e:
            print(f"\n[ERRO CRÍTICO] Falha ao buscar ID no TXT do catálogo: {e}\n")
        return None