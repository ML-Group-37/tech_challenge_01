# Tech Challenge 01

## 📊 API Vitivinicultura Embrapa

Esta API fornece acesso público aos dados de vitivinicultura brasileira, extraídos diretamente do site da Embrapa. Os dados abrangem produção, processamento, comercialização, importação e exportação de uvas, vinhos e derivados.

Todos os endpoints contam com suporte a **fallback inteligente**, permitindo o uso de backups locais (`db`) quando o site da Embrapa estiver fora do ar. Também é possível forçar uma nova coleta diretamente da web com o parâmetro `force=true`.

## 🚀 Funcionalidades

- Autenticação com JWT (`/register`, `/login`)
- Consulta aos dados da Embrapa nas abas:
  - Produção
  - Processamento
  - Comercialização
  - Importação
  - Exportação
- Scraping dinâmico via BeautifulSoup
- Fallback com banco de dados SQLite por ano/subtabela
- Docker com Watchtower (autoupdate contínuo)
- CI/CD com GitHub Actions + DockerHub
- Documentação Swagger automática

## 🔒 Segurança

- O acesso ao servidor está protegido por um **proxy reverso** usando [Zero Trust](https://www.cloudflare.com/pt-br/learning/security/glossary/what-is-zero-trust/) da [Cloudflare](https://www.cloudflare.com/pt-br/), impedindo que o IP do host seja identificado e evitando ataques como [DDoS](https://www.cloudflare.com/pt-br/ddos/).

## 📁 Estrutura Completa do Projeto

```bash
tech_challenge_01/
├── .github/
│   └── workflows/
│       └── upload-docker-image.yml         
│
├── docker/
│   ├── Dockerfile                          
│   ├── docker-compose.yml                  
│   └── README.md                           
│
├── tech_challenge/
│   ├── data/                               
│   │
│   ├── src/
│   │   └── tech_challenge/
│   │       ├── routes/                     
│   │       │   ├── comercializacao.py
│   │       │   ├── exportacao.py
│   │       │   ├── importacao.py     
│   │       │   ├── login.py     
│   │       │   ├── processamento.py     
│   │       │   ├── producao.py
│   │       │   └── register.py  
│   │       │
│   │       ├── schemas/                    
│   │       │   ├── api_schemas.py
│   │       │   ├── db_schemas.py
│   │       │   └── sub_tables.py
│   │       │
│   │       ├── services/
│   │       │   ├── auth.py
│   │       │   ├── db.py
│   │       │   └── scraper.py
│   │       │
│   │       ├── utils/
│   │       │   ├── common.py
│   │       │   ├── db.py
│   │       │   └── scraper.py
│   │       │
│   │       ├── main.py                     
│   │       └── db_bases.py
│   │
│   └── tests/ 
│       └── test_main.py
│
└── requirements.txt
```
### 🗂️ Explicação da Estrutura do Projeto

- **`.github/workflows/`**: Contém o workflow do GitHub Actions para CI/CD.
- **`docker/`**: Estrutura de containerização (imagem, compose, instruções).
- **`tech_challenge/data/`**: Banco local SQLite com fallback de scraping.
- **`src/tech_challenge/routes/`**: Define os endpoints da API por funcionalidade.
- **`src/tech_challenge/schemas/`**: Modelos de entrada/saída (`Pydantic`) e tabelas (`SQLAlchemy`).
- **`src/tech_challenge/services/`**: Implementações de scraping, autenticação e acesso ao banco.
- **`src/tech_challenge/utils/`**: Funções utilitárias para parsing, validação e manipulação de dados.
- **`src/tech_challenge/main.py`**: Ponto de entrada da aplicação FastAPI.
- **`src/tech_challenge/db_bases.py`**: Declara as bases do SQLAlchemy para uso em modelos ORM.
- **`tests/`**: Local para adicionar testes unitários e de integração com `pytest`.
- **`requirements.txt`**: Lista com as dependências do projeto (FastAPI, JWT, BS4, etc).

## 📖 Documentação da API

A documentação da API é gerada automaticamente com Swagger e está disponível em [http://localhost:8000/docs](http://localhost:8000/docs).

## 🔐 Autenticação

| Método | Caminho     | Descrição                   |
|--------|-------------|-----------------------------|
| POST   | `/register` | Cadastro de novo usuário     |
| POST   | `/login`    | Autenticação de usuário      |

> Após o login, utilize o token JWT como Bearer Token para acessar os endpoints protegidos.

### 📊 Endpoints de Dados

| Método | Caminho              | Descrição                                    | Autenticação |
|--------|----------------------|----------------------------------------------|--------------|
| GET    | `/producao`          | Produção de uvas e vinhos no Brasil          | ✅           |
| GET    | `/processamento`     | Processamento de uva                         | ✅           |
| GET    | `/comercializacao`   | Comercialização de produtos vitivinícolas    | ✅           |
| GET    | `/importacao`        | Importações de vinhos e derivados            | ✅           |
| GET    | `/exportacao`        | Exportações do setor vitivinícola            | ✅           |

### 📃 Informações Gerais

| Método | Caminho | Descrição                   |
|--------|---------|-----------------------------|
| GET    | `/`     | Informações básicas da API  |

> ℹ️ Todos os endpoints de dados aceitam o parâmetro opcional `?force=true` para forçar uma nova coleta diretamente do site da Embrapa (ignorando o cache local).

## 🧪 Execução local (sem Docker)

### 🔹 Linux / macOS

1. Clone o projeto:
   ```bash
   git clone https://github.com/ML-Group-37/tech_challenge_01.git
   cd tech_challenge_01

2. Crie e ative o ambiente virtual:
   ```bash
    python -m venv venv
    source venv/bin/activate

3. Instale as dependências:
   ```bash
    pip install -r requirements.txt

4. Execute o servidor local:
   ```bash
    export PYTHONPATH=tech_challenge/src && uvicorn tech_challenge.main:app --reload

5. Acesse a documentação interativa (Swagger):
   ```bash
    http://127.0.0.1:8000/docs

### 🔹 Windows (CMD ou PowerShell)

1. Clone o projeto:
   ```bash
   git clone https://github.com/ML-Group-37/tech_challenge_01.git
   cd tech_challenge_01

2. Crie e ative o ambiente virtual:
   ```bash
    python -m venv venv
    .\venv\Scripts\activate

3. Instale as dependências:
   ```bash
    pip install -r requirements.txt

4. Execute o servidor local:
   ```bash
    $env:PYTHONPATH="tech_challenge/src"; uvicorn tech_challenge.main:app --reload

5. Acesse a documentação interativa (Swagger):
   ```bash
    http://127.0.0.1:8000/docs


## ✅ Testes Automatizados

Este projeto utiliza **pytest** e **pytest-html** para garantir a qualidade dos endpoints da API.

Os testes cobrem:

- ✅ Cadastro e login de usuários
- ✅ Autenticação JWT e acesso autorizado aos endpoints
- ✅ Validação da resposta dos endpoints (`/producao`, `/processamento`, `/comercializacao`, `/importacao`, `/exportacao`)
- ✅ Verificação de status HTTP e formato dos dados (listas JSON)


### ⚙️ Requisitos para executar os testes

> Para que os testes funcionem corretamente, é necessário que a **API esteja rodando**.

### 📢 Recomendação

Abra **dois terminais**:

- **Terminal 1**: para rodar a API
- **Terminal 2**: para rodar os testes

   ```bash
    pytest tech_challenge/tests/ --html=testes_vitivinicultura.html --self-contained-html

## 🚀 Deploy

- O servidor está usando [Docker](https://www.docker.com/) para criar um container exclusivo para a aplicação.
- [Documentação](/docker/README.md) da configuração usada para o Docker.
- Para realizar um novo deploy, basta rodar a action [Docker Image CI](/.github/workflows/upload-docker-image.yml).
- A API atualizada estará disponível no subdomínio:  
  🔗 https://tc01.rteixeira.org/

## 👥 Autores

Projeto desenvolvido por alunos da Pós Tech em Machine Learning Engineering (FIAP):

- Antônio Victor Mendes Fonseca
- Iury da Rocha Miguel
- Pedro Farnetani de Almeida
- Robson de Paula Teixeira
- Thiago da Rocha Miguel

## 📄 Licença

Este projeto foi desenvolvido exclusivamente para fins educacionais no Tech Challenge da FIAP.
