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




async function carregarProgressoPessoal() {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) return;

    const metaDisplay = document.getElementById('meta-display');
    metaDisplay.innerHTML = 'Carregando progresso...';

    try {
        const response = await fetch(`${API_BASE_URL}/funcionarios/meta/progresso/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        if (response.status === 401) {
             metaDisplay.innerHTML = 'Sessão expirada. Faça login novamente.';
             return;
        }

        const data = await response.json();

        // 1. Renderização dos dados
        metaDisplay.innerHTML = `
            <h3>Seu Progresso Semanal (Meta: ${data.meta_semanal_horas}h)</h3>
            <p><strong>Horas Atuais:</strong> ${data.horas_trabalhadas_atuais.toFixed(2)}h</p>
            <p><strong>Horas Restantes:</strong> ${data.horas_restantes.toFixed(2)}h</p>
            <p><strong>Percentual da Meta:</strong> ${data.progresso_percentual.toFixed(2)}%</p>
            <div style="background-color: #ddd; height: 20px; border-radius: 5px; margin-top: 10px;">
                <div style="width: ${data.progresso_percentual}%; height: 100%; background-color: ${data.progresso_percentual >= 100 ? '#28a745' : '#007bff'}; border-radius: 5px;"></div>
            </div>
        `;
    } catch (error) {
        metaDisplay.innerHTML = 'Erro ao carregar dados da meta.';
        console.error('Erro ao carregar meta:', error);
    }
}



// --- FUNÇÃO UTILIÁRIA ---
function atualizarInterface(estaLogado) {
    loginArea.style.display = estaLogado ? 'none' : 'block';
    pontoBtn.style.display = estaLogado ? 'block' : 'none';
    logoutBtn.style.display = estaLogado ? 'block' : 'none';
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
            carregarProgressoPessoal();
            atualizarInterface(true);
            statusElement.textContent = 'Status: ✅ Login Efetuado!';
            setTimeout(() => {
                window.location.href = '/dashboard'; // Redirecionar após login
            }, 1500);
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
    atualizarInterface(false);
    statusElement.textContent = 'Status: Sessão Encerrada.';
});


// Verifica se o usuário já tem um token ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('accessToken')) {
        atualizarInterface(true);
        statusElement.textContent = 'Status: Pronto para Bater Ponto.';
    }
});



