from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

UNSET = object()

@dataclass(frozen=True)
class TreinoCreateDTO:
    nome: str
    data_hora: datetime
    treinador_id: UUID
    local_id: UUID
    esporte_id: UUID
    descricao: str | None = None


@dataclass(frozen=True)
class TreinoUpdateDTO:
    nome: str | None | object = UNSET
    data_hora: datetime | None | object = UNSET
    treinador_id: UUID | None | object = UNSET
    local_id: UUID | None | object = UNSET
    esporte_id: UUID | None | object = UNSET
    descricao: str | None | object = UNSET


TreinoDTO = TreinoCreateDTO