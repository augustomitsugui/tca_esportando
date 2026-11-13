from dataclasses import dataclass

from uuid import UUID

@dataclass(frozen=True)
class AtletaEsporteDTO:
    atleta_id: UUID
    esporte_id: UUID