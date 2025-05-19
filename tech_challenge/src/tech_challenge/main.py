from datetime import datetime

from fastapi import FastAPI
from icecream import ic

from tech_challenge.routes.comercializacao import router as comercializacao_router
from tech_challenge.routes.exportacao import router as exportacao_router
from tech_challenge.routes.importacao import router as importacao_router
from tech_challenge.routes.processamento import router as processamento_router
from tech_challenge.routes.producao import router as producao_router

app = FastAPI(
    title="API Vitivinicultura Embrapa",
    description="Fornece acesso público aos dados de vitivinicultura da Embrapa.",
    version="1.0.0",
)

# Registro das rotas
app.include_router(producao_router)
app.include_router(processamento_router)
app.include_router(comercializacao_router)
app.include_router(importacao_router)
app.include_router(exportacao_router)

ic("✅ API Vitivinicultura Embrapa está no ar!")


@app.get("/")
def read_root():
    """
    Endpoint raiz da API - fornece informações básicas do serviço.
    """
    return {
        "nome": "API de Vitivinicultura - Embrapa",
        "descricao": "Esta API fornece acesso estruturado aos dados públicos da vitivinicultura brasileira, extraídos do site da Embrapa.",
        "status": "Online",
        "documentacao": "http://127.0.0.1:8000/docs",
        "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "endpoints_disponiveis": {
            "/producao": "Produção de uvas e vinhos no Brasil",
            "/processamento": "Dados de processamento de uva",
            "/comercializacao": "Comercialização de produtos vitivinícolas",
            "/importacao": "Importações de vinhos e derivados",
            "/exportacao": "Exportações do setor vitivinícola",
        },
        "github_repo": "https://github.com/ML-Group-37/tech_challenge_01",
        "mantenedores": ["Antônio", "Iury", "Pedro", "Robson", "Thiago"],
    }
