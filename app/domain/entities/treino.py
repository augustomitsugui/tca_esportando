from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
    
@dataclass
class TreinoResumo:
    id: int
    nome: str
    descricao: Optional[str] = None
    
@dataclass(frozen=True)
class Treino:
    id: int
    nome: str
    descricao: Optional[str] = None
    alterado_em: datetime
    criado_em: datetime
