from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class LocalInstituicaoDTO:
    local_id: UUID
    instituicao_id: UUID
