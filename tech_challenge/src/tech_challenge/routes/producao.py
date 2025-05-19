from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from icecream import ic

from tech_challenge import scraper
from tech_challenge.schemas import ProducaoSchema

router = APIRouter()


@router.get(
    "/producao",
    response_model=List[ProducaoSchema],
    summary="Dados de produção",
    description="Retorna os dados da aba Produção da Embrapa. "
    "Utiliza fallback para CSV local em caso de falha.",
    tags=["Dados"],
)
def get_producao(
    year: Optional[int] = None,
):
    try:
        if year and (year < 1970 or year > 2024):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year must be between 1970 and 2024.",
            )

        df = scraper.get_producao_data(year)
        ic("Dados de Produção carregados com sucesso.")
        return [ProducaoSchema(**row) for row in df.to_dict(orient="records")]
    except RuntimeError as e:
        ic(f"Erro em /producao: {e}")
        raise HTTPException(status_code=503, detail=str(e))
