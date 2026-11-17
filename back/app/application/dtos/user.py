from dataclasses import dataclass
from uuid import UUID
@dataclass(frozen=True)
class UserDTO:
    id: UUID
    nome: str
    email: str
    senha: str
    is_active: bool
    is_verified: bool
    bio: str | None = None


UserCreateDTO = UserDTO