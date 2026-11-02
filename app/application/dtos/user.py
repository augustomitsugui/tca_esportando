from dataclasses import dataclass

@dataclass(frozen=True)
class UserDTO:
    id: int
    nome: str
    email: str
    bio: str | None = None