from dominio.interface.icatalogo_repositorio import ICatalogoRepository

class CatalogoService:
    def __init__(self, repository: ICatalogoRepository):
        self.catalogo_repo = repository

    def listar_todos_disponiveis(self):
        livros_brutos = self.catalogo_repo.listar_todos()
        return livros_brutos

    def buscar_livro_por_id(self, livro_id):
        if not livro_id or str(livro_id).strip() == "":
            return None, "ID do livro é inválido."
            
        livro = self.catalogo_repo.buscar_por_id(livro_id)
        if not livro:
            return None, "Livro não encontrado no catálogo."
            
        return livro, "Livro encontrado."