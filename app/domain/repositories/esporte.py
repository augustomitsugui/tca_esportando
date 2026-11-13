from abc import abstractmethod

from app.domain.entities.esporte import Esporte
from app.domain.repositories.base import BaseRepository
from uuid import UUID

class EsporteRepository(BaseRepository[Esporte]):
    
    @abstractmethod
    async def list_by_treinador(self, treinador_id: UUID) -> list[Esporte]: ...
    
    @abstractmethod
    async def list_by_local(self, local_id: UUID) -> list[Esporte]: ...

    @abstractmethod
    async def get_institution_id_by_user(self, user_id: UUID) -> UUID | None: ...

    @abstractmethod
    async def list_by_institution(self, institution_id: UUID) -> list[Esporte]: ...

    @abstractmethod
    async def get_institution_id_by_coordinator(
        self, user_id: UUID
    ) -> UUID | None: ...
