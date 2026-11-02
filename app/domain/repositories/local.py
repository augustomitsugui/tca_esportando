from abc import abstractmethod

from app.domain.entities.local import Local
from app.domain.repositories.base import BaseRepository

class LocalRepository(BaseRepository[Local]):
    @abstractmethod
    async def list_by_treinador(self, treinador_id: int) -> list[Local]: ...
    
    @abstractmethod
    async def list_by_esporte(self, esporte_id: int) -> list[Local]: ...