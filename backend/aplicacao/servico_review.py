from dominio.entidades.review import Review
from dominio.interface.ireview_repositorio import IReviewRepository

class ReviewService:

    def __init__(self, repository: IReviewRepository):
        self.repository = repository

    def adicionar_review(self, livro_id: int, usuario: str, texto: str):
        try:

            novo_review = Review(livro_id, usuario, texto)
            sucesso = self.repository.salvar(novo_review)
            
            if sucesso:
                return True, "Review publicado com sucesso!"
            else:
                return False, "Erro interno ao tentar salvar o review."
                
        except ValueError as e:

            return False, str(e)