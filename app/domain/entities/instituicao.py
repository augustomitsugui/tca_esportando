from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class InstituicaoResumo:
    id: UUID
    nome: str
    descricao: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

@dataclass(frozen=True)
class Instituicao:
    id: UUID
    criado_por_user_id: Optional[UUID]
    nome: str
    descricao: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    criado_em: datetime
    alterado_em: datetime
