from typing import Optional

from pydantic import BaseModel, Field, validator

from tech_challenge.utils.common import parse_quantity


class ProducaoSchema(BaseModel):
    Produto: str
    Quantidade_L: Optional[int] = Field(..., alias="Quantidade (L.)")

    @validator("Quantidade_L", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True
        from_attributes = True


class ProcessamentoSchema(BaseModel):
    Cultivar: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")

    @validator("Quantidade_Kg", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True
        from_attributes = True


class ComercializacaoSchema(BaseModel):
    Produto: str
    Quantidade_L: Optional[int] = Field(..., alias="Quantidade (L.)")

    @validator("Quantidade_L", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True
        from_attributes = True


class ImportacaoSchema(BaseModel):
    Países: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")
    Valor_USD: Optional[int] = Field(..., alias="Valor (US$)")

    @validator("Quantidade_Kg", "Valor_USD", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True
        from_attributes = True


class ExportacaoSchema(BaseModel):
    Países: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")
    Valor_USD: Optional[int] = Field(..., alias="Valor (US$)")

    @validator("Quantidade_Kg", "Valor_USD", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantity(value)

    class Config:
        validate_by_name = True
        from_attributes = True


class RegisterSchema(BaseModel):
    username: str
    password: str
