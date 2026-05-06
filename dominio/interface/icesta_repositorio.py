from abc import ABC, abstractmethod
from typing import List
from dominio.entidades.livro import Livro

class ICestaRepository(ABC):
    @abstractmethod
    def buscar_itens_por_usuario(self, usuario: str) -> List[Livro]:
        """Deve retornar a lista de livros na cesta do usuário."""
        pass

    @abstractmethod
    def adicionar(self, usuario: str, livro_id: int) -> bool:
        """Deve persistir a adição e retornar sucesso ou falha."""
        pass

    @abstractmethod
    def remover(self, usuario: str, livro_id: int) -> bool:
        """Deve persistir a remoção e retornar sucesso ou falha."""
        pass