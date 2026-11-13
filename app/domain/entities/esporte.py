from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

@dataclass
class EsporteResumo:
    id: UUID
    user_id: UUID
    nome: str
    descricao: Optional[str] = None

@dataclass(frozen=True)
class Esporte:
    id: UUID
    nome: str
    alterado_em: datetime
    criado_em: datetime
    user_id: Optional[UUID] = None
    descricao: Optional[str] = None
