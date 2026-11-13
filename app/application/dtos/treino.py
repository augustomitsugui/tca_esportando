from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

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
    nome: str | None = None
    data_hora: datetime | None = None
    treinador_id: UUID | None = None
    local_id: UUID | None = None
    esporte_id: UUID | None = None
    descricao: str | None = None


TreinoDTO = TreinoCreateDTO