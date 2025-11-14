// frontend/admin-panel.js

// 🛑 IMPORTANTE: Configure a URL base da sua API
const API_BASE_URL = 'web-production-f251d.up.railway.app'; 


const regNameInput = document.getElementById('reg-name');
const regMatriculaInput = document.getElementById('reg-matricula');
const regEmailInput = document.getElementById('reg-email');
const regPasswordInput = document.getElementById('reg-password');
const registerBtn = document.getElementById('register-btn');
const registerStatus = document.getElementById('register-status');
const adminLoginArea = document.getElementById('admin-login-area');
const adminPanel = document.getElementById('admin-panel');
const adminLoginBtn = document.getElementById('admin-login-btn');
const adminLogoutBtn = document.getElementById('admin-logout-btn');
const adminMatriculaInput = document.getElementById('admin-matricula');
const adminPasswordInput = document.getElementById('admin-password');
const panelStatus = document.getElementById('panel-status');
const panelStatusData = document.getElementById('panel-status-data');
const funcionariosTableBody = document.getElementById('funcionarios-table-body');
const regIsStaffInput = document.getElementById('reg-is-staff');
const registerArea = document.getElementById('register-area');




function atualizarInterfaceAdmin(estaLogado) {
    adminLoginArea.style.display = estaLogado ? 'none' : 'flex'; 
    adminPanel.style.display = estaLogado ? 'block' : 'none';
    registerArea.style.display = estaLogado ? 'block' : 'none';
}

function adminLogout() {
    // Limpar tokens
    localStorage.removeItem('adminAccessToken');
    localStorage.removeItem('adminRefreshToken');
    
    // Atualizar UI
    atualizarInterfaceAdmin(false);
    panelStatus.textContent = 'Sessão Administrativa Encerrada.';
    panelStatusData.textContent = 'Carregando dados...';
    funcionariosTableBody.innerHTML = '';
}



