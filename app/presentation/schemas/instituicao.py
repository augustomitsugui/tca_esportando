from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class InstituicaoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class InstituicaoUpdate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class InstituicaoResponse(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = {"from_attributes": True}
