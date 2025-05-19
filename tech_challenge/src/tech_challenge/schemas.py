from pydantic import BaseModel, Field, validator
from typing import Optional

def parse_quantidade(value: str | int | None) -> int | None:
    if isinstance(value, str):
        if value.strip() == "-":
            return None
        return int(value.replace(".", ""))
    return value

class ProducaoSchema(BaseModel):
    Produto: str
    Quantidade_L: Optional[int] = Field(..., alias="Quantidade (L.)")

    @validator("Quantidade_L", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantidade(value)

    class Config:
        allow_population_by_field_name = True 

class ProcessamentoSchema(BaseModel):
    Cultivar: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")

    @validator("Quantidade_Kg", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantidade(value)

    class Config:
        allow_population_by_field_name = True

class ComercializacaoSchema(BaseModel):
    Produto: str
    Quantidade_L: Optional[int] = Field(..., alias="Quantidade (L.)")

    @validator("Quantidade_L", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantidade(value)

    class Config:
        allow_population_by_field_name = True

class ImportacaoSchema(BaseModel):
    Países: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")
    Valor_USD: Optional[int] = Field(..., alias="Valor (US$)") 

    @validator("Quantidade_Kg", "Valor_USD", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantidade(value)

    class Config:
        allow_population_by_field_name = True

class ExportacaoSchema(BaseModel):
    Países: str
    Quantidade_Kg: Optional[int] = Field(..., alias="Quantidade (Kg)")
    Valor_USD: Optional[int] = Field(..., alias="Valor (US$)") 

    @validator("Quantidade_Kg", "Valor_USD", pre=True)
    def validar_quantidade(cls, value):
        return parse_quantidade(value)

    class Config:
        allow_population_by_field_name = True
