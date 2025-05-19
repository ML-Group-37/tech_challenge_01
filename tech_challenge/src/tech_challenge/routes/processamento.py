from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from icecream import ic

from tech_challenge import scraper
from tech_challenge.schemas import ProcessamentoSchema, ProcessamentoSubTables

router = APIRouter()


@router.get(
    "/processamento",
    response_model=List[ProcessamentoSchema],
    summary="Dados de processamento",
    description="Retorna os dados da aba Processamento da Embrapa. "
    "Utiliza fallback para CSV local em caso de falha.",
    tags=["Dados"],
)
def get_processamento(
    sub_table: Optional[ProcessamentoSubTables],
    year: Optional[int] = None,
):
    try:
        if year and (year < 1970 or year > 2024):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year must be between 1970 and 2024.",
            )

        # Verifica se a sub-tabela é válida
        if sub_table and sub_table not in ProcessamentoSubTables:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sub-table name.",
            )

        df = scraper.get_processamento_data(sub_table.value, year)
        ic("Dados de Processamento carregados com sucesso.")
        return [ProcessamentoSchema(**row) for row in df.to_dict(orient="records")]
    except RuntimeError as e:
        ic(f"Erro em /processamento: {e}")
        raise HTTPException(status_code=503, detail=str(e))
