from abc import abstractmethod
from uuid import UUID

from app.domain.entities.atleta import Atleta
from app.domain.repositories.base import BaseRepository


class AtletaRepository(BaseRepository[Atleta]):

    @abstractmethod
    async def list_by_treinador(self, treinador_id: UUID) -> list[Atleta]: ...

    @abstractmethod
    async def list_by_esporte(self, esporte_id: UUID) -> list[Atleta]: ...
