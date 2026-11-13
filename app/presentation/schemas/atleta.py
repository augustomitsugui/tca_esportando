from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AtletaCreate(BaseModel):
    nome: str = Field(max_length=100)
    email: EmailStr
    ano: int
    bio: Optional[str] = Field(default=None, max_length=1024)


class AtletaUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = None
    ano: Optional[int] = None
    bio: Optional[str] = Field(default=None, max_length=1024)


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
