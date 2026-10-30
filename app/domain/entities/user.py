import enum
from dataclasses import dataclass
from uuid import UUID


class UserRole(str, enum.Enum):
    COORDENADOR = "coordenador"
    TREINADOR = "treinador"
    ATLETA = "atleta"


@dataclass(frozen=True)
class UserIdentity:
    id: UUID
    email: str
    role: UserRole
