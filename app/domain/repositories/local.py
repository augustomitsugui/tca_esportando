from abc import abstractmethod

from app.domain.entities.local import Local
from app.domain.repositories.base import BaseRepository
from uuid import UUID

class LocalRepository(BaseRepository[Local]):
    @abstractmethod
    async def get_treinador_id_by_user(self, user_id: UUID) -> UUID | None: ...

    @abstractmethod
    async def list_by_creator(self, user_id: UUID) -> list[Local]: ...

    @abstractmethod
    async def list_by_treinador(self, treinador_id: UUID) -> list[Local]: ...
    
    @abstractmethod
    async def list_by_esporte(self, esporte_id: UUID) -> list[Local]: ...
