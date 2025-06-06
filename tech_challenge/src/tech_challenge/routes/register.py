from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from tech_challenge.schemas.api_schemas import RegisterSchema
from tech_challenge.schemas.db_schemas import User
from tech_challenge.utils.db import get_db, hash_password

router = APIRouter()


@router.post("/register", summary="Cadastro de novo usuário", tags=["Autenticação"])
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    """
    Registra um novo usuário no sistema.
    Args:
        user (RegisterSchema): Dados de registro contendo nome de usuário e senha.
        db (Session, opcional): Dependência da sessão do banco de dados SQLAlchemy.
    Raises:
        HTTPException: Se um usuário com o nome de usuário informado já existir (código de status 400).
    Returns:
        dict: Mensagem indicando o sucesso no cadastro do usuário.
    """

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    hashed_password = hash_password(user.password)

    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário cadastrado com sucesso"}
