import os
from datetime import datetime
from dominio.entidades.review import Review
from dominio.interface.ireview_repositorio import IReviewRepository

class TxtReviewRepository(IReviewRepository):
    def __init__(self):
        self.file_name = "banco_de_reviews.txt"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # Salva o TXT na raiz do projeto
        self.file_path = os.path.join(self.base_dir, '..', '..', self.file_name)

    def salvar(self, review: Review) -> bool:
        """
        Implementação concreta exigida pela interface.
        Salva os dados do review em um arquivo de texto simples.
        """
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Formata a linha de texto que será salva
        linha = f"[{data_atual}] Livro_ID: {review.livro_id} | Usuário: {review.usuario} | Review: {review.texto}\n"
        
        try:
            # Abre o arquivo em modo 'a' (append) para adicionar ao final sem apagar o que existe
            with open(self.file_path, 'a', encoding='utf-8') as arquivo:
                arquivo.write(linha)
            return True
        except Exception as e:
            print(f"Falha de infraestrutura ao salvar TXT: {e}")
            return False