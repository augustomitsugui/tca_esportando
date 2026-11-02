from abc import abstractmethod

from app.domain.entities.treinador import Treinador
from .base import BaseRepository

class TreinadorRepository(BaseRepository[Treinador]):
   
    @abstractmethod
    async def list_by_coordenador(self, coordenador_id: int) -> list[Treinador]: ...
    
    @abstractmethod
    async def list_by_esporte(self, esporte_id: int) -> list[Treinador]: ...
