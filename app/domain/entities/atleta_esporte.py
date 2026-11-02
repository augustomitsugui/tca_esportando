from dataclasses import dataclass
from datetime import datetime

@dataclass
class AtletaEsporteResumo:
    id: int
    atleta_id: int
    esporte_id: int
    
@dataclass(frozen=True)
class AtletaEsporte:
    id: int
    atleta_id: int
    esporte_id: int
    alterado_em: datetime
    criado_em: datetime 