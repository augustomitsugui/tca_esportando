from abc import ABC, abstractmethod

from app.domain.entities.esporte import Esporte
from app.domain.entities.atleta import Atleta


class AtletaEsporteRepository(ABC):

    @abstractmethod
    async def inscrever(self, atleta_id: int, esporte_id: int) -> None: ...

    @abstractmethod
    async def cancelar_inscricao(self, atleta_id: int, esporte_id: int) -> None: ...

    @abstractmethod
    async def list_by_atleta(self, atleta_id: int) -> list[Esporte]: ...

    @abstractmethod
    async def list_by_esporte(self, esporte_id: int) -> list[Atleta]: ...