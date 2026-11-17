from dataclasses import dataclass

from uuid import UUID

@dataclass(frozen=True)
class EsporteTreinadorDTO:
    id: UUID
    esporte_id: UUID
    treinador_id: UUID