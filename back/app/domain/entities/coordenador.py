from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from uuid import UUID

@dataclass
class CoordenadorResumo:
    id: UUID
    user_id: UUID
    nome: str
    email: str
    bio: Optional[str] = None

@dataclass(frozen=True)
class Coordenador:
    id: UUID
    user_id: UUID
    instituicao_id: UUID | None
    nome: str
    email: str
    alterado_em: datetime
    criado_em: datetime
    bio: Optional[str] = None
