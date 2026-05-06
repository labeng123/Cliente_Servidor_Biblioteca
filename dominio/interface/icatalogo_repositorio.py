from abc import ABC, abstractmethod
from typing import List, Optional
from dominio.entidades.livro import Livro

class ICatalogoRepository(ABC):
    @abstractmethod
    def listar_todos(self) -> List[Livro]:
        """Deve retornar uma lista de entidades Livro."""
        pass

    @abstractmethod
    def buscar_por_id(self, livro_id: int) -> Optional[Livro]:
        """Deve retornar um Livro específico ou None se não existir."""
        pass