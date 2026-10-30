from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class AtletaResumo:
    id: int
    nome: str
    ano: int
    bio: Optional[str] = None

@dataclass(frozen=True)
class Atleta:
    id: int
    nome: str
    ano: int
    bio: Optional[str] = None
    treinador_id: int
    alterado_em: datetime
    criado_em: datetime
