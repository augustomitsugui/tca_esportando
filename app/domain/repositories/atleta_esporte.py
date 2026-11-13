from abc import ABC, abstractmethod

from app.domain.entities.atleta_esporte import AtletaEsporte, AtletaEsporteStatus
from app.domain.entities.esporte import Esporte
from uuid import UUID


class AtletaEsporteRepository(ABC):
    @abstractmethod
    async def get(self, vinculo_id: UUID) -> AtletaEsporte | None: ...

    @abstractmethod
    async def inscrever(
        self, atleta_id: UUID, esporte_id: UUID
    ) -> AtletaEsporte: ...

    @abstractmethod
    async def solicitar(self, atleta_id: UUID, esporte_id: UUID) -> AtletaEsporte: ...

    @abstractmethod
    async def cancelar_inscricao(self, atleta_id: UUID, esporte_id: UUID) -> None: ...

    @abstractmethod
    async def list_by_atleta(self, atleta_id: UUID) -> list[AtletaEsporte]: ...

    @abstractmethod
    async def list_by_esporte(self, esporte_id: UUID) -> list[AtletaEsporte]: ...

    @abstractmethod
    async def list_by_atleta_status(
        self, atleta_id: UUID, status: AtletaEsporteStatus
    ) -> list[AtletaEsporte]: ...

    @abstractmethod
    async def list_pending_for_trainer(
        self, user_id: UUID
    ) -> list[AtletaEsporte]: ...

    @abstractmethod
    async def list_approved_for_trainer(
        self, user_id: UUID
    ) -> list[AtletaEsporte]: ...

    @abstractmethod
    async def get_atleta_id_by_user(self, user_id: UUID) -> UUID | None: ...

    @abstractmethod
    async def esporte_exists(self, esporte_id: UUID) -> bool: ...

    @abstractmethod
    async def list_available_esportes(self) -> list[Esporte]: ...

    @abstractmethod
    async def trainer_can_manage_esporte(
        self, esporte_id: UUID, user_id: UUID
    ) -> bool: ...

    @abstractmethod
    async def decide(
        self, vinculo_id: UUID, user_id: UUID, status: AtletaEsporteStatus
    ) -> AtletaEsporte: ...

    @abstractmethod
    async def cancel_pending(self, vinculo_id: UUID, atleta_id: UUID) -> bool: ...