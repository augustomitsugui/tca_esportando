import enum
from dataclasses import dataclass
from uuid import UUID


class UserRole(str, enum.Enum):
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


class RoleRequestRole(str, enum.Enum):
    TREINADOR = "treinador"
    COORDENADOR = "coordenador"


class RoleRequestStatus(str, enum.Enum):
    PENDENTE = "pendente"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
