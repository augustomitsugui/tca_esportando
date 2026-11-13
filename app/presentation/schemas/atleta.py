from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class AtletaCreate(BaseModel):
    nome: str
    email: EmailStr
    ano: int
    bio: Optional[str] = None


class AtletaUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    ano: Optional[int] = None
    bio: Optional[str] = None


class AtletaResponse(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    ano: int
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AtletaResumo(BaseModel):
    id: UUID
    nome: str
    ano: int

    model_config = ConfigDict(from_attributes=True)
