import os
from typing import Optional

import bcrypt
import pandas as pd
from icecream import ic
from pydantic import ValidationError
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from tech_challenge.schemas.api_schemas import (
    ComercializacaoSchema,
    ExportacaoSchema,
    ImportacaoSchema,
    ProcessamentoSchema,
    ProducaoSchema,
)
from tech_challenge.schemas.db_schemas import (
    Comercializacao,
    Exportacao,
    Importacao,
    Processamento,
    Producao,
)
from tech_challenge.services.db import DATA_DIR, SessionLocal

table_mapping = {
    "producao": (Producao, ProducaoSchema),
    "processamento": (Processamento, ProcessamentoSchema),
    "comercializacao": (Comercializacao, ComercializacaoSchema),
    "importacao": (Importacao, ImportacaoSchema),
    "exportacao": (Exportacao, ExportacaoSchema),
}


def hash_password(password: str) -> str:
    """
    Gera o hash de uma senha utilizando o algoritmo bcrypt.

    Args:
        password (str): A senha em texto plano que será convertida em hash.

    Returns:
        str: A senha convertida em um hash seguro.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Args:
        plain_password (str): A senha em texto plano fornecida pelo usuário.
        hashed_password (str): O hash da senha armazenado no banco de dados.

    Returns:
        bool: True se a senha fornecida corresponder ao hash armazenado, False caso contrário.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_db():
    """
    Obtém uma sessão de banco de dados para ser usada em operações.

    Esta função é um gerador que cria uma sessão de banco de dados usando
    o `SessionLocal` e garante que a sessão seja fechada após o uso.

    Yields:
        sqlalchemy.orm.Session: Sessão de banco de dados para ser usada em operações.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_table_name(
    table: str, sub_table: Optional[str] = None, year: Optional[int] = None
) -> str:
    """
    Gera o nome do arquivo ou tabela baseado nos parâmetros de tabela, sub-tabela e ano.

    Args:
        table (str): Nome da tabela principal.
        sub_table (Optional[str], opcional): Nome da sub-tabela. Padrão é None.
        year (Optional[int], opcional): Ano dos dados. Padrão é None.

    Returns:
        str: Nome gerado no formato apropriado, por exemplo:
            - "producao_vinifera_2023"
            - "producao_vinifera"
            - "producao_2023"
            - "producao"
    """

    if sub_table and year:
        return f"{table}_{sub_table}_{year}"
    if sub_table:
        return f"{table}_{sub_table}"
    if year:
        return f"{table}_{year}"

    return table


def get_database_path(table: str, year: int = None, sub_table: str = None) -> str:
    """
    Retorna o caminho completo para o arquivo de banco de dados de uma seção específica e ano.

    Args:
        table (str): Nome da seção (ex: "producao", "processamento").
        year (int, opcional): Ano para o qual o banco de dados será criado.
        sub_table (str, opcional): Nome da sub-tabela. Padrão é None.

    Returns:
        str: Caminho completo para o arquivo de banco de dados.
    """
    section_dir = os.path.join(DATA_DIR, table)
    os.makedirs(section_dir, exist_ok=True)
    table_name = generate_table_name(table=table, sub_table=sub_table, year=year)
    return os.path.join(section_dir, f"{table_name}.db")


def get_engine(table: str, year: int = None, sub_table: str = None):
    """
    Retorna um engine SQLAlchemy para o banco de dados de uma seção específica e ano.

    Args:
        table (str): Nome da tabela principal (ex: "producao", "processamento").
        year (int, opcional): Ano para o qual o banco de dados será criado. Padrão é None.
        sub_table (str, opcional): Nome da sub-tabela. Padrão é None.

    Returns:
        sqlalchemy.Engine: Engine SQLAlchemy conectado ao banco de dados especificado.
    """
    db_path = get_database_path(table=table, year=year, sub_table=sub_table)
    return create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )


def create_table(table: str, year: int = None, sub_table: str = None):
    """
    Cria a tabela correspondente no banco de dados específico para a seção e ano.

    Args:
        table (str): Nome da tabela principal (ex: "producao", "processamento").
        year (int, opcional): Ano para o qual a tabela será criada. Padrão é None.
        sub_table (str, opcional): Nome da sub-tabela. Padrão é None.

    Raises:
        ValueError: Se o modelo correspondente à tabela não for encontrado.

    Returns:
        None
    """
    engine = get_engine(table, year, sub_table)

    model, _ = table_mapping.get(table, (None, None))
    if not model:
        raise ValueError(f"Modelo para a tabela '{table}' não encontrado.")

    inspector = inspect(engine)
    if not inspector.has_table(model.__tablename__):
        model.__table__.create(bind=engine)


def save_data_in_db(
    df: pd.DataFrame, table: str, year: int = None, sub_table: str = None
):
    """
    Salva os dados de um DataFrame em uma tabela dinâmica no banco de dados.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem salvos.
        table (str): Nome da tabela principal (ex: "producao", "processamento").
        year (int, opcional): Ano para o qual os dados serão salvos.
        sub_table (str, opcional): Nome da sub-tabela. Padrão é None.

    Returns:
        None
    """
    engine = get_engine(table, year, sub_table)
    create_table(table, year, sub_table)  # Garante que a tabela exista
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        model, schema = table_mapping.get(table, (None, None))
        if not model or not schema:
            raise ValueError(
                f"Modelo ou schema para a tabela '{table}' não encontrado."
            )

        validated_records = []
        for record in df.to_dict(orient="records"):
            try:
                validated_record = schema(**record).dict(by_alias=False)
                validated_records.append(validated_record)
            except ValidationError as e:
                ic(f"Erro de validação: {e}")

        for record in validated_records:
            session.add(model(**record))
        session.commit()
    finally:
        session.close()


def load_data_from_db(
    table: str, year: int = None, sub_table: str = None
) -> pd.DataFrame:
    """
    Carrega os dados de uma tabela dinâmica no banco de dados e retorna como DataFrame.

    Args:
        table (str): Nome da tabela principal (ex: "producao", "processamento").
        year (int, opcional): Ano da tabela a ser carregada.
        sub_table (str, opcional): Nome da sub-tabela. Padrão é None.

    Returns:
        pd.DataFrame: DataFrame contendo os dados da tabela.

    Raises:
        ValueError: Se o modelo ou schema correspondente à tabela não for encontrado.
    """
    engine = get_engine(table, year, sub_table)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        model, schema = table_mapping.get(table, (None, None))
        if not model or not schema:
            raise ValueError(
                f"Modelo ou schema para a tabela '{table}' não encontrado."
            )

        result = session.query(model).all()

        records = [schema.from_orm(row).dict(by_alias=True) for row in result]
        return pd.DataFrame(records)
    finally:
        session.close()
