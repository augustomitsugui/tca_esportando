import enum
from dataclasses import dataclass
from uuid import UUID


class UserRole(str, enum.Enum):
    SUPERADMIN = "superadmin"
    COORDENADOR = "coordenador"
    TREINADOR = "treinador"
    ATLETA = "atleta"

@dataclass
class UserIdentity:
    id: UUID
    email: str
    hashed_password: str
    is_active: bool
    is_verified: bool
    role: UserRole
