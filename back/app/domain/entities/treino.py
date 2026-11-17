from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class Treino:
    id: UUID
    nome: str
    data_hora: datetime
    treinador_id: UUID
    local_id: UUID
    esporte_id: UUID
    criado_em: datetime
    alterado_em: datetime
    descricao: str | None = None


@dataclass(frozen=True)
class TreinoAgenda:
    treino_id: UUID
    treino_nome: str
    esporte_nome: str
    data_hora: datetime
    treinador_nome: str
    local_nome: str
    