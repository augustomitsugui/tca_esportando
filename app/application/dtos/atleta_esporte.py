from dataclasses import dataclass

from uuid import UUID

@dataclass(frozen=True)
class AtletaEsporteDTO:
    id: UUID
    atleta_id: UUID
    esporte_id: UUID