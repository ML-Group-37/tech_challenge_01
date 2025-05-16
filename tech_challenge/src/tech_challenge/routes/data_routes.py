from fastapi import APIRouter, HTTPException
from typing import List, Type
from pydantic import BaseModel
from icecream import ic

from tech_challenge.services.data_service import get_dados_aba
from tech_challenge.schemas import (
    ProducaoSchema,
    ProcessamentoSchema,
    ComercializacaoSchema,
    ImportacaoSchema,
    ExportacaoSchema,
)

router = APIRouter()

def gerar_endpoint(nome: str, schema: Type[BaseModel]):
    """
    Cria dinamicamente um endpoint GET para retornar os dados de uma aba com tipagem correta.

    Args:
        nome (str): Nome da aba e do endpoint.
        schema (BaseModel): Modelo Pydantic correspondente à aba.
    """
    @router.get(
        f"/{nome}",
        response_model=List[schema],
        summary=f"Dados de {nome.capitalize()}",
        description=f"Retorna os dados da aba {nome.capitalize()} da Embrapa. "
                    "Utiliza fallback para CSV local em caso de falha.",
        tags=["Dados"]
    )
    def endpoint():
        try:
            df = get_dados_aba(nome)
            ic(f"Dados de {nome} carregados com sucesso.")
            return df.to_dict(orient="records")
        except RuntimeError as e:
            ic(f"Erro em /{nome}: {e}")
            raise HTTPException(status_code=503, detail=str(e))

    return endpoint


# Geração dos endpoints com schemas específicos
gerar_endpoint("producao", ProducaoSchema)
gerar_endpoint("processamento", ProcessamentoSchema)
gerar_endpoint("comercializacao", ComercializacaoSchema)
gerar_endpoint("importacao", ImportacaoSchema)
gerar_endpoint("exportacao", ExportacaoSchema)
