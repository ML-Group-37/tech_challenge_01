from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from icecream import ic

from tech_challenge import scraper
from tech_challenge.schemas import ComercializacaoSchema

router = APIRouter()


@router.get(
    "/comercializacao",
    response_model=List[ComercializacaoSchema],
    summary="Dados de comercialização",
    description="Retorna os dados da aba Comercialização da Embrapa. "
    "Utiliza fallback para CSV local em caso de falha.",
    tags=["Dados"],
)
def get_comercializacao(
    year: Optional[int] = None,
):
    try:
        if year and (year < 1970 or year > 2024):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year must be between 1970 and 2024.",
            )

        df = scraper.get_comercializacao_data(year)
        ic("Dados de Comercialização carregados com sucesso.")
        return [ComercializacaoSchema(**row) for row in df.to_dict(orient="records")]
    except RuntimeError as e:
        ic(f"Erro em /comercializacao: {e}")
        raise HTTPException(status_code=503, detail=str(e))
