from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InstituicaoDTO:
    nome: str
    descricao: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
