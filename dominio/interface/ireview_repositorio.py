from abc import ABC, abstractmethod
from dominio.entidades.review import Review

class IReviewRepository(ABC):
    @abstractmethod
    def salvar(self, review: Review) -> bool:
        pass