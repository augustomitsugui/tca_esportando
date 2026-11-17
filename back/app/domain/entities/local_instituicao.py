from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LocalInstituicaoResumo:
    id: UUID
    local_id: UUID
    instituicao_id: UUID
    
@dataclass(frozen=True)
class LocalInstituicao:
    id: UUID
    local_id: UUID
    instituicao_id: UUID
    alterado_em: datetime
    criado_em: datetime
