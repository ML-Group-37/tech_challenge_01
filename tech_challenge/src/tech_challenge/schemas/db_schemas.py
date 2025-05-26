from sqlalchemy import Column, Float, Integer, String

from tech_challenge.db_bases import DynamicBase, UserBase


class User(UserBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Producao(DynamicBase):
    __tablename__ = "producao"

    id = Column(Integer, primary_key=True, index=True)
    Produto = Column(String, nullable=False)
    Quantidade_L = Column(Integer, nullable=True)


class Processamento(DynamicBase):
    __tablename__ = "processamento"

    id = Column(Integer, primary_key=True, index=True)
    Cultivar = Column(String, nullable=False)
    Quantidade_Kg = Column(Integer, nullable=True)


class Comercializacao(DynamicBase):
    __tablename__ = "comercializacao"

    id = Column(Integer, primary_key=True, index=True)
    Produto = Column(String, nullable=False)
    Quantidade_L = Column(Integer, nullable=True)


class Importacao(DynamicBase):
    __tablename__ = "importacao"

    id = Column(Integer, primary_key=True, index=True)
    Países = Column(String, nullable=False)
    Quantidade_Kg = Column(Float, nullable=True)
    Valor_USD = Column(Integer, nullable=True)


class Exportacao(DynamicBase):
    __tablename__ = "exportacao"

    id = Column(Integer, primary_key=True, index=True)
    Países = Column(String, nullable=False)
    Quantidade_Kg = Column(Float, nullable=True)
    Valor_USD = Column(Integer, nullable=True)
