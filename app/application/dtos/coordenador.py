from dataclasses import dataclass
from uuid import UUID
@dataclass(frozen=True)
class CoordenadorDTO:
    user_id: UUID
    nome: str
    email: str
    bio: str | None = None


CoodenadorDTO = CoordenadorDTO