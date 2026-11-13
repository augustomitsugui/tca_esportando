from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class InstituicaoCreate(BaseModel):
    nome: str = Field(max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=1024)
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class InstituicaoUpdate(BaseModel):
    nome: str = Field(max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=1024)
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class InstituicaoResponse(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = {"from_attributes": True}


class InstituicaoPublicResponse(BaseModel):
    id: UUID
    nome: str

    model_config = {"from_attributes": True}
