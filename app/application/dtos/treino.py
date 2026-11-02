from dataclasses import dataclass

@dataclass(frozen=True)
class TreinoDTO:
    id: int
    nome: str
    descricao: str | None = None