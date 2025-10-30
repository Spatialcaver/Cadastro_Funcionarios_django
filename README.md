# 🏢 Cadastro de Funcionários - Django REST Framework API

Este projeto é uma API RESTful completa desenvolvida com **Django** e **Django REST Framework (DRF)** para gerenciar o cadastro de funcionários, incluindo um relacionamento de Um para Muitos (One-to-Many) com a tabela de Empresas.

O projeto foi desenvolvido com foco em demonstrar as operações **CRUD (Create, Read, Update, Delete)** e conceitos essenciais do DRF, como Serializers, Generic Views e Validações customizadas.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework:** Django (5.x)
* **API Framework:** Django REST Framework (DRF)
* **Banco de Dados:** SQLite3 (Padrão Django)
* **Testes de API:** Postman

## 🚀 Funcionalidades da API

O projeto expõe dois endpoints principais: `funcionarios` e `empresas`.

### Funcionalidades do CRUD:

| Recurso | Método | Endpoint | Descrição |
| :--- | :--- | :--- | :--- |
| **Listar** | `GET` | `/api/funcionarios/` | Retorna a lista de funcionários (com Paginação). |
| **Criar** | `POST` | `/api/funcionarios/` | Cadastra um novo funcionário. |
| **Detalhe** | `GET` | `/api/funcionarios/{id}/` | Retorna os dados de um funcionário específico. |
| **Atualizar** | `PUT` / `PATCH` | `/api/funcionarios/{id}/` | Atualiza um funcionário (completa/parcial). |
| **Deletar** | `DELETE` | `/api/funcionarios/{id}/` | Remove um funcionário do banco de dados. |

### Validações e Relacionamentos Específicos

* **Validação Customizada:** O campo `CPF` possui uma validação manual no Serializer que garante que o número de caracteres seja exatamente 14 (ex: `000.000.000-00`).
* **Relacionamento:** `Funcionario` possui uma **ForeignKey** (`empresa`) para o modelo `Empresa`.
* **Exibição:** O nome legível da empresa é retornado nas respostas JSON da API (`StringRelatedField`) e é exibido corretamente no Django Admin.

---

## ⚙️ Como Rodar o Projeto Localmente

Siga estes passos para configurar e executar a API na sua máquina.

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
# venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install django djangorestframework

-----------------------------------
# Migrações e Superusuário



# Aplica todas as migrações (cria as tabelas de Funcionarios e Empresas)
python manage.py migrate

# Cria um usuário administrador para acessar o painel
python manage.py createsuperuser



#Executar o Servidor

py manage.py runserver

O Painel Administrativo estará em: http://127.0.0.1:8000/admin/


-------------------------------------------------------
#JSON de Exemplo: (Observação: Antes de enviar, crie pelo menos uma empresa no Django Admin para obter o ID)

##Criando user
{
    "nome": "Funcionário Exemplo",
    "cpf": "123.456.789-00", 
    "matricula": 1000001,
    "idade": 30,
    "cargo": "Analista Júnior",
    "empresa": 1  // ID da empresa cadastrada no Admin
}



##Criando Empresa

{
    "razao_social": "Exemplo de razão social", 
    "cnpj": "00.000.000/0000-00",
    "segmento": "exemplo de segmento"
    
}
