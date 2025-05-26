from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

SECRET_KEY = "ML_GROUP_37_Key"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    """
    Cria um token de acesso JWT com um tempo de expiração definido.

    Args:
        data (dict): Dados a serem codificados no token.
        expires_delta (timedelta, opcional): Tempo de expiração do token.
            O padrão é 30 minutos.

    Returns:
        str: Token JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """
    Verifica a validade de um token JWT.

    Args:
        token (str): Token JWT a ser verificado.

    Returns:
        dict: Dados decodificados do token, se válido.

    Raises:
        HTTPException: Se o token estiver expirado ou for inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
