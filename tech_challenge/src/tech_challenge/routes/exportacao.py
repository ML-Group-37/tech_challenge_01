from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from icecream import ic

from tech_challenge.schemas.api_schemas import ExportacaoSchema
from tech_challenge.schemas.sub_tables import ExportacaoSubTables
from tech_challenge.services import scraper
from tech_challenge.services.auth import verify_token

router = APIRouter()
security = HTTPBearer()


@router.get(
    "/exportacao",
    response_model=List[ExportacaoSchema],
    summary="Dados de exportação",
    description="Retorna os dados da aba Exportação da Embrapa. "
    "Utiliza fallback para CSV local em caso de falha.",
    tags=["Dados"],
)
def get_exportacao(sub_table: Optional[ExportacaoSubTables], year: Optional[int] = None, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Recupera dados de exportação para uma sub-tabela e ano especificados.
    Args:
        sub_table (Optional[ExportacaoSubTables]): A sub-tabela da qual obter os dados de exportação. Deve ser um membro válido de ExportacaoSubTables.
        year (Optional[int], optional): O ano para o qual obter os dados de exportação. Deve estar entre 1970 e 2024, inclusive. Padrão é None.
        credentials (HTTPAuthorizationCredentials): As credenciais HTTP de autorização para verificação do token.
    Returns:
        List[ExportacaoSchema]: Uma lista de registros de dados de exportação que correspondem aos critérios especificados.
    Raises:
        HTTPException: Se o ano estiver fora do intervalo permitido, a sub-tabela for inválida ou ocorrer um erro de execução durante a obtenção dos dados.
    """
    token = credentials.credentials
    verify_token(token)

    try:
        if year and (year < 1970 or year > 2024):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year must be between 1970 and 2024.",
            )

        # Verifica se a sub-tabela é válida
        if sub_table and sub_table not in ExportacaoSubTables:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sub-table name.",
            )

        df = scraper.get_exportacao_data(sub_table.value, year)
        ic("Dados de Exportação carregados com sucesso.")
        return [ExportacaoSchema(**row) for row in df.to_dict(orient="records")]
    except RuntimeError as e:
        ic(f"Erro em /exportacao: {e}")
        raise HTTPException(status_code=503, detail=str(e))
