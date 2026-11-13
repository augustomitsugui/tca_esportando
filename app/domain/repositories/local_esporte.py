from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.esporte import Esporte
from app.domain.entities.local import Local


class LocalEsporteRepository(ABC):
    @abstractmethod
    async def local_owned_by(self, local_id: UUID, user_id: UUID) -> bool: ...

    @abstractmethod
    async def esporte_owned_by(self, esporte_id: UUID, user_id: UUID) -> bool: ...

    @abstractmethod
    async def add(self, local_id: UUID, esporte_id: UUID) -> None:
        ...

    @abstractmethod
    async def remove(self, local_id: UUID, esporte_id: UUID) -> bool:
        ...

    @abstractmethod
    async def list_by_local(self, local_id: UUID) -> list[Esporte]:
        ...

    @abstractmethod
    async def list_by_esporte(self, esporte_id: UUID) -> list[Local]:
        ...
