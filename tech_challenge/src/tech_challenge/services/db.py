import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from tech_challenge.db_bases import UserBase
from tech_challenge.schemas.db_schemas import User

# Garante que a pasta 'data' exista
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../../../data")
os.makedirs(DATA_DIR, exist_ok=True)

metadata = MetaData()

# Caminho fixo para o banco de dados de usuários
USERS_DB_PATH = os.path.join(DATA_DIR, "users.db")

# Engine para o banco de dados de usuários
users_engine = create_engine(
    f"sqlite:///{USERS_DB_PATH}", connect_args={"check_same_thread": False}
)

# Sessão para o banco de dados de usuários
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=users_engine)

# Cria apenas a tabela de usuários no banco de dados `users.db`
UserBase.metadata.create_all(bind=users_engine)
