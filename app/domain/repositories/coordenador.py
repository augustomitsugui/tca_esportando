from abc import abstractmethod

from app.domain.entities.coordenador import Coordenador
from app.domain.repositories.base import BaseRepository
from uuid import UUID

class CoordenadorRepository(BaseRepository[Coordenador]):
    @abstractmethod
    async def list_by_esporte(self, esporte_id: UUID) -> list[Coordenador]: ...
    
    
