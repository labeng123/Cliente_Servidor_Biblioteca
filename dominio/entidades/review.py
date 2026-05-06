class Review:
    def __init__(self, livro_id: int, usuario: str, texto: str):

        texto_limpo = self._validar_e_limpar(texto)
        
        self.livro_id = livro_id
        self.usuario = usuario
        self.texto = texto_limpo

    def _validar_e_limpar(self, texto: str) -> str:
        if not texto or not texto.strip():
            raise ValueError("O review não pode estar vazio.")

        if len(texto) > 500:
            raise ValueError("O review excedeu o limite de 500 caracteres.")

        # Regra de negócio: Filtro de palavras ofensivas
        palavras_ofensivas = ["lixo", "merda", "idiota", "horrivel"]
        texto_lower = texto.lower()
        
        for palavra in palavras_ofensivas:
            if palavra in texto_lower:
                raise ValueError("O review contém linguagem inapropriada e viola nossas diretrizes.")

        return texto.strip()