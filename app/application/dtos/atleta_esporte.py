from dataclasses import dataclass

@dataclass(frozen=True)
class AtletaEsporteDTO:
    id: int
    atleta_id: int
    esporte_id: int