async function carregarControleGeral() {
    panelStatusData.textContent = 'Carregando lista de funcionários...';
    
    // 1. LER O TOKEN: Garante que o token recém-salvo seja usado
    const accessToken = localStorage.getItem('adminAccessToken'); 

    if (!accessToken) {
        panelStatusData.textContent = 'Acesso inválido. Por favor, faça login.';
        atualizarInterfaceAdmin(false);
        return;
    }

    try {
        
        const response = await fetch(`${API_BASE_URL}/funcionarios/controle/ranking/`, {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${accessToken}` 
            }
        });

        
        if (response.status === 401 || response.status === 403) {
            panelStatusData.textContent = `Acesso negado (${response.status}). Sessão expirada ou sem permissão.`;
            adminLogout();
            return;
        }

        const data = await response.json();
        
        
        const funcionarios = data.results || data; 

        if (Array.isArray(funcionarios)) {
             renderizarTabela(funcionarios); 
             panelStatusData.textContent = `Lista carregada com sucesso. Total: ${funcionarios.length} funcionários.`;
        } else {
             panelStatusData.textContent = 'Erro na estrutura de dados da API.';
        }

    } catch (error) {
        panelStatusData.textContent = 'Erro de conexão ou servidor ao carregar dados.';
        console.error('Erro:', error);
    }
}

function renderizarTabela(funcionarios) {
    funcionariosTableBody.innerHTML = '';
    
    funcionarios.forEach(func => {
        const row = funcionariosTableBody.insertRow();
        
        const nome = func.nome || 'N/A';
        const matricula = func.matricula || 'N/A';
        const cargo = func.cargo || 'N/A';
        // Garante que o progresso percentual seja tratado como número
        const percentual = parseFloat(func.progresso_percentual) || 0; 
        const atingida = func.meta_atingida;

        // Nome, Matrícula, Cargo
        row.insertCell().textContent = nome;
        row.insertCell().textContent = matricula;
        row.insertCell().textContent = cargo;

        // Progresso (%)
        row.insertCell().textContent = `${percentual.toFixed(2)}%`;

        // Meta Atingida
        const metaCell = row.insertCell();
        metaCell.textContent = atingida ? '✅ Atingida' : '❌ Não Atingida';
        metaCell.className = atingida ? 'meta-atingida-sim' : 'meta-atingida-nao';

    });
}


registerBtn.addEventListener('click', async () => {
    const accessToken = localStorage.getItem('adminAccessToken');
    if (!accessToken) {
        registerStatus.textContent = '❌ Faça login administrativo primeiro.';
        return;
    }

    const name = regNameInput.value;
    const matricula = regMatriculaInput.value;
    const email = regEmailInput.value;
    const password = regPasswordInput.value;
    
    // 🛑 CAPTURA O VALOR DO CHECKBOX
    const is_staff = regIsStaffInput.checked; 

    if (!name || !matricula || !email || !password) {
        registerStatus.textContent = '❌ Todos os campos de registro são obrigatórios.';
        return;
    }

    registerStatus.textContent = 'Status: Tentando registrar...';

    try {
        // 🛑 CORREÇÃO DE URL: Usar /auth/signup/ (conforme URLconf)
        const response = await fetch(`${API_BASE_URL}/auth/signup/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}` 
            },
            // 🛑 ADICIONA is_staff AO CORPO DA REQUISIÇÃO
            body: JSON.stringify({ name, matricula, email, password, is_staff }) 
        });

        const data = await response.json();

        if (response.status === 201) { 
            registerStatus.textContent = `✅ Usuário ${data.name || name} (Matrícula: ${data.matricula || matricula}) registrado com sucesso!`;
            
            // Limpa os campos após o sucesso
            regNameInput.value = '';
            regMatriculaInput.value = '';
            regEmailInput.value = '';
            regPasswordInput.value = '';
            regIsStaffInput.checked = false; // Limpa o checkbox

        } else if (response.status === 403 || response.status === 401) {
             registerStatus.textContent = '❌ Sem permissão. Seu token pode ter expirado ou não ser Staff/Admin.';
        } else {
            // Trata erros de validação
            const errorDetail = data.detail || JSON.stringify(data.matricula || data.email || data);
            registerStatus.textContent = `❌ Falha no Registro: ${errorDetail}`;
        }
    } catch (error) {
        registerStatus.textContent = '❌ Erro de conexão ao tentar registrar.';
        console.error('Erro de Rede:', error);
    }
});





// 1. Login do Admin
adminLoginBtn.addEventListener('click', async () => {
    const matricula = adminMatriculaInput.value;
    const password = adminPasswordInput.value;
    

    
    if (!matricula || !password) {
        panelStatus.textContent = '❌ Preencha todos os campos.';
        return;
    }

    panelStatus.textContent = 'Tentando Login...';

    try {
        
        const response = await fetch(`${API_BASE_URL}/auth/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ matricula, password })
        });

        const data = await response.json();

        if (response.ok) {
            const token = data.access;
            
          
            const meResponse = await fetch(`${API_BASE_URL}/auth/me/`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            const meData = await meResponse.json();
            const userProfile = meData.result || meData; 

          
            if (userProfile.is_staff || userProfile.is_superuser) {
                
                localStorage.setItem('adminAccessToken', data.access);
                localStorage.setItem('adminRefreshToken', data.refresh);
                
                adminMatriculaInput.value = '';
                adminPasswordInput.value = '';

                atualizarInterfaceAdmin(true);
                carregarControleGeral(); // Chama o carregamento AGORA
            } else {
                panelStatus.textContent = '❌ Acesso Negado: Permissão de Staff/Admin Requerida.';
            }
            
        } else {
            panelStatus.textContent = `❌ ${data.detail || 'Credenciais inválidas.'}`;
        }
    } catch (error) {
        panelStatus.textContent = '❌ Erro de conexão com a API.';
        console.error('Erro de Rede:', error);
    }
});



adminLogoutBtn.addEventListener('click', adminLogout);



document.addEventListener('DOMContentLoaded', () => {
    const accessToken = localStorage.getItem('adminAccessToken');
    if (accessToken) {
        atualizarInterfaceAdmin(true);
        carregarControleGeral();
    } else {
        atualizarInterfaceAdmin(false);
        panelStatus.textContent = 'Por favor, faça login para acessar o painel.';
    }
});