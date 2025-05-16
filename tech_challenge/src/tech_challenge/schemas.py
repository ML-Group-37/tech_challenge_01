from pydantic import BaseModel
from typing import Optional

class ProducaoSchema(BaseModel):
    Ano: int
    Região: str
    Uva: str
    Quantidade_kg: Optional[float]

    class Config:
        orm_mode = True

class ProcessamentoSchema(BaseModel):
    Ano: int
    Tipo_Uva: str
    Volume_Litros: Optional[float]

    class Config:
        orm_mode = True

class ComercializacaoSchema(BaseModel):
    Ano: int
    Produto: str
    Quantidade: Optional[float]
    Unidade: Optional[str]

    class Config:
        orm_mode = True

class ImportacaoSchema(BaseModel):
    Ano: int
    País_Origem: str
    Produto: str
    Quantidade_Litros: Optional[float]
    Valor_USD: Optional[float]

    class Config:
        orm_mode = True

class ExportacaoSchema(BaseModel):
    Ano: int
    País_Destino: str
    Produto: str
    Quantidade_Litros: Optional[float]
    Valor_USD: Optional[float]

    class Config:
        orm_mode = True
