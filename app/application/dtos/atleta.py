from dataclasses import dataclass
from uuid import UUID
@dataclass(frozen=True)
class AtletaDTO:
    user_id: UUID
    nome: str
    email: str
    ano: int
    bio: str | None = None
