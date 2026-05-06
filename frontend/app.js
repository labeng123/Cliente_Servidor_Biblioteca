// O endereço base do seu backend Python
const API_URL = 'http://localhost:5000/api';

// Inicialização: Assim que a página abre, busca os dados
document.addEventListener('DOMContentLoaded', () => {
    carregarCatalogo();
    carregarCesta();
});

// Função central de requisição para evitar repetição de código
async function fazerRequisicao(endpoint, metodo = 'GET', dados = null) {
    const config = {
        method: metodo,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (dados) {
        config.body = JSON.stringify(dados);
    }

    try {
        const resposta = await fetch(`${API_URL}${endpoint}`, config);
        const resultado = await resposta.json();
        
        if (!resposta.ok) {
            throw new Error(resultado.erro || 'Erro desconhecido na API');
        }
        
        return { sucesso: true, dados: resultado };
    } catch (erro) {
        mostrarMensagem(erro.message, 'erro');
        return { sucesso: false };
    }
}

// ==========================================
// MÉTODOS DE NEGÓCIO
// ==========================================

async function carregarCatalogo() {
    const resposta = await fazerRequisicao('/catalogo');
    if (resposta.sucesso) {
        renderizarLista('lista-catalogo', resposta.dados, criarItemCatalogo);
    }
}

async function carregarCesta() {
    const resposta = await fazerRequisicao('/cesta');
    if (resposta.sucesso) {
        renderizarLista('lista-cesta', resposta.dados, criarItemCesta);
    }
}

async function adicionarLivro(id) {
    const resposta = await fazerRequisicao('/cesta', 'POST', { livro_id: id });
    if (resposta.sucesso) {
        mostrarMensagem(resposta.dados.mensagem, 'sucesso');
        carregarCesta(); // Atualiza a tela
    }
}

async function removerLivro(id) {
    const resposta = await fazerRequisicao(`/cesta/${id}`, 'DELETE');
    if (resposta.sucesso) {
        mostrarMensagem(resposta.dados.mensagem, 'sucesso');
        carregarCesta(); // Atualiza a tela
    }
}

// ==========================================
// MANIPULAÇÃO DO DOM (HTML)
// ==========================================

function renderizarLista(idElemento, itens, funcaoCriarHTML) {
    const lista = document.getElementById(idElemento);
    lista.innerHTML = ''; // Limpa a lista antes de repintar
    
    if (itens.length === 0 && idElemento === 'lista-cesta') {
        lista.innerHTML = '<li class="vazio">Sua cesta está vazia.</li>';
        return;
    }

    itens.forEach(item => {
        lista.appendChild(funcaoCriarHTML(item));
    });
}

function criarItemCatalogo(livro) {
    const li = document.createElement('li');
    li.innerHTML = `
        <div class="livro-info">
            <strong>${livro.titulo}</strong><br>
            <small>${livro.livraria}</small>
        </div>
        <button onclick="adicionarLivro(${livro.id})">Alocar Livro</button>
    `;
    return li;
}

function criarItemCesta(livro) {
    const li = document.createElement('li');
    li.innerHTML = `
        <div class="livro-info">
            <strong>${livro.titulo}</strong>
        </div>
        <button class="btn-remover" onclick="removerLivro(${livro.id})">Devolver</button>
    `;
    return li;
}

function mostrarMensagem(texto, tipo) {
    const div = document.getElementById('mensagens-sistema');
    div.innerHTML = `<div class="alerta ${tipo}">${texto}</div>`;
    
    // Some após 3 segundos
    setTimeout(() => {
        div.innerHTML = '';
    }, 3000);
}