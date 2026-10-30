from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class TreinadorResumo:
    id: int
    nome: str
    email: str
    bio: Optional[str] = None
@dataclass(frozen=True)
class Treinador:
    id: int
    nome: str
    email: str
    bio: Optional[str] = None
    alterado_em: datetime
    criado_em: datetime
