from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from uuid import UUID

class CoordenadorResponse(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
class CoordenadorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    
class CoordenadroResumo(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    
class CoordenadorCreate(BaseModel):
    nome: str
    email: EmailStr
    bio: Optional[str] = None