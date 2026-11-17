from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
@dataclass
class EsporteTreinadorResumo:
    id: UUID
    esporte_id: UUID
    treinador_id: UUID
    
@dataclass(frozen=True)
class EsporteTreinador:
    id: UUID
    esporte_id: UUID
    treinador_id: UUID
    alterado_em: datetime
    criado_em: datetime