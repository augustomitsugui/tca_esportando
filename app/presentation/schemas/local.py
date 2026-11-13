from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class LocalCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None

class LocalUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

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