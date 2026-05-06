from dominio.interface.icesta_repositorio import ICestaRepository
from dominio.interface.icatalogo_repositorio import ICatalogoRepository

class CestaService:
    def __init__(self, cesta_repo: ICestaRepository, catalogo_repo: ICatalogoRepository):
        self.cesta_repo = cesta_repo
        self.catalogo_repo = catalogo_repo
        self.LIMITE_LIVROS = 3

    def obter_cesta_usuario(self, usuario):
        return self.cesta_repo.buscar_itens_por_usuario(usuario)

    def adicionar_item(self, usuario, livro_id):
        livro = self.catalogo_repo.buscar_por_id(livro_id)
        if not livro:
            return False, "Operação negada: Livro não encontrado no catálogo."

        itens_atuais = self.cesta_repo.buscar_itens_por_usuario(usuario)

        if len(itens_atuais) >= self.LIMITE_LIVROS:
            return False, f"Limite atingido: Você só pode ter {self.LIMITE_LIVROS} livros na cesta."

        for item in itens_atuais:
            if str(item.id) == str(livro_id):
                return False, f"O livro '{livro.titulo}' já está na sua cesta."

        sucesso = self.cesta_repo.adicionar(usuario, livro_id)
        if sucesso:
            return True, f"'{livro.titulo}' adicionado à cesta com sucesso!"
        else:
            return False, "Erro interno ao tentar salvar a cesta."

    def remover_item(self, usuario, livro_id):
        return self.cesta_repo.remover(usuario, livro_id)