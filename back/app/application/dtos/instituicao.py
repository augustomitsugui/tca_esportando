from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class InstituicaoDTO:
    nome: str
    criado_por_user_id: Optional[UUID] = None
    descricao: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
