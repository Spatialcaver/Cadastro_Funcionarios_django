# Cadastro de Funcionários

## Sobre:
### Este projeto tem como objetivo a criação de um sistema de cadastro e gerenciamento de funcionários e empresas, onde cada empresa pode ser composta por varios funcionários, o principal objetivo é o controle de colaboradores onde posteriormente será implementada uma função para monitoramento de carga horária por colaborador. 

---

## Documentação
_Link:_ `http://127.0.0.1:8000/schema/swagger-ui/`

--

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


## Funcionalidades

O projeto expõe dois endpoints principais: `funcionarios` e `empresas`.

### Funcionalidades do CRUD:

| Recurso | Método | Endpoint | Descrição |
| :--- | :--- | :--- | :--- |
| **Listar** | `GET` | `/core/v1/funcionarios/listar/` | Retorna a lista de funcionários (com Paginação). |
| **Criar** | `POST` | `/core/v1/funcionarios/registrar/` | Cadastra um novo funcionário. |
| **Atualizar** | `PUT` / `PATCH` | `/core/v1/funcionarios/atualizar/{id}/` | Atualiza um funcionário (completa/parcial). |
| **Deletar** | `DELETE` | `/core/v1/funcionarios/deletar/{id}/` | Remove um funcionário do banco de dados. |

## Endpoints

### Modelo de POST para Funcionários:  

Rota: `core/v1/funcionarios/registrar/`

```json

{
    "nome": "Funcionário Exemplo",
    "cpf": "123.456.789-00", 
    "matricula": 1000001,
    "idade": 30,
    "cargo": "Cargo Escolhido",
    "empresa": 1  
}
```


### Modelo de POST Empresas
Rota: `core/v2/empresas/registrar/`
```json
{
    "razao_social": "Exemplo de razão social", 
    "cnpj": "00.000.000/0000-00",
    "segmento": "exemplo de segmento"
    
}
```

### Modelo de GET 

#### Funcionários

Rota ```core/v1/funcionarios/listar/```

#### Empresas

Rota ```core/v2/empresas/listar/```



### Modelo de UPDATE 
#### Funcionários
Rota ```core/v1/funcionarios/atualizar/<int:pk>/```  Subistituir ```<int:pk>/``` pelo ID do objeto a ser atualizado, e alterar campos no ```JSON```.


```json

{
    "nome": "Alteração Exemplo",
    "cpf": "123.456.789-00", 
    "matricula": 1000001,
    "idade": 30,
    "cargo": "Cargo Escolhido",
    "empresa": 1  
}
```



#### Empresas

Rota ```core/v2/empresas/atualizar/<int:pk>/```  Subistituir ```<int:pk>/``` pelo ID do objeto a ser atualizado, e alterar campos no ```JSON```.

```json
{
    "razao_social": "Exemplo de Alteração na razão social", 
    "cnpj": "00.000.000/0000-00",
    "segmento": "exemplo de segmento"
    
}
```

### Modelo de DELETE 
#### Funcionários
Rota ```core/v1/funcionarios/deletar/<int:pk>/```  Subistituir ```<int:pk>/``` pelo ID do objeto a ser atualizado.

#### Empresas

Rota ```core/v2/empresas/deletar/<int:pk>/```  Subistituir ```<int:pk>/``` pelo ID do objeto a ser atualizado.




### Validações e Relacionamentos Específicos

* **Validação Customizada:** O campo `CPF` possui uma validação manual no Serializer que garante que o número de caracteres seja exatamente 14 (ex: `000.000.000-00`).
* **Relacionamento:** `Funcionario` possui uma **ForeignKey** (`empresa`) para o modelo `Empresa`.
* **Exibição:** O nome legível da empresa é retornado nas respostas JSON da API (`StringRelatedField`) e é exibido corretamente no Django Admin.

---

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