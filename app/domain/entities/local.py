from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from datetime import datetime

@dataclass
class LocalResumo:
    id: int
    nome: str
    descricao: Optional[str] = None 

@dataclass(frozen=True)
class Local:
    id: int
    nome: str
    descricao: Optional[str] = None
    alterado_em: datetime
    criado_em: datetime
    
    