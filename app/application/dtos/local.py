from dataclasses import dataclass

@dataclass(frozen=True)
class localDTO:
    id: int
    nome: str
    email: str
    descricao: str | None = None