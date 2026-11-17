from dataclasses import dataclass

from uuid import UUID

@dataclass(frozen=True)
class EsporteDTO:
    nome: str
    descricao: str | None = None