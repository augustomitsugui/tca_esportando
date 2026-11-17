from abc import ABC, abstractmethod

from app.domain.entities.esporte_treinador import EsporteTreinador
from uuid import UUID

class EsporteTreinadorRepository(ABC):

    @abstractmethod
    async def vincular(
        self, esporte_id: UUID, treinador_id: UUID
    ) -> EsporteTreinador: ...

    @abstractmethod
    async def desvincular(self, esporte_id: UUID, treinador_id: UUID) -> None: ...

    @abstractmethod
    async def list_by_esporte(
        self, esporte_id: UUID
    ) -> list[EsporteTreinador]: ...

    @abstractmethod
    async def get_treinador_id_by_user(self, user_id: UUID) -> UUID | None: ...

    @abstractmethod
    async def exists(self, esporte_id: UUID, treinador_id: UUID) -> bool: ...
