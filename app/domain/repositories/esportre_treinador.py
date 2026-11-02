from abc import ABC, abstractmethod

from app.domain.entities.esporte import Esporte
from app.domain.entities.treinador import Treinador


class EsporteTreinadorRepository(ABC):

    @abstractmethod
    async def vincular(self, esporte_id: int, treinador_id: int) -> None: ...

    @abstractmethod
    async def desvincular(self, esporte_id: int, treinador_id: int) -> None: ...

    @abstractmethod
    async def list_by_esporte(self, esporte_id: int) -> list[Treinador]: ...
