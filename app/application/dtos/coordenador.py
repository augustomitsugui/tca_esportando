from dataclasses import dataclass

@dataclass(frozen=True)
class coodenadorDTO:
    id: int
    nome: str
    email: str
    bio: str | None = None