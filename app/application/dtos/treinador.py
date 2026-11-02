from dataclasses import dataclass

@dataclass(frozen=True)
class TreinadorDTO:
    id: int
    nome: str
    email: str
    bio: str | None = None