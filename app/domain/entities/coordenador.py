from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class CoordenadorResumo:
    id: int
    nome: str
    email: str
    bio: Optional[str] = None

@dataclass(frozen=True)
class Coordenador:
    id: int
    nome: str
    email: str
    bio: Optional[str] = None
    alterado_em: datetime
    criado_em: datetime