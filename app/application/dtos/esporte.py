from dataclasses import dataclass

@dataclass(frozen=True)
class EsporteDTO:
    id: int
    nome: str
    descricao: str | None = None