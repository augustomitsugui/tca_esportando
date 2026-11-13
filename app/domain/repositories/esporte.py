from abc import abstractmethod

from app.domain.entities.esporte import Esporte
from app.domain.repositories.base import BaseRepository
from uuid import UUID

class EsporteRepository(BaseRepository[Esporte]):
    
    @abstractmethod
    async def list_by_treinador(self, treinador_id: UUID) -> list[Esporte]: ...
    
    @abstractmethod
    async def list_by_local(self, local_id: UUID) -> list[Esporte]: ...
