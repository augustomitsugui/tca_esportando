from abc import abstractmethod

from app.domain.entities.treino import Treino
from app.domain.entities.treino import TreinoAgenda
from app.domain.repositories.base import BaseRepository
from uuid import UUID


class TreinoRepository(BaseRepository[Treino]):
    @abstractmethod
    async def get_atleta_id_by_user(self, user_id: UUID) -> UUID | None: ...

    @abstractmethod
    async def get_treinador_id_by_user(self, user_id: UUID) -> UUID | None: ...

    @abstractmethod
    async def list_by_treinador(self, treinador_id: UUID) -> list[Treino]: ...

    @abstractmethod
    async def treinador_manages_esporte(
        self, treinador_id: UUID, esporte_id: UUID
    ) -> bool: ...

    @abstractmethod
    async def trainer_can_use_resources(
        self, treinador_id: UUID, esporte_id: UUID, local_id: UUID
    ) -> bool: ...

    @abstractmethod
    async def list_by_atleta(self, atleta_id: UUID) -> list[Treino]: ...

    @abstractmethod
    async def list_upcoming_by_atleta(
        self, atleta_id: UUID
    ) -> list[TreinoAgenda]: ...
