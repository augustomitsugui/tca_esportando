from datetime import datetime
from typing import Optional
from uuid import UUID


from pydantic import BaseModel


class TreinoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    data_hora: datetime
    treinador_id: UUID
    local_id: UUID
    esporte_id: UUID


class TreinoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    data_hora: Optional[datetime] = None
    treinador_id: Optional[UUID] = None
    local_id: Optional[UUID] = None
    esporte_id: Optional[UUID] = None


class TreinoResponse(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None
    data_hora: datetime
    treinador_id: UUID
    local_id: UUID
    esporte_id: UUID

    model_config = {"from_attributes": True}


class TreinoResumo(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str] = None


class TreinoAgendaResponse(BaseModel):
    treino_id: UUID
    treino_nome: str
    esporte_nome: str
    data_hora: datetime
    treinador_nome: str
    local_nome: str

    model_config = {"from_attributes": True}