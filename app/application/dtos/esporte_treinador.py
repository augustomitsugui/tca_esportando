from dataclasses import dataclass

@dataclass(frozen=True)
class EsporteTreinadorDTO:
    id: int
    esporte_id: int
    treinador_id: int