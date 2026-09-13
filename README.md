# FastOrder API

API REST para gerenciamento de pedidos de uma pizzaria, desenvolvida com Python e FastAPI.

O projeto foi desenvolvido com foco em **backend, autenticação, autorização, modelagem de banco de dados e regras de negócio**, simulando uma aplicação real de gerenciamento de pedidos.

## 🚀 Tecnologias

* Python
* FastAPI
* SQLAlchemy 2.0
* Pydantic
* Alembic
* SQLite
* JWT
* OAuth2
* bcrypt
* Git e GitHub
* Swagger / OpenAPI

## 📌 Funcionalidades

### Autenticação

* Cadastro de usuários
* Login
* Hash de senhas
* Autenticação utilizando JWT
* Access Token
* Refresh Token
* Verificação de usuário autenticado
* Controle de usuários ativos

### Usuários

* Criação de usuários
* Identificação do usuário autenticado
* Controle de permissões
* Diferenciação entre usuário comum e administrador

### Produtos

* Cadastro de produtos
* Controle de preço
* Controle de estoque
* Disponibilidade do produto
* Categorias
* Restrição de determinadas operações para administradores

### Pedidos

* Criação de pedidos
* Criação de pedidos para usuários específicos por administradores
* Visualização dos próprios pedidos
* Busca de pedidos
* Cancelamento de pedidos
* Controle de proprietário do pedido
* Status do pedido
* Cálculo do preço total

### Itens do pedido

* Associação entre produtos e pedidos
* Quantidade de produtos
* Preço unitário
* Observações
* Relacionamentos entre as entidades

## 🗄️ Modelagem

O sistema possui as seguintes entidades principais:

```text
Usuario
   │
   └── Pedido
          │
          └── ItemPedido
                  │
                  └── Produto
```

Os relacionamentos são implementados utilizando o SQLAlchemy 2.0.

## 🔐 Autorização

O sistema possui diferentes níveis de acesso.

Usuários autenticados podem acessar recursos relacionados aos próprios pedidos, enquanto determinadas operações administrativas são restritas a usuários com permissão de administrador.

Além da autenticação, o projeto implementa regras de autorização para impedir que um usuário manipule recursos pertencentes a outro usuário.

## 🛠️ Configuração do ambiente

O projeto utiliza variáveis de ambiente para armazenar configurações relacionadas à autenticação.

Após clonar o projeto, crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Importante:** não compartilhe sua `SECRET_KEY` e não envie o arquivo `.env` para o GitHub.

## 🧱 Banco de dados

O projeto utiliza **SQLite** durante o desenvolvimento e **SQLAlchemy 2.0** como ORM.

As alterações na estrutura do banco são controladas através do **Alembic**.

## ▶️ Como executar

Clone o repositório:

```bash
git clone https://github.com/EdnaldoCastro/FastApi-Project-.git
```

Entre na pasta:

```bash
cd FastApi-Project-
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Execute a aplicação:

```bash
uvicorn main:app --reload
```

Acesse a documentação:

```text
http://127.0.0.1:8000/docs
```

## 📚 API

A API possui documentação automática através do Swagger/OpenAPI disponibilizada pelo FastAPI.

Após iniciar o projeto, a documentação pode ser acessada em:

```text
/docs
```

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido como uma forma de aplicar conceitos de desenvolvimento backend em uma aplicação prática, indo além de operações CRUD básicas.

Durante o desenvolvimento foram trabalhados conceitos como:

* Arquitetura de APIs REST
* Autenticação e autorização
* JWT
* ORM
* Relacionamentos entre tabelas
* Foreign Keys
* Migrations
* Validação de dados
* Regras de negócio
* Controle de permissões
* Gerenciamento de pedidos e produtos
* Versionamento com Git

## 🔮 Próximos passos

* Desenvolvimento do frontend
* Integração do frontend com a API utilizando JavaScript
* Interface para gerenciamento de pedidos
* Melhorias na gestão de produtos e estoque
* Testes automatizados
* Deploy da aplicação
* Evolução da infraestrutura do projeto

## 👨‍💻 Autor

**Carlos Ednaldo**

Projeto desenvolvido para estudo e evolução prática em desenvolvimento backend com Python.
