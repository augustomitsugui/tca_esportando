from dataclasses import dataclass
from datetime import datetime

@dataclass
class EsporteTreinadorResumo:
    id: int
    esporte_id: int
    treinador_id: int
    
@dataclass(frozen=True)
class EsporteTreinador:
    id: int
    esporte_id: int
    treinador_id: int
    alterado_em: datetime
    criado_em: datetime