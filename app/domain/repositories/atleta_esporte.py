from abc import ABC, abstractmethod

from app.domain.entities.atleta_esporte import AtletaEsporte
from uuid import UUID


class AtletaEsporteRepository(ABC):

    @abstractmethod
    async def inscrever(
        self, atleta_id: UUID, esporte_id: UUID
    ) -> AtletaEsporte: ...

    @abstractmethod
    async def cancelar_inscricao(self, atleta_id: UUID, esporte_id: UUID) -> None: ...

    @abstractmethod
    async def list_by_atleta(self, atleta_id: UUID) -> list[AtletaEsporte]: ...

    @abstractmethod
    async def list_by_esporte(self, esporte_id: UUID) -> list[AtletaEsporte]: ...