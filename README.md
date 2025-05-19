# Tech Challenge 01

## 📊 API Vitivinicultura Embrapa

Esta API fornece acesso público aos dados de vitivinicultura brasileira, extraídos diretamente do site da Embrapa. Os dados abrangem produção, processamento, comercialização, importação e exportação de uvas, vinhos e derivados.

Todos os endpoints contam com suporte a **fallback inteligente**, permitindo o uso de backups locais (`.csv`) quando o site da Embrapa estiver fora do ar. Também é possível forçar uma nova coleta diretamente da web com o parâmetro `force=true`.

---

## 🚀 Deploy

- O servidor está usando [Docker](https://www.docker.com/) para criar um container exclusivo para a aplicação.
- [Documentação](/docker/README.md) da configuração usada para o Docker.
- Para realizar um novo deploy, basta rodar a action [Docker Image CI](/.github/workflows/upload-docker-image.yml).
- A API atualizada estará disponível no subdomínio:  
  🔗 https://tc01.rteixeira.org/

---

## 🔒 Segurança

- O acesso ao servidor está protegido por um **proxy reverso** usando [Zero Trust](https://www.cloudflare.com/pt-br/learning/security/glossary/what-is-zero-trust/) da [Cloudflare](https://www.cloudflare.com/pt-br/), impedindo que o IP do host seja identificado e evitando ataques como [DDoS](https://www.cloudflare.com/pt-br/ddos/).

---

## 📂 Endpoints disponíveis

| Método | Caminho              | Descrição                                    |
|--------|----------------------|----------------------------------------------|
| GET    | `/`                  | Informações sobre a API                      |
| GET    | `/producao`          | Produção de uvas e vinhos no Brasil          |
| GET    | `/processamento`     | Processamento de uva                         |
| GET    | `/comercializacao`   | Comercialização de produtos vitivinícolas    |
| GET    | `/importacao`        | Importações de vinhos e derivados            |
| GET    | `/exportacao`        | Exportações do setor vitivinícola            |

> Todos os endpoints aceitam `?force=true` para forçar scraping direto da fonte.

---

## 🧪 Execução local (sem Docker)

1. Clone o projeto:
   ```bash
   git clone https://github.com/ML-Group-37/tech_challenge_01.git
   cd tech_challenge_01

2. Crie e ative o ambiente virtual:
   ```bash
    python -m venv venv
    .\venv\Scripts\activate   # Windows
    source venv/bin/activate # Linux/macOS

3. Instale as dependências:
   ```bash
    pip install -r requirements.txt

4. Rode o servidor local:
   ```bash
    $env:PYTHONPATH="tech_challenge/src"; uvicorn tech_challenge.main:app --reload

5. Acesse a documentação interativa (Swagger):
   ```bash
    http://127.0.0.1:8000/docs
