from dataclasses import dataclass

@dataclass(frozen=True)
class UserDTO:
    id: int
    nome: str
    email: str
    senha: str
    is_active: bool
    is_verified: bool
    bio: str | None = None