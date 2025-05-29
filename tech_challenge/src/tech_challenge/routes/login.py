from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from tech_challenge.schemas.api_schemas import RegisterSchema
from tech_challenge.schemas.db_schemas import User
from tech_challenge.services.auth import create_access_token
from tech_challenge.utils.db import get_db, verify_password

router = APIRouter()


@router.post("/login", summary="Autenticação de usuário", tags=["Autenticação"])
def login(credentials: RegisterSchema, db: Session = Depends(get_db)):
    """
    Autentica um usuário com as credenciais fornecidas e retorna um token JWT se for bem-sucedido.
    Args:
        credentials (RegisterSchema): Credenciais de login do usuário (username e senha).
        db (Session, opcional): Sessão do banco de dados SQLAlchemy.
    Returns:
        dict: Um dicionário contendo o token de acesso e o tipo de token.
    Raises:
        HTTPException: Se o usuário não existir ou a senha estiver incorreta, retorna erro 401 Unauthorized.
    """

    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    access_token = create_access_token(data={"sub": credentials.username})
    return {"access_token": access_token, "token_type": "bearer"}
