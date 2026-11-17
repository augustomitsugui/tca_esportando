from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from uuid import UUID

@dataclass
class AtletaResumo:
    id: UUID
    user_id: UUID
    nome: str
    email: str
    ano: int
    bio: Optional[str] = None


@dataclass(frozen=True)
class Atleta:
    id: UUID
    user_id: UUID
    nome: str
    email: str
    ano: int
    alterado_em: datetime
    criado_em: datetime
    bio: Optional[str] = None
