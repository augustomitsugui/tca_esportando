from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from uuid import UUID

class EsporteCreate(BaseModel):
    nome: str = Field(max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=1024)

class EsporteUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=1024)

class EsporteResponse(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None
    instituicao_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)

class EsporteResumo(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None
    instituicao_id: Optional[UUID] = None

    model_config = {"from_attributes": True}
