from abc import abstractmethod

from app.domain.entities.treino import Treino
from app.domain.entities.treino import TreinoAgenda
from app.domain.repositories.base import BaseRepository
from uuid import UUID


class TreinoRepository(BaseRepository[Treino]):
    @abstractmethod
    async def list_by_atleta(self, atleta_id: UUID) -> list[Treino]: ...

    @abstractmethod
    async def list_upcoming_by_atleta(
        self, atleta_id: UUID
    ) -> list[TreinoAgenda]: ...
