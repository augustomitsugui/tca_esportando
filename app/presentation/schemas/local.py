from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

class LocalCreate(BaseModel):
    nome: str = Field(max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=1024)

class LocalUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=1024)

class LocalResponse(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LocalResumo(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None

    model_config = {"from_attributes": True}