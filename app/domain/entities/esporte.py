from typing import Optional
from dataclasses import dataclass, field

@dataclass
class EsporteResumo:
    id: int
    nome: str
    descricao: Optional[str] = None
    
@dataclass(frozen=True)
class Esporte:
    id: int
    nome: str
    descricao: Optional[str] = None
    alterado_em: datetime
    criado_em: datetime
    
    ##oaidoaissocorro