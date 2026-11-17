from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID
@dataclass
class TreinadorResumo:
    id: UUID
    user_id: UUID
    nome: str
    email: str
    bio: Optional[str] = None

@dataclass(frozen=True)
class Treinador:
    id: UUID
    user_id: UUID
    nome: str
    email: str
    alterado_em: datetime
    criado_em: datetime
    bio: Optional[str] = None
