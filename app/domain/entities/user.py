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
    hashed_password: str
    is_active: bool
    is_verified: bool
    role: UserRole
