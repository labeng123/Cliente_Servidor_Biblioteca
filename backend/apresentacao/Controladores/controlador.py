from flask import Blueprint, jsonify, request

def criar_blueprint_biblioteca(catalogo_service, cesta_service, review_service):
    # O url_prefix='/api' garante que todas as rotas comecem com /api
    biblioteca_bp = Blueprint('biblioteca', __name__, url_prefix='/api')

    @biblioteca_bp.route('/catalogo', methods=['GET'])
    def listar_catalogo():
        """Retorna todos os livros disponíveis no acervo em formato JSON."""
        try:
            livros = catalogo_service.listar_todos_disponiveis()
            # Serialização: Transformando os objetos de Domínio em dicionários básicos
            catalogo_json = [{"id": l.id, "titulo": l.titulo, "livraria": l.livraria} for l in livros]
            return jsonify(catalogo_json), 200
        except Exception as e:
            return jsonify({"erro": "Falha ao carregar o catálogo", "detalhes": str(e)}), 500

    @biblioteca_bp.route('/cesta', methods=['GET'])
    def listar_cesta():
        """Retorna os livros atualmente alocados na cesta."""
        try:
            alocacoes = cesta_service.listar_alocacoes()
            alocacoes_json = [{"id": l.id, "titulo": l.titulo, "livraria": l.livraria} for l in alocacoes]
            return jsonify(alocacoes_json), 200
        except Exception as e:
            return jsonify({"erro": "Falha ao carregar a cesta", "detalhes": str(e)}), 500

    @biblioteca_bp.route('/cesta', methods=['POST'])
    def adicionar_a_cesta():
        """Recebe um JSON com livro_id e aciona a regra de negócio."""
        dados = request.get_json()
        
        if not dados or 'livro_id' not in dados:
            return jsonify({"erro": "O campo 'livro_id' é obrigatório no corpo da requisição."}), 400
            
        try:
            livro_id = int(dados['livro_id'])
            cesta_service.adicionar_livro(livro_id)
            return jsonify({"mensagem": "Livro adicionado à cesta com sucesso."}), 201
        except ValueError as e:
            # O serviço lançou uma exceção de regra de negócio (ex: limite atingido)
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": "Erro interno ao processar alocação."}), 500

    @biblioteca_bp.route('/cesta/<int:livro_id>', methods=['DELETE'])
    def remover_da_cesta(livro_id):
        """Remove um livro específico passando o ID diretamente na URL."""
        try:
            cesta_service.remover_livro(livro_id)
            return jsonify({"mensagem": "Livro removido da cesta."}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @biblioteca_bp.route('/review', methods=['POST'])
    def adicionar_review():
        """Recebe o JSON do review e passa pela validação de domínio."""
        dados = request.get_json()
        
        if not dados or 'livro_id' not in dados or 'texto' not in dados:
            return jsonify({"erro": "Os campos 'livro_id' e 'texto' são obrigatórios."}), 400
            
        try:
            livro_id = int(dados['livro_id'])
            texto = dados['texto']
            review_service.adicionar_review(livro_id, texto)
            return jsonify({"mensagem": "Review publicado com sucesso."}), 201
        except ValueError as e:
            # Exceção disparada caso a Entidade Review detecte palavras ofensivas ou tamanho excedido
            return jsonify({"erro": str(e)}), 400

    return biblioteca_bp