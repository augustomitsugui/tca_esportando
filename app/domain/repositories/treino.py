from abc import abstractmethod

from app.domain.entities.esporte import Esporte
from app.domain.repositories.base import BaseRepository
from app.domain.entities.treino import Treino

class TreinoRepository(BaseRepository[Treino]):
    
    @abstractmethod
    async def list_by_atleta(self, atleta_id: int) -> list[Treino]: ...
    
