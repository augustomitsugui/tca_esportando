from dataclasses import dataclass

@dataclass(frozen=True)
class AtletaDTO:
    id: int
    nome: str
    ano: int
    email: str
    treinador_id: int
    bio: str | None = None
