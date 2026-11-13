from uuid import UUID

from pydantic import BaseModel

class EsporteTreinadorResponse(BaseModel):
    id: UUID
    esporte_id: UUID
    treinador_id: UUID
    
class EsporteTreinadorCreate(BaseModel):
    esporte_id: UUID
    treinador_id: UUID
    
class EsporteTreinadorUpdate(BaseModel):
    esporte_id: UUID
    treinador_id: UUID
    
class EsporteTreinadorResumo(BaseModel):
    id: UUID
    esporte_id: UUID
    treinador_id: UUID