# Cadastro de Funcionários

## Sobre:
### Este projeto tem como objetivo a criação de um sistema de cadastro e gerenciamento de funcionários e empresas, onde cada empresa pode ser composta por varios funcionários, o principal objetivo é o controle de colaboradores onde posteriormente será implementada uma função para monitoramento de carga horária por colaborador. 

---

## Documentação
_Link:_ `http://127.0.0.1:8000/schema/swagger-ui/`



## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework:** Django (5.x)
* **API Framework:** Django REST Framework (DRF)
* **Banco de Dados:** SQLite3 (Padrão Django)
* **Testes de API:** Postman

## Instalação do Projeto


### Instalação das dependencias
```bash
pip install -r requirements.txt
```

### Criando Usuário Super No Django Admin. 
```bash
python manage.py createsuperuser
```


## Funcionalidades e Endpoints

-  O projeto utiliza a arquitetura consolidada do DRF, onde cada View Genérica cobre múltiplas operações.

### Autenticação e Perfil:

| Recurso | Método | Endpoint | Proteção |
| :--- | :--- | :--- | :--- |
| **Login (Obter Token)** | `POST` | `/auth/token/` | AllowAny |
| **Logout (Invalidar Token)** | `POST` | `/auth/logout/` | JWT Token|
| **Perfil do Colaborador** | `GET / PATCH` | `/auth/me//` | JWT Token|


## CRUD Funcionarios e Empresas(App Funcionarios)
| Recurso | Método | Endpoint | Proteção |
| :--- | :--- | :--- | :--- |
| **Listar / Criar** | `GET / POST` | `/funcionarios/` | JWT Token |
| **Detalhe / Modificar / Deletar** | `GET / PUT / PATCH / DELETE` | `/funcionarios/{id}/` | JWT Token|


# Modelos de Requisição

### Login (Obtenção do Token)
Rota: ``` /auth/token```

``` json

{
    "email": "seu_email@dominio.com",
    "password": "sua_senha"
}

```

### Criação de Funcionário (POST)
Rota: ``` /funcionarios/``` (Requer Access Token no Header)

``` json

{
    "usuario": 1,         // ID do User (conta) criado no Admin
    "empresa": 1,         // ID da Empresa existente
    "cpf": "11122233344", 
    "matricula": "2025005",
    "cargo": "Desenvolvedor Pleno",
    "idade": 30
}

```




# Validações e Relacionamentos
- Validação CPF: O campo ```cpf``` é validado para ter exatamente 11 dígitos numéricos (a API remove a pontuação antes de validar).
- Relacionamento FK: O campo ```usuario``` (ForeignKey para ```contas.User```) e o campo ```empresa``` (ForeignKey para ```empresas.Empresa```) são obrigatórios na criação.

##  Como Rodar o Projeto Localmente

Siga estes passos para configurar e executar a API na sua máquina.
### O Painel Administrativo estará em: ```http://127.0.0.1:8000/admin/```
### 1. Pré-requisitos

Certifique-se de ter o Python 3.x e o `pip` instalados.

### 2. Configuração do Ambiente

```bash
# 1. Clone o repositório
git clone [https://github.com/SEU_USUARIO/django-funcionarios-api.git](https://github.com/SEU_USUARIO/django-funcionarios-api.git)
cd django-funcionarios-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Window

-----------------------------------
# 3. Migrações 

# Aplica todas as migrações (cria as tabelas de Funcionarios e Empresas)
python manage.py migrate

# Executar o Servidor

python py manage.py runserver