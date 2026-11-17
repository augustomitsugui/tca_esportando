from dataclasses import dataclass
from uuid import UUID
@dataclass(frozen=True)
class localDTO:
    nome: str
    descricao: str | None = None


LocalDTO = localDTO