from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
@dataclass
class AtletaEsporteResumo:
    id: UUID
    atleta_id: UUID
    esporte_id: UUID
    
@dataclass(frozen=True)
class AtletaEsporte:
    id: UUID
    atleta_id: UUID
    esporte_id: UUID
    alterado_em: datetime
    criado_em: datetime 