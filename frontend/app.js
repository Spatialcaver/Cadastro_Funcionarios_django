// frontend/app.js

const API_BASE_URL = 'http://127.0.0.1:8000'; // Sua API Django
const statusElement = document.getElementById('status');
const loginArea = document.getElementById('login-area');
const pontoBtn = document.getElementById('ponto-btn');
const logoutBtn = document.getElementById('logout-btn');
const loginBtn = document.querySelector('button');
const matriculaInput = document.querySelectorAll('input')[0];
const passwordInput = document.querySelectorAll('input')[1];
const statusDiv = document.querySelector('.status');
const perfilDisplay = document.getElementById('perfil-display');
const nomeColaborador = document.getElementById('nome-colaborador');
const matriculaColaborador = document.getElementById('matricula-colaborador');


function exibirDadosPerfil(nome, matricula) {
    nomeColaborador.textContent = `Bem-vindo, ${nome}!`;
    matriculaColaborador.textContent = matricula;
    perfilDisplay.style.display = 'block';
}

// --- FUNÇÃO UTILIÁRIA ---
function atualizarInterface(estaLogado) {
    loginArea.style.display = estaLogado ? 'none' : 'block';
    pontoBtn.style.display = estaLogado ? 'block' : 'none';
    logoutBtn.style.display = estaLogado ? 'block' : 'none';
    perfilDisplay.style.display = estaLogado ? 'block' : 'none';
}


// --- FUNÇÃO DE CARREGAMENTO ÚNICA (PROGRESSO E PERFIL) ---
async function carregarProgressoPessoal() {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) return;

    const metaDisplay = document.getElementById('meta-display');
    metaDisplay.innerHTML = 'Carregando progresso...';

    try {
        // CORRIGIR A URL para o que definimos
        const response = await fetch(`${API_BASE_URL}/funcionarios/progresso/`, { 
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        if (response.status === 401) {
             metaDisplay.innerHTML = 'Sessão expirada. Faça login novamente.';
             return;
        }

        const data = await response.json();
        
        // 1. **EXIBIÇÃO DO PERFIL (Dados lidos da API)**
        // Assumindo que o backend retorna colaborador (nome) e matricula
        const nome = data.colaborador || 'Colaborador'; 
        const matricula = data.matricula || 'N/A';
        
        exibirDadosPerfil(nome, matricula);
        
        // 2. **RENDERIZAÇÃO DA META (O que estava sumindo)**
        // Usando o operador || 0 para garantir que o HTML não quebre se o total_horas for null
        const horasAtuais = data.horas_trabalhadas_atuais || 0;
        const percentual = data.progresso_percentual || 0;

        metaDisplay.innerHTML = `
            <h3>Seu Progresso Semanal (Meta: ${data.meta_semanal_horas}h)</h3>
            <p><strong>Horas Atuais:</strong> ${horasAtuais.toFixed(2)}h</p>
            <p><strong>Horas Restantes:</strong> ${data.horas_restantes.toFixed(2)}h</p>
            <p><strong>Percentual da Meta:</strong> ${percentual.toFixed(2)}%</p>
            <div style="background-color: #ddd; height: 20px; border-radius: 5px; margin-top: 10px;">
                <div style="width: ${percentual}%; height: 100%; background-color: ${percentual >= 100 ? '#28a745' : '#007bff'}; border-radius: 5px;"></div>
            </div>
        `;
        
        // 3. Persistir os dados mais frescos (Nome/Matrícula) para o caso de reload
        localStorage.setItem('nomeColaborador', nome);
        localStorage.setItem('matriculaColaborador', matricula);

    } catch (error) {
        metaDisplay.innerHTML = 'Erro ao carregar dados da meta.';
        console.error('Erro ao carregar meta:', error);
    }
}

// --- 1. LOGIN (POST /auth/token/) ---
loginBtn.addEventListener('click', async () => {
    const matricula = matriculaInput.value;
    const password = passwordInput.value;

    if (!matricula || !password) {
        statusDiv.textContent = '❌ Preencha matrícula e senha.';
        return;
    }

    statusElement.textContent = 'Status: Tentando Login...';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ matricula, password })
        });

        const data = await response.json();

        if (response.ok) {
            // ARMAZENAMENTO CRÍTICO: Guarda o token na memória do navegador
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
          

            localStorage.setItem('nomeColaborador', data.funcionario_nome);
            localStorage.setItem('matriculaColaborador', data.funcionario_matricula);

            exibirDadosPerfil(data.funcionario_nome, data.funcionario_matricula);
            
            carregarProgressoPessoal();
            atualizarInterface(true);
            statusElement.textContent = 'Status: ✅ Login Efetuado!';
            
        } else {
            // Se as credenciais forem inválidas
            statusElement.textContent = `Status: ❌ ${data.detail || 'Erro de credenciais.'}`;
        }
    } catch (error) {
        statusElement.textContent = 'Status: ❌ Erro de conexão com a API.';
        console.error('Erro de Rede:', error);
    }
});


// --- 2. BATER PONTO (POST /funcionarios/ponto/bater/) ---
pontoBtn.addEventListener('click', async () => {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
        statusElement.textContent = 'Status: ⚠️ Faça login primeiro.';
        return;
    }

    statusElement.textContent = 'Status: Enviando Ponto...';

    try {
        const response = await fetch(`${API_BASE_URL}/funcionarios/ponto/bater/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`, // Chave de segurança JWT
                'Content-Type': 'application/json'
            },
            // Corpo vazio, pois a View identifica o usuário via Token
            body: JSON.stringify({}) 
        });

        const data = await response.json();

        if (response.status === 201) {
            statusElement.textContent = `Status: ✅ Entrada Registrada!`;
        } else if (response.status === 200) {
            statusElement.textContent = `Status: ✅ Saída Registrada! Horas: ${data.data.horas_trabalhadas || 'Calculando...'}`;
        } else {
            statusElement.textContent = `Status: ❌ Erro: ${data.message || data.detail || 'Token Inválido.'}`;
        }
    } catch (error) {
        statusElement.textContent = 'Status: ❌ Erro de rede ou servidor.';
    }
});


// --- 3. LOGOUT (Limpar Tokens) ---
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('nomeColaborador');
    localStorage.removeItem('matriculaColaborador');
    atualizarInterface(false);
    document.getElementById('meta-display').innerHTML = ''; // Limpa a exibição da meta
    statusElement.textContent = 'Status: Sessão Encerrada.';
});


// Verifica se o usuário já tem um token ao carregar a página
document.addEventListener('DOMContentLoaded', async () => {
    const accessToken = localStorage.getItem('accessToken');
    
    if (accessToken) {
        
        atualizarInterface(true);
        statusElement.textContent = 'Status: Carregando dados...';
        
        // 🛑 NOVO FLUXO: Carrega o perfil do backend (para dados mais frescos)
        
        
        // Carrega a meta (que é uma requisição separada)
        carregarProgressoPessoal();
        carregarDadosDoPerfil();
        
        statusElement.textContent = 'Status: Pronto para Bater Ponto.';
    }
});