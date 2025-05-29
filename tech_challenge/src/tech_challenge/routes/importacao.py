from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from icecream import ic

from tech_challenge.schemas.api_schemas import ImportacaoSchema
from tech_challenge.schemas.sub_tables import ImportacaoSubTables
from tech_challenge.services import scraper
from tech_challenge.services.auth import verify_token

router = APIRouter()
security = HTTPBearer()


@router.get(
    "/importacao",
    response_model=List[ImportacaoSchema],
    summary="Dados de importação",
    description="Retorna os dados da aba Importação da Embrapa. "
    "Utiliza fallback para CSV local em caso de falha.",
    tags=["Dados"],
)
def get_importacao(sub_table: Optional[ImportacaoSubTables], year: Optional[int] = None, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Busca dados de importação para uma sub-tabela e ano especificados, após verificar as credenciais do usuário.
    Args:
        sub_table (Optional[ImportacaoSubTables]): Sub-tabela da qual buscar os dados de importação. Deve ser um membro válido de ImportacaoSubTables.
        year (Optional[int], opcional): Ano para o qual buscar os dados. Deve estar entre 1970 e 2024, inclusive. Padrão é None.
        credentials (HTTPAuthorizationCredentials): Credenciais HTTP de autorização, fornecidas automaticamente por injeção de dependência.
    Raises:
        HTTPException: Se o ano estiver fora do intervalo válido.
        HTTPException: Se o nome da sub-tabela for inválido.
        HTTPException: Se ocorrer um erro de execução durante a obtenção dos dados.
    Returns:
        List[ImportacaoSchema]: Lista de registros de dados de importação, cada um representado como um objeto ImportacaoSchema.
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
        if sub_table and sub_table not in ImportacaoSubTables:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sub-table name.",
            )

        df = scraper.get_importacao_data(sub_table.value, year)
        ic("Dados de Importação carregados com sucesso.")
        return [ImportacaoSchema(**row) for row in df.to_dict(orient="records")]
    except RuntimeError as e:
        ic(f"Erro em /importacao: {e}")
        raise HTTPException(status_code=503, detail=str(e))
