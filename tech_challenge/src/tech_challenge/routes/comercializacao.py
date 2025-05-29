from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from icecream import ic

from tech_challenge.schemas.api_schemas import ComercializacaoSchema
from tech_challenge.services import scraper
from tech_challenge.services.auth import verify_token

router = APIRouter()
security = HTTPBearer()


@router.get(
    "/comercializacao",
    response_model=List[ComercializacaoSchema],
    summary="Dados de comercialização",
    description="Retorna os dados da aba Comercialização da Embrapa. "
    "Utiliza fallback para db local em caso de falha.",
    tags=["Dados"],
)
def get_comercializacao(year: Optional[int] = None, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Recupera dados de comercialização para um determinado ano.
    Args:
        year (Optional[int], opcional): Ano para o qual os dados de comercialização serão recuperados. Deve estar entre 1970 e 2024. Padrão é None.
        credentials (HTTPAuthorizationCredentials): Credenciais do token Bearer para autenticação, fornecidas automaticamente por injeção de dependência.
    Raises:
        HTTPException: Se o ano não estiver no intervalo válido (1970-2024), retorna 400 Bad Request.
        HTTPException: Se ocorrer um erro de execução durante a recuperação dos dados, retorna 503 Service Unavailable.
    Returns:
        List[ComercializacaoSchema]: Lista de entradas de dados de comercialização para o ano especificado.
    """

    token = credentials.credentials
    verify_token(token)

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
