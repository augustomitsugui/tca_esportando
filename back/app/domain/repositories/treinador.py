from abc import abstractmethod

from app.domain.entities.treinador import Treinador
from .base import BaseRepository
from uuid import UUID

class TreinadorRepository(BaseRepository[Treinador]):
   
    @abstractmethod
    async def list_by_coordenador(self, coordenador_id: UUID) -> list[Treinador]: ...
    
    @abstractmethod
    async def list_by_esporte(self, esporte_id: UUID) -> list[Treinador]: ...
