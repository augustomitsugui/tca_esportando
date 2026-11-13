from pydantic import BaseModel, ConfigDict
from typing import Optional

from uuid import UUID

class EsporteCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None

class EsporteUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class EsporteResponse(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class EsporteResumo(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None

    model_config = {"from_attributes": True}
