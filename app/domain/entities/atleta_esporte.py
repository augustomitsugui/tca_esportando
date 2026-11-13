from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum


class AtletaEsporteStatus(str, Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
@dataclass
class AtletaEsporteResumo:
    id: UUID
    atleta_id: UUID
    esporte_id: UUID
    status: AtletaEsporteStatus
    atleta_nome: str | None = None
    esporte_nome: str | None = None
    
@dataclass(frozen=True)
class AtletaEsporte:
    id: UUID
    atleta_id: UUID
    esporte_id: UUID
    status: AtletaEsporteStatus
    criado_em: datetime
    alterado_em: datetime
    atleta_nome: str | None = None
    esporte_nome: str | None = None