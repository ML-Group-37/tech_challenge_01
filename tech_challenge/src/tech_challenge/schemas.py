from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator

from tech_challenge.utils import parse_quantity


class ProducaoSchema(BaseModel):
    Produto: str
    Quantidade_L: Optional[int] = Field(..., alias="Quantidade (L.)")

    @validator("Quantidade_L", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True


class ProcessamentoSchema(BaseModel):
    Cultivar: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")

    @validator("Quantidade_Kg", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True


class ComercializacaoSchema(BaseModel):
    Produto: str
    Quantidade_L: Optional[int] = Field(..., alias="Quantidade (L.)")

    @validator("Quantidade_L", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True


class ImportacaoSchema(BaseModel):
    Países: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")
    Valor_USD: Optional[int] = Field(..., alias="Valor (US$)")

    @validator("Quantidade_Kg", "Valor_USD", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True


class ExportacaoSchema(BaseModel):
    Países: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")
    Valor_USD: Optional[int] = Field(..., alias="Valor (US$)")

    @validator("Quantidade_Kg", "Valor_USD", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True


# --- Enum para sub-tabelas --- #
class ProcessamentoSubTables(str, Enum):
    sub_table1 = "Viníferas"
    sub_table2 = "Americanas e híbridas"
    sub_table3 = "Uvas de mesa"
    sub_table4 = "Sem classificação"


class ImportacaoSubTables(str, Enum):
    sub_table1 = "Vinhos de mesa"
    sub_table2 = "Espumantes"
    sub_table3 = "Uvas frescas"
    sub_table4 = "Uvas passas"
    sub_table5 = "Suco de uva"


class ExportacaoSubTables(str, Enum):
    sub_table1 = "Vinhos de mesa"
    sub_table2 = "Espumantes"
    sub_table3 = "Uvas frescas"
    sub_table4 = "Suco de uva"
