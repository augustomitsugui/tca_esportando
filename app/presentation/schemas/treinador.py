from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TreinadorCreate(BaseModel):
    nome: str
    email: str
    bio: Optional[str] = None
    
class TreinadorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    
class TreinadorResponse(BaseModel):
    id: UUID
    nome: str
    email: str
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
class TreinadorResumo(BaseModel):
    id: UUID
    nome: str
    email: str

    model_config = ConfigDict(from_attributes=True)