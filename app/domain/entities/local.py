from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from uuid import UUID
@dataclass
class LocalResumo:
    id: UUID
    nome: str
    descricao: Optional[str] = None 

@dataclass(frozen=True)
class Local:
    id: UUID
    nome: str
    alterado_em: datetime
    criado_em: datetime
    descricao: Optional[str] = None
    
    